简单的BBS论坛
实现功能
1、整体参考“抽屉新热榜” ＋ “博客园”
2、实现不同论坛版块
3、帖子列表展示
4、个人博客主页
5、个人博客标签、分类、时间 筛选
6、帖子评论数、点赞数展示
7、允许登录用户发贴、评论、点赞
8、允许上传文件(个人头像)
9、可进行多级评论
10、个人博客后台管理(创建\编辑\删除文章,个人分类\个人标签管理,可以选择个人博客主题,)
11, 通过admin模块可以管理(添加\删除)论坛版动,管理博客的主题.



```
说明:
    启用前:请先通过admin模块进行版块,博客主题的添加(当前 admin模块 用户名:admin 密码:adminadmin 
                                                    版块:python go liunx  博客主题: 3个 )
                                                    
                                                    
                                                    
  程序结构:

 BBS/#主目录

  |- - -BBS/# 主程序目录

 |       |- - -init.py

 |       |- - -settings#配置文件

 |       |- - -urls.py#主路由

 |       |- - -wsgi.py#WSIG规范文件

 |

 |

 |- - -backend/#个人博客后台程序目录

 |       |- - -init.py

 |       |- - -admin.py

 |       |- - -apps.py

 |       |- - -auth/#登陆装饰函数目录

 |       |     |- - -auth.py #登陆装饰函数

 |       |

 |       |- - -forms/#表单验证函数目录

 |       |     |- - -article.py #表单验证函数

 |       |

 |       |- - -migrations

 |       |     |- - -init.py

 |       |

 |       |- - -models.py

 |       |

 |       |- - -templatetags/#注册为模块 load

 |       |     |- - -serach.py#条件搜索生成

 |       |

 |       |- - -tests.py

 |       |- - -urls.py#后台路由

 |       |

 |       |- - -views/#视图函数

 |       |     |- - -user.py#逻辑函数

 |

 |- - -db.sqlite3/Django自带数据库

 |- - -manage.py#管理Django程序

 |- - -Monaco.ttf#字体库

 |

 |- - -repository/#数据表结构目录

 |       |- - -init.py

 |       |- - -admin.py# django 管理注册

 |       |- - -apps.py

 |       |- - -migrations/#数据库操作日志

 |       |- - -models.py#表结构

 |       |- - -tests.py#单元测试

 |

 |

 |- - -static/#静态文件目录

 |       |- - -css/# css文件目录

 |       |- - -imgs/# 图片文件目录

 |       |- - -js/#js文件目录

 |       |- - -plugins/#前端框架文件目录

 |

 |- - -templates/#HTML文件目录

 |       |- - -backend_add_article.html#增加文章页面

 |       |- - -backend_article.html#个人文章页面

 |       |- - -backend_base_info.html#个人信息管理页面

 |       |- - -backend_category.html#个人分类管理页面

 |       |- - -backend_edit_article.html#个人文章编辑页面

 |       |- - -backend_index.html#个人管理主页面

 |       |- - -backend_no_article.html#个人无文章显示页面

 |       |- - -backend_tag.html#个人标签管理页面

 |       |- - -home.html#个人博客主页面

 |       |- - -home_detail.html#个人博客文章详细页面

 |       |- - -home_title_list.html#个人博客文章分类页面

 |       |- - -include/#include 目录(可包含)

 |       |       |- - -header.html#顶部菜单模板

 |       |- - -index.html#主页面

 |       |- - -login.html#登陆页面

 |       |

 |       |- - -master/#母板目录

 |       |       |- - -backend_layout.html#后台页面模板

 |       |       |- - -home_layout.html#显示页面模板

 |       |- - -register.html#注册页面

 |

 |- - -utils/#自定义插件目录

 |       |- - -check_code.py#验证码

 |       |- - -pagination.py#分页

 |       |- - -xss.py#XSS过滤

 |- - -web/#WEB主页面服务端程序目录

 |       |- - -init.py

 |       |- - -admin.py

 |       |- - -apps.py

 |       |- - -forms/#表单验证函数

 |       |       |- - -account.py#登陆相关

 |       |       |- - -base.py#表单相关

 |       |- - -migrations/#

 |       |- - -tests.py#

 |       |- - -urls.py#对应关系 (路由)

 |       |- - -views/##视图函数

 |       |       |- - -init.py

 |       |       |- - -account.py#登陆相关函数

 |       |       |- - -home.py#主页面相关函数

 |       |

 |

 |- - -README


                                                  
 
```

