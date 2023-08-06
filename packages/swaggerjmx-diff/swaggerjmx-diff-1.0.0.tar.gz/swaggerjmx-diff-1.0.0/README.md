# swaggerjmx-diff

[![Build Status](https://travis-ci.com/Pactortester/swaggerjmx-diff.svg?branch=master)](https://travis-ci.com/Pactortester/swaggerjmx-diff) ![PyPI](https://img.shields.io/pypi/v/swaggerjmx-diff) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/swaggerjmx-diff) ![GitHub top language](https://img.shields.io/github/languages/top/Pactortester/swaggerjmx-diff) ![PyPI - Downloads](https://img.shields.io/pypi/dm/swaggerjmx-diff?style=plastic) ![GitHub stars](https://img.shields.io/github/stars/Pactortester/swaggerjmx-diff?style=social) ![https://blog.csdn.net/flower_drop](https://img.shields.io/badge/csdn-%40flower__drop-orange)



## 安装


pip install swaggerjmx-diff


##  仓库地址：


- github：https://github.com/Pactortester/swaggerjmx-diff.git
- pypi：https://pypi.org/project/-diff


## 适用场景


1. 由于接口测试脚本编写耗时，而且需要持续维护，耗时耗力，使用此工具可以一键生成接口测试脚本.
2. swagger-ui接口文档一键生成jmx文件供jmeter使用.


## 功能


1. 对比2个 swagger json 是否有变化，监控 swagger的变动
2. 将新增/修改 的接口 组装成新的 swagger json
## Demo
- 可以直接访问 swagger_url (http://ip:port/v2/api-doc) 不需要登录的，使用Demo_1方式转换

```python
# -*- coding: utf-8 -*-

from swaggerjmx_diff.diff import *

with open('open-api-v1.json', 'r', encoding='utf8')as fp:
    json_data_v1 = json.load(fp)

with open('open-api-v2.json', 'r', encoding='utf8')as fp:
    json_data_v2 = json.load(fp)
    
contrast_result, result = contrast_swagger(json_data_v1, json_data_v2)

format_swagger_v2(diff_result=contrast_result, latest_swagger=json_data_v2)

```
