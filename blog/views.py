from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post, Category


# Create your views here.

class PostList(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = '-pk'
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

# def index(request):
#     posts = Post.objects.all().order_by('-pk') # order_by('-pk') : pk 기준 역순으로 출력
#     return render(request, 'blog/post_list.html', {'posts': posts},)

class PostDetail(DetailView):
    model = Post

# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(request, 'blog/post_detail.html', {'post': post},)
