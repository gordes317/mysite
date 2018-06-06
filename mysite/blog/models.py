from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class BlogArticles(models.Model):
    title = models.CharField(max_length=300)#1
    author = models.ForeignKey(User,related_name="blog_posts")#2
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:#3
        ordering = ("-publish",)
    def __str__(self):
        return self.title

# Create your models here.
