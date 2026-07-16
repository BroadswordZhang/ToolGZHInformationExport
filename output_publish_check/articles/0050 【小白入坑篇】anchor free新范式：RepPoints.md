---
标题: "【小白入坑篇】anchor free新范式：RepPoints"
公众号名称: "张大刀修炼手册"
作者: "张大刀修炼手册"
发布时间: "2022-04-07 23:00:02"
原文链接: "https://mp.weixin.qq.com/s/-iMqsgpLRs5W6Er11dSX9w"
文章详情_分享类型: "0"
文章ID: "2247491272"
是否已删除: "False"
版权状态: "11"
版权类型: "1"
阅读量: "339"
喜欢数: "6"
转载量: "0"
文章详情_投票ID: "[]"
文章详情_超级投票ID: "[]"
文章详情_封面图片: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibEcbwsy1rXChjHQGJBFmKefg67ejIibzdvSrKs5qKbSZiaDMhhB67ibUvAcrY7h0MVWskw3We0Q7RwdQ/0?wx_fmt=jpeg"
文章详情_智能产品信息: "0"
文章详情_修改状态: "1"
文章详情_互动类型: "2"
文章详情_可删除状态: "0"
点赞数: "12"
图文序号: "1"
文章详情_是否付费订阅: "0"
文章详情_是否来自转移: "0"
文章详情_公开标签信息: "{\"public_tag_list\": [], \"modify_times\": 0, \"init_tag_list_size\": 0}"
文章详情_文章合集信息: "{\"appmsg_album_infos\": []}"
文章详情_是否开启粉丝留言: "0"
文章详情_是否处于冷却状态: "0"
文章详情_2.35比1封面地址: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibEcbwsy1rXChjHQGJBFmKefwAJml2mmj91uhYFJe2kT2ISUoEzXvicGOe2q6nz8Eic7KZs6cNke8Nhw/0?wx_fmt=jpeg"
文章详情_16比9封面地址: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibEcbwsy1rXChjHQGJBFmKefwAJml2mmj91uhYFJe2kT2ISUoEzXvicGOe2q6nz8Eic7KZs6cNke8Nhw/0?wx_fmt=jpeg"
文章详情_是否禁止推荐: "0"
文章详情_发布线路信息: "{\"use_line\": 1, \"line_count\": 0, \"send_time\": 1649343602, \"is_appmsg_flag\": 1, \"is_use_flag\": 0}"
文章详情_来源声明类型: "0"
分享量: "1"
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
发布消息ID: "1000000033"
发布类型: "101"
发送状态: "{\"total\": 358, \"succ\": 358, \"fail\": 0, \"progress\": 100, \"userprotect\": 0}"
发布结果: "{\"msg_status\": 2, \"refuse_reason\": \"\", \"reject_index_list\": [], \"update_time\": 1752674454}"
是否新发布: "0"
文章详情_发布复制类型: "77"
文章详情_发布复制文章ID: "100007515"
文章分析_统计错误: "analysis page parsing failed"
---

# 【小白入坑篇】anchor free新范式：RepPoints

![]()

![]()

![]()

点击下方公众号关注，一起进步，持续传达瓜货

![]()

本文主要介绍RepPoints目标检测算法，可以看做是可变形卷积的一种延伸，它能提供更细粒度的分类和更方便的定位，代码已开源。

