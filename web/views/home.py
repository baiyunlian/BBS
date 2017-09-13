#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from repository import models
from django.urls import reverse
from utils.pagination import Page as Pagination
from backend.forms.article import callForm
from django.db import transaction
from utils.xss import XSSFilter
from django.shortcuts import HttpResponse
import json
from django.views.decorators import cache
import requests
#博客首页
def index(request, *args, **kwargs):
    """
    博客首页，展示全部博文
    :param request:
    :return:
    """
    #在线人数统计
    # if 'HTTP_X_FORWARDED_FOR' in request.META:
    #     ip = request.META['HTTP_X_FORWARDED_FOR']
    # else:
    #     ip = request.META['REMOTE_ADDR']
    # online_ips = cache.("online_ips", [])
    # if online_ips:
    #     online_ips = cache.get_many(online_ips).keys()
    # cache.set(ip, 0, 5 * 60)
    # if ip not in online_ips:
    #     online_ips.append(ip)
    # cache.set("online_ips", online_ips)
    #获取博文的分类列表
    article_type_list = models.ArticleType.objects.values()
    if kwargs:
        print(kwargs)
        article_type_id = int(kwargs['article_type_id'])#从前端获取id
        base_url = reverse('index',kwargs=kwargs)#跳转的页面
    else:
        article_type_id = None
        base_url = '/'
    #data_count = article_list = models.Article.objects.filter(**kwargs).count()
    data_count = models.Article.objects.filter(**kwargs).count()#博文数量统计
    page_obj = Pagination(request.GET.get('p'),data_count)#调用分页类生成对象
    #博文列表进行降序
    article_list = models.Article.objects.filter(**kwargs).order_by('-nid')[page_obj.start:page_obj.end]
    #所有博文列表
    article_read_list = models.Article.objects.all().order_by('-read_count')[:5]#阅读排序
    article_comm_list = models.Article.objects.all().order_by('-comment_count')[:5]#评论排序
    up_count_list = models.Article.objects.all().order_by('-up_count')[:5]#点赞排序
    article_comm_read = models.Article.objects.all().order_by('-comment_count').order_by('-read_count')[:5]#评论排序
    for i in article_read_list:
        print(i.title)
    #分页
    page_str = page_obj.page_str(base_url)
    if request.method=='POST':
        nid=request.POST.get('nid')#文章ID
        read_count=models.Article.objects.filter(nid=nid).first()
        read_count=int(read_count.read_count)+1#阅读数
        models.Article.objects.filter(nid=nid).update(read_count=read_count)#阅读数加1


    return render(
        request,
        'index.html',
        {#返回内容到前端
            'article_list': article_list,#博文列表
            'article_type_id': article_type_id,#博文分类 ID
            'article_type_list': article_type_list,#博文分类列表
            'page_str': page_str,#分页 对象
            'article_read_list':article_read_list,
            'article_comm_list':article_comm_list,
            'up_count_list':up_count_list,
            'article_comm_read':article_comm_read,
           # 'online_ips':online_ips
        }
    )

#个人博客主页
def home(request, site):
    """
    博主个人首页
    :param request:
    :param site: 博主的网站后缀如：http://xxx.com/wupeiqi.html
    :return:
    """
    #获取个人博客对象                                 跨表一次查询
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    #print(blog.theme.themename)
    if not blog:
        return redirect('/')
    tag_list = models.Tag.objects.filter(blog_id=blog.nid)#标签列表
    category_list = models.Category.objects.filter(blog_id=blog.nid)#分类列表
    # date_format(create_time,"%Y-%m")
    ids=blog.nid
    date_list = models.Article.objects.raw(
        'select nid,count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article where blog_id='+str(ids)+' group by strftime("%Y-%m",create_time)')
    #date_count=models.Article.objects.filter(blog_id=blog.nid).count()
    for item in date_list:
        print(item.nid,item.num,item.ctime)
    #当前博客文章 对象列表
    article_list = models.Article.objects.filter(blog_id=blog.nid).order_by('-nid').all()

    if request.method=='POST':
        nid=request.POST.get('nid')#文章ID
        read_count=models.Article.objects.filter(nid=nid).first()
        read_count=int(read_count.read_count)+1#阅读数
        models.Article.objects.filter(nid=nid).update(read_count=read_count)#阅读数加1
    return render(
        request,
        'home.html',
        {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            #'date_count': date_count,
            'article_list': article_list,

        }
    )



