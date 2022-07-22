from time import sleep
import pandas as pd
import os
import cv2
from datetime import datetime
from buildhat import DistanceSensor, Motor

# motor & sensor
RMotor = Motor('A')
LMotor = Motor('B') 

def motor_control(speed_L, speed_R):
    LMotor.start(speed_L*-1)
    RMotor.start(speed_R)

def car_move(direction):
    if direction == 'forward':
        motor_control(30,30)
    elif direction == 'back':
        motor_control(-20,-20)
    elif direction == 'left':
        motor_control(0,25)
    elif direction == 'right':
        motor_control(25,0)
    else:
        motor_control(0,0)

#GET DATASET
global imgList, directionList
countFolder = 0
count = 0
imgList = []
directionList = []

#GET CURRENT DIRECTORY PATH
myDirectory = os.path.join(os.getcwd(), 'DataCollected')

# CREATE A NEW FOLDER BASED ON THE PREVIOUS FOLDER COUNT
while os.path.exists(os.path.join(myDirectory,f'IMG{str(countFolder)}')):
    countFolder += 1
newPath = myDirectory +"/IMG"+str(countFolder)
os.makedirs(newPath)

def getImg(img,size=[480,240]):
    img = cv2.resize(img,(size[0],size[1]))
    return img

# SAVE IMAGES IN THE FOLDER
def saveData(img,direction):
    global imgList, directionList
    now = datetime.now()
    timestamp = str(datetime.timestamp(now)).replace('.', '')
    #print("timestamp =", timestamp)
    fileName = os.path.join(newPath,f'Image_{timestamp}.jpg')
    cv2.imwrite(fileName, img)
    imgList.append(fileName)
    directionList.append(direction)

# SAVE LOG FILE WHEN THE SESSION ENDS
def saveLog():
    global imgList, directionList
    rawData = {'Image': imgList,
                'direction': directionList}
    df = pd.DataFrame(rawData)
    df.to_csv(os.path.join(myDirectory,f'log_{str(countFolder)}.csv'), index=False, header=False)
    print('Log Saved')
    print('Total Images: ',len(imgList))

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    record = 0
    direction='stop'
    while True:
        _, img = cap.read()
        img = cv2.flip(cv2.flip(img, 1), 0)
        cv2.imshow('IMG',img)
        key=cv2.waitKeyEx(1) # 키보드에서 입력키받음
        if key == 0x1B: #ESC키
            break
        elif key==0x260000: # 방향키 0x260000==up
            direction='forward'
        elif key==0x280000: # 방향키 0x280000==down
            direction='back'
        elif key==0x250000: # 방향키 0x250000==left
            direction='left'
        elif key==0x270000: # 방향키 0x270000==right
            direction='right'
        else:
            direction='stop'

        if key == 32: #스페이스키를 입력 받으면 녹화 시작 or 종료
            record +=1
            sleep(0.3)
        if record == 1:
            img = getImg(img,size=[240,120])
            if direction != 'stop':
                saveData(img,direction)
        elif record == 2:
            saveLog()
            record = 0

        #car_move(direction)