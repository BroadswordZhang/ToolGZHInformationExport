---
标题: "【小白入坑篇】卷积及numpy实现"
公众号名称: "张大刀修炼手册"
作者: "张大刀修炼手册"
发布时间: "2022-03-16 20:30:00"
原文链接: "https://mp.weixin.qq.com/s/n41NGFxTFhw271ubBA_cMg"
文章详情_分享类型: "0"
文章ID: "2247484246"
是否已删除: "False"
版权状态: "11"
版权类型: "1"
阅读量: "451"
喜欢数: "8"
转载量: "2"
文章详情_投票ID: "[]"
文章详情_超级投票ID: "[]"
文章详情_封面图片: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibEKoxqfxM9fU6XlqqCfG1yftibBbNu25PtbGNLY2CibB6HRicgXv4lRRkyQciaVVRMxYEW6pWcjO8T4cg/0?wx_fmt=jpeg"
文章详情_智能产品信息: "0"
文章详情_修改状态: "1"
文章详情_互动类型: "2"
文章详情_可删除状态: "0"
点赞数: "18"
图文序号: "1"
文章详情_是否付费订阅: "0"
文章详情_是否来自转移: "0"
文章详情_公开标签信息: "{\"public_tag_list\": [], \"modify_times\": 0, \"init_tag_list_size\": 0}"
文章详情_文章合集信息: "{\"appmsg_album_infos\": []}"
文章详情_是否开启粉丝留言: "0"
文章详情_是否处于冷却状态: "0"
文章详情_2.35比1封面地址: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibEKoxqfxM9fU6XlqqCfG1yfDraMkUf2n6T2H8w9icg9KwpAMWXbu7rOgCibr15nUiaBIVh0BG20Hgckw/0?wx_fmt=jpeg"
文章详情_16比9封面地址: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibEKoxqfxM9fU6XlqqCfG1yfDraMkUf2n6T2H8w9icg9KwpAMWXbu7rOgCibr15nUiaBIVh0BG20Hgckw/0?wx_fmt=jpeg"
文章详情_是否禁止推荐: "0"
文章详情_发布线路信息: "{\"use_line\": 1, \"line_count\": 0, \"send_time\": 1647433800, \"is_appmsg_flag\": 1, \"is_use_flag\": 0}"
文章详情_来源声明类型: "0"
分享量: "5"
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
发布消息ID: "1000000013"
发布类型: "101"
发送状态: "{\"total\": 15, \"succ\": 15, \"fail\": 0, \"progress\": 100, \"userprotect\": 0}"
发布结果: "{\"msg_status\": 2, \"refuse_reason\": \"\", \"reject_index_list\": [], \"update_time\": 1752674458}"
是否新发布: "0"
文章详情_发布复制类型: "77"
文章详情_发布复制文章ID: "100000186"
文章分析_统计错误: "analysis page parsing failed"
---

# 【小白入坑篇】卷积及numpy实现

![]()

![]()

点击上方蓝字一起入坑

![]()

![]()

卷积神经网络（ConvNets或CNNs）作为一类神经网络，托起cv的发展，本文主要介绍卷积神经网络的灵魂——卷积操作，其原理，并以小白视角，完成卷积从0到1的numpy实现。

**![]()**

1

卷积神经网络（ConvNets或CNNs）作为人工智能的入门神经网络，已被广泛用于图像识别和分类等领域。除了为机器人和自动驾驶汽车提供视觉之外，ConvNets 在识别人脸、物体和交通标志方面也应用广泛。其中卷积操作作为cnn的灵魂，其出现加快了人工智能的发展。

**卷积**一词一开始出现在数学中，为了表示一个函数对另外一个函数所有微量的响应的总叠加效应；其本质上是一种过滤器，在一维信号上完成对信号的过滤，在二维图像上完成为图像的一种过滤，过滤掉其不重要部分，提取主要特征，这里主要详解图像的卷积操作，图像卷积并不是出最近才出现，而在传统图像处理中就有sobel过滤器做边缘检测时就用到了卷积。

2

了解卷积首先要了解其操作对象：图像，图像本质上为像素的矩阵：

![]()

如上图所示，上图所示的灰度图，为单通道，而一般图像会有RGB三通道，每个通道中，每个像素点的值在0~255之间，0为黑色，255为白色。卷积（conv）为卷积算子，为了方便理解，我们下图5\*5矩阵作为图像像素：

![]()

考虑另一个 3 X 3矩阵为卷积矩阵：

![]()

然后可以计算5x5图像和3x3矩阵的乘积：

![]()

