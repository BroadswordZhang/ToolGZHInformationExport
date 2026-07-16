---
标题: "YOLOU开源 | 汇集YOLO系列所有算法，集算法学习、科研改进、落地于一身！"
公众号名称: "张大刀修炼手册"
作者: "张大刀修炼手册"
发布时间: "2022-07-28 08:29:52"
原文链接: "https://mp.weixin.qq.com/s/0EJ4DHq0ZGgjzG1r1LHi9A"
文章详情_分享类型: "0"
文章ID: "2247496807"
是否已删除: "False"
版权状态: "201"
版权类型: "2"
阅读量: "450"
喜欢数: "6"
文章详情_投票ID: "[]"
文章详情_超级投票ID: "[]"
文章详情_封面图片: "https://mmbiz.qpic.cn/mmbiz_jpg/5ooHoYt0tglYD8piaEoib5Ek4cHfOdLib2gJLGo9oZ7SkOU3WibTBE7JbDAFMtIYjX7tvcHQJCM8S0uC2ELQxFria3g/0?wx_fmt=jpeg"
文章详情_智能产品信息: "0"
文章详情_修改状态: "1"
文章详情_互动类型: "2"
文章详情_可删除状态: "0"
点赞数: "10"
图文序号: "1"
文章详情_是否付费订阅: "0"
文章详情_是否来自转移: "0"
文章详情_公开标签信息: "{\"public_tag_list\": [], \"modify_times\": 0, \"init_tag_list_size\": 0}"
文章详情_文章合集信息: "{\"appmsg_album_infos\": []}"
文章详情_是否开启粉丝留言: "1"
文章详情_是否处于冷却状态: "0"
文章详情_2.35比1封面地址: "https://mmbiz.qpic.cn/mmbiz_jpg/5ooHoYt0tglYD8piaEoib5Ek4cHfOdLib2gJLGo9oZ7SkOU3WibTBE7JbDAFMtIYjX7tvcHQJCM8S0uC2ELQxFria3g/0?wx_fmt=jpeg"
文章详情_16比9封面地址: "https://mmbiz.qpic.cn/mmbiz_jpg/5ooHoYt0tglYD8piaEoib5Ek4cHfOdLib2gJLGo9oZ7SkOU3WibTBE7JbDAFMtIYjX7tvcHQJCM8S0uC2ELQxFria3g/0?wx_fmt=jpeg"
文章详情_是否禁止推荐: "0"
文章详情_发布线路信息: "{\"use_line\": 1, \"line_count\": 0, \"send_time\": 1658968192, \"is_appmsg_flag\": 1, \"is_use_flag\": 0}"
文章详情_来源声明类型: "0"
文章详情_是否强制转载: "0"
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
发布消息ID: "1000000055"
发布类型: "101"
发送状态: "{\"total\": 1776, \"succ\": 1776, \"fail\": 0, \"progress\": 100, \"userprotect\": 0}"
发布结果: "{\"msg_status\": 2, \"refuse_reason\": \"\", \"reject_index_list\": [], \"update_time\": 1752674449}"
是否新发布: "0"
文章详情_发布复制类型: "77"
文章详情_发布复制文章ID: "100013158"
文章分析_统计错误: "analysis page parsing failed"
---

# YOLOU开源 | 汇集YOLO系列所有算法，集算法学习、科研改进、落地于一身！

![]()

点击下方公众号关注，一起进步，持续传达瓜货

![]()

大家好，我是张大刀。

yolo系列的快速迭代，以及对应工程的快速更新，导致在做yolo比对，以及相关trick迁移时，花费不少精力，这里推荐yolo系列的算法实现库YOLOU，用一套工程，即可满足yolo系列的全方位实现，希望对大家有帮助。

![]()
> 这里推荐一个YOLO系列的算法实现库YOLOU，此处的“U”意为“United”的意思，主要是为了学习而搭建的YOLO学习库，也借此向前辈们致敬，希望不被骂太惨；
>
> 整个算法完全是以YOLOv5的框架进行，主要包括的目标检测算法有：YOLOv3、YOLOv4、YOLOv5、YOLOv5-Lite、YOLOv6、YOLOv7、YOLOX以及YOLOX-Lite。
>
> 同时为了方便算法的部署落地，这里所有的模型均可导出ONNX并直接进行TensorRT等推理框架的部署，后续也会持续更新。

