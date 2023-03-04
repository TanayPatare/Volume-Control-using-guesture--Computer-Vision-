import cv2
import time
import numpy as np
from hand_tracking_Module import hand_Detector as htm
import math 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

C_time = 0
P_time = 0
cap = cv2.VideoCapture(0)
detector = htm()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]
vol = 0
vol_bar = 400
vol_per = 0


while True:
    success, img = cap.read()
    img = detector.findhands(img)
    lmlist= detector.findPosition(img,draw=False)
    if len(lmlist) != 0:
        #print(lmlist[4],lmlist[8])

        cx1,cy1 = lmlist[4][1], lmlist[4][2]
        cx2,cy2 = lmlist[8][1], lmlist[8][2]
        cx,cy = (cx1+cx2)//2 , (cy1+cy2)//2

        cv2.circle(img,(cx1,cy1),15,(0,255,255),cv2.FILLED)
        cv2.circle(img,(cx2,cy2),15,(0,255,255),cv2.FILLED)
        cv2.circle(img,(cx,cy),15,(0,255,255),cv2.FILLED)
        cv2.line(img,(cx1,cy1),(cx2,cy2),(0,255,255),3)

        lenght = math.hypot(cx2-cx1,cy2-cy1) #printed vlues for same. max ~= 300, min ~= 50

        #mapping hand lenght to vol lenght
        vol = np.interp(lenght,[50,210],[min_vol,max_vol]) #printed vlues for same. max ~= 300, min ~= 50
        vol_bar = np.interp(lenght,[50,210],[400,140])
        vol_per = np.interp(lenght,[50,210],[0,100])

        volume.SetMasterVolumeLevel(vol, None)
        if lenght < 50:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)

    cv2.rectangle(img, (50,140),(85,400),(255,0,0),3)
    cv2.rectangle(img, (50, int(vol_bar)),(85,400),(255,0,0),cv2.FILLED)
    cv2.putText(img,str(int(vol_per)), (40,450),cv2.FONT_HERSHEY_COMPLEX,1,
            (255,0,0),3)
    C_time = time.time()
    fps = 1/(C_time-P_time)
    P_time = C_time

    cv2.putText(img,str(int(fps)), (10,70),cv2.FONT_HERSHEY_COMPLEX,3,
            (255,0,255),3)

    cv2.imshow("Image",img)
    cv2.waitKey(1)