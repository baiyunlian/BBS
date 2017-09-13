#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#BBS 
#2017/8/23    16:00
#__author__='Administrator'
from io import BytesIO
from django.shortcuts import render,HttpResponse,redirect
from web.forms.account import LoginForm,RegisterForm,UserInfoForm
from django.core.exceptions import ValidationError
from utils.check_code import create_validate_code
from repository import models
import json


def jsonp(request):
    func = request.GET.get('callback')
    content = '%s(100000)' %(func,)
    return HttpResponse(content)

#json 对错误信息对象进行处理
class JsonCustomEncoder(json.JSONEncoder):
    def default(self,field):
        if isinstance(field,ValidationError):#如果是错误信息进行处理
            return {'code':field.code ,'messages':field.messages}
        else:
            return json.JSONEncoder.default(self,field)
#登陆验证
def login2(request):
    if request.method=='GET':
        return render(request, 'login.html')
    elif request.method=='POST':
        #返回的字符串 字典
        ret={'status':True,'error':None,'data':None}
        #进行验证 调用loginform
        obj=LoginForm(request.POST)
        if obj.is_valid():
            print(obj.cleand_data)
        else:
            #加入错误信息
            ret['error']=obj.errors.as_data()
        #对错误信息对象进行转化处理 前端不用二次序列化
        result=json.dumps(ret,cls=JsonCustomEncoder)
        return HttpResponse(result)#转为json格式

#验证码函数
def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()#创建内存空间
    img, code = create_validate_code()#调用验证码图片生成函数 返回图片 和 对应的验证码
    img.save(stream, 'PNG')#保存为PNG格式
    request.session['CheckCode'] = code#保存在session中
    return HttpResponse(stream.getvalue())

#登陆验证
def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        result = {'status': False, 'message': None, 'data': None}
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')#获取正确的信息 用户名
            password = form.cleaned_data.get('password')#获取正确的信息 密码
            print(username,password)
            #在数据库进行查询
            user_info = models.UserInfo.objects. \
                filter(username=username, password=password). \
                values('nid', 'nickname',
                       'username', 'email',
                       'avatar',
                       'blog__nid',
                       'blog__site').first()
            #如果不存在 提示错误
            if not user_info:
                # result['message'] = {'__all__': '用户名或密码错误'}
                result['message'] = '用户名或密码错误'
            else:
                result['status'] = True
                request.session['user_info'] = user_info
                #如果自动登陆勾选
                if form.cleaned_data.get('rmb'):
                    #设置超时时间
                    request.session.set_expiry(60 * 60 * 24 * 7)
        else:
            #print(form.errors)
            if 'check_code' in form.errors:
                result['message'] = '验证码错误或者过期'
            else:
                result['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(result))


#注册
def register1(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method=='GET':
        obj=RegisterForm(request=request, data=request.POST)
        return render(request, 'register.html',{'obj':obj})

    elif request.method=='POST':
        #返回的字符串 字典
        ret={'status':True,'error':None,'data':None,'message': None,}
        #进行验证 调用RegisterForm
        obj=RegisterForm(request=request, data=request.POST)
        if obj.is_valid():
            username = obj.cleaned_data.get('username')
            password = obj.cleaned_data.get('password')
            email= obj.cleaned_data.get('email')
            print(username,password)
            user_info=models.UserInfo.objects.create(username=username,
                                                     password=password,
                                                     email=email,
                                                     nickname=username,
                                                     )
            request.session['user_info'] = user_info
            #return render(request,'home.html',{'obj.':obj})
            return HttpResponse(ret)

        else:
            #加入错误信息
            print(obj.errors)
            # if 'check_code' in obj.errors:
            #     ret['message'] = '验证码错误或者过期'
            # else:
            #     ret['message'] = ''
            ret['error']=obj.errors.as_data()
            #提示为False
            ret['status']=False
            #对错误信息对象进行转化处理 前端不用二次序列化
            ret=json.dumps(ret,cls=JsonCustomEncoder)
            print(ret)
        return HttpResponse(ret)#转为json格式
            # return render(request, 'register.html',{'obj':obj,'ret':ret})


#注册2 ajax 验证
def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method=='GET':
        obj=RegisterForm(request=request, data=request.POST)
        return render(request, 'register.html',{'obj':obj})

    elif request.method=='POST':
        #返回的字符串 字典
        ret={'status':False,'error':None,'data':None}
        #进行验证 调用RegisterForm
        obj=RegisterForm(request=request, data=request.POST)
        if obj.is_valid():
            username = obj.cleaned_data.get('username')#获取用户名
            password = obj.cleaned_data.get('password')
            email= obj.cleaned_data.get('email')
            #print(username,password,email)
            #数据库添加数据
            models.UserInfo.objects.create(username=username,
                                                     password=password,
                                                     email=email,
                                                     nickname=username, )
            #获取用户数据
            user_info= models.UserInfo.objects. \
                filter(username=username, password=password). \
                values('nid', 'nickname',
                       'username', 'email',
                       'avatar',
                       'blog__nid',
                       'blog__site').first()
            request.session['user_info'] = user_info
            #print(user_info.id)
            ret['status']=True
            ret['data']=obj.cleaned_data
            # print(obj.cleaned_data)
            # print(ret)
            ret=json.dumps(ret)#转为json格式
            #return HttpResponse(ret)
        else:
            #加入错误信息
            #print(obj.errors)
            ret['error']=obj.errors.as_data()
            #提示为False
            #ret['status']=False
            #对错误信息对象进行转化处理 前端不用二次序列化
            ret=json.dumps(ret,cls=JsonCustomEncoder)
            #print(ret)
            #print(ret)
        return HttpResponse(ret)

def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.clear()#注销使用
    return redirect('/')
