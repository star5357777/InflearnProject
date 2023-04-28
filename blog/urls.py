from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index),
    path('<int:pk>/', views.single_post_page),
]
