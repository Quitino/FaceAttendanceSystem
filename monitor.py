# -*- coding: UTF-8 -*-
import numpy as np
import freetype
import copy
import pdb
import face_recognition
import cv2
import os
from ft2 import put_chinese_text
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# 请注意：这个例子需要安装OpenCV
# 得到一个参考的摄像头# 0（默认）
video_capture = cv2.VideoCapture(1)
# 加载示例图片并学习如何识别它。
path ="face_data"#在同级目录下的face_data文件中放需要被识别出的人物图
total_image=[]
total_image_name=[]
total_face_encoding=[]
for fn in os.listdir(path): #fn 表示的是文件名
  total_face_encoding.append(face_recognition.face_encodings(face_recognition.load_image_file(path+"/"+fn))[0])
  fn=fn[:(len(fn)-4)]#截取图片名（这里应该把face_data文件中的图片名命名为为人物名）
  total_image_name.append(fn)#图片名字列表
while True:
  # 抓取一帧视频
  ret, frame = video_capture.read()
  frame=cv2.resize(frame, (0,0), fx=0.5, fy=0.5)#缩放，减少计算量
  # 发现在视频帧所有的脸和face_enqcodings
  face_locations = face_recognition.face_locations(frame)
  face_encodings = face_recognition.face_encodings(frame, face_locations)
  # 在这个视频帧中循环遍历每个人脸
  if face_locations==[]:
      frame=cv2.resize(frame, (0,0), fx=2, fy=2)
  for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
      # 看看面部是否与已知人脸相匹配。
      for i,v in enumerate(total_face_encoding):
          match = face_recognition.compare_faces([v], face_encoding,tolerance=0.5)
          name = "Unknown"
          if match[0]:
              name = total_image_name[i]
              break
      if len(face_locations)==1:
          frame=cv2.resize(frame, (0,0), fx=2, fy=2)
      # 画出一个框，框住脸
      left=left*2-10
      right=right*2+10
      top=top*2-10
      bottom=bottom*2+10
      cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
      # 画出一个带名字的标签，放在框下
      cv2.rectangle(frame, (left, bottom + 35), (right, bottom), (0, 0, 255), cv2.FILLED)
      
      line = name
 
      color = (255, 255, 255)
      pos = (left + 40, bottom+5)
      text_size = 25
 
      # ft = put_chinese_text('wqy-zenhei.ttc')
      ft = put_chinese_text('/home/nvidia/.local/share/fonts/KaiTi_GB2312.ttf')
      frame = ft.draw_text(frame, pos, line, text_size, color)
 


      #font = cv2.FONT_HERSHEY_DUPLEX
      #cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
  # 显示结果图像
  cv2.imshow('人脸识别系统', frame)
  # 按q退出
  if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  #p暂停，c恢复
  elif cv2.waitKey(1) & 0xFF == ord('p'):
      while True:
          if cv2.waitKey(1) & 0xFF == ord('c'):
              break

# 释放摄像头中的流
video_capture.release()
cv2.destroyAllWindows()
