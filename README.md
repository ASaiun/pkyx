# pkyx

pkyx是基于Flask开发的一个比较网站，灵感来自于[VSChart](http://vschart.com)。

demo: [pkyx](http://45.78.53.13)

## 开发过程
---

[Day 1：配置远程开发环境](http://tonnie17.github.io/2015/10/11/pkyx-day1/)

[Day 2：编写应用配置和视图](http://tonnie17.github.io/2015/10/15/pkyx-day2/)

[Day 3：编写RESTful API和测试数据库](http://tonnie17.github.io/2015/10/18/pkyx-day3/)

[Day 4：使用SuperVisor和Gunicorn优化应用](http://tonnie17.github.io/2015/10/21/pkyx-day4/)

[Day 5：编写用户和认证模块](http://tonnie17.github.io/2015/10/23/pkyx-day5/)

[Day 6：用模版继承组件化应用](http://tonnie17.github.io/2015/10/25/pkyx-day6/)

[Day 7：编写主功能](http://tonnie17.github.io/2015/10/29/pkyx-day7/)

[Day 8：使用GridFS实现文件上传](http://tonnie17.github.io/2015/10/30/pkyx-day8/)

[Day 9：配置Celery&Redis运行后台任务](http://tonnie17.github.io/2015/11/01/pkyx-day9/)

[Day 10：编写Dockerfile](http://tonnie17.github.io/2015/11/06/pkyx-day10/)

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
