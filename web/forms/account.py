#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets

from repository import models

from .base import BaseForm

#登陆验证
class LoginForm(BaseForm, django_forms.Form):
    username = django_fields.CharField(
        min_length=6,
        max_length=20,
        error_messages={'required': '用户名不能为空.', 'min_length': "用户名长度不能小于6个字符", 'max_length': "用户名长度不能大于32个字符"}
    )
    password = django_fields.RegexField(
        #正则表达
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=12,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符"}
    )
    #验证码框
    check_code = django_fields.CharField(
        error_messages={'required': '验证码不能为空.'}
    )
    #内置勾子 验证码 校对
    def clean_check_code(self):
        #获取输入的验证码                                      生成的验证码
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            #不相等  返回错误信息
            raise ValidationError(message='验证码错误', code='invalid')


#用户注册表单验证
class UserInfoForm(django_forms.Form):
    user = django_fields.CharField(
        error_messages={'required': '用户名不能为空.'},#required 为空时错误提示
        #widget=widgets.Textarea(attrs={'class': 'c1'}),#定制标签  样式
        #error_messages={'required': '用户名不能为空.'},#required 为空时错误提示
        #widget=widgets.Textarea(attrs={'class': 'c1'}),#定制标签  样式
        #widget=django_widgets.Input(attrs={'class': 'c1'}),#定制标签  样式 生成HTML标签(保留上一次提交的数据)
        #label="用户名",
        )
    pwd = django_fields.CharField(
        label="密码",
        max_length=12,#最多字符长度
        min_length=6,#最少字符长度
        error_messages={'required': '密码不能为空.', 'min_length': '密码长度不能小于6', "max_length": '密码长度不能大于12'},
        widget=django_widgets.PasswordInput(attrs={'class': 'c2'})
    )
    email = django_fields.EmailField(
        label="邮箱",
        error_messages={'required': '邮箱不能为空.','invalid':"邮箱格式错误"}#invalid 邮箱格式错误
    )
    '''
    # pwd = django_fields.CharField(
    #     label="密码",
    #     max_length=12,#最多字符长度
    #     min_length=6,#最少字符长度
    #     error_messages={'required': '密码不能为空.', 'min_length': '密码长度不能小于6', "max_length": '密码长度不能大于12'},
    #     widget=django_widgets.PasswordInput(attrs={'class': 'c2'})
    # )
    user_type=fields.ChoiceField(
        choices=[],#等于空列表
        widget=widgets.Select#下拉框选项  {{obj.user_type}}
    )
    user_type2=fields.ChoiceField(widget=widgets.Select(choices=[]))

    user_type3=ModelChoiceField(
        empty_label='请选择类型',
        queryset=models.UserType.objects.all(),
        to_field_name='id',
    )
    #重写父类 添加功能

    def __init__(self,*args,**kwargs):
        super(UserInfoForm,self).__init__(*args,**kwargs)
        self.fields['user_type'].choices=models.UserType.objects.valuse_list('id','name')#实例化时从数据库中取新数据
        self.fields['user_type2'].widget.choices=models.UserType.objects.valuse_list('id','name')#实例化时从数据库中取新数据
    '''

