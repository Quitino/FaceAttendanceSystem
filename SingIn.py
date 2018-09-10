# -*- coding: UTF-8 -*-
import face_recognition
import cv2
import os
import datetime
import time
from ft2 import put_chinese_text

print("欢迎使用人脸签到系统")
video_capture = cv2.VideoCapture(1)# 摄像头
print"摄像头读取完毕"
path ="face_data"# 在同级目录下的face_data文件中放需要被识别出的人物图
total_image=[]
total_image_name=[]
total_face_encoding=[]
singed=[]
name_of_sing_in=[]
name_of_unsing_in=[]
time_of_sing_in=[]
flag="wait"
def loadface():# 加载图片函数
  num=0
  del total_image_name[:]
  del name_of_sing_in[:]
  del name_of_unsing_in[:]
  del time_of_sing_in[:]
  for fn in os.listdir(path): #fn 表示的是文件名
      num+=1
      print "正在读取第%d个人脸数据\n" % num
      total_face_encoding.append(face_recognition.face_encodings(face_recognition.load_image_file(path+"/"+fn))[0])
      fn=fn[:(len(fn)-4)]#截取图片名（这里应该把face_data文件中的图片名命名为为人物名）
      total_image_name.append(fn)#图片名字列表
      name_of_unsing_in.append(fn)
      print"读取成功\n"
  print"读取完毕"
print("正在启动...")
loadface()
os.system("clear")
print"{0:=^30}".format("=")
print '{0:=^36}'.format("人脸签到系统")
print"{0:=^30}".format("=")
NotFirstPrint=0
now_time = datetime.datetime.now()
OpenTime = datetime.datetime.strftime(now_time,'%Y-%m-%d_%H:%M:%S')
os.system("mkdir ./sing_in_image/%s"%OpenTime)
times_of_find=0
while True:
  if times_of_find==20:
      print"寻找人脸超时"
      flag="wait"
      times_of_find=0
  while flag!="SingIn":
      print"\n"
      print "{0:=^35}".format("系统已暂停")
      print"{0:=^30}".format("=")
      print"{0: ^36}".format("输入SingIn开始签到")
      print"{0: ^36}".format("see查询签到情况")
      print"{0: ^38}".format("load重新读取人脸数据")
      print"{0: ^40}".format("  all查询已注册人脸签到的人员")
      print"{0: ^36}".format("其他指令无效")
      print"{0:=^30}".format("=")
      flag=raw_input()
      os.system("clear")
      print"{0:=^30}".format("=")
      print '{0:=^36}'.format("人脸签到系统")
      print"{0:=^30}".format("=")
      if flag=="exit" or flag=="load" or flag=="see" or flag=="all":
          break
  if flag=="load":
      print"正在重新读取人脸数据"    
      loadface()
      flag=="wait"
      continue
  if flag=="exit":
      print("系统已退出")
      break
  if flag=="all":
     flag="wait"
     print"\n"
     print"{0:=^36}".format("已注册人员：")
     for names in total_image_name:
         print"{0: ^32}".format("%s"%names)
     continue
  if flag=="see":
      flag="wait"
      print"\n"
      print"{0:=^36}".format("今日已签到：")
      print"\n"
      for names,times,number in zip( name_of_sing_in,time_of_sing_in,range( len(name_of_sing_in) ) ):
          print"{0: ^4}".format("%d"%(number+1)),
          print"{0: ^10}".format("%s"%names),
          print"{0: ^5}".format("已在%s"%times),
          print"{0: ^5}".format("签到")
      print"\n"
      print"{0:=^36}".format("今日未签到：")
      for names in name_of_unsing_in:
          print"{0: ^32}".format("%s"%names)
      continue
  if NotFirstPrint==0:
      print "程序已启动，请将脸对准摄像头"
      NotFirstPrint=1
  # 抓取一帧视频
  ret, frame = video_capture.read()
  times_of_find+=1
  print"正在尝试寻找人脸..."
  # 在这个视频帧中循环遍历每个人脸
  face_locations = face_recognition.face_locations(frame)
  name = "Unknown"
  if face_locations!=[]:
      print "已检测到人脸，正在识别..."
      NotFirstPrint=0
      face_encoding = face_recognition.face_encodings(frame)[0]# 只要第一张脸
  #for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
      # 判断面部是否与已知人脸相匹配。
      for i,v in enumerate(total_face_encoding):
          match = face_recognition.compare_faces([v], face_encoding,tolerance=0.5)#阈值
          if match[0]:
              name = total_image_name[i]
              break
 
  else:
      continue
      #putText无法显示中文
      #font = cv2.FONT_HERSHEY_DUPLEX
      #cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
  # 显示结果图像
  if name=="Unknown":
      print "未知人脸，请按回车重试"
      raw_input()
      flag="wait"
      print"请稍候..."
      time.sleep(2)
      os.system("clear")
      print"{0:=^30}".format("=")
      print '{0:=^36}'.format("人脸签到系统")
      print"{0:=^30}".format("=")
  elif i in singed:
      print "  %s  今日已签到，请勿重复签到"%name
      flag="wait"
  else:
      singed.append(i)
      now_time = datetime.datetime.now()
      time_str = datetime.datetime.strftime(now_time,'%Y-%m-%d %H:%M:%S')
      with open('sing_in.txt', 'a') as f:#签到信息保存至sing_in.txt中
           f.write('  %s  已在  %s  完成签到\n'%(name,time_str)) 
      cv2.imwrite("sing_in_image/%s/%s%s.jpg"%(OpenTime,name,time_str), frame)
      name_of_sing_in.append(name)
      time_of_sing_in.append(time_str)
      name_of_unsing_in.remove(name)
      # 框出人脸
      (top, right, bottom, left)=face_locations[0]
      left=left
      right=right
      top=top
      bottom=bottom
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


      cv2.namedWindow('%s'%name)
      cv2.imshow('%s'%name,frame)
      print "%s已签到，图像界面中按“Q”继续" %name
      cv2.waitKey(0)#waitKey后显示图像
      cv2.destroyAllWindows()  
      flag="wait"
      os.system("clear")
      print"{0:=^30}".format("=")
      print '{0:=^36}'.format("人脸签到系统")
      print"{0:=^30}".format("=")
  if flag=="exit":
      os.system("clear")
      break
# 释放摄像头中的流
video_capture.release()
cv2.destroyAllWindows()
print"摄像头已关闭"
print"系统已退出"
