<p align="center"><img src="static/img/logo.png" alt="Sak" height="100px"></p>

🍉 pysak 是一个简单、强大、干净的python公共函数库。

- [安装](#安装)
    - [依赖库](#依赖库)

- [快速上手](#快速上手)
    - [导入](#导入)

- [目录结构](#目录结构)
- [注意事项](#注意事项)
- [已知问题](#已知问题)
- [许可证](#许可证)
- [一些小技巧](#一些小技巧)
    - [pip指定源安装](#pip指定源安装)
    - [导出当前项目依赖](#导出当前项目依赖)

## 安装

### 依赖库
```
pip install -r requirements.txt -i https://pypi.douban.com/simple/
```

## 快速上手

### 导入
如果你将Sak放置于项目的根目录，你可以直接导入Sak，不需要任何前缀：
```
import Sak
```

## 许可证
MIT

## 一些小技巧

### pip指定源安装

```
#阿里源
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
 
#豆瓣
pip install -r requirements.txt -i https://pypi.douban.com/simple/
 
#清华大学
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 导出当前项目依赖

```
pip freeze > requirements.txt
```
