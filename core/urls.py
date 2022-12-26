from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('upload_comment', views.upload_comment, name='upload_comment'),
    path('like_post', views.like_post, name='like_post'),
    path('search', views.search, name='search'),
    path('search_post', views.search_post, name='search_post'),
    path('follow', views.follow, name='follow'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('password', views.password, name='password'),
]