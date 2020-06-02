"""Bcc_social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from . import views

router = routers.DefaultRouter()
router.register('posts',views.PostViewSet)
router.register('categories',views.CategoryViewSet)
router.register('readposts',views.ReadPostViewSet)
router.register('comments',views.CommentViewSet)


urlpatterns = [
    path('api/',include(router.urls)),
    path('', views.login_view),
    path('home/', views.home),
    path('byCategory/<int:id>', views.byCategory),
    path('api/posts/category/<cat_id>',views.PostByCategory.as_view()),
    path('abouts/', views.about),
    path('contacts/', views.contacts),
    path('blogs/', views.blog),
    path('login/', views.home),
    path('api/post/like/<int:id>', views.likes_api),
    path('api/post/hearts/<int:id>', views.hearts_api),
    path('api/post/sads/<int:id>', views.sads_api),

    path('api/postwithcomments', views.NestedPostList.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
