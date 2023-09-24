from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework.response import Response

from django.db.models.query_utils import Q

from apps.blog.pagination import MediumPagination, BigPagination, PaginationCommentsBlog
from apps.blog.serializer import CategorySerializers, BlogsSerializers
from apps.blog.models import Categoryes, Blogs

from apps.blog_reactions.models import LikeBlog
from apps.blog_reactions.serializer import LikesSerializer
from apps.blog_reactions.models import CommentsBlog
from apps.blog_reactions.serializer import CommentsBlogSerializer


# All categoryes
class AllCategorys (APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        categoryes = Categoryes.objects.all()
        if categoryes:
            serializer = CategorySerializers(categoryes, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "not_Found"}, status=status.HTTP_404_NOT_FOUND)


# all blogs
class AllBlogs (APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):

        if Blogs.objects.order_by("-creation").all():
            filter_blogs = Blogs.objects.filter(public=True)
            pagination = MediumPagination()
            response = pagination.paginate_queryset(filter_blogs, request)
            serializer = BlogsSerializers(response, many=True)
            return pagination.get_paginated_response(serializer.data)
        else:
            return Response({"Error": "No existen blogs amigo"}, status=status.HTTP_404_NOT_FOUND)


# Blogs by category view
class BlogsByCategoryView (APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        categorys = Categoryes.objects.all()
        if categorys:
            slug = request.query_params.get("slug")
            filter_category = Categoryes.objects.filter(slug=slug)
            if filter_category:
                blogs = []
                for data in filter_category:
                    blogs.extend(Blogs.objects.filter(
                        category=data.id, public=True))

                if blogs:
                    pagination = MediumPagination()
                    response = pagination.paginate_queryset(blogs, request)
                    serializer = BlogsSerializers(response, many=True)
                    return pagination.get_paginated_response(serializer.data)

                else:
                    return Response({"erorr": "not_Found"}, status=status.HTTP_404_NOT_FOUND)

            else:
                return Response({"erorr": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"erorr": "not_Found"}, status=status.HTTP_404_NOT_FOUND)


class BLogDetail (APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        if Blogs.objects.all():
            slug = request.query_params.get("slug")
            blog = Blogs.objects.filter(slug = slug)
            
            if blog:
                seiralizer = BlogsSerializers(blog, many=True)
                return Response(seiralizer.data,status=status.HTTP_200_OK)

            else:
                return Response({"erorr": "Este blog no existe"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"erorr": "not_Foundd"}, status=status.HTTP_404_NOT_FOUND)



class GetBlogLikes (APIView) :
    permission_classes = [permissions.AllowAny]
    
    def get(self,request,format=None) :
        
        if Blogs.objects.all().exists() :
            slug = request.query_params.get("slug")
            
            try :
                blog_model = Blogs.objects.get(slug = slug)
            
                if blog_model :
                    filter_likes_blog = LikeBlog.objects.filter(blog = blog_model.id)
                    all_likes = []
                    for data in filter_likes_blog :
                        all_likes.append(data.like)
                    
                    serializer = LikesSerializer(filter_likes_blog, many = True)
                    return Response ({
                        "all_likes" : sum(all_likes),
                        "likes_details" : serializer.data
                    },status=status.HTTP_200_OK)
        
                else:
                    return Response({"erorr": "Este blog no existe"}, status=status.HTTP_404_NOT_FOUND)
                
            except :
                return Response({"Error", "Error"},status=status.HTTP_409_CONFLICT)
            
        else:
                return Response({"erorr": "No existen blogs"}, status=status.HTTP_404_NOT_FOUND)
  
  
  
class GetBlogComments (APIView) :
   permission_classes = [permissions.AllowAny]    
   
   def get(self,request,format = None) :
       
        if Blogs.objects.all().exists() :
            slug = request.query_params.get("slug")
            filter_blog = Blogs.objects.filter(slug = slug)
            
            if filter_blog :
                for data in filter_blog :
                    filter_blog_comments = CommentsBlog.objects.order_by("-update").order_by("-creation").filter(blog = data.id) 
                    
                    if len(filter_blog_comments) != 0 :
                        pagination = PaginationCommentsBlog()
                        response = pagination.paginate_queryset(filter_blog_comments, request)
                        serializer = CommentsBlogSerializer(response, many = True)
                        return pagination.get_paginated_response({
                            "all" : len(filter_blog_comments),
                            "data" : serializer.data,
                        })
                    
                    else :
                        return Response({"erorr": "No existen comentarios"}, status=status.HTTP_404_NOT_FOUND)
                    
            else :
                return Response({"erorr": "Este blog no existe"}, status=status.HTTP_404_NOT_FOUND)
            
        else :
            return Response({"erorr": "Aun no hay blogs registrados"}, status=status.HTTP_404_NOT_FOUND)
                
                
    
class SearchBlogs (APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):

        if Blogs.objects.all():
            slug = request.query_params.get("slug")
            blogs = Blogs.objects.order_by(
                "-creation").filter(Q(title__startswith=slug), public=True)

            if blogs:
                pagination = BigPagination()
                response = pagination.paginate_queryset(blogs, request)
                serializer = BlogsSerializers(response, many=True)
                return pagination.get_paginated_response(serializer.data)

            else:
                return Response({"erorr": "not_Found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"erorr": "not_Found"}, status=status.HTTP_404_NOT_FOUND)