#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets
from web.forms.base import BaseForm
from repository import models

#文章表验证 生成
class ArticleForm(django_forms.Form):
    title = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '文章标题'})
    )
    summary = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '文章简介', 'rows': '3'})
    )
    #文章内容
    content = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content'})
    )
    #版块分类
    article_type_id = django_fields.ChoiceField(
        choices=[],
        widget=django_widgets.RadioSelect
    )
    #个人文章分类
    category_id = django_fields.ChoiceField(
        choices=[],
        widget=django_widgets.RadioSelect
    )
    #标签 分类
    tags = django_fields.MultipleChoiceField(
        choices=[],
        widget=django_widgets.CheckboxSelectMultiple
    )

    #重写父类  筛选个人的博文
    def __init__(self, request, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        blog_id = request.session['user_info']['blog__nid']
        #选择的分类
        self.fields['category_id'].choices = models.Category.objects.filter(blog_id=blog_id).values_list('nid','title')
        #选择的版块
        self.fields['article_type_id'].choices = models.ArticleType.objects.all().values_list('nid','article_type')
        #选择的标签
        self.fields['tags'].choices = models.Tag.objects.filter(blog_id=blog_id).values_list('nid', 'title')

#开通个人博客验证
class BlogForm(BaseForm, django_forms.Form):
    title = django_fields.CharField(
        error_messages={'required': '标题不能为空.'},#required 为空时错误提示
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '个人博客标题'})
    )
    urls=django_fields.CharField(
        error_messages={'required': '网址不能为空.'},#required 为空时错误提示
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '个人博客网址'})
    )
    # site=django_fields.CharField(
    #     widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '个人博客前缀'})
    # )
    # theme=django_fields.CharField(
    #     widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '博客主题'})
    # )


#回复表单验证
class callForm(BaseForm,django_forms.Form):
    #文章内容
    content = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content'})
    )