from django.contrib import admin

# Register your models here.
from repository import models
admin.site.register(models.ArticleType)# 版块分类 注册到DJANGO admin
admin.site.register(models.BlogTheme)#博客主题
