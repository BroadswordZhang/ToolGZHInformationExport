---
标题: "kaggle 面部关键点检测的实战总结"
公众号名称: "张大刀修炼手册"
作者: "张大刀修炼手册"
发布时间: "2022-03-10 22:42:47"
原文链接: "https://mp.weixin.qq.com/s/IfVkEh_p_mACAsNiV1IVbg"
文章详情_分享类型: "0"
文章ID: "2247483737"
是否已删除: "False"
版权状态: "100"
版权类型: "0"
阅读量: "206"
喜欢数: "3"
文章详情_投票ID: "[]"
文章详情_超级投票ID: "[]"
文章详情_封面图片: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibF0hITpwx5TO8yxASLIGiahYzUW1khn4MWfZsPkFe3RDhT2ia2H49KbMa1uaPsQIrJEOibs4QQ5xreOA/0?wx_fmt=jpeg"
文章详情_智能产品信息: "0"
文章详情_修改状态: "1"
文章详情_互动类型: "2"
文章详情_可删除状态: "0"
点赞数: "8"
图文序号: "1"
文章详情_是否付费订阅: "0"
文章详情_是否来自转移: "0"
文章详情_公开标签信息: "{\"public_tag_list\": [], \"modify_times\": 0, \"init_tag_list_size\": 0}"
文章详情_文章合集信息: "{\"appmsg_album_infos\": []}"
文章详情_是否开启粉丝留言: "0"
文章详情_是否处于冷却状态: "0"
文章详情_2.35比1封面地址: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibF0hITpwx5TO8yxASLIGiahY4TSAChaH0kLs76boPBDUx5Snn669kMCSm2CZCRbyYTeMX8Na5ziaqicQ/0?wx_fmt=jpeg"
文章详情_16比9封面地址: "https://mmbiz.qlogo.cn/mmbiz_jpg/xH40kQxnnibF0hITpwx5TO8yxASLIGiahY4TSAChaH0kLs76boPBDUx5Snn669kMCSm2CZCRbyYTeMX8Na5ziaqicQ/0?wx_fmt=jpeg"
文章详情_是否禁止推荐: "0"
文章详情_发布线路信息: "{\"use_line\": 1, \"line_count\": 0, \"send_time\": 1646923367, \"is_appmsg_flag\": 1, \"is_use_flag\": 0}"
文章详情_来源声明类型: "0"
分享量: "4"
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
发布消息ID: "1000000009"
发布类型: "101"
发送状态: "{\"total\": 8, \"succ\": 8, \"fail\": 0, \"progress\": 100, \"userprotect\": 0}"
发布结果: "{\"msg_status\": 2, \"refuse_reason\": \"\", \"reject_index_list\": [], \"update_time\": 1752674458}"
是否新发布: "0"
文章详情_发布复制类型: "77"
文章详情_发布复制文章ID: "100000088"
文章分析_统计错误: "analysis page parsing failed"
---

# kaggle 面部关键点检测的实战总结

**“** 本文以kaggle比赛中的人脸面部检测为实例，通过比赛，总结出数据分析、模型以及各种思考思路，主要以数据增强为主**”**

由于深度神经网络 (DNN) 具有大量可学习参数，因此需要大量标记数据来完成我们手头的任务。**数据增强**是增加标记训练数据多样性的一种常见方式。Andrew Ng 曾提到，在计算机视觉中，数据总是越多越好。图像增强也成为一种常见的隐式正则化技术，用于解决 DNN 中的过拟合问题。通常在图像增强中，我们使用翻转、旋转、缩放等的组合，但在关键点检测任务中，还需要将关键点与图像一起增强。所以这篇文章是关于如何在关键点检测任务中增加训练数据的实战总结。文章末尾提供了包含训练 DNN 的完整链接。

**|**面部关键点数据

* 先登录kaggle官网，进入脸部关键点检测竞赛页面，先下载数据：

https://www.kaggle.com/c/facial-keypoints-detection/leaderboard

![]()

先观察下载的数据，这里的关键点是由像素点索引空间中的(x,y) 指定。

> ‍left\_eye\_center，right\_eye\_center，left\_eye\_inner\_cor，
>
> left\_eye\_outer\_cor，right\_eye\_inner\_cor，
>
> right\_eye\_outer\_cor，left\_eyebrow\_inner\_end，
>
> left\_eyebrow\_outer\_end，right\_eyebrow\_inner\_end，
>
> right\_eyebrow\_outer\_end，nose\_tip，mouth\_left\_cor，
>
> mouth\_right\_cor，mouth\_center\_top\_lip，mouth\_center\_bottom\_lip



加载数据

```
train_read = pd.read_csv(data_path + '/training.csv', sep=',')print ('training data shape; ', train_read.shape)>>> training data shape;  (7049, 31)
```

