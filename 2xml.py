import os
import shutil
import json
from jsonpath import jsonpath
import copy
from lxml.etree import Element, SubElement, tostring, ElementTree
import cv2
import numpy as np

template_file = './template.xml' # xml模板
target_dir = './new/Annotations/' #新标注文件保存路径
paired_img = './new/JPEGImages/' #与xml配对图像保存路径


for dir in os.walk('D:/datatset-jsxs'):

    for name in dir[1]:
        if os.path.isdir(name) and name != '.idea':
            print(name)
            with open(name+'/annotations/data0.json', 'r', encoding='utf8') as f:
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
                            arr = np.append(arr, [[loc['top'], loc['height'], loc['left'], loc['width'], label]],
                                            axis=0)

                            for i in range(arr.shape[0]):
                                if i == 0:
                                    label = arr[i, 4]  # 标签名
                                    # 坐标
                                    ymin = arr[i, 0]  # ymin = top
                                    ymax = str(int(ymin) + int(arr[i, 1]))  # ymax = top + height
                                    xmin = arr[i, 2]  # xmin = left
                                    xmax = str(int(xmin) + int(arr[i, 3]))

                                    tree.parse(template_file)  # 解析树
                                    root = tree.getroot()  # 根节点
                                    root.find('filename').text = file_name

                                    # size
                                    sz = root.find('size')
                                    im = cv2.imread(name + '/data/0/' + file_name)  # 读取图片信息

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
                                    ymin = arr[i, 0]  # ymin = top
                                    ymax = str(int(ymin) + int(arr[i, 1]))  # ymax = top + height
                                    xmin = arr[i, 2]  # xmin = left
                                    xmax = str(int(xmin) + int(arr[i, 3]))

                                    obj_ori = root.find('object')

                                    obj = copy.deepcopy(obj_ori)  # 注意这里深拷贝

                                    obj.find('name').text = label
                                    bb = obj.find('bndbox')
                                    bb.find('xmin').text = xmin
                                    bb.find('ymin').text = ymin
                                    bb.find('xmax').text = xmax
                                    bb.find('ymax').text = ymax
                                    root.append(obj)

                                xml_file = file_name.split('.')[0] + ".xml"
                                # if 'jsxs' in label
                                tree.write(target_dir + xml_file, encoding='utf-8')
                                shutil.copyfile(name + '/data/0/' + file_name, paired_img + file_name)
