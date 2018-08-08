

* [1](#1)
  * [svm、手写数字](#svm、手写数字)

## 1
###  svm、手写数字
```python
# 加载数据集
from sklearn import datasets
iris = datasets.load_iris()
digits = datasets.load_digits()

print(digits.data)  # 样本特征
print(digits.target)  # 对应真实类别
print(digits.images[0])  # 图形形状（8， 8）

# 估计器 实现:支持向量分类（分类器）
from sklearn import svm
clf = svm.SVC(gamma=0.001, C=100)  # gamma:通过网格搜索及交叉验证找到良好值

# 训练（使用除最后一张意外的所有图像）
clf.fit(digits.data[:-1], digits.target[:-1])

# 预测最后一条
clf.predict(digits.data[-1:])
```

### 模型持久化
```python
# 模型
from sklearn import svm
from sklearn import datasets
clf = svm.SVC()
iris = datasets.load_iris()
X, y = iris.data, iris.target
clf.fit(X, y)  

# 内置持久化模块将模型保存
# 注意：pickle有一些安全性和维护性问题
import pickle
s = pickle.dumps(clf)  # 将模型转成字节流
clf2 = pickle.loads(s)  # 把字节流转成模型
clf2.predict(X[0:1])  # 预测

# 使用joblib  保存模型（只能序列化到磁盘，不能到字符串）
from sklearn.externals import joblib
joblib.dump(clf, 'filename.pkl')  # 存
clf = joblib.load('filename.pkl')  # 取
```
**注意：** pickle（和通过扩展的 joblib），在安全性和可维护性方面存在一些问题。 有以下原因
* 未经pickle信任的数据，可能会执行恶意代码
* 虽然模型可以在其他版本加载，但可能产生意想不到的结果
