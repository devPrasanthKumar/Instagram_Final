from django.urls import path

from .views import (
    HomeView,
    CreatePostView,
    UpdatePostView,
    ListPostView,
    LikeFormView,
    CommentFormView,
    PostDetailView,
    DeletePostView,
    CommentListView,
)


urlpatterns = [
    path("home", HomeView.as_view(), name="home"),
    path("create", CreatePostView.as_view(), name="create"),
    path("edit/<int:pk>", UpdatePostView.as_view(), name="edit"),
    path("", ListPostView.as_view(), name="list"),
    path("like/<int:post_pk>", LikeFormView.as_view(), name="like"),
    path("comment/<int:post_pk>", CommentFormView.as_view(), name="comment"),
    path("detail/<int:pk>", PostDetailView.as_view(), name="detail"),
    path("delete/<int:pk>", DeletePostView.as_view(), name="delete"),
    path("comment_list/<int:post_pk>", CommentListView.as_view(), name="comment_list"),
]
