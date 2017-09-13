#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import uuid
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db import transaction
from django.urls import reverse

from ..forms.article import ArticleForm,BlogForm
from ..auth.auth import check_login
from repository import models
from utils.pagination import Page as Pagination
from utils.xss import XSSFilter
from web.views import account
#装饰是否是登陆状态
@check_login
def index(request):
    return render(request, 'backend_index.html')

#博主个人信息
@check_login
def base_info(request):
    """
    博主个人信息
    :param request:
    :return:
    """
    user_id=request.session['user_info']['nid']##个人信息ID
    userinfo=models.UserInfo.objects.filter(nid=user_id).first()# 个人信息
    blog_info=models.Blog.objects.filter(user=user_id).first()#个人博客
    #print(userinfo,blog_info.urls)
    #博客主题列表
    blog_info_list=models.BlogTheme.objects.all()
    if request.method=="POST":
        ret={'status':False,'error':None,'data':None,}
        nickname=request.POST.get('nickname')#昵称
        if not nickname:#如果没有输入昵称 与用户名相同
            nickname=request.session['user_info']['username']
        models.UserInfo.objects.filter(nid=user_id).update(nickname=nickname)#更新昵称
        request.session['user_info']['nickname']=nickname#时间同步session中的昵称
        obj=BlogForm(request=request, data=request.POST)
        if obj.is_valid():
            #blogUrl=request.POST.get('blogUrl')#博客地址
            blogTheme=request.POST.get('theme')#主题ID

            #blogTile=request.POST.get('blogTile')#博客标题
            blogTile = obj.cleaned_data.get('title')#获取标题
            blogUrl = obj.cleaned_data.get('urls')#获取标题
            nids=models.Blog.objects.filter(user_id=user_id).first()

            if nids:#如果有博客了
                #进行更新
                blogobj=models.Blog.objects.filter(user_id=user_id).update(title=blogTile,urls=blogUrl,site=userinfo.username,theme_id=blogTheme)
            else:
                blogobj=models.Blog.objects.create(title=blogTile,urls=blogUrl,site=userinfo.username,theme_id=blogTheme,user_id=user_id)
                nids=models.Blog.objects.filter(user_id=user_id).first()
                request.session['user_info']['blog__nid']=user_id#blog id
                request.session['user_info']['blog__site']=userinfo.username
            ret['status']=True
            #ret['data']=obj.cleaned_data
            ret=json.dumps(ret)#转为json格式
            #return HttpResponse(ret)
        else:
            #加入错误信息
            ret['error']=obj.errors.as_data()
            #对错误信息对象进行转化处理 前端不用二次序列化
            ret=json.dumps(ret,cls=account.JsonCustomEncoder)
            print(ret)
        return HttpResponse(ret)
    return render(request, 'backend_base_info.html',{'blog_info_list':blog_info_list,'blog_info':blog_info,'userinfo':userinfo})

#更换头像
@check_login
def upload_avatar(request):
    ret = {'status': False, 'data': None, 'message': None}
    print(request.session['user_info'])
    if request.method == 'POST':
        file_obj = request.FILES.get('avatar_img')
        print(file_obj)
        if not file_obj:
            pass
        else:
            file_name = str(uuid.uuid4())+'.png'
            file_path = os.path.join('static/imgs/avatar', file_name)
            f = open(file_path, 'wb')
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
            ret['status'] = True
            ret['data'] = file_path
            #更新头像
            models.UserInfo.objects.filter(nid=request.session['user_info']['nid']).update(avatar=file_name)
            request.session['user_info']['avatar']=file_name

    return HttpResponse(json.dumps(ret))

