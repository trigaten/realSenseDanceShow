
import random
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
r = range(150)
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
        n = random.randint(-100, 100)
        print(n)
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        print("start")
        print(len(color_image))
        print(len(color_image[0]))
        print(len(color_image[0][0]))
        print(len(color_image[0][0]))
        color_image[0:640][0:480][49:479][45:300] += 100#int16(n)
        # for x in r:
        #     for y in r:
        #         newValue = 1 #int(((depth_image[x][y]) * (365)) / (2000))
        #         color_image[x][y][0]+= newValue
        #         color_image[x][y][1]+= newValue
        #         color_image[x][y][2]+= newValue

        # print("before")
        # print(color_image[101][101])
        # color_image[101][101][0]+=1234
        # print("after")
        # print(color_image[101][101])
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