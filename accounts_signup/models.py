from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    introduction = models.TextField()

    def __str__(self):
        return self.nickname
