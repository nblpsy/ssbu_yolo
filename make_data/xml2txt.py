#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs
import cv2
from glob import glob

XML_EXT = '.xml'
ENCODE_METHOD = 'utf-8'

class PascalVocReader:
    def __init__(self, filepath):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes = []
        self.filepath = filepath
        self.verified = False
        try:
            self.parseXML()
        except:
            pass

    def getShapes(self):
        return self.shapes

    def addShape(self, label, bndbox, filename, difficult):
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        self.shapes.append((label, points, filename, difficult))

    def parseXML(self):
        assert self.filepath.endswith(XML_EXT), "Unsupport file format"
        parser = etree.XMLParser(encoding=ENCODE_METHOD)
        xmltree = ElementTree.parse(self.filepath, parser=parser).getroot()
        filename = xmltree.find('filename').text
        path = xmltree.find('path').text
        try:
            verified = xmltree.attrib['verified']
            if verified == 'yes':
                self.verified = True
        except KeyError:
            self.verified = False

        for object_iter in xmltree.findall('object'):
            bndbox = object_iter.find("bndbox")
            label = object_iter.find('name').text
            # Add chris

            difficult = False
            if object_iter.find('difficult') is not None:
                difficult = bool(int(object_iter.find('difficult').text))
            self.addShape(label, bndbox, path, difficult)
        return True


classes = dict()
num_classes = 0

try:
    input = raw_input
except NameError:
    pass


parentpath = 'make_data/img/' #"Directory path with parent dir before xml_dir or img_dir"
addxmlpath = parentpath + 'xml_ano/right' #"Directory path with XML files"
addimgpath = parentpath + 'shot_right' #"Directory path with IMG files"
outputpath = parentpath + 'txt_ano' #"output folder for yolo format"
classes_txt = './classes.txt' #"File containing classes"
ext = '.jpg' #"Image file extension [.jpg or .png]"


if os.path.isfile(classes_txt):
    with open(classes_txt, "r") as f:
        class_list = f.read().strip().split()
        classes = {k : v for (v, k) in enumerate(class_list)}

xmlPaths = glob(addxmlpath + "/*.xml")
#imgPaths = glob(addimgpath + "/*"+ext)

for xmlPath in xmlPaths:
    tVocParseReader = PascalVocReader(xmlPath)
    shapes = tVocParseReader.getShapes()

    with open(outputpath + "/" + os.path.basename(xmlPath)[:-4] + ".txt", "w") as f:
        for shape in shapes:
            class_name = shape[0]
            box = shape[1]
            #filename = os.path.splittext(xmlPath)[0] + ext
            filename = os.path.splitext(addimgpath + "/" + os.path.basename(xmlPath)[:-4])[0] + ext

            if class_name not in classes.keys():
                classes[class_name] = num_classes
                num_classes += 1
            class_idx = classes[class_name]

            (height, width, _) = cv2.imread(filename).shape

            coord_min = box[0]
            coord_max = box[2]

            xcen = float((coord_min[0] + coord_max[0])) / 2 / width
            ycen = float((coord_min[1] + coord_max[1])) / 2 / height
            w = float((coord_max[0] - coord_min[0])) / width
            h = float((coord_max[1] - coord_min[1])) / height

            f.write("%d %.06f %.06f %.06f %.06f\n" % (class_idx, xcen, ycen, w, h))
            print(class_idx, xcen, ycen, w, h)

with open(parentpath + "classes.txt", "w") as f:
    for key in classes.keys():
        f.write("%s\n" % key)
        print(key)


# # パッケージのimport
# import os.path as osp
# import random
# # XMLをファイルやテキストから読み込んだり、加工したり、保存したりするためのライブラリ
# import xml.etree.ElementTree as ET

# import cv2
# import matplotlib.pyplot as plt
# import numpy as np
# import torch
# import torch.utils.data as data



# def make_datapath_list(rootpath):
#     """
#     データへのパスを格納したリストを作成する。

#     Parameters
#     ----------
#     rootpath : str
#         データフォルダへのパス

#     Returns
#     -------
#     ret : train_img_list, train_anno_list, val_img_list, val_anno_list
#         データへのパスを格納したリスト
#     """