##条件查询
def filter(request, site, condition, val,**kwargs):
    """
    分类显示
    :param request:
    :param site:
    :param condition:
    :param val:
    :return:
    """
    #个人所有博文
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/')
    ids=blog.nid#博客ID
    #print(kwargs)
    tag_list = models.Tag.objects.filter(blog_id=blog.nid)#标签列表
    category_list = models.Category.objects.filter(blog_id=blog.nid)#分类列表
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime  from repository_article where blog_id='+str(ids)+' group by strftime("%Y-%m",create_time)')
        #'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')
    date_count=models.Article.objects.filter(blog_id=blog.nid).count()
    template_name = "home_title_list.html"
    if condition == 'tag':
        article_list = models.Article.objects.filter(tags__nid=val, blog_id=blog.nid).all()
    elif condition == 'category':
        article_list = models.Article.objects.filter(category__nid=val, blog_id=blog.nid).all()
    elif condition == 'date':
        article_list = models.Article.objects.filter(blog_id=blog.nid).extra(
            where=['strftime("%%Y-%%m",create_time)=%s'], params=[val, ]).all()
    else:
        article_list = []
    if request.method=='POST':
        nid=request.POST.get('nid')#文章ID
        read_count=models.Article.objects.filter(blog_id=blog.nid).first()
        read_count=int(read_count.read_count)+1#阅读数
        models.Article.objects.filter(nid=nid).update(read_count=read_count)#阅读数加1

        blogusernid=request.POST.get('blogusernid')
        if blogusernid:
            user=request.session['user_info']['nid']#关注用户ID
            fans=models.UserFans.objects.filter(user_id=blogusernid,follower_id=user).count()
            if not fans:
                models.UserFans.objects.create(user_id=blogusernid,follower_id=user)#创建互粉


    return render(request,  template_name,
                  {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            'date_count': date_count,
            'article_list': article_list,

        })

#获取博文信息
def art_inof(site):
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    return blog


#博文详细页
def detail(request, site, nid,**kwargs):
    """
    博文详细页
    :param request:
    :param site:
    :param nid:
    :return:
    """
    #获取个人博客对象                                 跨表一次查询

    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    ids=blog.nid
    tag_list = models.Tag.objects.filter(blog=blog)#标签列表
    category_list = models.Category.objects.filter(blog=blog)#分类列表
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article where blog_id='+str(ids)+' group by strftime("%Y-%m",create_time)')
    art_data=models.Article.objects.filter(nid=nid).select_related('articledetail__article').first()#文章内容
    comment=models.Comment.objects.filter(article_id=nid).all()#所有评论
    #read_count=art_data.read_count#阅读数
    #read_count=int(read_count)+1
    #models.Article.objects.filter(nid=nid).update(read_count=read_count)#阅读数加1
    comment_count=comment.count()#评论数
    #评论对应分页数量
    page_obj = Pagination(request.GET.get('p'), comment_count)
    comm_list=models.Comment.objects.filter(article_id=nid).order_by('-nid')[page_obj.start:page_obj.end]
    #print(comm_list)
    #当前页数 默认为1
    #print(read_count,comment_count)
    if kwargs:
        base_url = reverse('detail',kwargs=kwargs)#跳转的页面
        print(kwargs)
    else:
        base_url = '/'+site+'/'+nid+'.html'#跳转的页面
    #print(base_url)
        #分页
    page_str = page_obj.page_str(base_url)
    #up_count=request.GET.get('up_count')#文章当前点赞数
    #down_count=request.GET.get('down_count')#文章当前点踩数
    user=request.session['user_info']['nid']#点赞用户ID
    ret={'edi':False}
                #return redirect('/'+site+'/'+art_nid+'.html')
    if request.method=='POST':
        ret={'edi':False,'up_count':None,'down_count':None}
        up_count=request.POST.get('up_count')#文章当前点赞数
        down_count=request.POST.get('down_count')#文章当前点踩数
        if up_count and nid:#如果获取到点赞的相关信息
            obj=models.UpDown.objects.filter(article_id=nid,user_id=user).count()
            if not obj:
                up_count=int(up_count)+1
                models.UpDown.objects.create(article_id=nid,user_id=user,up=True)#点赞
                models.Article.objects.filter(nid=nid).update(up_count=up_count)#文章点赞数更新
                ret['edi']=True
                ret['up_count']=up_count
                return HttpResponse(json.dumps(ret))
        elif down_count and nid :
            obj=models.UpDown.objects.filter(article_id=nid,user_id=user).count()
            if not obj:
                down_count=int(down_count)+1
                models.UpDown.objects.create(article_id=nid,user_id=user,up=True)#点赞
                models.Article.objects.filter(nid=nid).update(down_count=down_count)#文章点踩数更新
                ret['edi']=True
                ret['down_count']=down_count
                return HttpResponse(json.dumps(ret))
        form = callForm(request=request, data=request.POST)#表单验证
        if form.is_valid():#如果验证成功
            #with transaction.atomic():#
            content = form.cleaned_data.pop('content')#取出文章内容
            content = XSSFilter().process(content)#进行处理 调用单例模式
            reply=request.POST.get('reply')#取出回复的ID
            print(content,user,reply)
            if reply:
                models.Comment.objects.create(content=content,article_id=nid,user_id=user,reply_id=reply)
            else:
                models.Comment.objects.create(content=content,article_id=nid,user_id=user)
            models.Article.objects.filter(nid=nid).update(comment_count=comment_count)#评论数

    return render(request, 'home_detail.html',
                  {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            'article':art_data,
            'comment':comment,
            'page_str': page_str,#分页 对象
            'ret':ret
        })

