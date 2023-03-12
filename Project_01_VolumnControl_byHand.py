import cv2
import mediapipe as mp
import time
import Hand_Detector_Module as hdm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

camW , camH = 1000, 1400
cap = cv2.VideoCapture(0)
cap.set(3, camW)
cap.set(4, camH)

##------------------ For Volumn Control ----------------------##
######### https://github.com/AndreMiras/Pycaw ----for volumn ###
#--------------------------------------------------------------#
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRnge = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20, None)
minVol = volRnge[0]
maxVol = volRnge[1]
pre_time = 0
# Con_vol = 0
volBar = 400
volPer = 0
#---------------------------------------------------------------#

detector = hdm.HandDetector(detectionConfidence=0.6)
while True:
    success, frame = cap.read()
    frame = detector.FindHands(frame, False)
    lmList = detector.FindPosition(frame, False)
    
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy= (x1+x2)//2, (y1+y2)//2

        cv2.circle(frame , (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame , (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(frame, (x1,y1), (x2, y2), (255, 0, 255), 5)
        cv2.circle(frame , (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        # # length range 50 - 275
        # # volumn range -65.25 - 0

        ## Converter
        Con_vol = np.interp(length, [50, 275], [minVol, maxVol])
        volBar = np.interp(length, [50, 275], [400, 150])
        volPer = np.interp(length, [50, 275], [0, 100])
        # print(int(length), Con_vol)
        volume.SetMasterVolumeLevel(Con_vol, None)

        ## Hand Line Color 
        if length<=50:
            cv2.circle(frame , (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        elif length>=275:
            cv2.circle(frame , (cx, cy), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame , (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame , (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.line(frame, (x1,y1), (x2, y2), (0, 0, 255), 5)    

    ## Box for Showing Percentage
    if int(volPer)>=85:
        cv2.rectangle(frame, (50, 150), (85, 400), (0, 0, 255), 3)  
        cv2.rectangle(frame, (50, int(volBar)), (85, 400), (0, 0, 255), cv2.FILLED) 

    else:  
        cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)  
        cv2.rectangle(frame, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)

    cv2.putText(
        frame,
        f'{int(volPer)}%',
        (48, 419),
        cv2.FONT_HERSHEY_PLAIN, 1,
        (255, 200, 0),
        2
    )


    current_time = time.time()
    fps = 1/ (current_time-pre_time)
    pre_time = current_time

    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX

    # FPS Box
    start_point = (0, 0)
    end_point = (102, 32)
    color = (100, 0, 0)
    thickness = -1

    FPS_Box = cv2.rectangle(frame, start_point, end_point, color, thickness) 

    cv2.putText(
        FPS_Box,
        str(int(fps)),
        (31, 26),
        font, 1,
        (255, 200, 0),
        2
    )

    cv2.imshow("Camera", frame)
    if cv2.waitKey(10) == ord('0'):
        break
    
cap.release()
cv2.destroyAllWindows() 