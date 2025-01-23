from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status

from .serializers import PostSerializer, CommentSerializer, PostDetailSerializer, LikeSerializer
from .models import Post, Comment, Like
# 함수형 뷰
# 로직: 데이터 가져오기 -> 가져온 데이터 serializer로 직렬화 -> response 돌려주기

# @api_view(["GET", "POST"])
# def post_list(request):
#     if request.method == 'GET':
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
        
#     elif request.method == 'POST':
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(["GET", "PUT", "DELETE"])
# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
    
#     elif request.method == "PUT":
#         serializer = PostSerializer(post, data=request.data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)

#     elif request.method == 'DELETE':
#         post.delete()
#         data = {"delete": f"Post({pk}) is deleted."}
#         return Response(data, status=status.HTTP_200_OK)

# 클래스형 뷰(CBV)
from rest_framework.views import APIView

class PostListAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class PostDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        data = {"pk": f"{pk} is deleted."}
        return Response(data, status=status.HTTP_200_OK)

class CommentListAPIView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentDetailAPIView(APIView):
    def get_object(self, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk)

    def delete(self, request, post_pk, comment_pk):
        comment = self.get_object(comment_pk)
        comment.delete()
        data = {"pk": f"{comment_pk} is deleted."}
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, post_pk, comment_pk):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class LikeAPIView(APIView): 
    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        # user = request.user
        check_like = Like.objects.filter(post=post)
        likes_count = post.like.count() 
    
        if check_like:
            check_like.delete()
            message = "좋아요 취소"
            liked = False
            return Response({
                "message": message,
                "likes_count": likes_count,
                "liked": liked
            }, status=status.HTTP_204_NO_CONTENT)
        else:
            like = Like.objects.create(post=post)
            serializer = LikeSerializer(like)
            message = "좋아요 추가"
            liked = True
            return Response({
                "message": message,
                "likes_count": likes_count,
                "liked": liked,
                "like_data": serializer.data,
            }, status=status.HTTP_201_CREATED)
        
