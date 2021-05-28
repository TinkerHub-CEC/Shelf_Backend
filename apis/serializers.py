from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', ]
        #'title', 'description', 'url', 'file', 'image', 'stream_url']

# class BookmarkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bookmark
#         fields =['id', 'newscard', 'user']