# Django Quickstart

## 环境配置
### Django环境
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

### 数据库环境
Django默认使用sqlite3数据库，但实际工程环境一般使用mysql或者postgresql等。
（待续）

安装完成mysql后，还需要在项目文件做如下配置，以使用MySQL数据库为例：
- 安装所需的包，需要安装`pymysql`和`cryptography`


- 修改`settings.py`的数据库配置

```python
with open(os.path.join(BASE_DIR, 'siteconfig/MYSQL_PASSWORD.env')) as f:
    MYSQL_PASSWORD = f.read()
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '13306',
        'NAME': 'learndjango',
        'USER': 'user',
        'PASSWORD': MYSQL_PASSWORD,
        'TEST': {
            'NAME': 'testdjango',
        }
    }
```

- 修改应用的`__init__.py`文件

```python
import pymysql

pymysql.install_as_MySQLdb()
```

- 执行django脚手架命令
```bash
python manage.py makemigrations
python manage.py migrate
```


## 编写代码
Django的[官方文档入门教程](https://docs.djangoproject.com/en/3.1/intro/overview/)还是很全面的，讲解了后端和前端的基本代码，最基本的后台一般包括实现数据库ORM的Model（models.py），以及管理后台admin（admin.py），最基本的前台，包括网站的两级路由配置（urls.py），视图层实现业务逻辑（views.py），以及模板层提供html页面（templates/*.html）。


### 后端开发
Django的后端包括Model层和admin管理后台。

#### ORM层（models.py）
Django的Model API包括**字段选项**和**字段类型**两个部分，详情见[Model官方文档](https://docs.djangoproject.com/en/3.2/ref/models/fields/)。


```python
from django.db import models

class Student(models.Model):
    SEX_ITEMS = [
        (1, '男'),
        (2, '女'),
        (0, '未知')
    ]

    STATUS_ITEMS = [
        (0, '申请'),
        (1, '通过'),
        (2, '拒绝')
    ]

    name = models.CharField(max_length=128, verbose_name='姓名')
    sex = models.IntegerField(choices=SEX_ITEMS, verbose_name='性别')
    profession = models.CharField(max_length=128, verbose_name='职业')
    email = models.EmailField(verbose_name='邮箱')
    qq = models.CharField(max_length=128, verbose_name='QQ')
    phone = models.CharField(max_length=128, verbose_name='手机')
    status = models.IntegerField(choices=STATUS_ITEMS, default=0, verbose_name='审核状态')
    created_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="创建时间")

    def __str__(self) -> str:
        return f'Student: {self.name}'

    class Meta:
        verbose_name = "学员信息"
        verbose_name_plural = verbose_name
```


#### 管理后台（admin.py）
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


```python
from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sex', 'profession', 'email', 'qq', 'phone', 'status', 'created_time')
    list_filter = ('sex', 'status', 'created_time')
    search_fields = ('name', 'profession')
    fieldsets = (
        (None, {
            'fields': (
                'name',
                ('sex', 'profession'),
            ),
        }),
        ('高级', {
            'classes': ('collapse',),
            'fields': (
                ('email', 'qq', 'phone'),
                'status',
            ),
        }),
    )

admin.site.register(Student, StudentAdmin)
```


### 前台开发
Django的前台展示数据主要是靠Template层渲染View层，使用DRF时没有Template层，而提交数据使用Form层。

#### 网站路由（urls.py）
Django的路由是串联的两级，第一级是站点文件夹内的urls.py，第二级是各个APP文件夹内的urls.py，两级是url要拼接在一起，并且从上往下匹配，可以最下面会放一个404的路由，可参考[官方文档的例子](https://docs.djangoproject.com/en/3.2/topics/http/urls/#example)。

```python
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import index, Index

urlpatterns = [
    path('', index, name='index'),
    path('index', Index.as_view(), name='student_index'),
]
```


#### 业务逻辑层（views.py）
网站路由把访问的url与处理的业务逻辑挂钩，可以[基于函数](https://docs.djangoproject.com/en/3.2/topics/http/views/)，也可以[基于类](https://docs.djangoproject.com/en/3.2/topics/class-based-views/)。业务逻辑层的输入是request，函数或类实例根据业务逻辑进行加工，并输出response。在DRF的前后端分离模式下，response是一个json或xml，而在单体应用下，response是一个html。

```python
from django import forms
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from .models import Student
from .forms import StudentForm

# 基于函数的模板
def index(request):
    students = Student.objects.all()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            # cleaned_data = form.cleaned_data
            # student = Student()
            # student.name = cleaned_data['name']
            # student.sex = cleaned_data['sex']
            # student.email = cleaned_data['email']
            # student.profession = cleaned_data['profession']
            # student.qq = cleaned_data['qq']
            # student.phone = cleaned_data['phone']
            # student.save()
            return HttpResponseRedirect(reverse('student_index'))
    else:
        form = StudentForm()
    
    context = {
        'students': students,
        'form': form
    }
    return render(request, 'student/index.html', context=context)

# 基于类的模板
class Index(View):
    template_name = 'student/index.html'

    def get_context(self):
        context = {
            'students': Student.objects.all(),
        }
        return context

    def get(self, request):
        form = StudentForm()
        context = self.get_context()
        context.update({'form': form})
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('student_index'))
        context = self.get_context()
        context.update({'form': form})
        return render(request, self.template_name, context=context)
```

#### 页面显示层（templates/*.html）
这里会用到django自创的模板命令，此外，django的模板引擎还可以换成Jinja2，[模型字段的引用可以参考官方文档](https://docs.djangoproject.com/en/3.2/ref/models/instances/)。视图通过调用`render(request, template_name, context)`函数，来渲染模板，从而得到response。


#### 表单输入（forms.py）
Django可以事先定义好表单，然后在模板中使用。表单既可以继承自forms.Form类，[字段设置参考这里](https://docs.djangoproject.com/en/3.2/ref/forms/fields/)，也可以继承自forms.ModelForm，直接复用Model的代码，[详情可参考官方文档](https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/)。此外，django的表单还可以[对输入的数据进行校验](https://docs.djangoproject.com/en/3.2/ref/forms/validation/#cleaning-a-specific-field-attribute)。


### 中间件
Django的中间件在前端/后端之前被调用，而且会用于所有的请求/响应，Django框架提供了`django.utils.deprecaion.MiddlewareMixin`类以便于用户自定义站点的中间件。

`MiddlewareMixin`的接口按顺序包括：
1. `process_request(self, request)`：返回None才会执行后续的方法和中间件，返回HttpResonse则不会。
2. `process_view(self, request, func, *args, **kwargs)`
3. `process_exception(self, request, exception)`
4. `process_template_response(self, request, response)`：使用了模板才会调用。
5. `process_response(self, request, response)`：视图层业务处理或者模板层渲染发生异常时才会调用。

`process_response`似乎一定会被调用，但`process_view`等则不一定，例如不涉及业务处理，仅仅刷新页面的时候。

```python
import time
from django.http import response
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class TimeItMiddleware(MiddlewareMixin):
    def process_request(self, request):
        self.start_time = time.time()
        return None

    def process_view(self, request, func, *args, **kwargs):
        if request.path != reverse('index'):
            return None

        start = time.time()
        response = func(request)
        costed = time.time() - start
        print('process view: {:.2f}'.format(costed))
        return response

    def process_exception(self, request, exception):
        pass

    def process_template_response(self, request, response):
        costed = time.time() - self.start_time
        print('render cost: {:.2f}'.format(costed))
        return response

    def process_response(self, request, response):
        costed = time.time() - self.start_time
        print('request to response cost: {:.2f}'.format(costed))
        return response
```


### 测试
Django提供了一个`django.test.TestCase`的基类，开发者可以继承此类来实现自己的单元测试，如果不涉及数据库（测试数据与生产数据是隔离的），则可以使用`SimpleTestCase`作为基类，测试类提供的接口包括：
1. `setUp(self)`：初始化环境。
2. `test_xxxx(self)`：待测试的方法，均会被执行。
3. `tearDown(self)`：清理测试环境。

```python
from django.forms.fields import EmailField
from django.test import TestCase
from .models import Student

class StudentTestCase(TestCase):
    def setUp(self):
        Student.objects.create(
            name='1号玩家',
            sex = 1,
            email = '1@163.com',
            profession = '法师',
            qq = '11',
            phone = '111'
        )

    def test_create_and_sex_status(self):
        student = Student.objects.create(
            name='2号玩家',
            sex = 2,
            email = '2@163.com',
            profession = '战士',
            qq  = '22',
            phone = '222'
        )
        self.assertEqual(student.get_sex_display(), '女', '码表有误')

    def test_filter(self):
        Student.objects.create(
            name='3号玩家',
            sex = 1,
            email = '3@163.com',
            profession = '律师',
            qq = '33',
            phone = '333'
        )
        name = '3号玩家'
        students = Student.objects.filter(name=name)
        self.assertEqual(students.count(), 1, '过滤器有误')

    def test_get_index(self):
        client = self.client
        response = client.get('/student/')
        self.assertEqual(response.status_code, 200, 'homepage not availabel')

    def test_post_index(self):
        client = self.client
        data = dict(
            name='4号玩家',
            sex = 4,
            email = '4@163.com',
            profession = '警察',
            qq = '44',
            phone = '444'
        )
        response = client.post('/student/', data)
        self.assertTrue(b'4@163.com' in response.content, 'post失败')
```