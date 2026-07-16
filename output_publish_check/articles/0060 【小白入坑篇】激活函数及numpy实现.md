---
标题: "【小白入坑篇】激活函数及numpy实现"
公众号名称: "张大刀修炼手册"
作者: "张大刀修炼手册"
发布时间: "2022-03-20 19:36:29"
原文链接: "https://mp.weixin.qq.com/s/gH3gp513RhGfI4GcOTKyUg"
文章详情_分享类型: "0"
文章ID: "2247485360"
是否已删除: "False"
版权状态: "11"
版权类型: "1"
阅读量: "681"
喜欢数: "13"
转载量: "0"
文章详情_投票ID: "[]"
文章详情_超级投票ID: "[]"
文章详情_封面图片: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibEeXFAgQWRyfuh4PuMtxDNn8YSA8ibFehXhgDqdgGQTvibqeN5KkSYK0ibYtYJQrV4U30fTTJic90R6Hg/0?wx_fmt=jpeg"
文章详情_智能产品信息: "0"
文章详情_修改状态: "1"
文章详情_互动类型: "2"
文章详情_可删除状态: "0"
点赞数: "31"
图文序号: "1"
文章详情_是否付费订阅: "0"
文章详情_是否来自转移: "0"
文章详情_公开标签信息: "{\"public_tag_list\": [], \"modify_times\": 0, \"init_tag_list_size\": 0}"
文章详情_文章合集信息: "{\"appmsg_album_infos\": []}"
文章详情_是否开启粉丝留言: "0"
文章详情_是否处于冷却状态: "0"
文章详情_2.35比1封面地址: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibEeXFAgQWRyfuh4PuMtxDNn0qhibBA3dxtVRZt48acXIuYibkRHFwerNDOlhrpnleSJQuer0licDL9Ww/0?wx_fmt=jpeg"
文章详情_16比9封面地址: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibEeXFAgQWRyfuh4PuMtxDNn0qhibBA3dxtVRZt48acXIuYibkRHFwerNDOlhrpnleSJQuer0licDL9Ww/0?wx_fmt=jpeg"
文章详情_是否禁止推荐: "0"
文章详情_发布线路信息: "{\"use_line\": 1, \"line_count\": 0, \"send_time\": 1647776189, \"is_appmsg_flag\": 1, \"is_use_flag\": 0}"
文章详情_来源声明类型: "0"
分享量: "2"
文章详情_是否辟谣文章: "0"
文章详情_是否多图封面: "0"
文章详情_分享图片信息: "[]"
朋友圈点赞数: "0"
文章详情_图文展示类型: "0"
文章详情_广告信息: "{\"has_agreement_ad\": 0, \"is_recruit_agreement_ad\": 0}"
文章详情_文章音频信息: "[]"
文章详情_修改提示: "还可以修改3次"
文章详情_可修改状态: "1"
文章详情_修改详情说明: "[]"
文章详情_是否修改: "0"
文章详情_位置页展示: "0"
文章详情_可显示位置页: "0"
发布消息ID: "1000000024"
发布类型: "101"
发送状态: "{\"total\": 46, \"succ\": 46, \"fail\": 0, \"progress\": 100, \"userprotect\": 0}"
发布结果: "{\"msg_status\": 2, \"refuse_reason\": \"\", \"reject_index_list\": [], \"update_time\": 1752674457}"
是否新发布: "0"
文章详情_发布复制类型: "77"
文章详情_发布复制文章ID: "100001284"
文章分析_统计错误: "analysis page parsing failed"
---

# 【小白入坑篇】激活函数及numpy实现

![]()

![]()

点击上方蓝字一起入坑

![]()

![]()

卷积神经网络（ConvNets或CNNs）作为一类神经网络，托起深度学习的发展，本文主要介绍卷积神经网络的另外一个操作——激活操作，其背景、原理，并以小白视角，完成激活函数从0到1的numpy实现。

**![]()**

1

作为小白入坑篇系列，开始深度学习的另外一个操作”激活“，错过其他操作的请关注公众号后台领取。

