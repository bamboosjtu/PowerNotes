# Django Quickstart

## 环境配置
```bash
pip install pipenv
pipenv shell
pipenv install django
pipenv install djangorestframework

django-admin startproject siteconfig .
python manage.py startapp student
```

以上完成初始化配置，创建了项目和App，此时项目的目录结构如下。

```bash
# tree查看目录结构
.
├── manage.py
├── Pipfile
├── Pipfile.lock
├── README.md
├── siteconfig
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── student
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```

## 编写代码
Django的[官方文档入门教程](https://docs.djangoproject.com/en/3.1/intro/overview/)还是很全面的，讲解了后端和前端的基本代码，最基本的后台一般包括实现数据库ORM的Model（models.py），以及管理后台admin（admin.py），最基本的前台，包括网站的两级路由配置（urls.py），视图层实现业务逻辑（views.py），以及模板层提供html页面（templates/*.html）。

### 后端开发
Django的后端包括Model层和admin管理后台。

- ORM层
Django的Model API包括**字段选项**和**字段类型**两个部分，详情见[Model官方文档](https://docs.djangoproject.com/en/3.2/ref/models/fields/)。

- admin管理后台
为快速开发，一般会为每个模型注册一个管理后台，以便直接操作数据库，具体可以参考下[ModelAdmin options](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#modeladmin-options)。
  - 后台列表页的url为/admin/*model*/*model*
  - 后台编辑页的url为/admin/*model*/*model*/add或者/admin/*model*/*model*/*id*/change

比较常见的管理后台选项有：


| ModelAdmin options | 定义 |
|------------------|-----|
| [list_display](https://docs.djangoproject.com/en/3.2ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display) | 后台列表页上显示的字段，默认为__str__ |
| [list_filter](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter) | 后台列表页上显示的筛选字段 |
| [search_fields](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields) | 后台列表页上用于搜索的字段 |
| [fieldsets](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets) | 后台编辑页上显示的字段 |



### 前台开发
#### 页面展示
Django的前台界面展示主要是靠Template层渲染View层，使用DRF时没有Template层。

#### 页面交互
Django提交数据使用Form层。