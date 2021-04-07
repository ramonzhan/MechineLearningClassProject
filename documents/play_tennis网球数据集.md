# 打网球数据集

> 2021.4.5

play_tennis数据集是一个较小的二分类数据集，用于适合离散特征的模型测试，例如朴素贝叶斯、决策树等。只包含14条数据。记录14天中每天的天气、温度、湿度、风，输出适不适合打网球。

![image-20210405165419647](http://qiniu.nkudial.top/image-20210405165419647.png)

天气包括：sunny overcast rain三个离散值

温度包括：hot mild cool三个离散值

湿度包括：high normal两个离散值

风包括：weak strong两个离散值

四种特征共应有36种组合，而实际只有14种组合。所以有许多未出现的特征组合，需要一些策略来处理。

使用pandas库读取：

```python
import pandas as pd
datapath = "xxxxxxx/play_tennis.csv"   # 数据集文件存放的路径
df = pd.read_csv(path)
```





