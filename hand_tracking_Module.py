import cv2
import mediapipe as mp
import time


class hand_Detector():
    def __init__(self,mode = False, maxHands = 2, detectionCon=0.7,tracCon =0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.tracCon = tracCon

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findhands(self,img,draw = True):
        img_RGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_RGB )

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handlms,self.mphands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img,handno=0,draw = True):
        lmlist= []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                #converting cordinates to pixel value
                cx, cy =  int(lm.x * w), int(lm.y * h)
                lmlist.append([id,cx,cy])   
                if draw:
                    cv2.circle(img,(cx,cy),15,(0,255,255),cv2.FILLED)
        return lmlist
