from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post, Like, Comment
from django.contrib.auth.models import User

from .forms import PostForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.db.models import Count
from django.views.generic.base import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q

# Create your views here.


class HomeView(TemplateView):
    template_name = "feed/home.html"


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("list")
    login_url = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("list")
    login_url = "login"


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("list")
    login_url = "login"


class ListPostView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "posts"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        following = user.following.values_list("followed", flat=True)
        not_following = User.objects.exclude(id__in=following).exclude(id=user.id)
        print(not_following)
        suggested_post = Post.objects.filter(user__in=not_following)
        
        post = Post.objects.filter(user__in=following)
        # print(post)
        user_posts = Post.objects.filter(user=user)
        # print(user_post)
        post = post | user_posts
        # print(str(following))

        context["posts"] = post
        posts = user.post_set.all()
        print(posts)

        for post in context["posts"]:
            user_has_liked = Like.objects.filter(
                post=post, user=self.request.user
            ).exists()
            post.con = user_has_liked
            print(user_has_liked)

        return context


class LikeFormView(LoginRequiredMixin, View):
    model = Like
    fields = []
    login_url = "login"

    def post(self, request, post_pk, *args, **kwargs):
        user = self.request.user

        post = Post.objects.get(id=post_pk)
        print(post_pk)
        print(post)

        if Like.objects.filter(user=user, post=post).exists():
            like = Like.objects.get(user=user, post=post)
            like.delete()
        else:
            Like.objects.create(user=user, post=post)

        return redirect("list")


class CommentFormView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy("list")
    login_url = "login"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = self.request.user
        post_pk = self.kwargs.get("post_pk")
        post = Post.objects.get(pk=post_pk)

        form = CommentForm(self.request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.post = post
            comment.save()
        return super().form_valid(form)


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    context_object_name = "comments"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get("post_pk")
        print(post_id)
        post = Post.objects.get(pk=post_id)

        comment = self.model.objects.filter(post=post)
        context["comments"] = comment
        context["post"] = post_id
        print(comment)
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    form_class = PostForm
    context_object_name = "post"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get("pk")
        user_likes = Like.objects.filter(post=post_id, user=self.request.user)
        like_count = user_likes.count()

        context["like_count"] = like_count

        return context