训练数据中有 7049 张图像，但问题是数据集中有很多空值。仔细检查数据发现在 31 列中，除了 'nose\_tip\_x'、'nose\_tip\_y' 和 'Image' 列之外，所有列都有空值。我们先看下数据的分布:

![]()

关键点遵循正态分布，这里可以采用将 NaN 条目替换为分布均值。对于数据插补，从 ML角度看，需先将数据拆分为训练测试，再进行转换，否则容易导致数据泄漏。而在 Colab 中训练一个包含 7049 幅图像 + 增强图像的网络非常耗时，所以在这里决定只使用干净的数据。

```
train_clean = train_read.dropna(axis=0, how=’any’, inplace=False)train_clean = train_clean.reset_index(drop=True)print (‘data-frame shape with no null values: ‘, train_clean.shape)>>> data-frame shape with no null values:  (2140, 31)
```

使用干净的数据会大大减少训练规模（从 7049 幅图像减少到 2140 幅），而后再进行数据增强将非常方便。但在增强之前，需要做更多的处理。image 列包含像素值作为字符串，中间有空格。

```
clean_imgs = []for i in range(0, len(train_clean)):x_c = train_clean[‘Image’][i].split(‘ ‘) # split the pixel values based on the spacex_c = [y for y in x_c] # create the listed pixelsclean_imgs.append(x_c)clean_imgs_arr = np.array(clean_imgs, dtype=’float’) clean_imgs_arr = np.reshape(clean_imgs_arr, (train_clean.shape[0], 96, 96, 1))train_ims_clean = clean_imgs_arr/255。# 缩放图像
```

获取数据并可视化：

```
clean_keypoints_df = train_clean.drop('Image', axis=1)clean_keypoints_arr = clean_keypoints_df.to_numpy()
```

```
def vis_im_keypoint_notstandard(img, points, axs):  axs.imshow(img.reshape(96, 96))  xcoords = (points[0::2] + 0.)  ycoords = (points[1::2] + 0.)  axs.scatter(xcoords, ycoords, color='red', marker='o')
```

**|**面部关键点数据增强

## 线性对比度和高斯模糊

```
import imgaug as iaimport imgaug.augmenters as iaa  
def gnoise_lincontrast(im_tr, pt_tr):  seq = iaa.Sequential([iaa.LinearContrast((0.6, 1.5)),                         iaa.Sometimes(        0.80, iaa.GaussianBlur(sigma=(0., 2.0)))])  aug_ims = []  aug_pts = []  for im, pt in zip(im_tr, pt_tr):    f_im = seq(image=im)    aug_ims.append(im)    aug_ims.append(f_im)    aug_pts.append(pt)    aug_pts.append(pt)  return np.asarray(aug_ims), np.asarray(aug_pts)  
aug_ims_train_clean_g, aug_points_train_clean_g = gnoise_lincontrast(train_ims_clean, clean_keypoints_arr)
```

LinearContrast用于修改图像的对比度，GaussianBlur增强器用于使用高斯核模糊图像，sigma是高斯核的标准差，随机对 80% 的图像做高斯模糊。 将原始图像和增强图像可视化如下 --

![]()

## 缩放和旋转图像和关键点

## 为了数据集中包含旋转和缩放的图像，还需要相应地更改关键点。在这个问题中不建议使用Keras ImageDataGenerator类。Imgaug 库在这里非常方便。代码块分享如下 -

```
# include rotation augmentation   
from imgaug.augmentables import Keypoint, KeypointsOnImage  
def rotate_aug(im_tr, pt_tr):  seq = iaa.Sequential([iaa.Affine(rotate=15, scale=(0.8, 1.2))])  aug_ims = []  aug_pts = []  coordlist = []  for im, pt in zip(im_tr, pt_tr):    xcoord = pt[0::2]    ycoord = pt[1::2]    for i in range(len(xcoord)):       coordlist.append(Keypoint(xcoord[i], ycoord[i]))    kps = KeypointsOnImage(coordlist, shape=im.shape)      f_im, f_kp = seq(image=im, keypoints=kps)    all_coords = []    for k in range(len(kps.keypoints)):      before = kps.keypoints[k]      after = f_kp.keypoints[k]      all_coords.append(after.x)      all_coords.append(after.y)      all_coords_arr = np.asarray(all_coords)    aug_ims.append(im)    aug_ims.append(f_im)    aug_pts.append(pt)    aug_pts.append(all_coords)    coordlist.clear()  return np.asarray(aug_ims), np.asarray(aug_pts)    aug_ims_train_clean_g2, aug_points_train_clean_g2 = rotate_aug(aug_ims_train_clean_g, aug_points_train_clean_g)
```

定义由旋转和缩放图像组成的增强序列Sequential，旋转角度设置为0到15 度的随机值，缩放范围设置为原始图像的 80% 到 120%之间随机值。可视化结果如下——