#博主个人标签管理
@check_login
def tag(request, *args, **kwargs):
    """
    博主个人标签管理
    :param request:
    :return:
    """
    #博客的ID
    blog_id = request.session['user_info']['blog__nid']
    #标签名称对象列表
    data_tag=models.Tag.objects.all()
    #所对应博客的标签数量
    data_count = models.Tag.objects.filter(blog_id=blog_id).count()
    print(data_count)
    #文章对应分页内容字黄
    article_count={}
    for row in data_tag:
        title=row.title
        count=models.Article.objects.filter(blog_id=blog_id,tags__article2tag__article=row.nid).count()#统计 当前博客 对应标签 数
        article_count[title]=count#加入字典
    #当前页数 默认为1
    page = Pagination(request.GET.get('p', 1), data_count)
    #分类对象列表 当前页面
    result = models.Tag.objects.filter(blog_id=blog_id).order_by('-nid').only('nid', 'title','blog').select_related('blog')[page.start:page.end]
    #总页数 传入url
    page_str = page.page_str('tag.html')

    if request.method=='POST':
        ret={'status':False,'del':False,'edi':False}
        s=request.POST.get('nickname')#获取到提交的内容
        dels=request.POST.get('data')#要删除的分类
        oldname=request.POST.get('oldname')#旧标签
        newname=request.POST.get('newname')#新标签
        if s:
            user_id=request.session['user_info']['blog__nid']##个人信息blogID
            obj=models.Tag.objects.filter(title=s).count()#获取对应
            if obj:
                pass
            else:
                models.Tag.objects.create(title=s,blog_id=user_id)#添加新标签
                ret['status']=True
        if dels:#判断删除
            models.Tag.objects.get(title=dels).delete()
            ret['del']=True
        if newname:
            models.Tag.objects.filter(title=oldname).update(title=newname)
            ret['edi']=True
        return HttpResponse(json.dumps(ret))

    return render(request, 'backend_tag.html',
                  {'result': result,
                   'page_str': page_str,
                   'arg_dict': kwargs,
                   'data_count': data_count,
                   'data_tag':data_tag,
                   'article_count':article_count
                    }
                  )


#博主个人分类管理
@check_login
def category(request , *args, **kwargs):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    #博客的ID
    blog_id = request.session['user_info']['blog__nid']
    #print(blog_id,'*****************')
    #分类名称对象列表
    data_category=models.Category.objects.all()
    #分类数量
    data_count = models.Category.objects.filter(blog_id=blog_id).count()
    print(data_count)
    #文章对应分类数量
    article_count={}
    for row in data_category:
        title=row.title
        count=models.Article.objects.filter(blog_id=blog_id,category_id=row.nid).count()#统计 当前博客 对应分类 数
        article_count[title]=count#加入字典
    #当前页数 默认为1
    page = Pagination(request.GET.get('p', 1), data_count)
    #分类对象列表 当前页面
    result = models.Category.objects.filter(blog_id=blog_id).order_by('-nid').only('nid', 'title','blog').select_related('blog')[page.start:page.end]
    #总页数 传入url
    page_str = page.page_str('category.html')

    if request.method=='POST':
        ret={'status':False,'del':False,'edi':False}
        s=request.POST.get('nickname')#获取到提交的内容
        dels=request.POST.get('data')#要删除的分类
        oldname=request.POST.get('oldname')#旧分类名
        newname=request.POST.get('newname')#新分类名
        if s:
            user_id=request.session['user_info']['blog__nid']##个人信息 blogID
            obj=models.Category.objects.filter(title=s).count()#获取对应
            if obj:
                pass
            else:
                models.Category.objects.create(title=s,blog_id=user_id)#添加新标签
                ret['status']=True
        if dels:#判断删除
            models.Category.objects.get(title=dels).delete()
            ret['del']=True
        if newname:
            models.Category.objects.filter(title=oldname).update(title=newname)
            ret['edi']=True
        return HttpResponse(json.dumps(ret))

    return render(request, 'backend_category.html',
                  {'result': result,
                   'page_str': page_str,
                   'arg_dict': kwargs,
                   'data_count': data_count,
                   'data_category':data_category,
                   'article_count':article_count
                    }
                  )

