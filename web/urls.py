"""EdmureBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from .views import home
from .views import account

urlpatterns = [
    url(r'^jsonp.html$', account.jsonp),#注册
    url(r'^login.html$', account.login),#登陆
    url(r'^logout.html$', account.logout),#注销
    url(r'^register.html$', account.register),#注册
    url(r'^check_code.html$', account.check_code),# 验证码 校对
    url(r'^all/(?P<article_type_id>\d+).html$', home.index, name='index'),#版块标签
    url(r'^(?P<site>\w+).html$', home.home),#个人主页
    url(r'^(?P<site>\w+)/(?P<condition>((tag)|(date)|(category)))/(?P<val>\w+-*\w*).html$', home.filter,name='filter'),#条件
    #url(r'^(?P<site>\w+)/(?P<condition>((tag)|(date)|(category)))/(?P<val>\w+-*\w*).html$', home.followers),#关注
    url(r'^(?P<site>\w+)/(?P<nid>\d+).html$', home.detail,name='detail'),##博文详细页
    #url(r'^updown.html$', home.updown),##点赞详细页
    url(r'^', home.index),#首页
]
