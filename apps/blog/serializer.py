from rest_framework import serializers
from apps.blog.models import Categoryes,Blogs
from apps.user_system.serializer import ModelUserDjoserSerializers


class CategorySerializers (serializers.ModelSerializer):
    class Meta:
        model = Categoryes
        fields = ["name", "slug", "creation"]


class BlogsSerializers (serializers.ModelSerializer):
    category = CategorySerializers()
    user = ModelUserDjoserSerializers()
    
    class Meta:
        model = Blogs
        fields = ["title", "description", "slug", "content", "img", "views", "public", "creation", "update", "user", "category"]
        
