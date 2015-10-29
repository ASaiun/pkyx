# pkyx

pkyx是基于Flask开发的一个比较网站，灵感来自于[VSChart](http://vschart.com)。

## 开发过程
---

[Day 1：配置远程开发环境](http://livevilwt.me/blog/article/57/)

[Day 2：编写应用配置和视图](http://livevilwt.me/blog/article/58/)

[Day 3：编写RESTful API和测试数据库](http://livevilwt.me/blog/article/59/)

[Day 4：使用SuperVisor和Gunicorn优化应用](http://livevilwt.me/blog/article/60/)

[Day 5：编写用户和认证模块](http://livevilwt.me/blog/article/61/)

[Day 6：用模版继承组件化应用](http://livevilwt.me/blog/article/62/)

[Day 7：编写主功能](http://livevilwt.me/blog/article/63/)


## 安装依赖
---

`
pip install -r requirement.txt
`


## 配置文件
---

```
app/config.py
```

## 运行
---

`
gunicorn wsgi:app -c gunicorn.conf
`

or

`
python manage.py
`
