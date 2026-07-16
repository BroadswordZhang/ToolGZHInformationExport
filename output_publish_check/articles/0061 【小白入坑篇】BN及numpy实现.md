---
标题: "【小白入坑篇】BN及numpy实现"
公众号名称: "张大刀修炼手册"
作者: "张大刀修炼手册"
发布时间: "2022-03-19 19:30:00"
原文链接: "https://mp.weixin.qq.com/s/zmok_UK3sK81aoj8wBgKFg"
文章详情_share_type: "0"
文章ID: "2247484582"
是否已删除: "False"
版权状态: "11"
版权类型: "1"
阅读量: "268"
喜欢数: "6"
转载量: "1"
文章详情_vote_id: "[]"
文章详情_super_vote_id: "[]"
文章详情_cover: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibFdggLF2iaTXcFOXmfqDlX25uj6c8FP5cy91WE3e69vvJN3bcyic8wrKSNR9IwZmyCQOTGGmhHFDAiaA/0?wx_fmt=jpeg"
文章详情_smart_product: "0"
文章详情_modify_status: "1"
文章详情_appmsg_like_type: "2"
文章详情_can_delete_status: "0"
点赞数: "13"
图文序号: "1"
文章详情_is_pay_subscribe: "0"
文章详情_is_from_transfer: "0"
文章详情_public_tag_info: "{\"public_tag_list\": [], \"modify_times\": 0, \"init_tag_list_size\": 0}"
文章详情_appmsg_album_info: "{\"appmsg_album_infos\": []}"
文章详情_open_fansmsg: "0"
文章详情_is_cooling_article: "0"
文章详情_pic_cdn_url_235_1: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibFdggLF2iaTXcFOXmfqDlX25ibZzexfVib2Nib4yvxwId4Rc7gzMUnrwus8icfpWrSTGTvXCu1mzqNbk7A/0?wx_fmt=jpeg"
文章详情_pic_cdn_url_16_9: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibFdggLF2iaTXcFOXmfqDlX25ibZzexfVib2Nib4yvxwId4Rc7gzMUnrwus8icfpWrSTGTvXCu1mzqNbk7A/0?wx_fmt=jpeg"
文章详情_disable_recommend: "0"
文章详情_line_info: "{\"use_line\": 1, \"line_count\": 0, \"send_time\": 1647689400, \"is_appmsg_flag\": 1, \"is_use_flag\": 0}"
文章详情_claim_source_type: "0"
分享量: "1"
文章详情_is_rumor_refutation: "0"
文章详情_multi_picture_cover: "0"
文章详情_share_imageinfo: "[]"
朋友圈点赞数: "0"
文章详情_item_show_type: "0"
文章详情_ad_info: "{\"has_agreement_ad\": 0, \"is_recruit_agreement_ad\": 0}"
文章详情_audio_in_appmsg: "[]"
文章详情_modify_wording: "还可以修改3次"
文章详情_can_modify: "1"
文章详情_modify_detail_wording: "[]"
文章详情_appmsg_modified: "0"
文章详情_location_page_show: "0"
文章详情_can_location_page_show: "0"
发布消息ID: "1000000021"
发布类型: "101"
发送状态: "{\"total\": 35, \"succ\": 35, \"fail\": 0, \"progress\": 100, \"userprotect\": 0}"
发布结果: "{\"msg_status\": 2, \"refuse_reason\": \"\", \"reject_index_list\": [], \"update_time\": 1752674457}"
是否新发布: "0"
文章详情_publish_copy_type: "77"
文章详情_publish_copy_appmsg_id: "100000841"
文章分析_统计错误: "analysis page parsing failed"
---

# 【小白入坑篇】BN及numpy实现

![]()

![]()

点击上方蓝字一起入坑

![]()

![]()

卷积神经网络（ConvNets或CNNs）作为一类神经网络，托起cv的发展，本文主要介绍卷积神经网络的另外一个操作——BN操作，其原理，并以小白视角，完成池化从0到1的numpy实现。

**![]()**

1

作为小白入坑篇系列，开始今天的算子”BN“，错过其他算子的请关注公众号后台领取。

**BN**是BatchNormlization的缩写，及批量归一化。我们知道在训练神经网络的时候，我们会将输入图片进行归一化预处理，再放入网络中训练，这是为啥呢，其实这一步操作被称为“**白化**”，在机器学习中很常用，是一种规范化数据分布的方式，主要有两个目的：一是去除特征之间的相互依赖关系，保证特征间的独立性，另外一个原因是让所有的特征具有相同均值和方差的分布，即保证特征都服从正态分布。其中大家所熟知的PCA降维就是典型的白化，可以参考：PCA白化【5】【6】。

