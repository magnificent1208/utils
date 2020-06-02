
#coding=utf-8
import  xml.dom.minidom
import os,sys
 
rootdir = 'DATASET_FOLDER/Annotations'#存有xml的文件夹路径
list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
## 空列表
classes_list = [] 
for i in range(0,len(list)):
   print(list[i])
   path = os.path.join(rootdir,list[i])
   if os.path.isfile(path):   
      #打开xml文档
      dom = xml.dom.minidom.parse(path)
 
      #得到文档元素对象
      root = dom.documentElement
      cc=dom.getElementsByTagName('name')
              
      for i in range(len(cc)):
         c1 = cc[i]
         #列表中不存在则存入列表
         if classes_list.count(c1.firstChild.data)==0:
            classes_list.append(c1.firstChild.data) 
         #print(c1.firstChild.data)
print(classes_list)
print(len(classes_list))

