import cv2 #for working images and videos using opencv 
import numpy as np #handling arrays and mathematical operations
import time #for tracking time
import os #to handle file and folder operation
import math #handle mathematical calculations
import HandTrackingModule as htm #used to track hand movements

def save_canvas(canvas, filename="drawing.png"):
    timestamp = time.strftime("%Y%m%d_%H%M%S")  # Get current timestamp
    unique_filename = f"drawing_{timestamp}.png"  # Add timestamp to the filename
    cv2.imwrite(unique_filename, canvas)
    print(f"Canvas saved as {unique_filename}")

brushThickness = 15 #sets the thickness of the drawing brush
eraserThickness = 50 #sets the thickness of the eraser

folderPath = r"C:\Users\riyap\OneDrive\Pictures\MajorProjectDuplicate\HandTrackingProject\header" #points to the folder containing header images
myList = os.listdir(folderPath) #lists all files in the folderPath directory
print(myList)

overlayList = [] #A list that stores the header images loaded from the folder.
for imPath in myList: #Loops through each file name in myList, which contains all the file names of images in the folder (folderPath).
    image = cv2.imread(f'{folderPath}/{imPath}') #Reads each image file and appends it to overlayList
    overlayList.append(image) #adds the image to the overlayList list.
print(len(overlayList)) #prints the length of overlayList, showing how many images are stored in it.
header = overlayList[0] #assigns the first image in the overlayList to the variable header.
drawColor = (255.0,255) # sets the variable drawColor to a tuple with values (255.0, 255), which likely represents an RGB color (with only two values, it might need a third for proper color representation).

cap = cv2.VideoCapture(0) #initializes the webcam to capture video from the default camera

cap.set(3, 1280) #sets the video width to 1280 pixels.
cap.set(4, 720) #sets the video height to 720 pixels.

detector = htm.handDetector(detectionCon=0.85) # Creates a hand detection object with a confidence threshold of 85% for detecting hands.
xp, yp = 0, 0 #Initializes variables xp and yp to store previous x and y coordinates, initially set to 0.
imgCanvas = np.zeros((720, 1280, 3),np.uint8) # Creates a black canvas (720x1280 pixels) to draw on, with 3 color channels (RGB).

#Undo and Redo 
undoStack = []
redoStack = []

while True: #Starts an infinite loop to continuously capture video frames.

    success, img = cap.read() #Captures a frame from the webcam, storing it in img and success indicating if the capture is successful.
    img = cv2.flip(img, 1) #Flips the captured frame horizontally for mirror effect.

    img = detector.findHands(img) #Uses a hand detection method to detect hands in the image.
    lmList = detector.findPosition(img, draw=False) # Finds the positions of hand landmarks in the image without drawing them.

    if cv2.waitKey(1) & 0xFF == ord('q'):  #cv2.waitKey(1): Waits for 1 millisecond to check if a key is pressed 2)& 0xFF: Ensures the result is within the range of 0-255 (to handle platform-specific differences)  3)== ord('q'): Compares the key pressed with the ASCII value of 'q'.
        break #added by myself to quit after running

    #added by myself
    # Clear canvas with 'c' key
    if cv2.waitKey(1) & 0xFF == ord('c'):  # Press 'c' to clear the canvas
        print("Clearing Canvas with Key")
        undoStack.append(imgCanvas.copy())  # Save current state to undo stack
        imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # Reset canvas
        xp, yp = 0, 0  # Reset previous positions

     # Increase brush thickness with '+' key
    if cv2.waitKey(1) & 0xFF == ord('+'):  # Press '+' to increase brush thickness
        brushThickness += 5
        print(f"Brush Thickness Increased: {brushThickness}")

    # Decrease brush thickness with '-' key
    if cv2.waitKey(1) & 0xFF == ord('-'):  # Press '-' to decrease brush thickness
        brushThickness = max(5, brushThickness - 5)  # Minimum thickness = 5
        print(f"Brush Thickness Decreased: {brushThickness}")

        # Save canvas with 's' key
    if cv2.waitKey(1) & 0xFF == ord('s'):  # Press 's' to save the canvas
        save_canvas(imgCanvas)


     # Undo functionality with 'u' key
    if cv2.waitKey(1) & 0xFF == ord('u'):
        if undoStack:
            redoStack.append(imgCanvas.copy())  # Save current state to redo stack
            imgCanvas = undoStack.pop()  # Restore the last saved state
            print("Undo Action Performed")

    # Redo functionality with 'r' key
    if cv2.waitKey(1) & 0xFF == ord('r'):
        if redoStack:
            undoStack.append(imgCanvas.copy())  # Save current state to undo stack
            imgCanvas = redoStack.pop()  # Restore the last undone state
            print("Redo Action Performed")

    if len(lmList)!= 0: #This checks if the length of the list lmList is not equal to 0, meaning it checks if the list is not empty.
        #print(lmList)

        # tip of index, middle fingers
        x1,y1 = lmList[8][1:]#pointing finger  [ Extracts the coordinates (x, y) of the pointing finger (index finger, 8th landmark) from the list lmList.]
        x2,y2 = lmList[12][1:]#middle finger
        x3,y3 = lmList[4][1:]#thumb
        x4,y4 = lmList[20][1:]#small finger


        fingers = detector.fingersUp() # Checks which fingers are raised using the detector.
        #print(fingers)

        #selection mode - two fingers
        if fingers[1] and fingers[2]: #Checks if the index and middle fingers are both raised.
            xp, yp = 0, 0 # Resets the coordinates xp and yp to 0.
            print("Selection Mode") #Prints "Selection Mode" to indicate the selection mode is active.
            if y1 < 124: # Checks if the y1 coordinate is less than 125.
                if 55<x1<90: # Checks if the x1 coordinate is between 350 and 450.
                    header = overlayList[0] #Selects the first overlay from the list.
                    drawColor = (255, 0, 255) #Sets the drawing color to magenta (pink).
                elif 192<x1<220: # Checks if the x1 coordinate is between 550 and 750.
                    header = overlayList[1] # Selects the second overlay from the list.
                    drawColor = (0, 255, 0) # Sets the drawing color to green.
                elif 330<x1<360:  #Checks if the x1 coordinate is between 800 and 950.
                    header = overlayList[2] #Selects the third overlay from the list.
                    drawColor = (0, 0, 255)  #Sets the drawing color to Red
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
                                 
                elif 1070<x1<1100: #Checks if the x1 coordinate is between 1050 and 1200.
                    header = overlayList[7] #Selects the fourth overlay from the list.
                    drawColor = (0, 0, 0) #Sets the drawing color to black.
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED) #Draws a filled rectangle on the image based on the selected coordinates with the chosen color.


        #drawing mode - ppointing finger
        if fingers[1] and fingers[2]==False: #Check if only the index finger is up and the middle finger is down.
            cv2.circle(img, (x1,y1),15, drawColor, cv2.FILLED) #Draw a filled circle at the index finger's position on the image.
            print("Drawing Mode") # Print "Drawing Mode" to indicate the drawing mode is active.
            if xp==0 and yp==0: #If no previous position is set, initialize it with the current finger position.
                xp, yp = x1, y1 # Update the previous position to the current position.

            if drawColor == (0,0,0): #Check if the selected color is black (eraser mode).
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness) #Draw an erasing line on the main image.
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness) #Erase on the canvas with the eraser thickness.
            else: # If the selected color is not black, it’s brush mode.
                cv2.line(img, (xp,yp),(x1,y1), drawColor, brushThickness) #Draw a line on the main image with the selected brush color.
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness) #Draw on the canvas with the selected brush thickness.
                undoStack.append(imgCanvas.copy())

            xp, yp = x1, y1 #Update the previous position to the current position after drawing.

