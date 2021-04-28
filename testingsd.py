import cv2.cv2 as cv2
import datetime
import sys
import numpy as np
import os
import sqlite3
import pickle
import pandas as pd


captureDevice = cv2.VideoCapture(0) 

captureDevice.set(3, 650)  # Sets the camera width
captureDevice.set(4, 480)  # Sets the camera height
# Setting the window size for the face
minW = 0.1 * captureDevice.get(3)
minH = 0.1 * captureDevice.get(4)


detect = "haarcascade_frontalface_alt"
detectEyes = "haarcascade_eye.xml"
print("Files read")
#self.checkCascade()
ID = input("Input user ID:   ")
if (count_pictures(ID)):
  faceCascade = cv2.CascadeClassifier(detect)
  eye_cascade = cv2.CascadeClassifier(detectEyes)
  counter = 0  
  print("Detect #1")
  while True:
    ret, frame = captureDevice.read()
    if ret == True:
      # For now this will convert the frames to grey scale
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      print("Convert function #2")
      # detects the frames for different sizes
      faces = faceCascade.detectMultiScale(gray, 1.3, 5, minSize=(int(minW), int(minH)),flags=cv2.CASCADE_SCALE_IMAGE)
      # This will loop for every single student
      print("Loop is about to start")
      for (x, y, w, h) in faces:
          print(x, y, w, h)
          # Crop the photo frame into a rectangle
          #If faces found
          cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
          roi_color = (frame[y:y + h, x:x + w])
          ID, conf = detect.predict(gray[y:y + h, x:x + w])
          eyes = eye_cascade.detectMultiScale(roi_color)
          for (ex, ey, ew, eh) in eyes:
              cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
              # add the sample number
              counter = counter + 1
              # Save the face into the folder
              cv2.imwrite("Dataset/" + os.sep + ID + str(counter) + ".jpg", gray[y:y + h, x:x + w])
              # Showcase the frame
              cv2.imshow('Frame', frame)
              # Wait for only 80 milli
          if cv2.waitKey(100) & 0xFF == ord('f'):
              break
            # So this will break if the pictures are more than 100
          elif counter > 200:  # decreased the pictures due to scalability issues
              break

captureDevice.release()
cv2.destroyAllWindows()