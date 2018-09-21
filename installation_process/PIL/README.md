
### Image
```python
from PIL import Image  # 导入模块
img = Image.opne("test.png")  # 打开图片
img = self.img.convert('1')  # 图片二值化
x, y = img.size  # 获取图片尺寸
rgb_tuple = img.getpixel((x, y))  # 根据坐标获取像素点
img.putpixel((x, y), rgb_tuple)  # 根据坐标设置像素点
image2 = img.crop((1, 1, 4, 4))  # 根据坐标裁剪图片
image2.save("test2.png")  # 图片保存
new_img = img.resize((32, 40), Image.BILINEAR)  # 修改图片大小
```

