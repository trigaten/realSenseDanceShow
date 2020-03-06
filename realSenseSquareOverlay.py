
import pyrealsense2 as rs
import numpy as np
import cv2

# get screen size in pixels
import ctypes
user32 = ctypes.windll.user32
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)
print(width)
# ctrl alt m to stop code
# Configure depth and color streams

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming

pipeline.start(config)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        test_image_gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        haar_cascade_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces_rects = haar_cascade_face.detectMultiScale(test_image_gray, scaleFactor = 1.2, minNeighbors = 5)
        for (x,y,w,h) in faces_rects:
            if x>0 and x < 480 and y > 0 and y < 300:
                for i in range(100):
                    for j in range(100):
                        d = 0
                        if depth_image[x][y] > 50:
                            d = 2
                        else:
                            d = 1
                        color_image[y+i+50][x+j+50][0] = int(0.1 * depth_image[y+i+50][x+j+50])
                        color_image[y+i+50][x+j+50][1] = int(0.1 * depth_image[y+i+50][x+j+50])
                        color_image[y+i+50][x+j+50][2] = int(0.1 * depth_image[y+i+50][x+j+50])
                            
                        # if x > 120:
                        #     if x > 240:
                        #         color_image[y+i+50][x+j+50][0] = d * 150
                        #         color_image[y+i+50][x+j+50][1] = d * 1
                        #         color_image[y+i+50][x+j+50][2] = d * 1
                        #     else:
                        #         color_image[y+i+50][x+j+50][0] = d * 1
                        #         color_image[y+i+50][x+j+50][1] = d * 100
                        #         color_image[y+i+50][x+j+50][2] = d * 1
                        # else:
                        #     color_image[y+i+50][x+j+50][0] = d * 5
                        #     color_image[y+i+50][x+j+50][1] = d * 5
                        #     color_image[y+i+50][x+j+50][2] = d * 50

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        # cv2.imshow('RealSense', images)
        cv2.imshow('RealSense', color_image)
        cv2.waitKey(1)

finally:
    # Stop streaming
    pipeline.stop()