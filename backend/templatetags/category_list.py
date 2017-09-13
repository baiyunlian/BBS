#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#BBS 
#2017/9/4    8:23
#__author__='Administrator'
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register=template.Library()#注册为模板