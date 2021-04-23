# [Auto-Fly]广软飞Young自动连接
>这个项目是为了能在Liunx里面使用学校宽带,最终来实现内外网映射。<br/>
>使用11层的神经网络进行训练实现验证码识别,最终达到97%的准确率,准确率还是挺不错的。<br/>
> 项目包括 数据集的采集和人工标签 数据集训练 网络连接和自动重连

## 1.演示视频

>正在肝...

## 2.快速开始

默认使用CPU进行前向运算，如果需要使用GPU平台，需要安装CUDA和TF-gpu版本，同时需要将`requirements.txt`中`tensorflow==2.4.1`改为`tensorflow-gpu==2.4.1`



需要修改如下：

```
wlanacip = "183.3.151.148" #服务器IP 不需要修改
wlanuserip = "172.16.xxx.xxx" # 学校DHCP分配的IP
```

### Windows平台

```
pip install requirements.txt -y -i https://pypi.tuna.tsinghua.edu.cn/simple
python auto_fly_young_win10.py
```

## Docker

> 正在肝...
>
> 在ubuntu里面装tensorflow和opencv限制太多了，目前还不知道能不能在树莓派ARM里面实现
>
> 学校网络真的忒慢了



## 3.框架设计

- 训练数据的采集和人工标注
  - 用Qt画了个简单的窗口进行人工标注
- 神经网络搭建
  - 图像分割
  - 34分类任务
  - 11层类似LeNet网络搭建
  - 输入22*22 输出34
- 网络连接
  - 登录接口RSA加密处理
  - 自动重连



![image-20210423222930615](C:\Users\goodhao\AppData\Roaming\Typora\typora-user-images\image-20210423222934066.png)

![image-20210423223017682](C:\Users\goodhao\AppData\Roaming\Typora\typora-user-images\image-20210423223017682.png)

不同大小的数据集对loss的影响

```
#500数据集  loss: 3.4084 - accuracy: 0.0951 - val_loss: 3.3525 - val_accuracy: 0.0556
#1000数据集 loss: 0.6837 - accuracy: 0.8083 - val_loss: 0.2254 - val_accuracy: 0.9534
#3000数据集  loss: 0.2575 - accuracy: 0.9542 - val_loss: 0.1514 - val_accuracy: 0.9765
```

##### windowToast提示

![image-20210423223354834](https://i.loli.net/2021/04/23/3UORgkypaYKcMCI.png)

![image-20210423223422317](https://i.loli.net/2021/04/23/9CGhxY4vDEbKXO6.png)

## 目录结构

> 正在肝...



## 已知问题

- 图像分割效果差，导致识别最终准确率低，平均需要识别4次验证码才能成功。后期采用垂直投影进行图像分割。



## 实际效果

- 断线可在10秒内进行重连成功。



## 性能分析

由于tensorflow和opencv两大库，内存占用无法避免

![image-20210423224513236](https://i.loli.net/2021/04/23/lfjBaA2uoEzU9me.png)