大家好，我是张大刀，作为cvpr《Oriented RepPoints for Aerial Object Detection》的前传，继续填坑RepPoints ，想了解RepPoints 前传可变形卷积DCN系列的可以点击[这里](http://mp.weixin.qq.com/s?__biz=MzU3ODk2Njc5Mg==&mid=2247490816&idx=1&sn=6017318496afc0cb71fdab28bcb16874&chksm=fd6c1967ca1b9071069816bbdd79b4b475ef68050d60e9e99377d5484d5dd64084eca0346989&scene=21#wechat_redirect)。**RepPoints**是微软研究院提出的一种基于点集的目标表示方法，登顶ICCV2019，关于RepPoints系列，网上已经有大篇非常好的详细描述，这里主要是方便自己理解的一些梳理，感兴趣的小伙伴可以参见文末的参考链接。

> **前言**

在目标检测场景中，一般有**anchor base**和**anchor free** 两种思路，在anchor base 算法中，如faster RCNN、Yolov3、v4、v5等模型效果往往受限于anchor的参数配置，如anchor的大小、正负样本采样等。在anchor free 算法中，也分为两种思路，**anchor-point**的算法和**key-point**的算法，anchor-point通过预测目标中心点(x,y)及边框距中心点的距离(w,h)来检测目标，典型的此类算法有Yolov1，FCOS等，而key-point方法是通过检测目标的边界点（如：角点），再将边界点配对组合成目标的检测框，此类算法包括CornerNet等。

**Reppints**可以看做这两种思路的结合。它同anchor-point一样，在feature map的每个location位置，以该location做为中心，去预测一个box，但是它预测的不是类似FCOS那样的到box四个边界的距离，而是预测的一系列**reppoints**，然后通过把这些点映射为box得到最终的结果。

> 1
>
> **Reppints**

RepPoints 是一种新的目标表示方法，是基于可变形卷积的一种延伸，增加了对可变形卷积中特征点的训练监督，并对特征点进行目标检测，它提供了更细粒度的定位和更方便的分类。

![]()

如图所示，RepPoints是一组点，通过学习自适应地将自己置于目标之上，该方式限定了目标的空间范围，并且表示具有重要语义信息的局部区域。

01

原理

与Yolov1一样，如一张640\*640的图片，在backbone提取特征过后，如果经过5次下采样后，feature map成20\*20的长宽，yolov1的做法是将20\*20映射到原图上，有20\*20的网格grid，每个网格32\*32的像素，默认为目标的中心点落在的所在grid负责预测该目标，该grid下采样到feature map上就成了一点，那我们只需要预测出四个维度：目标中心点(x,y)偏移该grid中心点多少，以及目标的长宽即：

![]()

就可以预测出目标的具体位置。所以feature map的channel维度上需要学习（x,y,w,h）4个channel来对目标定位。

与Yolov1不同的是，**RepPoints**需要预测出9个点，即在每个feature map对应的location位置，网络需要学习出9组偏移量，如下图所示，

![]()

如20\*20长宽的feature map,共有400个点，对于每个点需要预测出9个点，来调整样本点的位置：

![]()

(△xk,△yk)分别为预测点相对于中心点的偏差，n一般取9，怎么去学习这个偏差值呢，这块和可变形卷积DCN原理相同，对DCN感兴趣的的可以点击[这里](http://mp.weixin.qq.com/s?__biz=MzU3ODk2Njc5Mg==&mid=2247490816&idx=1&sn=6017318496afc0cb71fdab28bcb16874&chksm=fd6c1967ca1b9071069816bbdd79b4b475ef68050d60e9e99377d5484d5dd64084eca0346989&scene=21#wechat_redirect)。

综上可以发现其实这个检测思路和FCOS和YOLO等有一点点像，都是把每个位置作为中心点，作者认为Yolov1这类检测虽然也是anchor free，但是需要4d空间（x,y,w,h），这里只需要二维空间（x,y），即9个点的坐标，似乎9个点去还原一个box有点多余，理论上两个点就可以还原一个box了，但是作者认为学习9个点计算出的box更准确，他发现这9个点经常落在极点或者对语义表达很有帮助的地方，如下图。

![]()

02

**网络RPdet**

综上，作者设计整个检测器架构如图：

![]()

总体上，该方法是基于全卷积网络实现的，输入图像经过FPN主干网络后，经过一次3x3的可变形卷积，预测的offset经过坐标计算，得到第一次的RepPoints，可形变卷积继续提取特征，再预测得到offset和每个位置的分类结果，由offset计算得到细化后第二次的RepPoints。最终将每个位置的RepPoints转换预测框，加上分类结果，得到目标检测的结果。

具体的实现网络如图：

![]()

即**Class分支**仅使用Offset1的输出值，而卷积独立进行。Offset2则继续使用Offset1子网络的特征图。Class分支和Offset2分支都使用了可形变卷积。

目标表示的演化过程如下：

![]()

RepPoints检测器由两个基于可变形卷积的识别阶段构成，思路同faster RCNN一样，不断的修正目标检测位置：

![]()

03

**loss**

根据上面location学习的点，怎么把reppoints转化为box来衡量检测结果和gt的差异，这里作者给出了几种不同的思路：

1. **Min-max function**：在所有点中找最小和最大值，获得囊括所有点的外接矩形框；

2. **Partial min-max function**：选取部分点进行上述操作

3. **Moment-based function**：求出所有样本点的均值和方差，通过另外两个全局学习的系数将均值和方差还原为box。

作者通过得到box和gt的top-left与bottom-right之间的smooth l1误差来监督，实验发现，这三种思路得到的结果差异比较小(在0.1%内)。

定位loss计算时，将RepPoints按照转换函数，转换为预测框，然后使用**smooth L1 Loss**。第一次和第二次RepPoints的定位损失均只计算正样本。

总的来说，第一次RepPoints计算一次定位损失，同时考虑上分类损失。使第一次RepPoints的训练额外结合了分类的监督信息，这一点和可形变卷积的过程一致。

第二次RepPoints再计算一次定位损失，但是不计算分类损失了。

> 2
>
> 实验

作者基于RepPoints做了消融实验和对比实验：

01

**RepPoints vs Bounding Box**

![]()

在MS-COCO数据集上的对比实验

02

**消融实验**

对于生成第一次RepPoints时，监督信息来源的消融实验，对于RepPoints来说，转换为预测框计算定位损失显得很有效。同时，引入分类监督信息，可以进一步提高性能。

![]()

03

**转换函数**

![]()

性能差别不大，T3最好，但是T3需要学习两个全局系数。

04

**与其他模型对比**

![]()

在单阶段方法中表现很好，并且借助多尺度训练和多尺度测试能够进一步提升精度，远超先前的two-stage方法。

> 结语

综上，RepPoints完成，RepPoints在19年时，感觉借鉴了很多faster RCNN的思路，最大的亮点是**增加了对于可形变卷积的监督**。可形变卷积有很强的表达能力，很好的性能，因此尝试加强对于可形变卷积的监督，增加可形变卷积的特征点和目标检测中物体的联系。即可形变卷积中的特征点，经过设计训练后，是可以具有一定的显式语义信息的。

RepPoints中的特征点倾向于表示物体的中心点和极点，可以看做是一种关键点检测的过程，不过因为通过gt框去监督，相对来说对关键点的监督较弱。但是关键点只是一种可视化结果，可能其学习的是无法表达的语义信息，所以如果真的直接基于关键点去监督，反而可能画蛇添足，缺少泛化性。

下一篇：《Oriented RepPoints for Aerial Object Detection》

论文地址：

*https://arxiv.org/abs/1904.11490*

开源代码地址：

*https://github.com/microsoft/RepPoints*

参考：

*[1]  https://blog.csdn.net/qq\_21949357/article/details/102656708*

*[2]  https://zhuanlan.zhihu.com/p/64522910*

*[3]  https://zhuanlan.zhihu.com/p/260656201*

*[4]  https://zhuanlan.zhihu.com/p/136175181*

*[5]  https://blog.csdn.net/qq\_30146937/article/details/104530348*

*[6]  https://www.zhihu.com/question/322372759/answer/670961802*

*[7]  https://www.jiqizhixin.com/articles/2019-10-30-3*

---

如果有任何困惑和疑问，欢迎进入公众号，添加微信号一起交流。

如果觉得写的内容对您有一点点启发和帮助，顺手再看![]()

如果有用 点个在看
