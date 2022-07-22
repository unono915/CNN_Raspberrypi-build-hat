from time import sleep
import pandas as pd
import os
import cv2
from datetime import datetime

cap = cv2.VideoCapture(0)
direction = 0
while True:
    _, img = cap.read()
    cv2.imshow("Image",img)
    key=cv2.waitKeyEx(1) # 키보드에서 입력키받음
    if key == 0x1B: #ESC키
        break
    elif key==0x260000: # 방향키 방향 전환 0x260000==up
        direction=0
    elif key==0x280000: # 방향키 방향 전환 0x280000==down
        direction=1
    elif key==0x250000: # 방향키 방향 전환 0x250000==left
        direction=2
    elif key==0x270000: # 방향키 방향 전환 0x270000==right
        direction=3
    print(key)