**激活函数（Activation Function）**的激活来源于生物学人脑中的神经元信息传递过程中的神经元的激活，神经元的激活可以有两种模型结构——跳变式和连续式。跳变式激活方式是：引入一个阈值，当输入信息经过某种处理后大于阈值即表示激活，小于阈值表示未激活（这和我们的step激活函数是不是很类似）；连续式激活方式表示神经元不是只有激活和未激活两种状态，而是有不同的激活水平，输入信息经过某种处理后直接输出激活水平。

![]()

而在深度学习中为何要引入激活函数呢，主要是引入网络的**非线性**表达，深度学习中的卷积、BN以及FC层均是对数据的线性变换（αX +β型），但是一般的数据分布都是非线性的，如下图，无法通过一条线性直线将数据红绿数据分开，那怎么办，有两种方法：1，如下左图，像机器学习中的SVM一样引入核函数，将二维平面引入三维上，通过线性的超平面完成线性可分；2. 像右图一样，将划分的线掰弯，完成非线性可分。因为深度学习中一般场景复杂，采用右边的方式，所以引入非线性的激活函数，强化网络的学习能力，解决线性模型无法解决的问题。

![]()![]()

2

了解了激活函数出现的背景后，我们来看目前常用的一些激活函数，是时候祭出这张魔性的图了：

![]()

当然现在激活函数界已经不止这么多了，主要分成几类饱和类激活函数、非饱和类激活函数以及softmax这类的：

1、饱和类激活函数：Sigmoid、Tanh等；

2、非饱和类激活函数：Relu、ELU【指数线性单元】、PReLU【参数化的ReLU 】、RReLU【随机ReLU】等；

3、输入不只单个x的激活函数：SoftMax、Maxout等。

**饱和类激活函数：**

**1. sigmoid**

sigmoid函数也叫逻辑函数，用于隐藏层的输出，输出在(0,1)之间，它可以将一个实数映射到(0,1)的范围内，一般用于二分类网络。常用于在特征相差比较复杂或是相差不是特别大的时候效果比较好。该函数将大的负数转换成趋于0，将大的正数转换为趋于1。公式如下：

![]()

其函数以及导数可视化如下：

![]()  ![]()

从公式可以看出Sigmoid将一个 (−∞ ,+∞ ) 之内的实数值变换到区间 [0,1]，同时因为Sigmoid单调递增，对结果不会产生影响，至于为何要用sigmoid这个函数，sigmoid函数来源于伯努利分布中的inverse link function，具体参见【4】，同时sigmoid函数梯度平滑，函数可微，符合深度学习中的反向传播，但sigmoid也有很多不足：

1、梯度消失：Sigmoid 函数在趋近 0 和 1 的时候梯度趋近于 0。反向传播时，输出接近 0 或 1 的神经元其梯度趋近于 0。这些神经元叫做饱和神经元。因此，这些神经元的权重不会更新。而与此类神经元相连的神经元的权重也更新得很慢。该问题叫做梯度消失。因此，想象一下，如果一个大型神经网络包含 Sigmoid 神经元，而其中很多个都处于饱和状态，那么该网络反向传播则无意义。

2、不以零为中心：Sigmoid 输出不以零为中心，会降低权重更新的效率。

3、计算成本高昂：exp() 函数与其他非线性激活函数相比，在芯片上计算成本高昂。

为了解决sigmoid中不以0为中心的问题，引入tanh激活函数。

**2. Tanh**

Tanh 激活函数又叫作双曲正切激活函数（hyperbolic tangent activation function）。

![]()

其函数以及导数可视化如下：

![]()

与 Sigmoid 函数类似，Tanh 函数也使用真值，但 Tanh 函数将其压缩至-1 到 1 的区间内。与 Sigmoid 不同，Tanh 函数的输出以零为中心，因为区间在-1 到 1 之间。你可以将 Tanh 函数想象成两个 Sigmoid 函数放在一起。在实践中，Tanh 函数的使用优先性高于 Sigmoid 函数。负数输入被当作负值，零输入值的映射接近零，正数输入被当作正值。它解决了Sigmoid函数的不是zero-centered输出问题。但是梯度消失（gradient vanishing）的问题和幂运算的问题仍然存在。

