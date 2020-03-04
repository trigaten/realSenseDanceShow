import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    
    
    test_image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    haar_cascade_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    faces_rects = haar_cascade_face.detectMultiScale(test_image_gray, scaleFactor = 1.2, minNeighbors = 5)
    print('Faces found: ', len(faces_rects))
    # for i in range(len(faces_rects)):
    #     for i in range(100):
    #         for j in range(100):
    #            frame[i][j][0] = 100
    
    for (x,y,w,h) in faces_rects:
        if x>0 and x < 480 and y > 0 and y < 300:
            for i in range(100):
                for j in range(100):
                    frame[y+i+50][x+j+50][0] = 100
                    frame[y+i+50][x+j+50][1] = 100
                    frame[y+i+50][x+j+50][2] = 100
    #     if x>0 and x < 480 and y > 0 and y < 300:
    #          frame[x][y][0] = 100
    #          frame[x][y][1] = 100
    #          frame[x][y][2] = 100
    #          print(x)
    #          print(y)

    cv2.imshow('frame',frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()