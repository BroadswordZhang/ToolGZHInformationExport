---
标题: "分割大一统——Segment Anything深度体验"
公众号名称: "张大刀修炼手册"
作者: "张大刀修炼手册"
发布时间: "2023-04-07 17:30:00"
原文链接: "https://mp.weixin.qq.com/s/qtk1Ds3hdNi4NOwrw2tDrg"
文章详情_分享类型: "0"
文章ID: "2247501297"
是否已删除: "False"
版权状态: "11"
版权类型: "1"
阅读量: "2738"
喜欢数: "8"
转载量: "3"
文章详情_投票ID: "[]"
文章详情_超级投票ID: "[]"
文章详情_封面图片: "https://mmbiz.qpic.cn/mmbiz_jpg/xH40kQxnnibEwXgniaCw7Uym0KWeYmUrSTLmo6PPj9tgIiaMASEl0dhkQWAZJKEYFZeqXJ0TMaq3FUZRlOs4e1KvQ/0?wx_fmt=jpeg"
文章详情_智能产品信息: "0"
文章详情_修改状态: "1"
文章详情_互动类型: "2"
文章详情_可删除状态: "0"
点赞数: "26"
图文序号: "1"
文章详情_是否付费订阅: "0"
文章详情_是否来自转移: "0"
文章详情_公开标签信息: "{\"public_tag_list\": [], \"modify_times\": 0, \"init_tag_list_size\": 0}"
文章详情_文章合集信息: "{\"appmsg_album_infos\": []}"
文章详情_是否开启粉丝留言: "1"
文章详情_是否处于冷却状态: "0"
文章详情_2.35比1封面地址: "https://mmbiz.qpic.cn/mmbiz_jpg/xH40kQxnnibEwXgniaCw7Uym0KWeYmUrSTqBiaMW3ic27OrZjpvpkSic2XykMkQo5nOY1TOm1rREtC75wq5e1LibdJZg/0?wx_fmt=jpeg"
文章详情_16比9封面地址: "https://mmbiz.qpic.cn/mmbiz_jpg/xH40kQxnnibEwXgniaCw7Uym0KWeYmUrSTqBiaMW3ic27OrZjpvpkSic2XykMkQo5nOY1TOm1rREtC75wq5e1LibdJZg/0?wx_fmt=jpeg"
文章详情_是否禁止推荐: "0"
文章详情_发布线路信息: "{\"use_line\": 1, \"line_count\": 0, \"send_time\": 1680859839, \"is_appmsg_flag\": 1, \"is_use_flag\": 0}"
文章详情_来源声明类型: "0"
分享量: "17"
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
发布消息ID: "1000000073"
发布类型: "101"
发送状态: "{\"total\": 3367, \"succ\": 3367, \"fail\": 0, \"progress\": 100, \"userprotect\": 0}"
发布结果: "{\"msg_status\": 2, \"refuse_reason\": \"\", \"reject_index_list\": [], \"update_time\": 1752674445}"
是否新发布: "0"
文章详情_发布复制类型: "77"
文章详情_发布复制文章ID: "100017563"
文章分析_统计错误: "analysis page parsing failed"
---

# 分割大一统——Segment Anything深度体验

![]()

点击下方公众号关注，一起进步，持续传达瓜货

![]()

Segment Anything 做为Facebook 推出的object分割模型（SAM）和数据集（SA-1B），万物可分割。基于NLP的思路，SAM提出了promp的交互的概念，即通过提示返回有效的mask，提示如point, box等，可以用于下游任务。

> **前言**

大家好，我是张大刀。

昨天早上一大早起来，就被SAM刷屏，Segment Anything，万物可分割：

![]()

乍一看，真的强，边缘分割的平滑，同时对于各个区域划分的合理。在实际的工作中，分割相对于检测和分类任务，标注会花费大量的人力物力，这样至少会节省掉大量的标注。预计后面一些分割场景，如病理和自动驾驶行业会带来一波快速增长。下面我们来仔细了解下这个模型。

**01 SAM的安装使用**

SAM使用有两种方法，一种进入官网的demo网页上传图片测试，一种是安装SAM库，代码测试。

第一种方法简单，进入demo网页：

Segment Anything | Meta AI (segment-anything.com)

上传一张图片，不做任何promp提示：

![]()

通过box的prompt提示：

![]()

通过point的prompt提示：

![]()

效果确实挺好的，目前的基于text分割的功能还没开放。

第二种方法是基于github安装库来测试：

github: https://github.com/facebookresearch/segment-anything

按照readme中安装库和环境，基于编写测试脚本：

