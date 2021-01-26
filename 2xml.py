import os
import shutil
import json
from jsonpath import jsonpath
import copy
from lxml.etree import Element, SubElement, tostring, ElementTree
import cv2
import numpy as np
import threading

# BASE_PATH = r"E:/dataset/prj-m9p9jphvxtkgfghe"

template_file = './template.xml' # xml模板
target_dir = 'E:/dataset-jsxs/Annotations/' #新标注文件保存路径
paired_img = 'E:/dataset-jsxs/JPEGImages/' #与xml配对图像保存路径

def splitJSON(rootpath):
    with open(rootpath + '/data0.json', 'r', encoding='utf8') as f:
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
                    if label != 'jsxs':
                        continue
                    else:
                        arr = np.append(arr, [[loc['top'], loc['height'], loc['left'], loc['width'], label]], axis=0)
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
                                sz.find('height').text = str(anno['location']['height'])
                                sz.find('width').text = str(anno['location']['width'])
                                try:
                                    sz.find('depth').text = str(anno['location']['depth'])
                                except KeyError:
                                    # print(file_name + '无法找到depth标签，直接置为3')
                                    sz.find('depth').text = str(3)

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
                    tree.write(target_dir + xml_file, encoding='utf-8')
                    shutil.copyfile(rootpath + '/../data/0/' + file_name, paired_img + file_name)
            print('保存文件：'+ trainfiles['imageName'].split('.')[0] + ".xml")

def walkdir(BASE_PATH):
    for root, dirs, files in os.walk(BASE_PATH, topdown=False):
        print('正在执行 ' + root)
        if len(files) == 2 and files[0] == 'data0.json':
            data = json.load(open(root + '/labels.json', 'r', encoding='utf8'))
            label = []
            for dic in data:
                label.append(dic['labelName'])
            print(label)
            if 'jsxs' in label or 'jsxs\ ' in label:
                print('找到含锈蚀数据:' + root)
                splitJSON(root)
            else:
                continue
        else:
            continue



# 尝试多线程
th1 = threading.Thread(target=walkdir, args=(r'E:/dataset/prj-mfem9jnj2rhbzrea',))  ##创建线程
th1.start()  ##启动线程
th2 = threading.Thread(target=walkdir, args=(r'E:/dataset/prj-p1yxm4766e15utiw',))
th2.start()
th3 = threading.Thread(target=walkdir, args=(r'E:/dataset/prj-p2tj56uc62termgk',))
th3.start()
th4 = threading.Thread(target=walkdir, args=(r'E:/dataset/prj-s88ph50hieufwwzb',))
th4.start()
th5 = threading.Thread(target=walkdir, args=(r'E:/dataset/prj-vej3rcx7e3m72v6u',))
th5.start()
th6 = threading.Thread(target=walkdir, args=(r'E:/dataset/prj-ygaj3h3km66zfwdh',))
th6.start()
th7 = threading.Thread(target=walkdir, args=(r'E:/dataset/prj-yjjwpj31avp9m8q4',))
th7.start()