#博主个人文章管理
@check_login
def article(request, *args, **kwargs):
    """
    博主个人文章管理
    :param request:
    :return:
    """
    #博客的ID
    blog_id = request.session['user_info']['blog__nid']
    #条件字典
    condition = {}
    for k, v in kwargs.items():#判断是否选为全部
        if v == '0':
            pass
        else:
            condition[k] = v
    condition['blog_id'] = blog_id
    #文章数量
    data_count = models.Article.objects.filter(**condition).count()
    #当前页数 默认为1 调用分页类
    page = Pagination(request.GET.get('p', 1), data_count)
    #分页文章对象列表
    result = models.Article.objects.filter(**condition).order_by('-nid').only('nid', 'title','blog').select_related('blog')[page.start:page.end]
    #总页数
    page_str = page.page_str(reverse('article', kwargs=kwargs))
    #所属博文列表
    category_list = models.Category.objects.filter(blog_id=blog_id).values('nid', 'title')
    #版块分类列表
    type_l=[]
    types= models.ArticleType.objects.all().values('nid','article_type')#分类对象列表
    for i in types:
        tup=(int(i['nid']),i['article_type'])
        type_l.append(tup)#元组列表追加
    type_list = map(lambda item: {'nid': item[0], 'title': item[1]}, type_l)#文章列表
    kwargs['p'] = page.current_page#当前页码
    if request.method=='POST':
        ret={'status':False,'del':False,'edi':False}
        art_id=request.POST.get('art_id')
        print(art_id)
        models.Article.objects.filter(nid=art_id).delete()
        ret['del']=True
        return HttpResponse(json.dumps(ret))

    return render(request,
                  'backend_article.html',
                  {'result': result,
                   'page_str': page_str,
                   'category_list': category_list,
                   'type_list': type_list,
                   'arg_dict': kwargs,
                   'data_count': data_count
                   }
                  )

#添加文章
@check_login
def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = ArticleForm(request=request)#进行文章验证
        return render(request, 'backend_add_article.html', {'form': form})
    elif request.method == 'POST':
        form = ArticleForm(request=request, data=request.POST)#表单验证
        if form.is_valid():
            with transaction.atomic():#事务操作
                tags = form.cleaned_data.pop('tags')#标签
                content = form.cleaned_data.pop('content')#取出文章内容
                print(content)
                content = XSSFilter().process(content)#进行处理 调用单例模式
                form.cleaned_data['blog_id'] = request.session['user_info']['blog__nid']#博客ID
                obj = models.Article.objects.create(**form.cleaned_data)#加入数据库
                #文章内容
                models.ArticleDetail.objects.create(content=content, article=obj)#加入文章内容
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article_id=obj.nid, tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)

            return redirect('/backend/article-0-0.html')
        else:
            return render(request, 'backend_add_article.html', {'form': form})
    else:
        return redirect('/')

#编辑文章
@check_login
def edit_article(request, nid):
    """
    编辑文章
    :param request:
    :return:
    """
    #博客ID
    blog_id = request.session['user_info']['blog__nid']
    if request.method == 'GET':
        obj = models.Article.objects.filter(nid=nid, blog_id=blog_id).first()
        if not obj:
            return render(request, 'backend_no_article.html')
        tags = obj.tags.values_list('nid')
        if tags:
            tags = list(zip(*tags))[0]
        init_dict = {
            'nid': obj.nid,
            'title': obj.title,
            'summary': obj.summary,
            'category_id': obj.category_id,
            'article_type_id': obj.article_type_id,
            'content': obj.articledetail.content,
            'tags': tags
        }
        form = ArticleForm(request=request, data=init_dict)
        return render(request, 'backend_edit_article.html', {'form': form, 'nid': nid})
    elif request.method == 'POST':
        form = ArticleForm(request=request, data=request.POST)
        if form.is_valid():
            obj = models.Article.objects.filter(nid=nid, blog_id=blog_id).first()
            if not obj:
                return render(request, 'backend_no_article.html')
            with transaction.atomic():
                content = form.cleaned_data.pop('content')
                content = XSSFilter().process(content)
                tags = form.cleaned_data.pop('tags')
                models.Article.objects.filter(nid=obj.nid).update(**form.cleaned_data)
                models.ArticleDetail.objects.filter(article=obj).update(content=content)
                models.Article2Tag.objects.filter(article=obj).delete()
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article_id=obj.nid, tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)
            return redirect('/backend/article-0-0.html')
        else:
            return render(request, 'backend_edit_article.html', {'form': form, 'nid': nid})