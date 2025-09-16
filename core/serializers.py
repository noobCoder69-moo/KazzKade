from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Post, Comment, Like
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )
        user.set_password(validated_data["password"])  
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "bio", "first_name", "last_name",
            "followers_count", "following_count", "posts"
        ]
        
        def get_follower_count(self, obj):
            return obj.followers.count()
        def get_following_count(self, obj):
            return obj.following.count()

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'text', 'created_at', 'comments', 'like_count']
    

    def get_like_count(self, obj):
        return obj.likes.count()
    

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at', 'like_count']

    def get_likes(self, obj):
        return obj.likes.count()
    
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    content_type = serializers.SerializerMethodField()
    

    class Meta:
        model = Like
        fields = ['id', 'user', 'object_id', 'content_type', 'created_at']

    def get_content_type(self, obj):
        return obj.content_type.model
    