当一张图片输入到神经网络经过各层计算之后，这个分布将不会满足刚才经过Image Normalization操作之后的分布了，可能每一层均需适应新的数据分布规律，同时网络的层与层之间存在着高度的关联性和耦合性，而且激活函数的出现使得很可能一些新的数据会落入激活函数的饱和区，导致神经网络训练的梯度消失 。种种原因让我们在深度学习训练的时候需要尝试不同的学习率、初始化参数（如xavier初始化）等方式让模型尽快收敛。BN的原作者将这一现象称为**Internal Covariate Shift**，在网络训练过程中，因为网络参数变化引起的内部节点的数据分布发生变化的现象。基于机器学习中的白化，这里针对深度学习提出了BN，本质一样的，即通过归一化操作，将数据分布整体上服从正态分布（均值为0，方差为1），那为啥还需要γ和β这两个线性变化参数呢？主要原因是白化操作虽然好，但是会削弱数据的表达能力，好比一下子将一片树林肆意放飞的小鸟都抓到家里的笼子里，小鸟都飞不动了，还是需要将笼子的规格尽可能能保证鸟儿能飞起来，而这个笼子多大和放在哪儿则是需要学习的γ和β。

2

了解了BN出现的原因后，我们来看BN的具体操作：

![]()

主要分成以下几步：

* 对输入数据求平均值
* 基于均值，对输入数据求方差
* 基于均值和方差，对输入数据归一化
* 对归一化后的数据做线性变化，即γ和β

**首先**是输入数据：输入数据由几个方面决定：1. BN层放到网络层的哪里；2. 输入数据的大小；

BN的位置，是BN层在网络层中的位置，BN原论文作者的建议是**Conv-BN-ReLu**，将BN层放到激活函数前，解释是因为非线性单元的输出分布形状会在训练过程中变化，归一化无法消除他的方差偏移，将BN层放到卷积和FC层后，全连接和卷积层的输出一般是一个对称,非稀疏的一个分布，更加类似高斯分布，对他们进行归一化会产生更加稳定的分布。而如果放在像relu这样的激活函数后面，如果你输入的数据是一个高斯分布，经过Relu后小于0的被抑制了，这样的类似高斯分布会被完全破坏，后面再做BN又强行拉到高斯分布，操作就很迷。。

2019年有篇文章专门就BN层在网络层的位置写了一篇论文【1】，该论文以三种架构在深度是逐渐增加的AlexNet、VGG16、ResNet-20网络，数据集逐渐复杂 CIFAR10, CIFAR100 and Tiny ImagNet上做了实验。

![]()

实验结果是，在网络简单如AlexNet情况下，第三个架构比前两个效果好，收敛更快，而在复杂网络如ResNet下的复杂数据集散，第一个架构的收敛更快。

![]()

![]()

![]()

这里大概的结论是，针对复杂场景和复杂网络，第一种架构是不二之选，而针对简单场景和简单网络，可能数据本身不太精确，会更快一点，挺玄学的。。有兴趣的小伙伴可以研究下。

综上，一般情况下，我们会将BN层放到卷积和FC层之后，激活函数之前。

2. 输入数据的大小，主要指数据的batch多大，一般来说batch\_size 太小的话，两个相邻batch之间数据差异大，在训练时的梯度震荡比较严重，不利于收敛；而batch\_size过大时，两个batch之间数据基本无差异，梯度也就没有区别了，整个训练过程会沿一个方向走，不震荡，容易陷入局部拟合中出不来。而实际情况一般是batch\_size在cpu/gpu资源允许的情况下，尽可能大就好了。。

**其次**是各个均值和方差的计算，这里主要说下卷积和FC层后的BN计算:

首先是卷积后的BN，因为卷积操作的feature map 为 形状为N×C×H×W,如下图所示N=3, C=5, H=3, W=3。这里的BN操作，主要计算每一层的均值和方差，即首先将3个蓝色层的feature map拿出来，计算其均值和方差，再去绿色层计算，这样每一层计算完后，会有5层对应的均值和方差；

![]()

同理全连接层的feature map 形状为N×n,这里N=5，也是计算每一层的均值和方差，会有5对均值和方差。

![]()

而实际计算中会不仅仅考虑此次batch的均值和方差，会将前一次的batch的均值和方差以一定权重加入进来即（EMA）：

![]()

以上说的是训练时，在测试时，BN的均值和方差也有几种方式：1，是取整个测试机的均值和方差；2. 是对应数据的均值和方差；3.是将训练集的最后一次均值和方差保存下来，作为测试集的均值方差；一般情况采用第3种，如pytorch中BN的实现。以上的种种操作皆表明，训练集与测试集分布尽可能保持一致，否则均值和方差就会差别很大。