将卷积矩阵在图像上依次从左到右从上到下滑动1个像素（也称stride），对于每个位置，对卷积矩阵和对应图像的像素点相乘后相加，得到最终的整数，作为输出矩阵中的单个元素，上图为单通道图像，对于一般的三通道图像，kernel的in\_channel也需要保证为3通道。计算过程如下图，在计算完每层的feature后，每层的feature对应位置相加后得到最终输出feature层。

![]()

在CNN中，3×3矩阵称为”**滤波器**“、”**内核**“或”**特征检测器**“，输出的矩阵称为”**卷积特征**“、”**feature map**“，从上述动图中看出，不停的kernel会对同一种输入图像产生不同的特征图，如下图，先输入一张原始图片：

![]()

选择不同的滤波器矩阵对图像做卷积操作，实现边缘检测、锐化和模糊等操作--检测图像的不同特征，如边缘、曲线等：

![]()

实际卷积操作特征形成如下图：

![]()

红色和绿色框为两个卷积kernel，在输入图像上滑动、卷积分别生成两张特征图，如图所示。而因为卷积kernel的size确定了他只能获得图像局部的依赖关系（当然你可以将kernel的size设成图像大小。。），在实际CNN中，需要通过训练来学习这些kernel的值以确定他们需要从图像中提取哪些特征。

3

conv卷积算子的**实现**torch、tensorflow等框架中均已封装好，拿来即用，非常方便，这边是方便自己理解，通过numpy 从0实现conv。思路如下，因为考虑conv算子不仅需要前向计算，还需要反向更新，所以先建个Layers类：

```
 1import numpy as np  
 3import os  
 4  
 5class Layers():  
 6    def __init__(self, name):  
 7        self.name = name   
 8  
 9    def forward(self, x):  
10        pass  
11  
12    def zero_grad(self):  
13        pass   
14  
15    def backward(self, grad_out):  
16        pass  
17  
18    def update(self, lr):  
19        pass  
20
```

conv卷积算子集成Layer类，前向和反向实现如下：

