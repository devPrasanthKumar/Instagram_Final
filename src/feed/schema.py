import graphene
from graphene_django import DjangoObjectType
from .models import Post, Like, Comment
from django.contrib.auth.models import User
import graphene
import graphql_jwt
from graphene_django.forms.mutation import DjangoModelFormMutation
from .forms import PostForm


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class LikeType(DjangoObjectType):
    class Meta:
        model = Like
        fields = "__all__"


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ["id", "comment"]


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"

    user = graphene.Field(UserType)
    like_cout = graphene.String()
    all_comment = graphene.List(CommentType)

    def resolve_like_cout(self, info):
        return self.get_like_count

    def resolve_all_comment(self, info):
        return Comment.objects.filter(post=self)


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    all_post = graphene.Field(PostType, id=graphene.ID())
    all_comments = graphene.List(CommentType)
    comment = graphene.Field(CommentType, id=graphene.ID())

    def resolve_all_comments(self, info):
        return Comment.objects.all()

    def resolve_comment(self, info):
        return Comment.objects.get(id=id)

    def resolve_all_posts(self, info):
        return Post.objects.all()

    def resolve_all_post(self, info, id):
        return Post.objects.get(id=id)


class PostMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        image = graphene.String(required=True)
        locations = graphene.String()
        caption = graphene.String()

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, **input):
        user_id = input.pop("user_id")
        user = User.objects.get(id=user_id)
        image = input.pop("image")
        locations = input.pop("locations")
        caption = input.pop("caption")
        post = Post(user=user, image=image, location=locations, caption=caption)

        post.save()

        return PostMutation(post=post)


class PostUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        image = graphene.String()
        locations = graphene.String()
        caption = graphene.String()

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id, image=None, locations=None, caption=None):
        post = Post.objects.get(id=id)
        if image is not None:
            post.image = image
        if locations is not None:
            post.location = locations
        if caption is not None:
            post.caption = caption
        post.save()
        return PostUpdateMutation(post=post)


class PostDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id):
        post = Post.objects.get(id=id)
        post.delete()
        return PostDeleteMutation(post=post)


class CommentMutation(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)
        comments = graphene.String()

    comment = graphene.Field(CommentType)

    @classmethod
    def mutate(cls, root, info, **input):
        user_id = input.pop("user_id")
        user = User.objects.get(id=user_id)
        post_id = input.pop("post_id")
        post = Post.objects.get(id=post_id)
        comments = input.pop("comments")
        comment = Comment(post=post, user=user, comment=comments)
        comment.save()
        return CommentMutation(comment=comment)


class LikeMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        post_id = graphene.ID(required=True)

    like = graphene.Field(LikeType)

    @classmethod
    def mutate(cls, root, info, **input):
        user_id = input.pop("user_id")
        user = User.objects.get(id=user_id)
        post_id = input.pop("post_id")
        post = Post.objects.get(id=post_id)
        like = Like(user=user, post=post)
        like.save()
        return LikeMutation(like=like)


class Mutation(graphene.ObjectType):
    post = PostMutation.Field()
    post_update = PostUpdateMutation.Field()
    post_delete = PostDeleteMutation.Field()
    like = LikeMutation.Field()
    comment = CommentMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
