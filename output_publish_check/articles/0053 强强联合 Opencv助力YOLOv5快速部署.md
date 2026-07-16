---
标题: "强强联合|Opencv助力YOLOv5快速部署"
公众号名称: "张大刀修炼手册"
作者: "张大刀修炼手册"
发布时间: "2022-03-31 23:45:42"
原文链接: "https://mp.weixin.qq.com/s/vUrkuyMwD6Yk1MLc1VCW0A"
文章详情_分享类型: "0"
文章ID: "2247490200"
是否已删除: "False"
版权状态: "11"
版权类型: "1"
阅读量: "794"
喜欢数: "9"
转载量: "0"
文章详情_投票ID: "[]"
文章详情_超级投票ID: "[]"
文章详情_封面图片: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibFzLbxZ6RjOyg6CvOyGckdicYbgIibeDj5JMjQUicrSTiaG76ibPvdOeToDTDQoRLgIICxibibPtD0okIDiag/0?wx_fmt=jpeg"
文章详情_智能产品信息: "0"
文章详情_修改状态: "1"
文章详情_互动类型: "2"
文章详情_可删除状态: "0"
点赞数: "25"
图文序号: "1"
文章详情_是否付费订阅: "0"
文章详情_是否来自转移: "0"
文章详情_公开标签信息: "{\"public_tag_list\": [], \"modify_times\": 0, \"init_tag_list_size\": 0}"
文章详情_文章合集信息: "{\"appmsg_album_infos\": []}"
文章详情_是否开启粉丝留言: "0"
文章详情_是否处于冷却状态: "0"
文章详情_2.35比1封面地址: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibFzLbxZ6RjOyg6CvOyGckdicTjq7ictoBobePkfGpibdZ2G9MetCZ7ZwcXVEBHxnd1MI7cJT1ficU8Ftw/0?wx_fmt=jpeg"
文章详情_16比9封面地址: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibFzLbxZ6RjOyg6CvOyGckdicTjq7ictoBobePkfGpibdZ2G9MetCZ7ZwcXVEBHxnd1MI7cJT1ficU8Ftw/0?wx_fmt=jpeg"
文章详情_是否禁止推荐: "0"
文章详情_发布线路信息: "{\"use_line\": 1, \"line_count\": 0, \"send_time\": 1648741542, \"is_appmsg_flag\": 1, \"is_use_flag\": 0}"
文章详情_来源声明类型: "0"
分享量: "11"
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
发布消息ID: "1000000030"
发布类型: "101"
发送状态: "{\"total\": 251, \"succ\": 251, \"fail\": 0, \"progress\": 100, \"userprotect\": 0}"
发布结果: "{\"msg_status\": 2, \"refuse_reason\": \"\", \"reject_index_list\": [], \"update_time\": 1752674455}"
是否新发布: "0"
文章详情_发布复制类型: "77"
文章详情_发布复制文章ID: "100006535"
文章分析_统计错误: "analysis page parsing failed"
---

# 强强联合|Opencv助力YOLOv5快速部署

![]()

![]()

![]()

点击下方公众号关注，一起进步，持续传达瓜货

![]()

opencv提出DNN模块，致力于各类算法的c++和Python部署，本文以yolov5为例，实战算法的推理过程，代码开源，除opencv外对框架零依赖，是端侧部署的重点选择。

> **前言**

yolov5在目标检测任务中被公认为在速度和准确性最好的目标检测模型之一，相信大家对yolov5已经很熟悉，不熟悉的小伙伴可以去看江大白老师的《**深入浅出Yolo系列之Yolov5核心基础知识完整讲解**》【1】。同时因为yolov5s和yolov5m的轻量化，可以轻松与嵌入式设备继承。

opencv从3.5版本后引入**DNN**模块，对接深度学习，随着4.5版本的迭代，DNN模块开始支持darknet、caffe、onnx等框架，能够实现对算法的快速部署，无需安装其他框架，特别适合**端侧设备**。

这里先简要介绍下opencv的DNN模块，然后在通过代码演示支持onnx的YOLOv5在OpenCV中的使用。

> 1
>
> **Opencv DNN 模块**

OpenCV中的**dnn**（Deep Neural Network module）模块在3.3版本从拓展库中正式release发版，是专门用来实现深度神经网络相关功能的模块。OpenCV自己并不能训练神经网络模型，但是它可以载入别的深度学习框架（例如TensorFlow、Caffe等等）训练好的模型，然后使用该模型做inference（预测）。而且OpenCV在载入模型时会使用自己的dnn模块对**模型重写**，使得模型的运行效率更高。同时**零依赖**，只依赖 opencv，如果你被 caffe 虐过，那么就知道零依赖是多么如沐清风。

所以如果你想在OpenCV项目中融入深度学习模型，可以先用自己熟悉的深度学习框架训练好，然后使用OpenCV的dnn模块载入。

> 2
>
> opencv 助力 yolov5

