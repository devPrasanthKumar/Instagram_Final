from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    locations = models.CharField(max_length=200, null=True, blank=True)
    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="profile/",
        default="profile/default.png",
    )
    # followers = models.ManyToManyField(User, related_name="followers", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.username

    def get_followers(self):
        return self.followers.all()

    @property
    def get_follower(self):
        return self.user.followed_by.filter(followed=self.user)

    @property
    def get_follower_count(self):
        return self.user.followed_by.filter(followed=self.user).count()

    @property
    def get_following(self):
        return self.user.following.filter(user=self.user)

    @property
    def get_following_count(self):
        return self.user.following.filter(user=self.user).count()

    @property
    def get_following_user_post(self):
        return self.user.following.filter(user=self.user).values_list(
            "user__post__id", flat=True
        )

    def get_posts_count(self):
        return self.user.post_set.all().count()


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(
        User,
        related_name="followed_by",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
