from django.urls import path
from . import views

urlpatterns = [
    # path("", views.post_list, name="post_list"),
    # path("<int:pk>/", views.post_detail, name="post_detail"),
    path("", views.PostListAPIView.as_view(), name="post_list"),
    path("<int:pk>/", views.PostDetailAPIView.as_view(), name="post_detail"),
    path("<int:pk>/comments/", views.CommentListAPIView.as_view(), name="comment_list"),
    path("<int:post_pk>/comments/<int:comment_pk>/", views.CommentDetailAPIView.as_view(), name="comment_detail"),
    path("<int:post_pk>/like/", views.LikeAPIView.as_view(), name="post_like"),
]