import os

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=50)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%y/%m/%d', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%y/%m/%d', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    # null을 했지만 카테고리 설정을 하지 않으면 저장할 때 오류가 난다. 이유는 DB에 null 값이 들어가도 상관 없다는 의미
    # form을 검사할 때 blank <- form이 비어있어도 된다를 설정하지 않으면 저장하는 과정에서 에러가 날 수 밖에 없음.

    tag = models.ManyToManyField(Tag, null=True, blank=True)
    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author} {self.content}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]