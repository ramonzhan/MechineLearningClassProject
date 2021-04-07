# sql语句的pandas实现

> **张文政**
>
> **2020年6月21日**

sql是数据库的语言，可以方便地进行各种增、删、改、查操作，其中的group、join、where等操作更是十分方便。pandas是python的一个数据分析库，以dataframe的格式保存表格数据。那如何像sql操作数据库一样地操作pandas的dataframe，就是一个很有意义的问题。对于将来的办公自动化也很有帮助。

数据库中最重要的建是主键，用于唯一标识表中的一条记录；pandas中默认的主键是行index。

## 1. pandas基本操作

```python
# 创建一个toydataframe
import pandas as pd
df = pd.DataFrame({'total_bill': [16.99, 10.34, 23.68, 23.68, 24.59],
                   'tip': [1.01, 1.66, 3.50, 3.31, 3.61],
                   'sex': ['Female', 'Male', 'Male', 'Male', 'Female']})
df  # 1. 打印dataframe的情况，一般用head()
df.dtypes   # 2. 打印每列的数据类型，str在dataframe中是object类型
# total_bill    float64
# tip           float64
# sex            object
# dtype: object
df.columns   # 3. 打印字段名
# Index(['total_bill', 'tip', 'sex'], dtype='object')
df.shape  # 打印表格行数与列数  (5,3)
df.values  # 转换成numpy.array
```

|       | total_bill | tip  | sex    |
| ----- | ---------- | ---- | ------ |
| **0** | 16.99      | 1.01 | Female |
| **1** | 10.34      | 1.66 | Male   |
| **2** | 23.68      | 3.50 | Male   |
| **3** | 23.68      | 3.31 | Male   |
| **4** | 24.59      | 3.61 | Female |

## 2. sql语句与pandas的对应

介绍select，where，group，as，join，order的用法。

+ **SELECT**

select负责从表中选取数据。语法为：`SELECT colname FROM tablename`

选取**多行多列**时，使用Dataframe的loc和iloc方法。其中loc根据列名，行indexlist或切片来返回；iloc根据行列indexlist或切片来返回。注意默认的行与列index都是从0开始的。返回结果仍是Dataframe；

```python
df.iloc[1:3, 1:3]   # 第1、2行的第1、2列
df.iloc[[1,2,4], [1, 2]]   # 第1、2、4行的第1、2列
df.loc[[1,2,4], ['total_bill', 'tip']]   # 第1、2、4行的total_bill和tip列
```

选取**单个元素**时，使用Dataframe的at和iat方法快速实现。其中at根据列名和行index；iat根据行列index，类似于loc和iloc。返回结果直接是个值。

```python
df.at[3, 'tip']   # 第3行的tip列
df.iat[3, 1]   # 第3行的第1列
```

选取**某些行的所有列/某些列的所有行**时，直接使用Dataframe本身。选取某些行的所有列时，使用行切片，如果不要连续的行，则使用loc即可；选取某些列的所有行时，直接输入列名的list即可。

```python
df[1:3]   # 第1、2行的所有列，仍是dataframe
df.loc[[1,3], :]   # 第1、3行的所有列，仍是dataframe
df['total_bill']   # total_bill列，是个series
df[['total_bill', 'tip']]   # total_bill和tip列，仍是dataframe
```

+ **WHERE**

where在sql中负责有条件地从表中选取数据。语法为：`SELECT colname FROM tablename WHERE colname operator value`。在pandas可以使用[]，query，isin等方法实现。

```python
df[df['sex'] == 'Female']   # 返回sex列为Female的行的全部列，仍是dataframe
df[df['total_bill'] > 20]  # 返回total_bill列大于20的
df.query('total_bill > 20')  # 另一种写法
```


除了上面的对单列的条件，也可以使用**and/or/not逻辑**，或者**属于**关系。

```python
df[(df['sex'] == 'Female') & (df['total_bill'] > 20)]   # and
df[(df['sex'] == 'Female') | (df['total_bill'] > 20)]   # or
df[-(df['sex'] == 'Male')]   # not
df[df['total_bill'].isin([21.01, 23.68, 24.59])]   # in
df[-df['total_bill'].isin([21.01, 23.68, 24.59])]  # not in
```

 也可以使用string function结合正则表达式使用：`df[-df.app.str.contains('^微信\d+$')]`

+ **GROUP BY**

GROUP BY 语句用于结合**合计函数**，根据**一个或多个列对结果集进行分组**。其语法为：

`SELECT colname1, aggregate_func(colname) FROM tablename WHERE colname operator value GROUP BY colname1`

pandas的groupby包括 sum, count, min, mean, max等，或者直接用agg函数指定对多列的合计。

基本地，groupby可以根据一列来进行分组：

```python
df.groupby('sex')['tip'].sum()  # 根据sex进行分组，并对每个sex的tip加和
# > sex
# > Female    2
# > Male      3
# Name: tip, dtype: int64
df.groupby('sex').count()   # 根据sex分组，对其余每列统计有值的个数
# > 	total_bill  tip
# > sex 
# > Female      2    2
# > Male        3    3
df.groupby('sex')['tip'].count()  # 仅对tip列统计有值的个数
df.groupby('sex').agg({'tip': np.min, 'total_bill': np.sum})  # 使用agg函数为不同列指定不同的合计函数
```

+ **AS**

AS在sql中用于指定列的别名，方便理解。在pandas中，类似的可以使用rename来更改列名（inplace=True的话就把原来的dataframe也更改了）

`df.rename(columns={'total_bill': 'total', 'tip': 'pit', 'sex': 'xes'}, inplace=True)`

+ **JOIN**

 join 用于把来自两个或多个表的行结合起来，基于这些表之间的共同字段，从这些表中查询数据。常见的JOIN有4种，INNER JOIN (JOIN), LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN。第一种为内连接，后三种为外连接。语法为

`SELECT colname FROM table1 (INNER/LEFT/RIGHT/FULL OUTER) JOIN table2 ON table1.colname=table2.colname`

**INNER JOIN**：取表1和表2的交集；**LEFT JOIN**：产生表1的完全集，而2表中匹配的则有值，没有匹配的则以null值取代；RIGHT JOIN与LEFT JOIN相反；**FULL OUTER JOIN**：产生1和2的并集。但是需要注意的是，对于没有匹配的记录，则会以null做为值。

以下面两个表为例:

```python
df1 = pd.DataFrame({'total_bill': [16.99, 10.34, 23.68, 23.68, 24.59, 12.32],
                    'tip': [1.01, 1.66, 3.50, 3.31, 3.61, 3.9],
                    'sex': ['Female', 'Male', 'Male', 'Male', 'Female','Male']})
df2 = pd.DataFrame({'total_b': [16.99, 10.34, 23.68, 23.68, 24.59],
                    'ti': [1.01, 1.66, 3.50, 3.31, 3.61],
                    'sex': ['Female', 'Male', 'Male', 'Male', 'Female']})
```