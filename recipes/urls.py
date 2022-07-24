from . import views
from django.urls import path
from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('postcreate/', CreatePost.as_view(), name='createpost'),
    path('postdelete/<int:pk>', DeletePost.as_view(), name='deletepost'),
    path('postupdate/<int:pk>', Updatepost.as_view(), name='updatepost'),
    path('item/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]
