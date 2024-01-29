from django.urls import path
from .views import (
    UserView,
    UserFormView,
    ProfileUpdateView,
    ProfileView,
    FollowFormView,
    UserLoginView,
    FollowListView,
    ProfileListView,
    UserLogoutView,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("template", UserView.as_view(), name="view"),
    path("signup", UserFormView.as_view(), name="signup"),
    path("update/<int:pk>", ProfileUpdateView.as_view(), name="update"),
    path("profile/<int:pk>", ProfileView.as_view(), name="profile"),
    path("follow/<int:user_pk>", FollowFormView.as_view(), name="follow"),
    path("login", UserLoginView.as_view(), name="login"),
    # path("logout", LogoutView.as_view(), name="logout"),
    path("follow_list/<int:user_pk>", FollowListView.as_view(), name="follow_list"),
    path("profile_list", ProfileListView.as_view(), name="profile_list"),
    path("logout", UserLogoutView.as_view(), name="logout"),
]