yolov5的官方代码是用pytorch框架写的，因为opencv 的DNN模块不支持pytorch 的训练模型，这里先将其转成onnx模型，opencv支持的格式，转换的过程及代码参见yolov5 github官网【2】。

以下我们分别使用Python和c++分四个步骤来完成推理整个过程：

1. 加载yolov5模型

2. 输入图像完成预测

3. 预测结果解析

4. 打印生成图片

01

**加载yolov5模型**

此步骤由一行代码组成，用于导入模型：

Python：

```
```
```
import cv2  
  
net = cv2.dnn.readNet('yolov5s.onnx')
```
```
```

c++:

```
```
```
```
#include <opencv2/opencv.hpp>  
  
int main(int, char **)  
{  
    auto net = cv::dnn::readNet("yolov5s.onnx");  
  
    return 0;  
}
```
```
```
```

02

**输入图像完成预测**

在输入图像前，需要先对图像处理，使得模型的**输入接口对齐**，这里图像在模型输入时需要是归一化后的尺寸在640x640的RGB图像：这里使用DNN模块对图像归一化。

python:

```
```
```
```
def format_yolov5(source):  
  
    # put the image in square big enough  
    col, row, _ = source.shape  
    _max = max(col, row)  
    resized = np.zeros((_max, _max, 3), np.uint8)  
    resized[0:col, 0:row] = source  
  
    # resize to 640x640, normalize to [0,1[ and swap Red and Blue channels  
    result = cv2.dnn.blobFromImage(resized, 1/255.0, (640, 640), swapRB=True)  
  
    return resul
```
```
```
```

c++:

```
```
```
```
cv::Mat format_yolov5(const cv::Mat &source) {  
  
    // put the image in a square big enough  
    int col = source.cols;  
    int row = source.rows;  
    int _max = MAX(col, row);  
    cv::Mat resized = cv::Mat::zeros(_max, _max, CV_8UC3);  
    source.copyTo(resized(cv::Rect(0, 0, col, row)));  
  
    // resize to 640x640, normalize to [0,1[ and swap Red and Blue channels  
    cv::Mat result;  
    cv::dnn::blobFromImage(source, result, 1./255., cv::Size(INPUT_WIDTH, INPUT_HEIGHT), cv::Scalar(), true, false);  
  
    return result;
```
```
```
```

对处理后的图像调用模型：

Python:

```
```
```
```
predictions = net.forward()  
output = predictions[0]
```
```
```
```

c++:

```
```
```
```
std::vector<cv::Mat> predictions;  
net.forward(predictions, net.getUnconnectedOutLayersNames());  
const cv::Mat &output = predictions[0];
```
```
```
```

03

**解析预测结果**

在对图像做检测后，返回output 2D数组中的所有预测结果，下图代表了结果的数组结构：

![]()

这个数组预测了 25,200 个框，每个框都是一个 85 位的一维数组。每个一维数组保存一个检测的数据。该数组的前 4 个位置是xywh边界框矩形的坐标，第五位置是该检测框的置信水平。第 6 到第 85 个元素是每个类别的分数。下面的代码显示了如何从二维数组中**解析数据**：

Python:

```
```
```
```
def unwrap_detection(input_image, output_data):  
    class_ids = []  
    confidences = []  
    boxes = []  
  
    rows = output_data.shape[0]  
  
    image_width, image_height, _ = input_image.shape  
  
    x_factor = image_width / 640  
    y_factor =  image_height / 640  
  
    for r in range(rows):  
        row = output_data[r]  
        confidence = row[4]  
        if confidence >= 0.4:  
            classes_scores = row[5:]  
            _, _, _, max_indx = cv2.minMaxLoc(classes_scores)  
            class_id = max_indx[1]  
            if (classes_scores[class_id] > .25):  
                confidences.append(confidence)  
                class_ids.append(class_id)  
                x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()   
                left = int((x - 0.5 * w) * x_factor)  
                top = int((y - 0.5 * h) * y_factor)  
                width = int(w * x_factor)  
                height = int(h * y_factor)  
                box = np.array([left, top, width, height])  
                boxes.append(box)  
  
    return class_ids, confidences, boxes
```
```
```
```

当然，并非 25,200 次检测中的每一次检测都是实际检测，我们使用一些阈值来过滤，使用if confidence > 0.4过滤掉低置信度检测框。

值得注意的是，输入图像是 640x640。因此，有必要将坐标重新缩放xywh到实际输入尺寸：

```
```
```
```
```
x, y, w, h = row[0], row[1], row[2], row[3]   
left = int((x - 0.5 * w) * x_factor)   
top = int((y - 0.5 * h) * y_factor)   
width = int(w * x_factor)   
height = int(h * y_factor)   
box = [left, top, width, height]   
boxes.append(box)
```
```
```
```
```

即使过滤低置信度检测框，前面的代码也会生成重复的框：

![]()

**非最大抑制(NMS)** 算法来消除重叠/重复检测框：

Python

```
```
```
```
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45)   
  
result_class_ids = []  
result_confidences = []  
result_boxes = []  
  
