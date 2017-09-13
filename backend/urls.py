'''#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#BBS 
#2017/8/23    19:03
#__author__='Administrator'
'''
from django.conf.urls import url
from django.conf.urls import include
from .views import user

urlpatterns = [
    url(r'^index.html$', user.index),#后台个人欢迎页面
    url(r'^base-info.html$', user.base_info),#后台个人信息页面
    url(r'^tag.html$', user.tag),#后台个人标签页面
    url(r'^category.html$', user.category),#后台个人分类页面
    url(r'^article-(?P<article_type_id>\d+)-(?P<category_id>\d+).html$', user.article,name='article'),#后台个人管理文章
    url(r'^add-article.html$', user.add_article),#后台个人添加文章
    url(r'^edit-article-(?P<nid>\d+).html$', user.edit_article),#后台个人修改文章
    url(r'^upload-avatar.html$', user.upload_avatar),#后台个人更换头像

]
