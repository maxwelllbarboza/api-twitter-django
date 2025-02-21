from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from .models import Post, Follow


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

    def validate_user_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"message": "E-mail já existe."})
        return value
        

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), 
        slug_field='id'  
    )

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at']
        read_only_fields = ['id', 'created_at']  
        
    def validate_author(self, value):       
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(f"O autor com ID {value.id} não existe.")
        return value   


class FollowSerializer(serializers.ModelSerializer):
    
    follower = serializers.SlugRelatedField(
        queryset=User.objects.all(), 
        slug_field='id'  
    )
    
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), 
        slug_field='id'  
    )

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['id', 'created_at'] 
           
class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()           