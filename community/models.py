from django.db import models

# from accounts.models import User


class Post(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=100)
    context = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)
