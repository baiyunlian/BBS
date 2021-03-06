# Create your models here.
from django.db import models


#用户表
class UserInfo(models.Model):
    """
    用户表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.CharField(verbose_name='头像',max_length=128,)#可以为空
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    fans = models.ManyToManyField(verbose_name='粉丝们',
                                  to='UserInfo',
                                  through='UserFans',
                                  through_fields=('user', 'follower'))


#博客表
class Blog(models.Model):
    """
    博客信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    urls = models.CharField(verbose_name='个人博客网址', max_length=168,null=True)
    site = models.CharField(verbose_name='个人博客前缀', max_length=32, unique=True)
    theme = models.ForeignKey(verbose_name='博客主题',to='BlogTheme',to_field='nid')
    user = models.OneToOneField(to='UserInfo', to_field='nid')#一对一外键关联

#主题表
class BlogTheme(models.Model):
    nid=models.BigAutoField(primary_key=True)
    themename=models.CharField(verbose_name='主题名称',max_length=32)

#互粉关系表
class UserFans(models.Model):
    """
    互粉关系表
    """
    user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='nid', related_name='users')
    follower = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='nid', related_name='followers')
    #索引字段
    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]

#博主个人文章分类表
class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    #外键关联   博客
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')

#文章表(内容)
class ArticleDetail(models.Model):
    """
    文章详细表
    """
    content = models.TextField(verbose_name='文章内容', )
    #外键对应的文章表
    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid')

#文章点赞表
class UpDown(models.Model):
    """
    文章顶或踩
    """
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='赞或踩用户', to='UserInfo', to_field='nid')
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]

#评论表
class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    #      自关联
    reply = models.ForeignKey(verbose_name='回复评论', to='self', related_name='back', null=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')

#标签对应博客表
class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')


#版块
class ArticleType(models.Model):
    nid=models.IntegerField(primary_key=True)
    article_type=models.CharField(verbose_name='版块名称',max_length=128)

#文章表
class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章简介', max_length=255)
    read_count = models.IntegerField(default=0)#阅读数
    comment_count = models.IntegerField(default=0)#评论数
    up_count = models.IntegerField(default=0)#点赞数
    down_count = models.IntegerField(default=0)#踩数
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', null=True)
    article_type=models.ForeignKey(verbose_name='版块',to='ArticleType',to_field='nid',null=True)
    #多对多 与标签 的第三张表
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

#文章对应标签表
class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid')

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

