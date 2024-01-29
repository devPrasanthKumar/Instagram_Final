from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from .forms import SignupForm, ProfileForm
from django.db.models import Count
from .models import Profile, Follow
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.urls import reverse_lazy


# Create your views here.


class UserView(TemplateView):
    template_name = "user/user.html"


class UserFormView(CreateView):
    model = User
    form_class = SignupForm
    template_name = "user/user_form.html"
    success_url = reverse_lazy("login")


class ProfileListView(ListView):
    model = Profile
    context_object_name = "profiles"

    def get_queryset(self):
        profile = Profile.objects.all()
        query = self.request.GET.get("search")
        print(query)
        if query:
            profile = Profile.objects.filter(
                Q(username__icontains=query)
                | Q(bio__icontains=query)
                | Q(locations__icontains=query)
            )
        return profile


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    # template_name = "user/profile_update.html"
    success_url = reverse_lazy("profile")


class ProfileView(DetailView):
    model = Profile
    context_object_name = "profiles"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        following_users = Follow.objects.filter(user=self.request.user)
        user_pk = self.object.user
        post = user_pk.post_set.all()
        print(post)
        context["posts"] = post
        context["posts_count"] = self.object.get_posts_count()

        context["following_users"] = following_users

        return context


class FollowFormView(View):
    model = Follow
    fields = []

    def post(self, request, *args, **kwargs):
        user = self.request.user
        followed_user_pk = self.kwargs.get("user_pk")

        followed_user = User.objects.get(pk=followed_user_pk)

        if Follow.objects.filter(user=user, followed=followed_user).exists():
            Follow.objects.filter(user=user, followed=followed_user).delete()
        else:
            Follow.objects.create(user=user, followed=followed_user)

        return redirect("profile", pk=followed_user_pk)


class FollowListView(ListView):
    model = Follow
    context_object_name = "follows"

    def get_queryset(self):
        user = self.request.user
        print(Follow.objects.filter(user=user))
        return Follow.objects.filter(user=user)


class UserLoginView(LoginView):
    template_name = "user/login.html"
    next_page = "list"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("profile")
        return super().dispatch(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    success_url = reverse_lazy("login")