#注册验证
class RegisterForm1(BaseForm, django_forms.Form):
    #输出的用户名
    username=django_fields.CharField(
        min_length=6,
        max_length=20,
        error_messages={'required': '用户名不能为空.', 'min_length': "用户名长度不能小于6个字符", 'max_length': "用户名长度不能大于32个字符"},
        widget=django_widgets.Input(attrs={'type':"text", 'class':"form-control", 'id':"username" ,'name':"username" ,'placeholder':"请输入用户名"}),#定制标签  样式 生成HTML标签(保留上一次提交的数据)
    )
    email=django_fields.EmailField(
        #label="邮箱",
        error_messages={'required': '邮箱不能为空.','invalid':"邮箱格式错误"},#invalid 邮箱格式错误
        widget=django_widgets.EmailInput(attrs={'type':"email", 'class':"form-control", 'id':"username" ,'name':"email" ,'placeholder':"请输入邮箱"})
    )
    password = django_fields.RegexField(
        #正则表达
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=12,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符",
                        'message':None},
        widget=django_widgets.PasswordInput(attrs={'type':"password", 'class':"form-control", 'id':"username" ,'name':"password" ,'placeholder':"请输入密码"})

    )
    confirm_password=django_fields.CharField(
        #正则表达
        error_messages={'required': '确认密码不能为空.',
                        'invalid': '确认密码不对',
                        },
        widget=django_widgets.PasswordInput(attrs={'type':"password", 'class':"form-control", 'id':"username" ,'name':"confirm_password" ,'placeholder':"请输入确认密码"})
    )

    #验证码框
    check_code = django_fields.CharField(
        error_messages={'required': '验证码不能为空.'},
        widget=django_widgets.PasswordInput(attrs={'type':"password", 'class':"form-control", 'id':"username" ,'name':"check_code" ,'placeholder':"请输入验证密码"})
    )


     #内置勾子
    def clean_username(self):
        #查询是否存在
        username=self.cleaned_data['username']
        u =models.UserInfo.objects.filter(username=username).count()
        if not u:
            return self.cleaned_data['username']
        else:
            raise ValidationError(message='用户名已经存在',code='invalid')

    def clean_email(self):
        email=self.cleaned_data['email']
        e=models.UserInfo.objects.filter(email=email).count()
        if not e:
            return  self.cleaned_data['email']
        else:
            raise ValidationError('邮箱已经被注册!',code='invalid')
    #内置勾子 验证码 校对
    def clean_check_code(self):
        #获取输入的验证码                                      生成的验证码
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            #不相等  返回错误信息
            raise ValidationError(message='验证码错误', code='invalid')
        else:
            return self.cleaned_data['check_code']
    #确认密码
    def clean_confirm_password(self):
        pwd=self.request.POST.get('password')
        pwd2=self.cleaned_data['confirm_password']
        print(pwd,pwd2)
        if pwd != pwd2:
            raise ValidationError('二次输入密码不匹配')
        else:
            return self.cleaned_data['confirm_password']

#注册验证  ajax
class RegisterForm(BaseForm, django_forms.Form):
    #输出的用户名
    username=django_fields.CharField(
        min_length=6,
        max_length=20,
        error_messages={'required': '用户名不能为空.', 'min_length': "用户名长度不能小于6个字符", 'max_length': "用户名长度不能大于32个字符"},
    )
    email=django_fields.EmailField(
        error_messages={'required': '邮箱不能为空.','invalid':"邮箱格式错误"},#invalid 邮箱格式错误
    )
    password = django_fields.RegexField(
        #正则表达
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=12,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符",
                        'message':None},
    )
    confirm_password=django_fields.CharField(
        #正则表达
        error_messages={'required': '确认密码不能为空.',
                        'invalid': '确认密码不对',
                        },
    )
    #验证码框
    check_code = django_fields.CharField(
        error_messages={'required': '验证码不能为空.'},
    )

    #内置勾子
    #用户名重复查询
    def clean_username(self):
        #查询是否存在
        username=self.cleaned_data['username']
        u =models.UserInfo.objects.filter(username=username).count()
        if not u:
            return self.cleaned_data['username']
        else:
            raise ValidationError(message='用户名已经存在',code='invalid')
    #邮箱重复查询
    def clean_email(self):
        email=self.cleaned_data['email']
        e=models.UserInfo.objects.filter(email=email).count()
        if not e:
            return  self.cleaned_data['email']
        else:
            raise ValidationError('邮箱已经被注册!',code='invalid')
    # 验证码 校对
    def clean_check_code(self):
        #获取输入的验证码                                      生成的验证码
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            #不相等  返回错误信息
            raise ValidationError(message='验证码错误', code='invalid')
        else:
            return self.cleaned_data['check_code']
    #确认密码
    def clean_confirm_password(self):
        pwd=self.request.POST.get('password')
        pwd2=self.cleaned_data['confirm_password']
        if pwd != pwd2:
            raise ValidationError('二次输入密码不匹配')
        else:
            return self.cleaned_data['confirm_password']
