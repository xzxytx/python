
### 字节流 <-> 图片
```python
import io
from PIL import Image # 注意我的Image版本是pip3 install Pillow==4.3.0
import requests
 
res = requests.get('http://images.xxx.com/-7c0dc4dbdca3.webp')
 
byte_stream = io.BytesIO(res.content) # 把请求到的数据转换为Bytes字节流(这样解释不知道对不对，可以参照[廖雪峰](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431918785710e86a1a120ce04925bae155012c7fc71e000)的教程看一下)
 
roiImg = Image.open(byte_stream)  # Image打开二进制流Byte字节流数据
 
imgByteArr = io.BytesIO()   # 创建一个空的Bytes对象
 
roiImg.save(imgByteArr, format='PNG') # PNG就是图片格式，我试过换成JPG/jpg都不行
 
imgByteArr = imgByteArr.getvalue()  # 这个就是保存的二进制流
 
# 下面这一步只是本地测试， 可以直接把imgByteArr，当成参数上传到七牛云
with open("./abc.png", "wb") as f:
  f.write(imgByteArr)
```
参考： https://www.jb51.net/article/142392.htm



### selenium设置chrome请求头：
```python
# !/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
# 进入浏览器设置
options = webdriver.ChromeOptions()
# 设置中文
options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
browser = webdriver.Chrome(chrome_options=options)
url = "https://httpbin.org/get?show_env=1"
browser.get(url)
browser.quit()
```

### fromkeys()  统一对键设置值， 去重
{}.fromkeys(('x','y'), -1)