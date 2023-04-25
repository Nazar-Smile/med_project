from django.urls import path
from apps.blog import views

urlpatterns = [
    path('', views.PostListView.as_view(), name="post_list"),
    path('post/list/<slug:category_slug>/', views.PostListView.as_view(),name="post_category_list"),
    path('post/detail/<int:pk>/', views.PostDetailView.as_view(), name="post_detail"),
]
