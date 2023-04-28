from django.urls import path

from blog import views
from blog.views import PostList

app_name = 'blog'

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/', views.single_post_page),
]
