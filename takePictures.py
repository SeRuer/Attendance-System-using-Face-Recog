import cv2
import os
import numpy as np
import pandas as pd
import datetime
import time

# Counter for images
def count_pictures(k):
    try:
        float(k)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(k)
        return True
    except (TypeError, ValueError):
        pass

        return False

print("Camera on")
captureDevice = cv2.VideoCapture(0)
captureDevice.set(3, 650)  # Sets the camera width
captureDevice.set(4, 480)  # Sets the camera height


#self.checkCascade()
ID = input("Input user ID:   ")
studentName = input("Please Input the student name: ")
if (count_pictures(ID) and studentName.isalpha()):
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    expressionCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")
    eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    counter = 0
    print("Detect #1")
    while True:
        ret, frame = captureDevice.read()

        #For now this will convert the frames to grey scale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #print("Convert function #2")
        # detects the frames for different sizes
        faces = faceCascade.detectMultiScale(gray, 2, 6)
        #print("Loop is about to start")
        for (x, y, w, h) in faces:
            print([x, y, w, h])
            colour = frame[y:y + h, x:x + w]
            grayGray = gray[y:y + h, x:x + w]
            # Crop the photo frame into a rectangle
            #If faces found
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # add the sample number
            # noinspection PyArgumentList
            eye = eyeCascade.detectMultiScale(colour)

            for (ex, ey, ew, eh) in eye:
                cv2.rectangle(colour, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                smileFace = expressionCascade.detectMultiScale(grayGray)
                for (xx, yy, ww, hh) in smileFace:
                    cv2.rectangle(colour, (xx, yy), (xx + ww, yy + hh), (0, 255,0), 2)

            counter = counter + 1
            # Save the face into the folder
            cv2.imwrite("Dataset/" + os.sep + ID + "." + str(studentName) +"."+ str(counter) +".jpg", gray[y:y + h, x:x + w])
            # Showcase the frame
            cv2.imshow('Taking Images', frame)
        # Wait for only 200 milli
        if cv2.waitKey(200) & 0xFF == ord('f'):
            cv2.destroyAllWindows()
            break
                # So this will break if the pictures are more than 100
        elif counter > 1000:
            break


captureDevice.release()