# -*- coding: UTF-8 -*-   
import face_recognition   
import cv2   
import os   
import ft2   
#中文支持,加载微软雅黑字体  
ft = ft2.put_chinese_text('msyh.ttf')    
# 获取摄像头# 0（默认）   
video_capture = cv2.VideoCapture(0)   
# 加载待识别人脸图像并识别。   
basefacefilespath ="images"#faces文件夹中放待识别任务正面图,文件名为人名,将显示于结果中  
baseface_titles=[] #图片名字列表  
baseface_face_encodings=[] #识别所需人脸编码结构集  
#读取人脸资源  
for fn in os.listdir(basefacefilespath): #fn 人脸文件名  
    baseface_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(basefacefilespath+"/"+fn))[0])   
    fn=fn[:(len(fn)-4)]   
    baseface_titles.append(fn)#   
while True:   
    # 获取一帧视频   
    ret, frame = video_capture.read()   
    # 人脸检测,并获取帧中所有人脸编码  
    face_locations = face_recognition.face_locations(frame)   
    face_encodings = face_recognition.face_encodings(frame, face_locations)   
    # 遍历帧中所有人脸编码   
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):   
        # 与baseface_face_encodings匹配否?   
        for i,v in enumerate(baseface_face_encodings):   
            match = face_recognition.compare_faces([v], face_encoding,tolerance=0.5)   
            name = "?"   
            if match[0]:   
                name = baseface_titles[i]   
                break   
        name=unicode(name,'gb2312')#gbk is also ok.  
        print(name)  
        # 围绕脸的框   
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)   
        # 框下的名字(即,匹配的图片文件名)  
        cv2.rectangle(frame, (left, bottom), (right, bottom+35), (0, 0, 255), cv2.FILLED)   
        frame = ft.draw_text(frame, (left + 2, bottom + 12), name, 16,  (255, 255, 255))    
        # show结果图像   
        cv2.imshow('Video', frame)   
    # 按q退出   
    if cv2.waitKey(1) & 0xFF == ord('q'):   
        break   
# 释放摄像头中的流   
video_capture.release()   
cv2.destroyAllWindows()  
