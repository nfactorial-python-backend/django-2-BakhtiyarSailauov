from django.db import models


class News(models.Model):
    title = models.TextField(max_length=50)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.title


class Comments(models.Model):
    content = models.TextField(max_length=150)
    created_at = models.DateTimeField()
    News = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
