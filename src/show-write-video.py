import cv2
import numpy as np

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'avc1')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter('./resource/demo.mp4', fourcc, 20, (width, height), True)

while True:
  rec, frame = cap.read()

  # print(frame)

  frame = cv2.flip(frame, 1)
  
  cv2.imshow('demo', frame)

  writer.write(frame)

  if cv2.waitKey(10) & 0xFF == 27:
    break

# 释放
writer.release()
cap.release()
cv2.destroyAllWindows()