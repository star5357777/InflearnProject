from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.models import Post, Category, Tag


# Create your views here.

class PostList(ListView):
    model = Post

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

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostCreate(CreateView, UserPassesTestMixin ,LoginRequiredMixin):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    template_name = 'blog/post_form.html'

    def test_func(self):        # 특별한 user만 접근을 허용하고 싶다면 UserPassesTestMixin을 통해 test_fucn 함수를 사용해서 검사를 한다.
        return self.request.user.is_superuser or self.request.user.is_staff # 요청한 user가 staff 또는 superuser 권한을 가지고 있는지.


    def form_valid(self, form): # CreateView는 form_valid 함수가 기본적으로 탑재되어 있어 override하면 된다. form valid는 form에 입력한 값이 유효한지를 검사해주는 함수이다.
        current_user = self.request.user # 요청을 보낸 사용자의 정보를 담는 것
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user # Post Create에서 제공하는 form의 instance에 author이라는 필드에 current_user(요청한 사용자)의 정보를 담는 것
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/blog/')

class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs): # 서버에 사용자가 요청할 때 post,get 방식이 있는데 이것이 post 방식인지 get으로 요청했는지 알아내는 역할을 하는 기능. 해당하는 post 유저가 권한이 있는 유저인지 확인할 수 있다.
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied # 신기한 부분은 템플릿을 지정하지 않았는데 create에 있는 form을 그대로 사용하여 html 파일을 만들지 않아도 페이지가 나온다는


def category_page(request, slug):
    category = Category.objects.get(slug=slug)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': Post.objects.filter(category=category),
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category
        }
    )

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'tag': tag
        }
    )

# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(request, 'blog/post_detail.html', {'post': post},)