为了解决梯度消失问题，我们来讨论另一类非线性激活函数——**修正线性单元**（rectified linear unit，ReLU），该函数明显优于前面两个函数，是现在使用最广泛的函数。

**1. Relu**

Relu激活函数的解析式：

‍‍‍‍‍‍‍‍‍‍![]()

Relu函数及其导数的图像如下图所示：

![]()

Relu激活函数优点：

当输入 x<0 时，输出为 0，当 x> 0 时，输出为 x。该激活函数使网络更快速地收敛。它不会饱和，即它可以对抗梯度消失问题，至少在正区域（x> 0 时）可以这样，因此神经元至少在一半区域中不会把所有零进行反向传播。由于使用了简单的阈值化（thresholding），ReLU 计算效率很高。

Relu激活函数缺点是不以零为中心：和 Sigmoid 激活函数类似，ReLU 函数的输出不以零为中心。前向传导（forward pass）过程中，如果 x < 0，则神经元保持非激活状态，反向传导（backward pass）中梯度为0，这样权重无法得到更新，网络无法学习。当 x = 0 时，该点的梯度未定义，但是这个问题在实现中通过采用左侧或右侧的梯度的方式得到解决。

尽管存在这两个问题，ReLU目前仍是最常用的activation function，在搭建人工神经网络的时候推荐优先尝试！

为了解决 ReLU 激活函数中的梯度消失问题，当 x < 0 时，我们使用 Leaky ReLU——该函数试图修复 dead ReLU 问题。下面我们就来详细了解 Leaky ReLU。

**2. LeakyRelu**

![]()

Leaky Relu函数及其导数的图像如下图所示：一般α取0.01。

![]()

人们为了解决Dead ReLU Problem，提出了将ReLU的前半段设为α x而非0，通常α = 0.01。理论上来讲，Leaky ReLU有ReLU的所有优点，外加不会有Dead ReLU问题，但是在实际操作当中，并没有完全证明Leaky ReLU总是好于ReLU。

Leaky ReLU 可以得到更多扩展。不让 x 乘常数项，而是让 x 乘超参数，这看起来比 Leaky ReLU 效果要好。该扩展就是 Parametric ReLU。

**3. P-Relu**

![]()

![]()

其中 α是超参数。这里引入了一个随机的超参数 α，它可以被学习，因为你可以对它进行反向传播。这使神经元能够选择负区域最好的梯度，有了这种能力，它们可以变成 ReLU 或 Leaky ReLU。

**4. ELU**

函数表达式：

![]()

函数及其导数的图像如下图所示：

![]()

ELU也是为解决ReLU存在的问题而提出，显然，ELU有ReLU的基本所有优点，以及：不会有Dead ReLU问题
输出的均值接近0，zero-centered

它的一个小问题在于计算量稍大。类似于Leaky ReLU，理论上虽然好于ReLU，但在实际使用中目前并没有好的证据ELU总是优于ReLU。

## **5. Gelu激活函数**

Gelu激活函数的解析式：

![]()

Gelu激活函数及其导数的图像如下图所示：

![]()

bert中使用的激活函数，作者经过实验证明比relu等要好。原点可导，不会有Dead ReLU问题。值得注意的是最近席卷NLP领域的BERT等预训练模型几乎都是用的这个激活函数。

## **6. Swich激活函数**

该函数又叫作自门控激活函数，它由谷歌的研究者发布，数学公式为：

![]()

Swich激活函数及其导数的图像如下图所示：

![]()

根据上图，从图像上来看，Swish函数跟ReLu差不多，唯一区别较大的是接近于0的负半轴区域，因此，Swish 激活函数的输出可能下降，即使在输入值增大的情况下。大多数激活函数是单调的，即输入值增大的情况下，输出值不可能下降。而 Swish 函数为 0 时具备单侧有界（one-sided boundedness）的特性，它是平滑、非单调的。但是在浅层网络上，性能与relu差别不大。

