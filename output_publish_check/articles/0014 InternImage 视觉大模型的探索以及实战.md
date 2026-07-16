---
标题: "InternImage| 视觉大模型的探索以及实战"
公众号名称: "张大刀修炼手册"
作者: "张大刀修炼手册"
发布时间: "2023-03-24 21:22:00"
原文链接: "https://mp.weixin.qq.com/s/uqQ-zVejaLtOG-iZFteW1A"
文章详情_分享类型: "0"
文章ID: "2247501210"
是否已删除: "False"
版权状态: "11"
版权类型: "1"
阅读量: "493"
喜欢数: "2"
转载量: "3"
文章详情_投票ID: "[]"
文章详情_超级投票ID: "[]"
文章详情_封面图片: "https://mmbiz.qpic.cn/mmbiz_jpg/xH40kQxnnibG4tpWJeib0Nwu4JNbMIkibPuCKoKCcpKnxoC6MUfpC3sf9haDRgXI76l2526SI42PuNmkW4qnIyxwg/0?wx_fmt=jpeg"
文章详情_智能产品信息: "0"
文章详情_修改状态: "1"
文章详情_互动类型: "2"
文章详情_可删除状态: "0"
点赞数: "9"
图文序号: "1"
文章详情_是否付费订阅: "0"
文章详情_是否来自转移: "0"
文章详情_公开标签信息: "{\"public_tag_list\": [], \"modify_times\": 0, \"init_tag_list_size\": 0}"
文章详情_文章合集信息: "{\"appmsg_album_infos\": []}"
文章详情_是否开启粉丝留言: "1"
文章详情_是否处于冷却状态: "0"
文章详情_2.35比1封面地址: "https://mmbiz.qpic.cn/mmbiz_jpg/xH40kQxnnibG4tpWJeib0Nwu4JNbMIkibPuERDlTNrICdeXQKy41RrnBpOQoRCliazYsmRx8EfoGFeibicRt9b5tl3Fw/0?wx_fmt=jpeg"
文章详情_16比9封面地址: "https://mmbiz.qpic.cn/mmbiz_jpg/xH40kQxnnibG4tpWJeib0Nwu4JNbMIkibPuERDlTNrICdeXQKy41RrnBpOQoRCliazYsmRx8EfoGFeibicRt9b5tl3Fw/0?wx_fmt=jpeg"
文章详情_是否禁止推荐: "0"
文章详情_发布线路信息: "{\"use_line\": 1, \"line_count\": 1, \"send_time\": 1679664132, \"is_appmsg_flag\": 1, \"is_use_flag\": 0}"
文章详情_来源声明类型: "0"
分享量: "9"
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
发布消息ID: "1000000072"
发布类型: "101"
发送状态: "{\"total\": 3314, \"succ\": 3314, \"fail\": 0, \"progress\": 100, \"userprotect\": 0}"
发布结果: "{\"msg_status\": 2, \"refuse_reason\": \"\", \"reject_index_list\": [], \"update_time\": 1752674445}"
是否新发布: "0"
文章详情_发布复制类型: "77"
文章详情_发布复制文章ID: "100017054"
文章分析_统计错误: "analysis page parsing failed"
---

# InternImage| 视觉大模型的探索以及实战

![]()

点击下方公众号关注，一起进步，持续传达瓜货

![]()

InternImage做为backbone的基础大模型，将可变形卷积与transformer的框架相结合，在分类、检测以及分割等图像任务上均有提点。个人觉得最主要的是他相对于transformer对算力、数据量等的要求，有着conv的朴素感，亲测在分类和检测任务上均有不同程度上的提点。

> **前言**

大家好，我是张大刀。

我回来了，前段时间因为工作、生活各类事情，一直鸽，鸽会上瘾，前几天有个小伙伴跟我说，大刀，你已经写公众号一年了呢。说的有些惭愧，因为已经鸽了有一个季度了。从这周开始，开始维持每两周一次的更新，欢迎打脸![]()。

下面进入正文，去年在paperwithcode上看到coco刷新榜：

![]()

