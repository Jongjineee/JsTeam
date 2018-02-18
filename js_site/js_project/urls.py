"""js_site URL Configuration

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
from django.conf.urls import url, include
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'js_project'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.profile, name='profile'),
    url(r'^profile_update/$', login_required(views.ProfileUpdateView.as_view()), name='profile_update'),
    url(r'^content/(?P<pk>[0-9]+)/$', views.content, name='content'),
    url(r'^content/(?P<pk>[0-9]+)/comments/$', views.comment_new, name='comment_new'),
    url(r'^about/$', views.about, name='about'),
    url(r'^first_project/$', views.first_project, name='first_project'),
    url(r'^second_project/$', views.second_project, name='second_project'),
    url(r'^second_project/second_report/$', views.second_report, name='second_report'),
    url(r'^second_project/second_media/$', views.second_media, name='second_media'),
    url(r'^first_project/first_video/$', views.first_video, name='first_video'),
    url(r'^first_project/first_report/$', views.first_report, name='first_report'),
    url(r'^first_project/first_ppt/$', views.first_ppt, name='first_ppt'),
    url(r'^content/(?P<pk>[0-9]+)/delete/$', views.delete, name='delete'),

]