**7. Selu激活函数**

Selu激活函数的解析式

![]()

其实就是ELU乘了个lambda，关键在于这个lambda是大于1的。以前relu，prelu，elu这些激活函数，都是在负半轴坡度平缓，这样在activation的方差过大的时候可以让它减小，防止了梯度爆炸，但是正半轴坡度简单的设成了1。而selu的正半轴大于1，在方差过小的的时候可以让它增大，同时防止了梯度消失。这样激活函数就有一个不动点，网络深了以后每一层的输出都是均值为0方差为1。

当其中参数取为γ=1.0507，α=1.6733时，在网络权重服从标准正态分布的条件下，各层输出的分布会向标准正态分布靠拢。这种「自我标准化」的特性可以避免梯度消失和爆炸的问题，让结构简单的前馈神经网络获得甚至超越 state-of-the-art 的性能。

selu的证明部分前提是权重服从正态分布，但是这个假设在实际中并不能一定成立，众多实验发现效果并不比relu好。同时selu在芯片上的计算也远大于Relu计算。

目前还有另外一类函数他们的输入不止一个x，如softmax 、maxout这里有争议点是他们能否被称为激活函数，因为如softmax本质是归一化，将所有数据归一化成概率，并没有激活或抑制，但是从激活的目的看，激活主要增加非线性，而softmax函数存在指数操作，当然有非线性操作，所以也可以称为激活函数。这里暂且将其作为激活函数介绍。

**1. softmax 函数**

![]()

可以看到，Softmax函数把输出映射成区间在(0,1)的值，并且做了归一化，所有元素的和累加起来等于1。可以直接当作概率对待，可以用于多分类中，同时softmax也是连续可导，可以用于反向传播。那为啥softmax函数这样设计呢，这个与其后面的损失函数以及对应的反向传导有关，里面的深意参考【7】，这里暂且不提。

**2. MaxOut函数**

Maxout可以看做是在深度学习网络中加入一层激活函数层,包含一个参数k.这一层相比ReLU,sigmoid等,其特殊之处在于增加了k个神经元,然后输出激活值最大的值.

![]()

其中：

![]()

与常规激活函数不同的是,它是一个可学习的分段线性函数.然而任何一个凸函数，都可以由线性分段函数进行逼近近似。其实我们可以把以前所学到的激活函数：ReLU、abs激活函数，看成是分成两段的线性函数，如下示意图所示：实验结果表明Maxout与Dropout组合使用可以发挥比较好的效果。

![]()

Maxout的拟合能力是非常强的，它可以拟合任意的的凸函数。作者从数学的角度上也证明了这个结论，即只需2个 maxout 节点就可以拟合任意的凸函数了（相减），前提是”隐隐含层”节点的个数可以任意多.

这样 Maxout 神经元就拥有 ReLU 单元的所有优点（线性和不饱和），而没有它的缺点（死亡的ReLU单元）。然而和 ReLU 对比，它每个神经元的参数数量增加了一倍，这就导致整体参数的数量激增。

**更多的激活函数请参见下图：**

![]()

![]()