![]()

## 水平翻转：图像和关键点：

## 图像的水平翻转numpy fliplr；对于关键点，水平翻转中，y 坐标不变，但 x 坐标改变。由于图像的维度是 (96, 96)，我们通过 (96-x) 得到翻转的 x 点。下面是代码块——

```
def flip_im_points0(img, points):   flip_im = np.fliplr(img)  xcoords = points[0::2]  ycoords = points[1::2]  new_points = []  for i in range(len(xcoords)):    xp = xcoords[i]    yp = ycoords[i]    new_points.append(96-xp)    new_points.append(yp)  return flip_im, np.asarray(new_points)   
def aug_flip0(im_tr, pt_tr):  aug_ims = []  aug_pts = []  for im, pt in zip(im_tr, pt_tr):    f_im, f_pts = flip_im_points0(im, pt)    aug_ims.append(im)    aug_ims.append(f_im)    aug_pts.append(pt)    aug_pts.append(f_pts)  return np.asarray(aug_ims), np.asarray(aug_pts)  
aug_ims_train_clean_g3, aug_points_train_clean_g3 = aug_flip0(aug_ims_train_clean_g2,                                                          aug_points_train_clean_g2)### visualization part: fig = plt.figure(figsize=(13, 10))npics= 24count = 1for i in range(npics):  ipic = i # use this to see original and augmented image side by side#   ipic = np.random.choice(aug_ims_train_clean.shape[0])  ax = fig.add_subplot(npics/4 , 6, count, xticks=[],yticks=[])  vis_im_keypoint_notstandard(aug_ims_train_clean_g3[ipic], aug_points_train_clean_g3[ipic], ax)  count = count + 1  plt.margins(0,0)plt.gca().xaxis.set_major_locator(plt.NullLocator())plt.gca().yaxis.set_major_locator(plt.NullLocator())plt.tight_layout()  
plt.savefig(data_path+'/aug_ims_kps_flip_h.png', bbox_inches = 'tight', pad_inches = 0, dpi=200)plt.show()
```

综上，将数据集从 2140 张图扩增到 17120 张。部分图像如下——

![]()

对数据随机shuffle:

```
from sklearn.utils import shuffleaug_ims_train_final, aug_points_train_final = shuffle(aug_ims_train_clean_g3, aug_points_train_clean_g3)
```

**|****面部关键点检测训练**

数据增强后我们现在开始构建 DNN 模型并准备训练。将原始 InceptionV3 结构简化，神经网络结构如下。

![]()

添加‘callbacks’类：

```
class customCallbacks(tf.keras.callbacks.Callback):  def on_epoch_end(self, epoch, logs=None):    self.epoch = epoch + 1    if self.epoch % 50 == 0:      print ('epoch num {}, train acc: {}, validation acc:                      {}'.format(epoch, logs['mae'], logs['val_mae']))reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_mae', factor=0.8,                              patience=25, min_lr=1e-5, verbose=1)
```

开始训练拟合模型：

```
face_key_model2_aug.compile(loss='mse',                        optimizer=Adam(learning_rate=3e-3),                        metrics=['mae'])face_key_model2_aug_train_clean = face_key_model2_aug.fit(aug_ims_train_final, aug_points_train_final,                                                   validation_split= 0.05,                                                   batch_size=64, epochs=300,                                                   callbacks=[customCallbacks(), reduce_lr],                                           verbose=0)
```

训练验证曲线如下：

![]()

**|**面部关键点检测测试

下一步是预测测试图像的关键点——

```
predict_points_aug2_clean = face_key_model2_aug.predict(test_ims)  
print ('check shape of predicted points: ', predict_points_aug2_clean.shape)>>> check shape of predicted points:  (1783, 30)
```

有 1783 张测试图像，对预测结果的部分图片可视化 -

```
fig = plt.figure(figsize=(10, 8))npics= 12count = 1for i in range(npics):  # ipic = i  ipic = np.random.choice(test_ims.shape[0])  ax = fig.add_subplot(npics/3 , 4, count, xticks=[],yticks=[])  vis_im_keypoint_notstandard(test_ims[ipic], predict_points_aug2_clean[ipic], ax)  count = count + 1  
  
plt.tight_layout()plt.savefig(data_path+'/prediction_keypoints.png', dpi=200, bbox_inches = 'tight', pad_inches = 0)plt.show()
```

![]()

**|****总结**

这篇文章介绍kaggle竞赛中人脸关键点检测实战，这里更专注于数据增强部分，并给与相关思路和代码。整个代码 如下：

> https://github.com/suvoooo/Learn-TensorFlow/blob/master/Facial\_Keypoint\_Kaggle.ipynb
>
> github地址

![]()