#     # 画像ファイルとアノテーションファイルへのパスのテンプレートを作成
#     imgpath_template = osp.join(rootpath, 'JPEGImages', '%s.jpg')
#     annopath_template = osp.join(rootpath, 'Annotations', '%s.xml')

#     # 訓練と検証、それぞれのファイルのID（ファイル名）を取得する
#     train_id_names = osp.join(rootpath + 'ImageSets/Main/train.txt')
#     val_id_names = osp.join(rootpath + 'ImageSets/Main/val.txt')

#     # 訓練データの画像ファイルとアノテーションファイルへのパスリストを作成
#     train_img_list = list()
#     train_anno_list = list()

#     for line in open(train_id_names):
#         file_id = line.strip()  # 空白スペースと改行を除去
#         img_path = (imgpath_template % file_id)  # 画像のパス
#         anno_path = (annopath_template % file_id)  # アノテーションのパス
#         train_img_list.append(img_path)  # リストに追加
#         train_anno_list.append(anno_path)  # リストに追加

#     # 検証データの画像ファイルとアノテーションファイルへのパスリストを作成
#     val_img_list = list()
#     val_anno_list = list()

#     for line in open(val_id_names):
#         file_id = line.strip()  # 空白スペースと改行を除去
#         img_path = (imgpath_template % file_id)  # 画像のパス
#         anno_path = (annopath_template % file_id)  # アノテーションのパス
#         val_img_list.append(img_path)  # リストに追加
#         val_anno_list.append(anno_path)  # リストに追加

#     return train_img_list, train_anno_list, val_img_list, val_anno_list



# # ファイルパスのリストを作成
# rootpath = "make_data/img/label_img"
# train_img_list, train_anno_list, val_img_list, val_anno_list = make_datapath_list(
#     rootpath)

# # 動作確認
# print(train_img_list[0])





#########################################################
# import pandas as pd
# from lxml import etree

# def xml_to_dataframe(xml_file):
#     with open(xml_file) as f:
#         xml_data = f.read()
#     xml_tree = etree.XML(xml_data)
#     data = []
#     for item in xml_tree.iter():
#         data.append(item.attrib)
#     df = pd.DataFrame(data)
#     return df

# xml_file = ''
# for i in range(len())
# xml_to_dataframe(xml_file)

# ##########Please edit this section only.#######################################################################################################
 
# #  The paths must end with '/'.      
# absolutepath_of_directory_with_xmlfiles = 'make_data/img/xml_ano/left'  #　It is okay to have a mix of xml files and images in the same directory.
# absolutepath_of_directory_with_imgfiles = 'make_data/img/shot_left'
# absolutepath_of_directory_with_yolofiles = 'make_data/img/txt_ano'  # Yolo files will be created under this directory.
# absolutepath_of_directory_with_classes_txt = 'make_data/preprocessed/'  # You do not need to create classes.txt. classes.txt will be generated automatically.
# absolutepath_of_directory_with_error_txt = 'make_data/preprocessed/'  # The file names of files that do not have a paired xml or image file will be written to a text file under this directory.
 
# #####################################################################################################################################################
 
# import os
# import cv2
# from lxml import etree
# from xml.etree import ElementTree
# from glob import glob
 
 
# class GetDataFromXMLfile:
#     def __init__(self, xmlfile_path):
#         self.xmlfile_path = xmlfile_path
#         self.xmlfile_datalists_list = []
 
#     def get_datalists_list(self):
#         self.parse_xmlfile()
#         return self.xmlfile_datalists_list
 
#     def parse_xmlfile(self):
#         lxml_parser = etree.XMLParser(encoding='utf-8')
#         xmltree = ElementTree.parse(self.xmlfile_path, parser=lxml_parser).getroot()
 
#         for object in xmltree.findall('object'):
#             xmlfile_datalist = []
#             class_name = object.find('name').text
#             xmlfile_datalist.append(class_name)
#             bndbox = object.find("bndbox")
#             xmlfile_datalist.append(bndbox)
#             self.xmlfile_datalists_list.append(xmlfile_datalist)
 