总之，激活函数放在深度学习中扮演着很重要的角色，至于放在在网络层的哪里 ，这里可以参考上一篇[BN算子](http://mp.weixin.qq.com/s?__biz=MzU3ODk2Njc5Mg==&mid=2247484582&idx=1&sn=215cd31c8ae0c6c3eecfa2a4010915e9&chksm=fd6c00c1ca1b89d777dfcaafbc478ff429c763e01e8e82cf0fb29c54c41468d38c42b4bf7ce8&scene=21#wechat_redirect)中的实验，一般放在卷积计算单元后。

3

激活函数的**实现**torch、tensorflow等框架中均已封装，这里方便自己理解，利用numpy从0实现，同时激活函数有的超参数，这里继承Layers类，Layers类参见上一篇[卷积算子](http://mp.weixin.qq.com/s?__biz=MzU3ODk2Njc5Mg==&mid=2247484246&idx=1&sn=fb98a9b101951af9c8d150a60f4fef45&chksm=fd6c0731ca1b8e270b12ed2170870a8d3285a77a0658569018f245ddb80332755c980be4eea2&scene=21#wechat_redirect)的实现，关注公众号后台领取：

```
import numpy as np  
from module import Layers class ReluActivator(Layers):  
    def __init__(self)  
        super(ReluActivator).__init__(name)  
  
    def forward(self, weighted_input):  
        return max(0, weighted_input)  
  
    def backward(self, output):  
        return 1 if output > 0 else 0  
  
class LeakyReluActivator(Layers):  
    def __init__(self, alpha)  
        super(LeakyReluActivator).__init__(name)  
        self.alpha = alpha  
  
    def forward(self, weighted_input):  
        return max(self.alpha*weighted_input, weighted_input)  
  
    def backward(self, output):  
        return 1 if output > 0 else self.alpha  
  
class PReluActivator(Layers):  
    def __init__(self)  
        super(LeakyReluActivator).__init__(name)  
        self.alpha = 1  
  
    def forward(self, weighted_input):  
        return max(self.alpha*weighted_input, weighted_input)  
  
    def backward(self, output):  
        return 1 if output > 0 else self.alpha  
  
    def update(self. lr)  
        self.alpha -=self.alpha*lr  
  
class IdentityActivator(Layers):  
    def __init__(self)  
        super(IdentityActivator).__init__(name)  
  
    def forward(self, weighted_input):  
        return weighted_input  
  
    def backward(self, output):  
        return 1  
  
  
class SigmoidActivator(Layers):  
    def __init__(self)  
        super(SigmoidActivator).__init__(name)  
  
    def forward(self, weighted_input):  
        return 1.0 / (1.0 + np.exp(-weighted_input))  
  
    def backward(self, output):  
        return output * (1 - output)  
  
  
class TanhActivator(Layers):  
    def __init__(self)  
        super(TanhActivator).__init__(name)  
  
    def forward(self, weighted_input):  
        return 2.0 / (1.0 + np.exp(-2 * weighted_input)) - 1.0  
  
    def backward(self, output):  
        return 1 - output * output
```

4

综上针对饱和与非饱和激活函数，Sigmoid和tanh的特点是将输出限制在(0,1)和(-1,1)之间，说明Sigmoid和tanh适合做概率值的处理，例如LSTM中的各种门；而ReLU就不行，因为ReLU无最大值限制。同样，根据ReLU的特征，Relu适合用于深层网络的训练，而Sigmoid和tanh则不行，因为它们会出现梯度消失。但是 Relu就不会出现梯度消失吗？其实我们仔细分析发现梯度衰减因子不仅包括激活函数导数还有多个权重连乘，梯度消失只是表面说法，按照这样理解，底层使用非常大的学习率，或者人工添加梯度噪音，原则上也能回避，有不少论文这样试了，然而目前来看，有用，但没太大的用处。残差网络论文也提到，深层原因训练不好的本质难题可能不是衰减或者消失，具体是啥。这个欢迎有兴趣的小伙伴讨论。

**参考**

[1] https://en.wikipedia.org/wiki/Activation\_function

[2] https://zhuanlan.zhihu.com/p/192497127?utm\_source=wechat\_timeline

[3] https://zhuanlan.zhihu.com/p/192497127?utm\_source=wechat\_timeline

[4] https://en.m.wikipedia.org/wiki/Generalized\_linear\_model

[5] https://www.zhihu.com/question/22334626

[6] https://zhuanlan.zhihu.com/p/176988745

[7] https://www.zhihu.com/question/23765351

---

如果有任何困惑和疑问，欢迎进入公众号，添加微信号一起交流。

如果觉得写的内容对您有一点点启发和帮助，顺手再看![]()

如果有用 点个在看

![]()
