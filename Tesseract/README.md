
windows
python -m pip install --upgrade pip  # 更新源
pip install pytesseract


image = Image.open('test.jpg')

text = pytesseract.image_to_string(image)



### 安装Tesseract

https://github.com/tesseract-ocr/

#### windows:
- 页面寻找下载包:  https://github.com/UB-Mannheim/tesseract/wiki
- 中文数据集：  https://github.com/tesseract-ocr/tesseract/wiki/Data-Files  # 放到tessdata文件下
- 已下载好的解压可直接使用: Tesseract-OCR.zip
- 配置path： C:\Program Files\Tesseract-OCR  # 默认位置
- 配置环境变量： TESSDATA_PREFIX = C:\Program Files\Tesseract-OCR\tessdata
```
# tesseract imagename outputbase [-l lang] [-psm pagesegmode] [configfile...]
tesseract myscan.png out  # 运行
tesseract test.jpg out -l chi_sim  # 简体中文
```
python 调用
```python
# 第一种
import subprocess
subprocess.call(["tesseract", "-l", "chi_sim", "图片.png", "结果"])
# 第二种
from PIL import Image
import pytesseract
pytesseract.image_to_string(Image.open('图片.jpg'),lang='chi_sim')
```


CentOS 7
yum install tesseract 


### 安装pytesseract
pip install pytesseract