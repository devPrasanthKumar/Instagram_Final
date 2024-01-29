from django.urls import path
from .views import profile, postApiView, postListApiView, CommentCreateViewApi
from .views import (
    PostListCreateViewApi,
    PostRetrieveUpdateDestroyAPIView,
    CommentApiView,
    PostViewSet,
    ProfileViewSet,
    CommentViewSet,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from rest_framework import routers

router = DefaultRouter()
router.register("commentview", CommentViewSet, basename="CommentViewSet")
router.register("postview", PostViewSet, basename="post")
router.register("profileview", ProfileViewSet, basename="profile")


urlpatterns = [
    path("users/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", profile, name="profileApi"),
    path("post/", postApiView, name="postApi"),
    path("post_list/<int:pk>/", postListApiView, name="post_list"),
    path("comment_api/<int:pk>/", CommentApiView, name="comment_api"),
    path("post_list_create/", PostListCreateViewApi.as_view(), name="post_list_create"),
    path(
        "post_retrieve_update_destroy/<int:post_id>/",
        PostRetrieveUpdateDestroyAPIView.as_view(),
        name="post_retrieve_update_destroy",
    ),
    path(
        "comment_api_view/<int:pk>/",
        CommentCreateViewApi.as_view(),
        name="comment_api_view",
    ),
    # path("comment_viewset/<int:pk>", CommentViewSet.as_view({"post": "create"}), name="comment_viewset"),
]

urlpatterns += router.urls
