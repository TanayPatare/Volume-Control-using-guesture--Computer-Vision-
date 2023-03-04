import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils

C_time = 0
P_time = 0

while True:
    success, img = cap.read()
    img_RGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(img_RGB )

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):
                h, w, c = img.shape

                #converting cordinates to pixel value
                # lm.x - coordinate, cx - pixel 
                cx, cy =  int(lm.x * w), int(lm.y * h)
                if id == 8:
                    cv2.circle(img,(cx,cy),15,(0,255,255),cv2.FILLED)
            mpDraw.draw_landmarks(img,handlms,mphands.HAND_CONNECTIONS)

    C_time = time.time()
    fps = 1/(C_time-P_time)
    P_time = C_time

    cv2.putText(img,str(int(fps)), (10,70),cv2.FONT_HERSHEY_COMPLEX,3,
                (255,0,255),3)

    cv2.imshow("Image",img)
    cv2.waitKey(1)