#         img_filename = xmltree.find('filename').text
        
#         self.add_data_to_datalist(img_filename)
    
#     def add_data_to_datalist(self, img_filename):
#         for xmlfile_datalist in self.xmlfile_datalists_list:
#             xmin = float(xmlfile_datalist[1].find('xmin').text)
#             ymin = float(xmlfile_datalist[1].find('ymin').text)
#             xmax = float(xmlfile_datalist[1].find('xmax').text)
#             ymax = float(xmlfile_datalist[1].find('ymax').text)
#             bndbox_coordinates_list = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
#             xmlfile_datalist[1] = bndbox_coordinates_list
#         self.xmlfile_datalists_list.append(img_filename)
#         self.xmlfile_datalists_list.append(self.xmlfile_path)
 
 
# class CreateYOLOfile:
#     def __init__(self, xmlfile_datalists_list, classes_list):
#         self.xmlfile_datalists_list = xmlfile_datalists_list
#         self.xmlfile_path = self.xmlfile_datalists_list.pop()
#         self.img_filename = self.xmlfile_datalists_list.pop()
#         self.yolofile_path = absolutepath_of_directory_with_yolofiles + os.path.basename(self.xmlfile_path).split('.', 1)[0] + '.txt'
#         self.classes_list = classes_list
#         try:
#             (self.img_height, self.img_width, _) = cv2.imread(absolutepath_of_directory_with_imgfiles + self.img_filename).shape
#             self.create_yolofile()
#         except:
#             with open(absolutepath_of_directory_with_error_txt+'xmlfiles_with_no_paired.txt', 'a') as f:
#                 f.write(os.path.basename(self.xmlfile_path)+'\n')
 
#     def create_yolofile(self):
#         for xmlfile_datalist in self.xmlfile_datalists_list:
#             yolo_datalist = self.convert_xml_to_yolo_format(xmlfile_datalist)
 
#             with open(self.yolofile_path, 'a') as f:
#                 f.write("%d %.06f %.06f %.06f %.06f\n" % (yolo_datalist[0], yolo_datalist[1], yolo_datalist[2], yolo_datalist[3], yolo_datalist[4]))
 
#     def convert_xml_to_yolo_format(self, xmlfile_datalist):
#         class_name = xmlfile_datalist[0]
#         self.add_class_to_classeslist(class_name)
#         bndbox_coordinates_list = xmlfile_datalist[1]
#         coordinates_min = bndbox_coordinates_list[0]
#         coordinates_max = bndbox_coordinates_list[2]
 
#         class_id = self.classes_list.index(class_name)
#         yolo_xcen = float((coordinates_min[0] + coordinates_max[0])) / 2 / self.img_width
#         yolo_ycen = float((coordinates_min[1] + coordinates_max[1])) / 2 / self.img_height
#         yolo_width = float((coordinates_max[0] - coordinates_min[0])) / self.img_width
#         yolo_height = float((coordinates_max[1] - coordinates_min[1])) / self.img_height
#         yolo_datalist = [class_id, yolo_xcen, yolo_ycen, yolo_width, yolo_height]
 
#         return yolo_datalist
    
#     def add_class_to_classeslist(self, class_name):
#         if class_name not in self.classes_list:
#             self.classes_list.append(class_name)
 
 
# class CreateClasssesfile:
#     def __init__(self, classes_list):
#         self.classes_list = classes_list
 
#     def create_classestxt(self):
#         with open(absolutepath_of_directory_with_classes_txt + 'classes.txt', 'w') as f:
#             for class_name in self.classes_list:
#                 f.write(class_name+'\n')
 
 
# xmlfiles_pathlist = glob(absolutepath_of_directory_with_xmlfiles + "/*.xml")
# classes_list = []
 
# for xmlfile_path in xmlfiles_pathlist:
#     process_xmlfile = GetDataFromXMLfile(xmlfile_path)
#     xmlfile_datalists_list = process_xmlfile.get_datalists_list()
#     CreateYOLOfile(xmlfile_datalists_list, classes_list)
 
# process_classesfile = CreateClasssesfile(classes_list)
# process_classesfile.create_classestxt()