
### 基础知识
* ndarray.ndim：数组的轴（维度）的个数。在Python世界中，维度的数量被称为rank。
* ndarray.shape：数组的维度。这是一个整数的元组，表示每个维度中数组的大小。对于有n行和m列的矩阵，shape将是(n,m)。因此，shape元组的长度就是rank或维度的个数 ndim。
* ndarray.size：数组元素的总数。这等于shape的元素的乘积。
* ndarray.dtype：一个描述数组中元素类型的对象。可以使用标准的Python类型创建或指定dtype。另外NumPy提供它自己的类型。例如numpy.int32、numpy.int16和numpy.float64。
* ndarray.itemsize：数组中每个元素的字节大小。例如，元素为 float64 类型的数组的 itemsize 为8（=64/8），而 complex32 类型的数组的 itemsize 为4（=32/8）。它等于 ndarray.dtype.itemsize 。
* ndarray.data：该缓冲区包含数组的实际元素。通常，我们不需要使用此属性，因为我们将使用索引访问数组中的元素。

```python
>>> import numpy as np
>>> a = np.arange(15).reshape(3, 5)  # 创建范围15，3层5个的数组
>>> a

>>> a.shape  # 获取数组的维度
>>> a.ndim  # 数组的轴（维度）的个数
>>> a.dtype.name  # 类型
>>> a.itemsize  # 数组中每个元素的字节大小
>>> a.size  # 数组元素的总数。这等于shape的元素的乘积。

>>> type(np.array([6, 7, 8])) == type(a)  # True
```

#### 数组的创建
有几种创建数组的方法。

```python
>>> import numpy as np
>>> a = np.array([2, 3, 4])  # 参数必须是list
>>> b = np.array([1.2, 3.5, 5.1])
>>> b = np.array([(1.5,2,3), (4,5,6)])  # 可以是多维创建
>>> c = np.array( [ [1,2], [3,4] ], dtype=complex )  # 自定义数组类型

```

* 创建具有初始占位符内容的数组。
* 减少数组增长，因增长操作发费很大。
* zeros:0组成
* ones:1组成
* empty:内容随机并取决于存储器状态
* 默认类型：float64

```python
>>> np.zeros( (3,4) )  # 创建值为0的数组
>>> np.ones( (2,3,4), dtype=np.int16 )  # 创建值为1的int类型数组
>>> np.empty( (2,3) )  # 随机值

>>> np.arange( 10, 30, 5 )  # 类似range函数， 创建10-30间隔5的数组
>>> np.arange( 0, 2, 0.3 )  

# 浮点最好用 linspace
>>> from numpy import pi
>>> np.linspace( 0, 2, 9 )                 # 9 numbers from 0 to 2
array([ 0.  ,  0.25,  0.5 ,  0.75,  1.  ,  1.25,  1.5 ,  1.75,  2.  ])
>>> x = np.linspace( 0, 2*pi, 100 )        # useful to evaluate function at lots of points
>>> f = np.sin(x)
```
另见：
---
array, zeros, zeros_like, ones, ones_like, empty, empty_like, arange, linspace, numpy.random.rand, numpy.random.randn, fromfunction, fromfile


### 打印数组
```python
>>> a = np.arange(6)  # 一维
>>> print(a)

>>> b = np.arange(12).reshape(4, 3)  # 二维
>>> print(b)

>>> c = np.arange(24).reshape(2, 3, 4)  # 三维
>>> print(c)

# 设置强制打印整个数组， 开启只需要输入具体值
>>> np.set_printoptions(threshold=np.nan)
```

参考：https://www.numpy.org.cn/user_guide/quickstart_tutorial/the_basics.html