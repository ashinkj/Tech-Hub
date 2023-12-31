from django.urls import path
from .views import (
    
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,  
    CommentCreateView 
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('searchpage/>', views.search_user, name='search-page'),
    path('like/<int:pk>/', views.like_post, name='like-post'),
    path('post/<int:pk>/comment/',CommentCreateView.as_view(), name='user-comment'),
    path('about/', views.about, name='blog-about'),
]
