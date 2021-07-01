# Vue新手避坑不完全指南

[toc]

## 参考资料
- [4小时快速玩转vue.js](https://www.bilibili.com/video/BV1aK4y1K7xx)：无vue的要求，大致理解Vue框架的体系，Vue项目结构，Vue-router/Vuex/Ajax。
- [使用RESTful API探索艺术世界](https://www.bilibili.com/video/BV1kQ4y1R7xQ)：了解下前后端交互使用的api。
- [Vuetify教程](https://www.bilibili.com/video/BV1ib411a7ND)：纯英文，版本有点老，学习如何使用vuetify官方文档。
- [Bootstrap快速上手](https://www.bilibili.com/video/BV1aK4y1K7xx)：理解Vue的12 grid的布局，vuetify和bootstrap间没有依赖关系，但是都是栅格布局。
- MS Reactor系列
    - [Vue.js开发入门](https://www.bilibili.com/video/BV1W5411T7c5)：从html/css/js的角度理解vue.js，并搭建一个简单的应用。
    - [Vue.js创建动态页面](https://www.bilibili.com/video/BV1Ko4y1C7xG?t=5)：数据渲染和表单输入。
    
## 一. 环境准备
我遇到的第一个坑是如何构建出类似whaleweb的项目目录，有一个困扰了我很久的问题是本项目除了vue、vue-cli这几个包外，还有vuetify、@mdi/font等包，尤其是`@mdi/font`这个包未安装会导致`v-icon`无法正确显示。

- Step1：安装nvm

windows用户参考[这里](https://github.com/coreybutler/nvm-windows)

- Step2：安装node

```bash
nvm install 14
nvm use 14
node --version
```

- Step3：安装vue、vue-cli

> Vue CLI 致力于将 Vue 生态中的工具基础标准化。它确保了各种构建工具能够基于智能的默认配置即可平稳衔接，这样你可以专注在撰写应用上，而不必花好几天去纠结配置的问题。与此同时，它也为每个工具提供了调整配置的灵活性，无需 eject。

```bash
npm install -g vue
npm install -g vue-cli
```

- Step4：初始化工程

这里使用vue-cli的脚手架，不太理解webpack和simple等模板的不同，vue-cli创建项目的官网文档可参考[这里](https://cli.vuejs.org/zh/guide/creating-a-project.html#vue-create)。
初始化配置vue-router要选，es-lint千万别选。

```bash
vue init webpack
npm install

# 本项目用到的相关插件
npm install axios --save
npm install vuetify --save
npm install @mdi/font --save
npm install material-design-icons-iconfont -D
npm install vue-router --save

# 启动项目
npm run dev

# 编译打包
npm run build
```

- Step5：VSCode的插件
我装了Vetur、vue、Vue、vue-beautify、vuetify-snippets、vuetify-vscode，不过都是自己随便找的，希望能够提供进一步的指导。


## 二. 理解目录结构与配置文件

我创建好的工程项目的目录结构如下。学习的时候比较困扰的是代码应该写在那里（`/src`），以及这一系列的配置文件，包括但不限于怎么修改前端端口号，怎么设置后端的端口号。

```bash
.
├── build
│   ├── build.js
│   ├── check-versions.js
│   ├── logo.png
│   ├── utils.js
│   ├── vue-loader.conf.js
│   ├── webpack.base.conf.js
│   ├── webpack.dev.conf.js
│   └── webpack.prod.conf.js
├── config
│   ├── dev.env.js
│   ├── index.js
│   └── prod.env.js
├── node_modules
│   ├── .bin
│   │   └── ...
│   └── ...
├── src
│   ├── App.vue
│   ├── assets
│   │   └── logo.png
│   ├── components
│   │   └── HelloWorld.vue
│   ├── main.js
│   └── router
│       └── index.js
├── static
│   └── .gitkeep
├── .babelrc
├── .editorconfig
├── .postcssrc.js
├── index.html
├── package-lock.json
├── package.json
└── README.md
```


对于配置配置文件，`package.json`似乎是与node相关的配置文件，可以查看和自定义npm命令。`build/`和`config/`似乎是与vue.js项目相关的配置文件，但不知道怎么和vue-cli的文档对应，使用过程中需要修改或理解的地方有

- `build/webpack.base.conf.js`将`@`定义为`src/`，不理解这个没法理解源文件的路径。
- `config/index.js`中`port`和`proxyTable`的定义，但是这个好像只能用于dev环境，在test和prod环境中无效。
    - `port`与前端通过那个端口访问有关
    - `proxyTable`与前端服务重定向到那个后端服务有关，在本机上联调的时候需要使用。


## 三. 理解vue项目是如何运行的

vue的教材一般上来直接讲v-directives和数据绑定，无助于将页面与代码进行对应，折腾了很久发现关键是理解`main.js`和`App.vue`这两个文件，个人觉得官方教程[vue.js介绍](https://cn.vuejs.org/v2/guide/index.html)写的不是很清楚。

`whale-web`中`App.vue`直接引用vue-router，过早的牵扯到了路由的知识，建议这里改成在App.vue中实现布局，而不是在Layout组件中实现布局，并用路由`router/index.js`进行重定向。

但是这里很坑的一点是vuetify的预置布局的github代码全部打不开，只能参考它的Application组件的[文档](https://vuetify.cn/zh-Hans/components/application/#%E9%BB%98%E8%AE%A4%E5%BA%94%E7%94%A8%E7%A8%8B%E5%BA%8F%E6%A0%87%E8%AE%B0)，并注销`v-navigation-drawer`。

这里有一个疑问，现在的网站是不是都是按照导航栏`v-app-bar`、主要内容`v-main`、页脚v-footer的三段式布局？


## 四、理解.vue文件和component
第一个Vue的Task是自定义导航栏，建议通过这个任务，演示Vue的组件和路由，这一步可以实现站点的模块的划分。

这里要同时了解：
1. vue.js的[组件](https://cn.vuejs.org/v2/guide/components.html)，.vue文件包括template/script/style三个部分，分别与html/js/css对应。
2. vue-router中的路由配置，修改`router/index.js`文件，其中的component会替换`<router-view></router-view>`的内容。
3. vuetify的组件`v-btn`和`v-icon`，图标库iconfonts的安装参考[这里](https://vuetify.cn/zh-Hans/customization/icons/#install-font-awesome-5-icons)，查找图标可看[这里](https://pictogrammers.github.io/@mdi/font/5.4.55/)，

如果还能讲解下如何自定义组件就更好了。


## 五、构建列表页和详情页
第二个Vue的Task是构建列表页和详情页。

列表页的构建会大量的用到`v-card`这个组件，和`v-for`这个指令。v-directives和数据绑定不难理解，构建列表页本身还是比较轻松的，主要麻烦的排版，必须要理解bootstrap的12个格子，vuetify的[grid文档](https://vuetify.cn/zh-Hans/components/grids/)我是没看懂，最后找了B站的视频，才搞清楚了`v-row`和`v-col`这些。

组件之间的数据传递要实操比较多次，例如列表页点击一个按钮，打开详情页，这里会牵扯到vue-router的子路由的知识。


## 六、Ajax
Ajax获得后端数据本身不难，麻烦的是怎么处理跨站，在本地开发环境下，要修改配置文件`config/index.js`中的`proxyTable`，而远程开发环境下，我也不知道怎么做，大作业中设置了重定向，所以不用处理跨站，希望能够详细讲解一下跨站。


## 未完待续
以下两个功能，我也买开始实操。
- vuex
- form
- 产品经理or设计师与前端的工作界面
- mock