```
```
```
```
```
import numpy as np  
import torch  
import matplotlib.pyplot as plt  
import cv2  
import os,sys  
from PIL import Image  
  
def show_mask(mask, ax, random_color=False):  
    if random_color:  
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)  
    else:  
        color = np.array([30/255, 144/255, 255/255, 0.6])  
    h, w = mask.shape[-2:]  
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)  
    #ax.imshow(mask_image)  
    return mask_image  
  
def show_points(coords, labels, ax, marker_size=375):  
    pos_points = coords[labels==1]  
    neg_points = coords[labels==0]  
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)  
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)     
  
def show_box(box, ax):  
    x0, y0 = box[0], box[1]  
    w, h = box[2] - box[0], box[3] - box[1]  
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))      
  
  
sam_checkpoint = "/home/segment-anything-main/checkpoints/sam_vit_h_4b8939.pth"  
device = "cuda"  
model_type = "default"  
images_dir = "/home/seg/images/"  
result_dir = "/home/seg/results/"  
  
def show_anns(anns):  
    if len(anns) == 0:  
        return  
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)  
    ax = plt.gca()  
    ax.set_autoscale_on(False)  
    polygons = []  
    color = []  
    for ann in sorted_anns:  
        m = ann['segmentation']  
        img = np.ones((m.shape[0], m.shape[1], 3))  
        color_mask = np.random.random((1, 3)).tolist()[0]  
        for i in range(3):  
            img[:,:,i] = color_mask[i]  
        ax.imshow(np.dstack((img, m*0.25)))  
  
import sys  
sys.path.append("..")  
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor  
  
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)  
sam.to(device=device)  
  
mask_generator = SamAutomaticMaskGenerator(sam)  
  
for image_name in os.listdir(images_dir):  
    image = cv2.imread(os.path.join(images_dir, image_name))  
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
    masks = mask_generator.generate(image)  
  
    print(len(masks))  
    print(masks[0].keys())  
  
    plt.figure(figsize=(20,20))  
    plt.imshow(image)  
    show_anns(masks)  
    plt.axis('off')  
    plt.savefig(os.path.join(result_dir,image_name))  
    # plt.show()
```
```
```
```
```

与网页上的对比来看，这里左上角的树枝没有被分割出来。同时这里没有prompt的提示，无法针对性的分割。

![]()

同时通过script/amg.py文件，可以得到分割的数据，可以对其数据分析，用于下游任务等：

![]()

**02 SAM的原理**

分割任务之前大致有两种方法。第一种是交互式分割，需要人为迭代细化掩码，如ps里面的抠图，或者是word中自带的背景删除。第二种，通过分割模型，大量标注数据集，训练模型达到自动化分割的效果。SAM 则集两家之所长，通过point和box的prompt，加上单一的模型，可以轻松地执行交互式分割和自动分割。

![]()

从整个流程上看，先通过图像编码器对图像编码，再基于输出的图像的embeding 和mask生成token,并与提示编码器生成的embeding 输入进mask的解码器，并对输出结果进入head中，通过

**图像编码器**：论文使用了预训练的视觉Transformer（ViT）进行图像编码，得到图像的feature map:  
在segment\_anything/modeling/sam.py:

![]()

**提示编码器：**prompt 以点、框和mask的形式（文本的形式需要加入CLIP的训练），通过对点、框等做位置编码，通过点和框得到稀疏embeding, 通过mask得到密集embeding。

![]()

**掩码解码器**：掩码解码器将图像embedding、提示embeding和token映射到mask:

![]()

**动态掩码预测头:** 在mask解码器中，在运行transformer之后，对mask embedding 进行上采样，并通过MLP将输出token映射到动态线性分类器，得到每个mask为前景的概率。

![]()

**解决歧义：**本文中经验发现一个point一般对应了3个mask输出（mask通常最多有三个深度：整体、部分和子部分）。

![]()

通过计算IOU的概率得分，排序选择（这里大刀没找到排序相关的概念，如果大家有找到，欢迎探讨）：

![]()

同时因为代码中只公开了推理代码，在论文中有写在训练过程中，只在mask上反向传播最小的损失。

**效率：**论文中显示prompt编码器和mask解码器在浏览器上运行，CPU上约为50ms，这样可以支持交互式的prompt。

**损失和训练：**使用focal loss和dice loss的来监督mask生成。并通过随机prompt的方式来模拟交互进行训练。

> **结语**

论文主要以模型和数据集为主，介绍了整个模型的一个搭建以及数据集的构建，数据集的构建这里就没有细说了，感兴趣的可以看原文。

同时因为是segment anything，所以，他学习的是object的信息，对于label的信息是无法给予的，这点在blog中也说了，所以他能0样本迁移：

![]()

而对demo中展示的基于text输出label完成分割的例子，在论文中也说了，是训练了一个CLIP，并将CLIP的图像embedding和文本的embedding做了对齐后，这样推理时输入文本后，通过text embedding检索image embedding，进而完成分割。 

![]()

不管怎样，segment anything 已经刮起了CV的浪潮，期待！！

参考：

[1] https://arxiv.org/pdf/2304.02643.pdf

[2] https://github.com/facebookresearch/segment-anything

![]( "卖萌蔬菜动图特殊用途")

---

最后，为了便于大家学习交流，创建了深度学习的**算法交流群**，包括但不限于CV，nlp, 算法，开发，IT技术等。欢迎大家入群一起学习交流～（因群人数满200人，只能邀请进群，请公众号后台加我微信，拉你进群～

如果觉得写的内容对您有一点点启发和帮助，顺手再看![]()

如果有用 点个在看
