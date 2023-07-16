import cv2
import numpy as np
import math

import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

cap_window_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cap_window_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 食指在骨骼点数组中的下标
index_finger_subscript = 8

# 中指在骨骼点数组中的下标
index_middle_subscript = 12

# 食指在窗口中的坐标
index_finger_x = 0
index_finger_y = 0

# 中指在窗口中的坐标
middle_finger_x = 0
middle_finger_y = 0

# 中指食指之间的距离
fingertip_distance = 0

# 食指坐标到方块x y的距离 
distance_x = 0
distance_y = 0

on_block = False

box_x = 100
box_y = 100

box_width = 100
box_height = 100

while True:
  rec, frame = cap.read()

  frame = cv2.flip(frame, 1)

  frame.flags.writeable = False
  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  results = hands.process(frame)

  frame.flags.writeable = True
  frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      mp_drawing.draw_landmarks(
        frame,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style())
       
      landmark_x_list = []
      landmark_y_list = []

      for landmark in hand_landmarks.landmark :
        landmark_x_list.append(landmark.x)
        landmark_y_list.append(landmark.y)

      index_finger_x = int(landmark_x_list[index_finger_subscript] * cap_window_width)
      index_finger_y = int(landmark_y_list[index_finger_subscript] * cap_window_height)
  
      middle_finger_x = int(landmark_x_list[index_middle_subscript] * cap_window_width)
      middle_finger_y = int(landmark_y_list[index_middle_subscript] * cap_window_height)

      fingertip_distance = math.hypot((index_finger_x-middle_finger_x),(index_finger_y-middle_finger_y))

  if(fingertip_distance < 80):
    if((index_finger_x  > box_x and index_finger_x < box_x + box_width) and 
       (index_finger_y > box_y and index_finger_y < box_y + box_height)): 
         if on_block == False:
           distance_x = abs(index_finger_x - box_x)
           distance_y = abs(index_finger_y - box_y)
           on_block = True
  else:
    on_block = False

  # 计算方块实时坐标
  if(on_block) :
     box_x = index_finger_x - distance_x
     box_y = index_finger_y - distance_y

  cv2.rectangle(frame,(box_x,box_y),(box_x + box_width ,box_y + box_height),(255,0,0),-1)
  
  cv2.imshow('machine-learning', frame)

  if cv2.waitKey(10) & 0xFF == 27:
    break

cap.release()
cv2.destroyAllWindows()