**最后**是对归一化后的数据做线性变化，即γ和β，对于上面的卷积和FC层，则对应着5组γ和β，而这个γ和β我们并不知道要取多少，这就是BN层要训练的参数。

3

BN(BatchNormlization)批量归一化算子的**实现**torch、tensorflow等框架中均已封装好，拿来即用，非常方便，这边是方便自己理解，通过numpy 从0实现BN。思路如下，同样考虑继承Layers类，Layer类的代码参见conv算子：

BN算子继承Layer类，前向和反向实现如下：

```
```
```
```
import numpy as np  
from module import Layers  
  
class BatchNormlization(Layers):  
    """  
    https://blog.csdn.net/weixin_44754861/article/details/108343938?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_utm_term~default-5.pc_relevant_paycolumn_v3&spm=1001.2101.3001.4242.4&utm_relevant_index=7  
  
    """  
    def __init__(self, name, x,eps =1e-7, momentum =0.9, mode = "train"):  
        super(BatchNormlization).__init__(name)  
        self.eps =eps  
        self.input = x  
        n, c, h, w = x.shape  
        self.momentum = momentum  
        self.running_mean = np.zeros(c)  
        self.running_var = np.zeros(c)  
        self.gamma = np.random(c)  
        self.beta =np.random(c)  
        self.mode = mode  
  
    def add_dim(x, dim):  
        return np.expand_dims(x, axis=dim) # batch   
  
    def forward(self):  
        ib, ic, ih, iw = self.input.shape  
  
        self.input = self.input.transpose(1, 0, 2, 3).reshape([ic, -1]) # n,c,h,w ->c, n*h*w  
        if self.mode =="train":  
            self.var = np.sqrt(self.var +self.eps) #   
            self.mean = np.mean(self.input, axis=0) # 每个channel的均值  
            self.mean = self.add_dim(self.mean, 1) # 与后面的self.input 维度一致  
            self.var = np.var(self.input, axis=0) #每个channel的方差  
            self.var = self.add_dim(self.var , 1)  
            self.gamma = self.add_dim(self.gamma, 1)  
            self.beta = self.add_dim(self.beta, 1)  
            self.running_mean = self.momentum * self.running_mean + (1-self.momentum) *self.mean  
            self.running_var = self.momentum * self.running_var + (1-self.momentum) *self.var  
            self.input_ = (self.input -  self.running_mean)/(self.running_var + self.eps)  
            dout = (self.input_*self.gamma +self.beta ).reshape(ic,ib, ih, iw).transpose(1, 0, 2, 3)  
            self.cache = (self.input_, self.gamma, (self.input - self.running_mean, self.running_var + self.eps))  
        elif self.mode =="test":  
            x_hat = (self.input - self.running_mean) / (np.sqrt(self.running_var + self.eps))  
            dout = self.gamma * x_hat + self.beta  
        else:  
            raise ValueError("Invalid forward batch normlization mode")  
        return dout, self.cache  
  
  
    def backward(self, dout):  
        N, D = dout.shape  
        x_, gamma, x_minus_mean, var_plus_eps =self.cache  
  
        # calculate gradients  
        dgamma = np.sum(x_ * dout, axis=0)  
        dbeta = np.sum(dout, axis=0)  
  
        dx_ = np.matmul(np.ones((N,1)), gamma.reshape((1, -1))) * dout  
        dx = N * dx_ - np.sum(dx_, axis=0) - x_ * np.sum(dx_ * x_, axis=0)  
        dx *= (1.0/N) / np.sqrt(var_plus_eps)  
  
        return dx, dgamma, dbeta  
  
    def update(self, lr, dgamma, dbeta):  
        self.gamma -= dgamma *lr  
        self.beta -= dbeta*lr
```
```
```
```

4

在BN之后，各路英雄纷纷祭出大招：Layer Normlization, Instance Normlization，Group Normlization,   CBN, CmBN等，有兴趣小伙伴可以搜索比较。至于BN对于整个深度学习网络的影响，以及影响有多大也有论文研究【2】，以及对应的相关中文解读【3】,欢迎大家一起阅读分享。

**参考**

[1] 《An Empirical Study on Position of the Batch Normalization Layer in Convolutional Neural Networks》

[2] 《 How Does Batch Normalization Help Optimization?》

[3] https://zhuanlan.zhihu.com/p/52132614

[4] https://zhuanlan.zhihu.com/p/92495231

[5] http://ufldl.stanford.edu/tutorial/unsupervised/PCAWhitening/

[6] https://blog.csdn.net/hjimce/article/details/50864602

---

如果有任何困惑和疑问，欢迎进入公众号，添加微信号一起交流。

如果觉得写的内容对您有一点点启发和帮助，顺手再看![]()

如果有用 点个在看

![]()
