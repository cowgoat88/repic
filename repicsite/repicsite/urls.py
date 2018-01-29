"""repicsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from repicimages import views
from django.conf.urls import url
from rest_framework import routers
from scrap import views as scrap_views

router = routers.DefaultRouter()
router.register(r'submission', scrap_views.SubmissionViewSet)
router.register(r'subredditsList', scrap_views.SubredditsListViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.images, name='splash'),
    path('images/', views.images, name='images'),
    path('scrap/', scrap_views.submissionSet),
    url(r'^praw/', include(router.urls)),
    path('subreddits/', scrap_views.subredditsList),
    url(r'^subredditslist/', include(router.urls))
]
