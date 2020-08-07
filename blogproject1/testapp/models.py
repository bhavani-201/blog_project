from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


class custommanager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


# Create your models here.
class Post(models.Model):
    STATUE_CHOICES=(('draft','DRAFT'),('published','PUBLISHED'))
    title=models.CharField(max_length=64)
    slug=models.SlugField(max_length=64,unique_for_date='publish')
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.PROTECT)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUE_CHOICES,default='draft')
    objects=custommanager()
    tags=TaggableManager()
    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])