##changes
        if all(fingers[i] == 0 for i in range(0, 5)): #checks if all five fingers are closed 
            imgCanvas = np.zeros((720, 1280, 3), np.uint8) #resets the canvas to a blank black image
            xp, yp = [x1, y1] #update the starting position for drawing to the current finger position

        ## Adjust the thickness of the line using the index finger and thumb
        selecting = [1, 1, 0, 0, 0]  # Selecting the thickness of the line, index and middle fingers are up
        setting = [1, 1, 0, 0, 1]  # Setting the thickness chosen, where index,middle and pinky fingers are up.
        if all(fingers[i] == j for i, j in zip(range(0, 5), selecting)) or all(
                fingers[i] == j for i, j in zip(range(0, 5), setting)): #Checks if the current hand gesture matches either the selecting or setting gesture.

            # Getting the radius of the circle that will represent the thickness of the draw
            # using the distance between the index finger and the thumb.
            r = int(math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2) / 3) #Calculates a radius based on the distance between two points (x1, y1) and (x3, y3) in a 2D plane.

            # Getting the middle point between these two fingers
            x0, y0 = [(x1 + x3) / 2, (y1 + y3) / 2] #This uses the midpoint formula to find the center between two points on a 2D plane.

            # Getting the vector that is orthogonal to the line formed between
            # these two fingers
            v1, v2 = [x1 - x3, y1 - y3] #Calculates the vector between two points.
            v1, v2 = [-v2, v1] #Rotates the vector by 90 degrees.

            # Normalizing it
            mod_v = math.sqrt(v1 ** 2 + v2 ** 2) #Computes the magnitude (length) of the vector using the pythagorean theorem.
            v1, v2 = [v1 / mod_v, v2 / mod_v] #Normalizes the vector to unit length.

            # Draw the circle that represents the draw thickness in (x0, y0) and orthogonaly
            # translated c units
            c = 3 + r #Sets a distance offset based on the radius.
            x0, y0 = [int(x0 - v1 * c), int(y0 - v2 * c)] #Adjusts the midpoint by moving it along the rotated vector.
            cv2.circle(image, (x0, y0), int(r / 2), drawColor, -1) #Draws a circle at the adjusted midpoint with a specified radius and color.

            # Setting the thickness chosen when the pinky finger is up
            if fingers[4]: #checks if thw pinky fingers is up
                thickness = r #radius
                cv2.putText(image, 'Check', (x4 - 25, y4 - 8), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0, 0, 0), 1) #Displays the text "Check" near the pinky finger position.

            xp, yp = [x1, y1] #Updates the starting position for the next drawing action.

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY) #Converts imgCanvas to a grayscale image.
    _, imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV ) #Creates a binary inverted image where pixels below 50 are white, and others are black
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR) #Converts the inverted grayscale image back to a color (BGR) image.
    img = cv2.bitwise_and(img,imgInv) #Combines the original image and the inverted image using a bitwise AND operation.
    img = cv2.bitwise_or(img,imgCanvas) #Merges the modified image and imgCanvas using a bitwise OR operation.


    img[0:124, 0:1280] = header #Overlays the header image at the top of img
    #img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img) #Displays the resulting image in a window named "Image"
    #cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1) #Waits for 1 millisecond for a key press (used for real-time updates).
