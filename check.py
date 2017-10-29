#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""feature detection."""

import cv2
import os
import numpy as np

IMG_DIR1 = os.path.abspath(os.path.dirname(__file__)) + '/downloads/'
IMG_SIZE = (200, 200)
sep = "//"

files1 = os.listdir(IMG_DIR1)

def checkFileNum( path ):
  ch = os.listdir( path )
  count = 0
  for c in ch:
    if os.path.isdir( path+c ):
      checkFileNum( path+c+sep )
    else:
      count += 1
  print("\n"+path+" : "+str(count)+" files" )
  return count
def checker(files,IMG_SIZE,IMG_DIR):
    f = 0
    counter = 0
    for file1 in files:
        a = []
        TARGET_FILE = file1
        target_img_path = IMG_DIR + TARGET_FILE
        target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
        target_img = cv2.resize(target_img, IMG_SIZE)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        # detector = cv2.ORB_create()
        detector = cv2.AKAZE_create()
        (target_kp, target_des) = detector.detectAndCompute(target_img, None)
        print('TARGET_FILE: %s' % (TARGET_FILE))
        for file in files:
            if file == '.DS_Store' or file == TARGET_FILE:
                a.append(0)
                continue
            comparing_img_path = IMG_DIR + file
            try:
                if f != 0:
                    break
                comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
                comparing_img = cv2.resize(comparing_img, IMG_SIZE)
                (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
                matches = bf.match(target_des, comparing_des)
                dist = [m.distance for m in matches]
                ret = sum(dist) / len(dist)
                if ret < 130:
                    a.append(1)
                else:
                    a.append(0)
            except cv2.error:
                try:
                    ret = 100000
                    print("エラーが出る画像ファイルを削除しました。\n")
                    os.remove(IMG_DIR + file)
                except FileNotFoundError:
                    f += 1
        if counter == 0:
            l = list(a)
        else:
            l1 = list(a)
            l = [x + y for (x, y) in zip(l, l1)]
        if f != 0:
            break

        counter += 1
    return f, l
errornum, ls = checker(files1,IMG_SIZE,IMG_DIR1)
n = 0
if errornum == 0:
    c = checkFileNum( IMG_DIR1 )
    c /= 3.5
    print("信頼基準数 = ",c)
    print("各画像の信頼度数 = ",ls)
    for number in ls:
        if number <= c:
            os.remove(IMG_DIR1 + files1[n])
        n += 1
else:
    IMG_DIR2 = os.path.abspath(os.path.dirname(__file__)) + '/downloads/'
    files2 = os.listdir(IMG_DIR2)
    print("画像ファイルの一致度を計算中")
    errornum, ls = checker(files2,IMG_SIZE,IMG_DIR2)
    c = checkFileNum( IMG_DIR2 )
    c /= 3.5
    print("\n信頼基準数 = ",c)
    print("各画像の信頼度数 = ",ls)
    for number in ls:
        if number <= c:
            os.remove(IMG_DIR2 + files2[n])
        n += 1
print("一致度の低い画像ファイルを削除しました。")
