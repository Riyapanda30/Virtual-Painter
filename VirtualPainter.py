import cv2 
import numpy as np 
import time 
import os 
import math 
import HandTrackingModule as htm

def save_canvas(canvas, filename="drawing.png"):
    timestamp = time.strftime("%Y%m%d_%H%M%S")  
    unique_filename = f"drawing_{timestamp}.png"  
    cv2.imwrite(unique_filename, canvas)
    print(f"Canvas saved as {unique_filename}")

brushThickness = 15 
eraserThickness = 50 

folderPath = r"C:\Users\riyap\OneDrive\Pictures\MajorProjectDuplicate\HandTrackingProject\header" 
myList = os.listdir(folderPath) 
print(myList)

overlayList = [] 
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}') 
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0] 
drawColor = (255.0,255) 

cap = cv2.VideoCapture(0) 

cap.set(3, 1280)
cap.set(4, 720) 

detector = htm.handDetector(detectionCon=0.85) 
xp, yp = 0, 0 
imgCanvas = np.zeros((720, 1280, 3),np.uint8)

#Undo and Redo 
undoStack = []
redoStack = []

while True: 

    success, img = cap.read() 
    img = cv2.flip(img, 1) 

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False) 

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

    if cv2.waitKey(1) & 0xFF == ord('c'): 
        print("Clearing Canvas with Key")
        undoStack.append(imgCanvas.copy()) 
        imgCanvas = np.zeros((720, 1280, 3), np.uint8) 
        xp, yp = 0, 0 
   
    if cv2.waitKey(1) & 0xFF == ord('+'): 
        brushThickness += 5
        print(f"Brush Thickness Increased: {brushThickness}")

    if cv2.waitKey(1) & 0xFF == ord('-'): 
        brushThickness = max(5, brushThickness - 5)  
        print(f"Brush Thickness Decreased: {brushThickness}")

    if cv2.waitKey(1) & 0xFF == ord('s'): 
        save_canvas(imgCanvas)

    if cv2.waitKey(1) & 0xFF == ord('u'):
        if undoStack:
            redoStack.append(imgCanvas.copy()) 
            imgCanvas = undoStack.pop()
            print("Undo Action Performed")

    if cv2.waitKey(1) & 0xFF == ord('r'):
        if redoStack:
            undoStack.append(imgCanvas.copy()) 
            imgCanvas = redoStack.pop() 
            print("Redo Action Performed")

    if len(lmList)!= 0: 

        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]
        x3,y3 = lmList[4][1:]
        x4,y4 = lmList[20][1:]


        fingers = detector.fingersUp() 

        if fingers[1] and fingers[2]: 
            xp, yp = 0, 0 
            print("Selection Mode") 
            if y1 < 124: 
                if 55<x1<90: 
                    header = overlayList[0] 
                    drawColor = (255, 0, 255) 
                elif 192<x1<220: 
                    header = overlayList[1] 
                    drawColor = (0, 255, 0)
                elif 330<x1<360:  
                    header = overlayList[2] 
                    drawColor = (0, 0, 255) 
                elif 450<x1<480:
                    header = overlayList[3]
                    drawColor = (115, 115, 115)
                elif 568<x1<600 :
                    header = overlayList[4]
                    drawColor = (235, 212, 105)
                elif 745<x1<785 :
                    header = overlayList[5]
                    drawColor = (128, 0, 128)
                elif 895<x1<935 :
                    header = overlayList[6]
                    drawColor = (98, 132, 116)
                                 
                elif 1070<x1<1100: 
                    header = overlayList[7]
                    drawColor = (0, 0, 0) 
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1,y1),15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp==0 and yp==0: 
                xp, yp = x1, y1 

            if drawColor == (0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness) 
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness) 
            else: 
                cv2.line(img, (xp,yp),(x1,y1), drawColor, brushThickness) 
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness) 
                undoStack.append(imgCanvas.copy())

            xp, yp = x1, y1 

        if all(fingers[i] == 0 for i in range(0, 5)): 
            imgCanvas = np.zeros((720, 1280, 3), np.uint8) 
            xp, yp = [x1, y1]


        selecting = [1, 1, 0, 0, 0] 
        setting = [1, 1, 0, 0, 1] 
        if all(fingers[i] == j for i, j in zip(range(0, 5), selecting)) or all(
                fingers[i] == j for i, j in zip(range(0, 5), setting)): 

            r = int(math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2) / 3) 
                    
            x0, y0 = [(x1 + x3) / 2, (y1 + y3) / 2]
            v1, v2 = [x1 - x3, y1 - y3]
            v1, v2 = [-v2, v1] 

            mod_v = math.sqrt(v1 ** 2 + v2 ** 2)
            v1, v2 = [v1 / mod_v, v2 / mod_v] 

            
            c = 3 + r 
            x0, y0 = [int(x0 - v1 * c), int(y0 - v2 * c)] 
            cv2.circle(image, (x0, y0), int(r / 2), drawColor, -1) #

            if fingers[4]: 
                thickness = r #radius
                cv2.putText(image, 'Check', (x4 - 25, y4 - 8), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0, 0, 0), 1)
            xp, yp = [x1, y1]

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV ) 
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR) 
    img = cv2.bitwise_and(img,imgInv) 
    img = cv2.bitwise_or(img,imgCanvas) 


    img[0:124, 0:1280] = header 
    cv2.imshow("Image", img) 
    cv2.waitKey(1) 