```
  2import numpy as np  
  3from module import Layers  
  4  
  5class Con2d(Layers):  
  6    """  
  7    卷积前向：  
  8    输入：input:[b, cin, h, w]  
  9         weight：[cin, cout, ksize, ksize], stride, padding   
 10    计算过程：  
 11        1.  将权重拉平成：[cout, cin*ksize*ksize] self.weight 先transpose(1, 0, 2,3) 再reshpe(cout, -1)  
 12        2.  将输入整理成：[b*hout*wout,cin*ksize*ksize]:   
 13            先根据hin和win 通过pad, ksize和stride计算出hout和wout (h+2*pad-ksize)//stride + 1 (b, cout, hout, wout)  
 14            再根据img展平，整理成自己的：img  (b, hout, wout, cin*kszie*ksize)  -> (b*hout*wout, cin*kszie*ksize)  
 15        3. 两者相乘后，np.dot 再去reshape (cout, b*hout*wout) -> (b, cout, hout*wout)  
 16    """  
 17    """  
 18    卷积反向：  
 19    输入：input:[b, cout, hout, wout] -loss   
 20    计算过程：   
 21        1. 将输入换成输出格式： [b, cout, hout, wout] -> [cout, b, hout, wout] ->[cout, b*hout*wout]   
 22        2. 计算的输入与之前的图相乘： (cout, b*hout*wout) * (b*hout*wout, cin*kszie*ksize) -> (cout, cin*kszie*ksize) 得到更新后的权重  
 23        3. 将更新后的权重与图相乘，  
 24  
 25    """  
 26    def __init__(self,name, in_channel, out_channel, kernel_size, padding, stride=1 ):  
 27        super(Con2d,self).__init__(name)  
 28        self.in_channel = in_channel  
 29        self.out_channel = out_channel  
 30        self.ksize = kernel_size  
 31        self.padding = padding  
 32        self.stride = stride  
 33  
 34        self.weights = np.random.standard_normal((out_channel, in_channel, kernel_size, kernel_size))  
 35        self.bias = np.zeros(out_channel)  
 36        self.grad_w = np.zeros(self.weights.shape)  
 37        self.grad_b = np.zeros(self.bias.shape)  
 38  
 39    def img2col(self, x, ksize, strid):  
 40        b,c,h,w = x.shape # (5, 3, 34, 34)  
 41        img_col = []  
 42        for n in range(b): # 5  
 43                for i in range(0, h-ksize+1, strid):  
 44                    for j in range(0, w-ksize+1, strid):  
 45                        col = x[n,:, i:i+ksize, j:j+ksize].reshape(-1) # (1, 3, 4, 4) # 48  
 46                        img_col.append(col)  
 47        return np.array(img_col) # (5, 3, 31, 31, 48)  
 48  
 49    def forward(self, x):  
 50        self.x = x #(5, 3, 34,34)  
 51        weights = self.weights.reshape(self.out_channel, -1) # (12, 3*4*4)  
 52        x = np.pad (x, ((0,0), (0,0), (self.padding, self.padding), (self.padding, self.padding)), "constant") # (5, 3, 34, 34)  
 53        b, c, h, w = x.shape  
 54        self.out = np.zeros((b, self.out_channel, (h-self.ksize)//self.stride+1, (w-self.ksize)//self.stride+1))# (5, 12, 31, 31)  
 55        self.img_col = self.img2col(x, self.ksize, self.stride) #  (5, 31, 31, 48) #(4805, 48)  
 56        out = np.dot(weights, self.img_col.T).reshape(self.out_channel, b, -1).transpose(1, 0,2) # (12 ,48) *(48, 4805) = (12, 4805) =(12, 5, 961) =(5, 12, 961)  
 57        self.out = np.reshape(out, self.out.shape)   
 58        return self.out  
 59  
 60    def backward(self, grad_out):  
 61        b, c, h, w = self.out.shape  
 62        grad_out_ = grad_out.transpose(1, 0, 2, 3 )  
 63        grad_out_flag = np.reshape(grad_out_,[self.out_channel, -1]) # [cout, b*h*w]  
 64        self.grad_w = np.dot(grad_out_flag, self.img_col).reshape(c, self.in_channel, self.ksize, self.ksize) #  (cout, cin*kszie*ksize)  -权重值  
 65        self.grad_b = np.sum(grad_out_flag, axis=1) # [cout] -偏置值  
 66        tmp = self.ksize -self.padding -1  
 67        grad_out_pad = np.pad(grad_out, ((0,0),(0,0),(tmp, tmp),(tmp,tmp)),'constant')  
 68        weights = self.weights.transpose(1, 0, 2, 3).reshape([self.in_channel, -1]) # [cin. cout*ksize*ksize]  
 69        col_grad = self.img2col(grad_out_pad, self.ksize, 1) #   
 70        next_eta = np.dot(weights, col_grad.T).reshape(self.in_channel, b, -1).transpose(1, 0, 2)  
 71        next_eta = np.reshape(next_eta, self.x.shape)  
 72        return next_eta  
 73  
 74    def zero_grad(self):  
 75        self.grad_w = np.zeros_like(self.grad_w)    
 76        self.grad_b = np.zeros_like(self.grad_b)  
 77  
 78    def update(self, lr=1e-3):  
 79        self.weights -= lr*self.grad_w  
 80        self.bias -= lr*self.grad_b   
 81  
 82    # def __sing_conv(self,x):  
 83    #     x = np.pad(x, ((0,0),(0,0),(self.padding, self.padding),(self.padding, self.padding)), 'constant', constant_val = 0 )# 对输入做padding  
 84    #     # make sure the output shape   
 85    #     b, c, h, w = x.shape  
 86    #     oh = (h - self.ksize)/self.stride + 1   
 87    #     ow = (w - self.ksize)/self.stride + 1   
 88    #     out = np.zeros((b, self.out_channel,oh, ow))  
 89    #     for num in range(b):  
 90    #         for o in range(self.out_channel):  
 91    #             for i in range(0, oh, self.stride):  
 92    #                 for j in range(0, ow, self.stride):  
 93    #                     x = i * self.stride  
 94    #                     y = j * self.stride  
 95    #                     out[num, o, i, j] = np.sum(x[num,:, x:x+self.ksize, y:y+self.ksize] * self.weights + self.bias[o])  
 96    #     return out   
 97if __name__ == '__main__':  
 98    x = np.ones([2,3,32,32])  
 99    conv = Con2d('conv1',3,12,3,1,1)  
100    for i in range(100):  
101       y = conv.forward(x)  
102       loss =abs( y - 1)  
103       x = conv.backward(loss)  
104       lr = 1e-4   
105       conv.update(lr)  
106       print(np.sum(loss))
```

从卷积的实现发现，卷积操作中一大时间花费在将图像转成矩阵img2col函数上，这也是后面在模型轻量化过程中，mobilenet深度可分离卷积 + 1x1卷积中，1x1卷积无需img2col，易于在芯片端部署，加快卷积速度。

如果觉得我写的内容对您有一点点启发和帮助，顺手再看![]()

如果有用 点个在看

![]()
