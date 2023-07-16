import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

start_time = time.time()

while True:
  rec, frame = cap.read()

  frame = cv2.flip(frame, 1)

  # cv2.circle(img=frame,center=(300,300),radius=100,color=(0,0,255),thickness=10)

  current_time = time.time()
  frame_rate = int(1/(current_time - start_time))
  start_time= current_time
  
  cv2.putText(frame,  'frame rate:'+str(frame_rate), (80, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

  cv2.imshow('demo', frame)



  if cv2.waitKey(10) & 0xFF == 27:
    break

cap.release()
cv2.destroyAllWindows()