#博文详细页
def detail2(request, site, nid,**kwargs):
    """
    博文详细页
    :param request:
    :param site:
    :param nid:
    :return:
    """
    #获取个人博客对象                                 跨表一次查询

    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    tag_list = models.Tag.objects.filter(blog=blog)#标签列表
    category_list = models.Category.objects.filter(blog=blog)#分类列表
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')
    art_data=models.Article.objects.filter(nid=nid).select_related('articledetail__article').first()#文章内容
    comment=models.Comment.objects.filter(article_id=nid).all()#所有评论
    read_count=art_data.read_count#阅读数
    read_count=int(read_count)+1

    comment_count=comment.count()#评论数
    #评论对应分页数量
    page_obj = Pagination(request.GET.get('p'), comment_count)
    comm_list=models.Comment.objects.filter(article_id=nid).order_by('-nid')[page_obj.start:page_obj.end]
    #print(comm_list)
    #当前页数 默认为1
    #print(read_count,comment_count)
    if kwargs:
        base_url = reverse('detail',kwargs=kwargs)#跳转的页面
        print(kwargs)
    else:
        base_url = '/'+site+'/'+nid+'.html'#跳转的页面
    print(base_url)
        #分页
    page_str = page_obj.page_str(base_url)
    up_count=request.GET.get('up_count')#文章当前点赞数
    down_count=request.GET.get('down_count')#文章当前点踩数
    user=request.session['user_info']['nid']#点赞用户ID
    if request.method=='GET':
        if up_count and nid:#如果获取到点赞的相关信息
            obj=models.UpDown.objects.filter(article_id=nid,user_id=user).count()
            if not obj:
                up_count=int(up_count)+1
                models.UpDown.objects.create(article_id=nid,user_id=user,up=True)#点赞
                models.Article.objects.filter(nid=nid).update(up_count=up_count)#文章点赞数更新
        elif down_count and nid :
            obj=models.UpDown.objects.filter(article_id=nid,user_id=user).count()
            if not obj:
                down_count=int(down_count)+1
                models.UpDown.objects.create(article_id=nid,user_id=user,up=True)#点赞
                models.Article.objects.filter(nid=nid).update(down_count=down_count)#文章点踩数更新
        else:
            models.Article.objects.filter(nid=nid).update(read_count=read_count)#阅读数加1
                #return redirect('/'+site+'/'+art_nid+'.html')
    elif request.method=='POST':
        form = callForm(request=request, data=request.POST)#表单验证
        if form.is_valid():#如果验证成功
            #with transaction.atomic():#
            content = form.cleaned_data.pop('content')#取出文章内容
            content = XSSFilter().process(content)#进行处理 调用单例模式
            reply=request.POST.get('reply')#取出回复的ID
            print(content,user,reply)
            if reply:
                models.Comment.objects.create(content=content,article_id=nid,user_id=user,reply_id=reply)
            else:
                models.Comment.objects.create(content=content,article_id=nid,user_id=user)
            models.Article.objects.filter(nid=nid).update(comment_count=comment_count)#评论数

    return render(request, 'home_detail.html',
                  {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            'article':art_data,
            'comment':comment,
            'page_str': page_str,#分页 对象
        })