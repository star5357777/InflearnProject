from django.shortcuts import render

from blog.models import Post


# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-pk') # order_by('-pk') : pk 기준 역순으로 출력
    return render(request, 'blog/index.html', {'posts': posts},)

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(request, 'blog/single_page.html', {'post': post},)