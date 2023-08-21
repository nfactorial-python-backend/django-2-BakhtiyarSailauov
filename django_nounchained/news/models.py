from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.TextField(max_length=50)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def has_comments(self):
        if Comments.objects.filter(News=self):
            return True
        return False


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=150)
    created_at = models.DateTimeField()
    News = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
