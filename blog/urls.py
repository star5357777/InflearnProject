from django.urls import path

from blog import views
from blog.views import PostList, PostDetail

app_name = 'blog'

urlpatterns = [
    path('category/<str:slug>/', views.category_page),
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
]

