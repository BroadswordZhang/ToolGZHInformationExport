---
标题: "文本图像数据增强方法，不只是Augraphy"
公众号名称: "张大刀修炼手册"
作者: "张大刀修炼手册"
发布时间: "2022-09-02 17:22:39"
原文链接: "https://mp.weixin.qq.com/s/VcYWSOHFEL846xMHJg3CmQ"
文章详情_分享类型: "0"
文章ID: "2247497814"
是否已删除: "False"
版权状态: "11"
版权类型: "1"
阅读量: "443"
喜欢数: "5"
转载量: "0"
文章详情_投票ID: "[]"
文章详情_超级投票ID: "[]"
文章详情_封面图片: "https://mmbiz.qpic.cn/mmbiz_jpg/xH40kQxnnibHkQ7j3tt5eE8zcKhiaBFAMeNb6KWicXJKKTWl277YlkjvjAicOIKfbo0Peb4q85KS2kkXicoEL5Xkvuw/0?wx_fmt=jpeg"
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
文章详情_是否开启粉丝留言: "1"
文章详情_是否处于冷却状态: "0"
文章详情_2.35比1封面地址: "https://mmbiz.qpic.cn/mmbiz_jpg/xH40kQxnnibHkQ7j3tt5eE8zcKhiaBFAMeAQuicaOibt7Y2HlCy9sob0vCLzwR34LC6osHIVdCpq3v6ia3RVGAwbNKA/0?wx_fmt=jpeg"
文章详情_16比9封面地址: "https://mmbiz.qpic.cn/mmbiz_jpg/xH40kQxnnibHkQ7j3tt5eE8zcKhiaBFAMeAQuicaOibt7Y2HlCy9sob0vCLzwR34LC6osHIVdCpq3v6ia3RVGAwbNKA/0?wx_fmt=jpeg"
文章详情_是否禁止推荐: "0"
文章详情_发布线路信息: "{\"use_line\": 1, \"line_count\": 0, \"send_time\": 1662110559, \"is_appmsg_flag\": 1, \"is_use_flag\": 0}"
文章详情_来源声明类型: "0"
分享量: "10"
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
发布消息ID: "1000000058"
发布类型: "101"
发送状态: "{\"total\": 1954, \"succ\": 1954, \"fail\": 0, \"progress\": 100, \"userprotect\": 0}"
发布结果: "{\"msg_status\": 2, \"refuse_reason\": \"\", \"reject_index_list\": [], \"update_time\": 1752674448}"
是否新发布: "0"
文章详情_发布复制类型: "77"
文章详情_发布复制文章ID: "100014162"
文章分析_统计错误: "analysis page parsing failed"
---

# 文本图像数据增强方法，不只是Augraphy

![]()

点击下方公众号关注，一起进步，持续传达瓜货

![]()

大家好，我是张大刀。

今天在逛arxiv时（好吧，承认我在摸鱼），发现了一个很有用的文本图像的数据增强库Augraphy，最重要的是，代码开源！

![]()

作为大刀的卷友们，不能让大家不知道![]()，开卷吧！

**1. 干啥的**

Augraphy 是一种文本图像的数据增强库，可以对干净的文本图像数据增强，模拟出打印机痕迹、打印油墨以及手写字迹随时间退化、纸张褶皱等效果。瞅瞅这个效果：

![]()

Augraphy 提供了24种数据增强方式：

![]()

**2. 怎么用**

Augraphy 已经打包成一个python包，可以通过：

```
pip install augraphy
```

来安装，具体调用案例：

```
import augraphy; import cv2 pipeline = augraphy.default_augraphy_pipeline() img = cv2.imread("image.png") data = pipeline.augment(img)augmented = data["output"]
```

***github:  https://github.com/sparkfish/augraphy***

***arxiv:  https://arxiv.org/pdf/2208.14558.pdf***

**3. 福利篇**

对于ocr文本图像的数据增强，不同于一般图像分类等任务的数据增强，是不是有一个系统的研究方向，果不其然，又找到了一篇ICCV2021 自然场景文本识别中的数据增强，相对于模拟纸张的数据增强，这篇自然场景下的文本图像数据增强，提供了36种数据增强方法：

除了一般的图像上的模糊、噪声、颜色、旋转、缩放等数据增强方式外，还增加了弯曲、扭曲、网格线、雾化、雪化、雨点等用于ocr识别上的数据增强：

![]()

![]()

![]()

这个代码也是开源的，具体使用参见开源代码：

***github: https://github.com/roatienza/straug***

***arxiv:https://arxiv.org/pdf/2108.06949.pdf***

**4. 思考**

虽说误打误撞中找了跟自己研究方向没有关系的两个库，想起之前恶劣天气下的目标检测任务的数据增强，可以用上述的数据增强方式试试，也算的有用的吧。

> **结语**

以上为分享了两个文本图像的数据增强库，希望对大家有用。

![]( "卖萌蔬菜动图特殊用途")

最后，为了便于大家学习交流，创建了深度学习的**算法交流群**，包括但不限于CV，nlp, 算法，开发，IT技术等。欢迎大家入群一起学习交流～（若二维码失效，请公众号后台加我微信，拉你进群～

![]()

如果觉得写的内容对您有一点点启发和帮助，顺手再看![]()

如果有用 点个在看
