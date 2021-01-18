# coding:utf-8
'''
json拆分处理：https://blog.csdn.net/Strive_For_Future/article/details/107564274
json to xml 处理： https://blog.csdn.net/qq_44315987/article/details/106207971

旧图像文件夹：./data/0/
旧标签文件：./annotations/data0
拆分后json标签文件：./new_annotations

xml模板: ./template.xml
处理好的VOC格式数据集标签： ./xml/Annotations
与标签配对的图片地址： ./xml/JPEGImages
'''
import os
import shutil
import json
from jsonpath import jsonpath
import copy
from lxml.etree import Element, SubElement, tostring, ElementTree
import cv2
import numpy as np


template_file = './template.xml' # xml模板

image_dir = './data/0/'  # 旧图像文件夹
train_file = './annotations/data0.json'  # 存储了全部图片信息的json文件

target_dir = './xml/Annotations/' #新标注文件保存路径
paired_img = './xml/JPEGImages/' #与xml配对图像保存路径


#------------------------------------------break down json file
# def save_json(save_path,data):
#     assert save_path.split('.')[-1] == 'json'
#     with open(save_path,'w') as file:
#         json.dump(data,file)

# with open('annotations/data0.json', 'r', encoding='utf8') as f:
#     for line in f.readlines():
#         dic = json.loads(line)
#         print(dic['imageName'].split('.')[0])
#         save_json("./new_annotations/"+dic['imageName'].split('.')[0]+".json",dic)


#------------------------------------------json to xml
with open('annotations/data0.json', 'r', encoding='utf8') as f:
    for line in f.readlines():
        trainfiles = json.loads(line)
        tree = ElementTree()
        for k in enumerate(trainfiles):
            annos = trainfiles['annotations']
            file_name = trainfiles['imageName']
            arr = np.empty([0, 5], int)
            for anno in annos:
                loc = anno['location']
                label = anno['labelName']
                # label = labels[anno['labelName']]
                arr = np.append(arr, [[loc['top'], loc['height'], loc['left'], loc['width'], label]], axis=0)


                for i in range(arr.shape[0]):
                    if i == 0:
                        label = arr[i, 4]  # 标签名
                        # 坐标
                        ymin = arr[i,0] #ymin = top
                        ymax = str(int(ymin) + int(arr[i,1]))  #ymax = top + height
                        xmin = arr[i,2] #xmin = left
                        xmax = str(int(xmin) + int(arr[i,3]))

                        tree.parse(template_file)  # 解析树
                        root = tree.getroot()  # 根节点
                        root.find('filename').text = file_name

                        # size
                        sz = root.find('size')
                        im = cv2.imread(image_dir + file_name)  # 读取图片信息

                        sz.find('height').text = str(im.shape[0])
                        sz.find('width').text = str(im.shape[1])
                        sz.find('depth').text = str(im.shape[2])

                        # object
                        obj = root.find('object')
                        obj.find('name').text = label
                        bb = obj.find('bndbox')
                        bb.find('xmin').text = xmin
                        bb.find('ymin').text = ymin
                        bb.find('xmax').text = xmax
                        bb.find('ymax').text = ymax

                        # 有多个标签需要添加object
                    else:
                        label = arr[i, 4]  # 标签名
                        # 坐标
                        ymin = arr[i,0] #ymin = top
                        ymax = str(int(ymin) + int(arr[i,1]))  #ymax = top + height
                        xmin = arr[i,2] #xmin = left
                        xmax = str(int(xmin) + int(arr[i,3]))

                        obj_ori = root.find('object')

                        obj = copy.deepcopy(obj_ori)  # 注意这里深拷贝

                        obj.find('name').text = label
                        bb = obj.find('bndbox')
                        bb.find('xmin').text = xmin
                        bb.find('ymin').text = ymin
                        bb.find('xmax').text = xmax
                        bb.find('ymax').text = ymax
                        root.append(obj)

                    xml_file = file_name.split('.')[0]+".xml"
                    # if 'jsxs' in label
                    tree.write(target_dir + xml_file, encoding='utf-8')
                    shutil.copyfile(image_dir + file_name , paired_img + file_name)
