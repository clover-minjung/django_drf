from rest_framework import serializers
from .models import Post, Comment, Like

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("post",)
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("post")
        return ret

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ("user",)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        # 사용할 모델
        model = Post
        # 직렬화 할 필드
        fields = "__all__"

class PostDetailSerializer(PostSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    total_likes = serializers.IntegerField(source='likes.count', read_only=True)
