from .serializers import ProfileSerializer, PostSerializer, CommentSerializer
from user.models import Profile
from feed.models import Post, Comment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
    GenericViewSet,
    ViewSet,
)
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed


@api_view(["GET", "POST"])
def profile(request):
    if request.method == "GET":
        profile = Profile.objects.all()
        serilizer = ProfileSerializer(profile, many=True)
        return Response(serilizer.data)
    elif request.method == "POST":
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


@api_view(["GET", "POST"])
def postApiView(request):
    if request.method == "GET":
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


@api_view(["GET", "PATCH", "DELETE"])
def postListApiView(request, pk):
    if request.method == "GET":
        post = Post.objects.get(id=pk)
        print(post)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == "PATCH":
        post = Post.objects.get(id=pk)

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)
    elif request.method == "DELETE":
        post = Post.objects.get(id=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def CommentApiView(request, pk):
    post = Post.objects.get(id=pk)
    user = request.user
    print(user)
    if request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=user)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class PostListCreateViewApi(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["user_id", "location", "caption"]


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"
    lookup_url_kwarg = "post_id"


class ProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "id"
    lookup_url_kwarg = "profile_id"
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["user", "location", "caption"]


class CommentCreateViewApi(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "id"

    def perform_create(self, serializer):
        post_id = self.kwargs.get("pk")
        user = self.request.user
        post = Post.objects.get(id=post_id, user=user)
        serializer.save(post=post, user=self.request.user)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all() 
    serializer_class = PostSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["user", "location", "caption"]

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST")


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def update(self, request, pk=None):
        user = self.request.user
        post = Post.objects.get(id=pk, user=user)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=self.request.user)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)