for i in indexes:  
    result_confidences.append(confidences[i])  
    result_class_ids.append(class_ids[i])  
    result_boxes.append(boxes[i])
```
```
```
```

综上Python版对预测结果解析完成，下面是c++版本：

c++:

```
```
```
```
```
struct Detection  
{  
    int class_id;  
    float confidence;  
    cv::Rect box;  
};  
  
void detect(const cv::Mat &input_image, constcv::Mat &output, std::vector<Detection> &output) {  
  
    float x_factor = input_image.cols / 640.;  
    float y_factor = input_image.rows / 640.;  
  
    float *data = (float *)outputs[0].data;  
  
    const int dimensions = 85;  
    const int rows = 25200;  
  
    std::vector<int> class_ids;  
    std::vector<float> confidences;  
    std::vector<cv::Rect> boxes;  
  
    for (int i = 0; i < rows; ++i) {  
  
        float confidence = data[4];  
        if (confidence >= .4) {  
  
            float * classes_scores = data + 5;  
            cv::Mat scores(1, className.size(), CV_32FC1, classes_scores);  
            cv::Point class_id;  
            double max_class_score;  
            minMaxLoc(scores, 0, &max_class_score, 0, &class_id);  
            if (max_class_score > SCORE_THRESHOLD) {  
  
                confidences.push_back(confidence);  
  
                class_ids.push_back(class_id.x);  
  
                float x = data[0];  
                float y = data[1];  
                float w = data[2];  
                float h = data[3];  
                int left = int((x - 0.5 * w) * x_factor);  
                int top = int((y - 0.5 * h) * y_factor);  
                int width = int(w * x_factor);  
                int height = int(h * y_factor);  
                boxes.push_back(cv::Rect(left, top, width, height));  
            }  
  
        }  
  
        data += 85;  
  
    }  
  
    std::vector<int> nms_result;  
    cv::dnn::NMSBoxes(boxes, confidences, SCORE_THRESHOLD, NMS_THRESHOLD, nms_result);  
    for (int i = 0; i < nms_result.size(); i++) {  
        int idx = nms_result[i];  
        Detection result;  
        result.class_id = class_ids[idx];  
        result.confidence = confidences[idx];  
        result.box = boxes[idx];  
        output.push_back(result);  
    }  
}
```
```
```
```
```

04

**打印生成图片**

打印带有检测结果的图像：

Python：

```
```
```
```
```
class_list = []  
with open("classes.txt", "r") as f:  
    class_list = [cname.strip() for cname in f.readlines()]  
  
colors = [(255, 255, 0), (0, 255, 0), (0, 255, 255), (255, 0, 0)]  
  
for i in range(len(result_class_ids)):  
  
    box = result_boxes[i]  
    class_id = result_class_ids[i]  
  
    color = colors[class_id % len(colors)]  
  
    conf  = result_confidences[i]  
  
    cv2.rectangle(image, box, color, 2)  
    cv2.rectangle(image, (box[0], box[1] - 20), (box[0] + box[2], box[1]), color, -1)  
    cv2.putText(image, class_list[class_id], (box[0] + 5, box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
```
```
```
```
```

05

**附加但重要（CUDA）**

运行计算机视觉需要大量的处理时间。通常即使是功能强大的 CPU 也不足以提供实时对象检测。配备 NVIDIA 卡的计算机可以使用其 **GPU** 通过 CUDA 来处理其代码。Opencv也支持**CUDA 调用**：

Python：

```
```
```
```
```
```
# load the model as usual  
net = cv2.dnn.readNet('yolov5s.onnx')  
  
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)  
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
```
```
```
```
```
```

C++:

```
```
```
```
```
```
auto net = cv::dnn::readNet("yolov5s.onnx");  
  
net.setPreferableBackend(cv::dnn::DNN_BACKEND_CUDA);  
net.setPreferableTarget(cv::dnn::DNN_TARGET_CUDA_FP16);
```
```
```
```
```
```

如果没有配备 NVIDIA 卡的计算机，代码将自动切换回 CPU 模式。如果有一台带有 NVIDIA 卡的计算机，但代码无法在 GPU 上运行，可能需要重新安装支持 CUDA 的 OpenCV。

> 结语

相关代码已开源，从上述代码可以看出，推理过程只依赖opencv和numpy,彻底摆脱了对深度学习框架的依赖，同时支持cuda，调用GPU，特别适合对资源要求很高的嵌入式设备，希望opencv持续给劲新的惊喜。

代码：*https://github.com/doleron/yolov5-opencv-cpp-python*

参考：

*[1]  https://zhuanlan.zhihu.com/p/172121380*

*[2]  https://github.com/ultralytics/yolov5/releases*

*[3]  https://github.com/opencv/opencv/blob/master/modules/dnn/src/onnx/onnx\_importer.cpp*

*[4]  https://zhuanlan.zhihu.com/p/449778377*

---

如果有任何困惑和疑问，欢迎进入公众号，添加微信号一起交流。

如果觉得写的内容对您有一点点启发和帮助，顺手再看![]()

如果有用 点个在看