相对于其他的检测框架上了transformer, Internimage 采用的是相对传统的卷积网络，不过这里的卷积是可变形卷积，关于可变形卷积以及dcnv1v2 不了解的，可以看[这里](http://mp.weixin.qq.com/s?__biz=MzU3ODk2Njc5Mg==&mid=2247490816&idx=1&sn=6017318496afc0cb71fdab28bcb16874&chksm=fd6c1967ca1b9071069816bbdd79b4b475ef68050d60e9e99377d5484d5dd64084eca0346989&scene=21#wechat_redirect)。整体上看Internimage虽然站上65map的高位，但是他的模型规模达到了2.18B，这里我们主要学习internimage的思路，是基于VIT网络架构，想要一个模块能保留MSHA(多头注意力机制)的全局信息同时能降低其计算量，基于此提出了两个创新点：1） 提出DCNV3; 2) 提出work的模型框架Internimage Model。 

1

DCNV3

**01 DCNv3背景**

首先提出我们的DCNV3：

![]()

从上图中可以看出MHSA多头注意力机制，获取的是全局信息，但是需要对全局信息扫描，参数量大，对多头注意力和VIT不太了解的可以看[这里](http://mp.weixin.qq.com/s?__biz=MzU3ODk2Njc5Mg==&mid=2247492959&idx=1&sn=13a39fb0dbf826fe02b563c2ec71eafb&chksm=fd6fe138ca18682e13c3361f6d530e3d27ea4aeea73615940185188d7bc06905aee17020ae24&scene=21#wechat_redirect)。

而普通的卷积则只能获得局部信息而且卷积因为其强归纳偏置，如旋转平移不变性，会限制其学习更具鲁棒一般的特性，对应的优势是**参数量小**，如何结合两者的优势呢，这里是基于DCNv2的灵感进行改进，在规则卷积中加入随机的依赖关系以及自适

应的空间聚合。

对于普通卷积：

![]()

对于[DCNV2](http://mp.weixin.qq.com/s?__biz=MzU3ODk2Njc5Mg==&mid=2247490816&idx=1&sn=6017318496afc0cb71fdab28bcb16874&chksm=fd6c1967ca1b9071069816bbdd79b4b475ef68050d60e9e99377d5484d5dd64084eca0346989&scene=21#wechat_redirect)，这里我们大概回顾下：

![]()

其中为输出特征中的某一点值，通过卷积获得点x和y方向的偏移量，因为不一定是整数，所以需要基于输入的特征值双线性插值获得值x(p0+pk+△pk)，同时增加mk，通过sigmoid, 位于（0,1）之间，如果系数为0，就表示这部分区域的特征对输出没有影响，这个系数可通过训练学习得到。这样DCNv2因为有采样点的偏移量其实已经满足了远距离获取信息的能力，那为啥不直接将DCNv2用在算法中呢，作者在文中是这样写的，因为DCNv2 大家对它的定位一直是常规卷积的一种拓展，所以在训练的时候，会先加载常规的卷积的预训练模型，再做微调。如果是做大规模视觉模型的baseline ，需要从头训练。所以对其进行优化。个人猜测可能是用了DCNv2从头训练模型难收敛，于是引入DCNv3。

**02 DCNv3**

DCNV3 相对于DCNV2改进的点有以下三点：

1. 在DCNv2的基础上即将卷积部分换成**分组卷积**，这样的话会增加信息量，如DCNv2中有K个采样点，采用分组卷积，如分4组后，这样变相的学到了4K个采样点的信息，这样对全局信息获取到更多的信息量。

2. 采用**深度可分离卷积**，则是在分组卷积完成后，使用深度卷积，完成权重的共享。

3. **归一化**：在DCNV2中的归一化是每个采样点通过sigmoid归一化到[0,1],而K个采样点，会归一化到[0,k]，在大规模参数和数据训练时，会有DCN层梯度的不稳定，所以这里是对K个采样点通过softmax归一化到[0,1]。

这样DCNv3的公式则变成：

![]()

使用DCNv3则带来一个新的问题：常规的conv因其局部信息的局限性，在设计backbone网络时会考虑增加深度来增大感受野，而DCNv3则无需考虑这个问题，那他需要怎样去设计backbone网络呢？

2

InternImage

作者设计了InternImage的网络如下：

![]()

作者借鉴了vit网络中的有效部分：**LN（层归一化）、FFN（前向反馈网络）和GELU（激活函数）**，并增加DCNv3模块，整体上看整个网络架构更偏向于transformer的架构，但是其参数量以及训练要求仅比conv类的高一点。同yolov5s/l/m/x，InternImage 通过C1,C'和L循环次数，通过实验适配出以下几种配置，让网络模型有了T/S/B/L/XL/H几个规模。

![]()

3

代码

论文中，作者以此为backbone在图像分类、目标检测、图像分割等多个任务中都有不同程度的涨点。本文中大刀也试着将代码用在自己的目标检测任务中实际测测。

作者的代码基于mm系列，检测类为mmdetection框架。

**01 训练测试**

安装环境时除了安装mmdet，还需要对dcnv3算子进行编译：

```
```
```
cd ./ops_dcnv3sh ./make.sh
```
```
```

训练的配置和mmdetection保持一致，官网检测类coco格式提供了maskRCNN 和cascadeNet 网络，因为maskRCNN需要有分割标签，cascadeNet模型较大，这里大刀直接用了fasterRCNN做快速验证。在自己的自有训练集上提了**5个点**左右：

![]()

fastercnn的size为477M，相对于InternImage-T 531M，相对较少，性能上稍差也是情有可原，但是InternImage能无脑提几个点，应该不只是参数量上的堆叠。

同时在图像分类领域中，自己的数据集上InternImage 相对于resnet50的acc也从0.88提到了0.9。

**02 部署**

因为新支持的算子，代码中也支持转成onnx和tensorrt:

```
```
```
```
# -------------------------------------------------------# InternImage

```
# Copyright (c) 2022 OpenGVLab  
# Licensed under The MIT License [see LICENSE for details]  
# --------------------------------------------------------  
  
import os  
import time  
import argparse  
  
import torch  
from tqdm import tqdm  
  
from config import get_config  
from models import build_model  
  
def get_args():  
    parser = argparse.ArgumentParser()  
    parser.add_argument('--model_name', type=str,  
                        default='internimage_t_1k_224')  
    parser.add_argument('--ckpt_dir', type=str,  
                        default='/mnt/petrelfs/share_data/huangzhenhang/code/internimage/checkpoint_dir/new/cls')  
    parser.add_argument('--onnx', default=False, action='store_true')  
    parser.add_argument('--trt', default=False, action='store_true')  
  
    args = parser.parse_args()  
    args.cfg = os.path.join('./configs', f'{args.model_name}.yaml')  
    args.ckpt = os.path.join(args.ckpt_dir, f'{args.model_name}.pth')  
    args.size = int(args.model_name.split('.')[0].split('_')[-1])  
  
    cfg = get_config(args)  
    return args, cfg  
  
def get_model(args, cfg):  
    model = build_model(cfg)  
    ckpt = torch.load(args.ckpt, map_location='cpu')['model']  
  
    model.load_state_dict(ckpt)  
    return model  
  
def speed_test(model, input):  
    # warmup  
    for _ in tqdm(range(100)):  
        _ = model(input)  
  
    # speed test  
    torch.cuda.synchronize()  
    start = time.time()  
    for _ in tqdm(range(100)):  
        _ = model(input)  
    end = time.time()  
    th = 100 / (end - start)  
    print(f"using time: {end - start}, throughput {th}")  
  
def torch2onnx(args, cfg):  
    model = get_model(args, cfg).cuda()  
  
    # speed_test(model)  
  
    onnx_name = f'{args.model_name}.onnx'  
    torch.onnx.export(model,  
                      torch.rand(1, 3, args.size, args.size).cuda(),  
                      onnx_name,  
                      input_names=['input'],  
                      output_names=['output'])  
  
    return model  
  
def onnx2trt(args):  
    from mmdeploy.backend.tensorrt import from_onnx  
  
    onnx_name = f'{args.model_name}.onnx'  
    from_onnx(  
        onnx_name,  
        args.model_name,  
        dict(  
            input=dict(  
                min_shape=[1, 3, args.size, args.size],  
                opt_shape=[1, 3, args.size, args.size],  
                max_shape=[1, 3, args.size, args.size],  
            )  
        ),  
        max_workspace_size=2**30,  
    )  
  
def check(args, cfg):  
    from mmdeploy.backend.tensorrt.wrapper import TRTWrapper  
  
    model = get_model(args, cfg).cuda()  
    model.eval()  
    trt_model = TRTWrapper(f'{args.model_name}.engine',  
                           ['output'])  
  
    x = torch.randn(1, 3, args.size, args.size).cuda()  
  
    torch_out = model(x)  
    trt_out = trt_model(dict(input=x))['output']  
  
    print('torch out shape:', torch_out.shape)  
    print('trt out shape:', trt_out.shape)  
  
    print('max delta:', (torch_out - trt_out).abs().max())  
    print('mean delta:', (torch_out - trt_out).abs().mean())  
  
    speed_test(model, x)  
    speed_test(trt_model, dict(input=x))  
  
def main():  
    args, cfg = get_args()  
  
    if args.onnx or args.trt:  
        torch2onnx(args, cfg)  
        print('torch -> onnx: succeess')  
  
    if args.trt:  
        onnx2trt(args)  
        print('onnx -> trt: success')  
        check(args, cfg)  
  
if __name__ == '__main__':  
    main()
```
```
```
```
```

看其推理速度很快：

![]()

不过网上的issue都是关于dcnv3的适配以及算子不支持的情况，期待后期DCNv3的支持，以及后面在移动端等平台上的支持，如果算子的支持达到了，后面很多模型的backbone网络可以换成InternImage。

期待通用大模型“书生2.5”后续多模态的各种集合。

> **结语**

以上为大刀最近使用Internimage backbone的一些尝试，效果惊喜，大家可以多多尝试。

=====碎碎念

文章大刀花了一周，倒不是因为内容有多复杂或深度，而是很久没有写，想写chatgpt,想写图文生成，又想写最近做的另外一些事情，最后一直拖延症。这里给大家一个亲测有效治疗或者说是缓解拖延症的好方法：是在看李松蔚老师的课程中学到的，5%的改变，每次只改变5%，如写公众号，每天规定自己只写20分钟，在这20分钟里只写公众号，超过了20分钟，看心情再写。这篇文章就是在这种场景下写的。希望和大家一起进步![]()

参考：

[1] https://github.com/OpenGVLab/InternImage

[2] https://arxiv.org/abs/2211.05778

![]( "卖萌蔬菜动图特殊用途")

---

最后，为了便于大家学习交流，创建了深度学习的**算法交流群**，包括但不限于CV，nlp, 算法，开发，IT技术等。欢迎大家入群一起学习交流～（因群人数满200人，只能邀请进群，请公众号后台加我微信，拉你进群～

如果觉得写的内容对您有一点点启发和帮助，顺手再看![]()

如果有用 点个在看
