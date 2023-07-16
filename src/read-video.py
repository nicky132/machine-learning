import cv2
import numpy as np 

cap = cv2.VideoCapture('./resource/demo.mp4')

if not cap.isOpened():
  print('文件不存在或者编码错误')

while True:
  ret, frame = cap.read()

  if not ret:
     break

  cv2.imshow('demo', frame)

  if cv2.waitKey(10) & 0xFF == 27:
    break

# 释放
cap.release()
cv2.destroyAllWindows()