## 模型精度对比

### 服务端模型

这里主要是对于YOLO系列经典化模型的训练对比，主要是对于YOLOv5、YOLOv6、YOLOv7以及YOLOX的对比，部分模型还在训练之中，后续所有预训练权重均会放出，同时对应的ONNX文件也会给出，方便大家部署应用落地。

注意，这里关于YOLOX也没完全复现官方的结果，后续有时间还会继续调参测试，尽可能追上YOLOX官方的结果。

下表是关于YOLOU中模型的测试，也包括TensorRT的速度测试，硬件是基于3090显卡进行的测试，主要是针对FP32和FP16进行的测试，后续的TensorRT代码也会开源。目前还在整理之中。

![]()

### 轻量化模型

为了大家在手机端或者其他诸如树莓派、瑞芯微、AID以及全志等芯片的部署，YOLOU也对YOLOv5和YOLOX进行了轻量化设计。

下面主要是对于边缘端使用的模型进行对比，主要是借鉴之前小编参与的YOLOv5-Lite的仓库，这里也对YOLOX-Lite进行了轻量化迁移，总体结果如下表所示，YOLOX-Lite基本上可以超越YOLOv5-Lite的精度和结果。

![]()

# 如何使用YOLOU？

## 安装

这里由于使用的是YOLOv5的框架进行的搭建，因此安装形式也及其的简单，具体如下：

```
git clone https://github.com/jizhishutong/YOLOU  
cd YOLOU  
pip install -r requirements.txt
```

## 数据集

这里依旧使用YOLO格式的数据集形式，文件夹形式如下：

```
train: ../coco/images/train2017/  
val: ../coco/images/val2017/
```

具体的标注文件和图像list如下所示：

```
├── images            # xx.jpg example  
│   ├── train2017          
│   │   ├── 000001.jpg  
│   │   ├── 000002.jpg  
│   │   └── 000003.jpg  
│   └── val2017           
│       ├── 100001.jpg  
│       ├── 100002.jpg  
│       └── 100003.jpg  
└── labels             # xx.txt example        
    ├── train2017         
    │   ├── 000001.txt  
    │   ├── 000002.txt  
    │   └── 000003.txt  
    └── val2017           
        ├── 100001.txt  
        ├── 100002.txt  
        └── 100003.txt
```

## 参数配置

YOLOU为了方便切换不同模型之间的训练，这里仅仅需要配置一个`mode`即可切换不同的模型之间的检测和训练，具体意义如下：

![]()

注意：这里的`mode`主要是对于Loss计算的选择，对于YOLOv3、YOLOv4、YOLOv5、YOLOR以及YOLOv5-Lite直接设置`mode=yolo`即可，对于YOLOX以及YOLOX-Lite则设置`mode=yolox`，对于YOLOv6和YOLOv7则分别设置`mode=yolov6和mode=yolov7`；

注意由于YOLOv7使用了Aux分支，因此在设置YOLOv7时有一个额外的参数需要配置，即`use_aux=True`。

具体训练指令如下：

```
python train.py --mode yolov6 --data coco.yaml --cfg yolov6.yaml --weights yolov6.pt --batch-size 32
```

检测指令如下：

```
python detect.py --source 0  # webcam  
                            file.jpg  # image   
                            file.mp4  # video  
                            path/  # directory  
                            path/*.jpg  # glob  
                            'https://youtu.be/NUsoVlDFqZg'  # YouTube  
                            'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream
```

# 检测结果

## 服务端模型

![]()

## 轻量化模型

![]()

# 参考

[1].https://github.com/jizhishutong/YOLOU

最后，为了便于大家学习交流，创建了深度学习的**算法交流群**，包括但不限于CV，nlp, 算法，开发，IT技术等。欢迎大家入群一起学习交流～（若二维码失效，请公众号后台加我微信，拉你进群～

![]()

如果觉得写的内容对您有一点点启发和帮助，顺手再看![]()

如果有用 点个在看
