from rest_framework import serializers
from .models import Post,Category,Comment
from django.contrib.auth import(
    get_user_model,
)

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class ReadPostSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    class Meta:
        model = Post
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentReadSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = '__all__'
 
class NestedPostSerializer(serializers.ModelSerializer):
     comments = CommentReadSerializer(many=True)
     category=CategorySerializer()
     class Meta:
         model = Post
         fields = ['id','category','comments','title','description','date_created','picture','likes','author','sads','hearts']

def create(self, validated_data):
        comments_data = validated_data.pop('comments')
        post = Post.objects.create(**validated_data)
        for comment_data in comments_data:
            Comment.objects.create(post=post,**comment_data)
        return post    
