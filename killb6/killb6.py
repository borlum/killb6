import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image

from cv_bridge import CvBridge
import cv2
import time
import face_recognition

import imutils

import base64
import numpy as np
min_size      = (50, 100) #(10, 10) # (50, 100)#
image_scale   = 4
haar_scale    = 1.2 #1.2 #1.1
min_neighbors = 2 #5
haar_flags    = cv2.CASCADE_SCALE_IMAGE #0 #cv2.CASCADE_SCALE_IMAGE

haarfile = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
#haarfile = '/usr/share/opencv4/haarcascades/haarcascade_upperbody.xml'
#haarfile = '/usr/share/opencv4/haarcascades/haarcascade_fullbody.xml'


cascade = cv2.CascadeClassifier()
cascade.load(haarfile)
br = CvBridge()

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_img = self.create_publisher(Image, 'facial_detection/img', 1)
        self.publisher_center = self.create_publisher(String, 'facial_detection/center_point', 1)
        
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.jokke)
        self.i = 0

        self.webcam = cv2.VideoCapture(0)

        #self.webcam.set(3, 50)
        #self.webcam.set(4, 50)

        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def timer_callback3(self):
        tic = time.perf_counter()
        check, captured_frame = self.webcam.read()
        output_frame = captured_frame.copy()
        toc = time.perf_counter()

        print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")


        # Convert original image to BGR, since Lab is only available from BGR
        captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGRA2BGR)
        # First blur to reduce noise prior to color space conversion
        captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3)
        # Convert to Lab color space, we only need to check one channel (a-channel) for red here
        captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab)
        # Threshold the Lab image, keep only the red pixels
        # Possible yellow threshold: [20, 110, 170][255, 140, 215]
        # Possible blue threshold: [20, 115, 70][255, 145, 120]
        captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([20, 150, 150]), np.array([190, 255, 255]))
        # Second blur to reduce more noise, easier circle detection
        captured_frame_lab_red = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)
        # Use the Hough transform to detect circles in the image
        circles = cv2.HoughCircles(captured_frame_lab_red, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_red.shape[0] / 8, param1=100, param2=18, minRadius=5, maxRadius=60)

        x, y, w, h = (output_frame.shape[1]/2, output_frame.shape[0]/2, 0, 0)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            cv2.circle(output_frame, center=(circles[0, 0], circles[0, 1]), radius=circles[0, 2], color=(0, 255, 0), thickness=2)

        msg = String()
        detected = 1 if circles is not None else 0
        #msg.data = "%d,%d,%d" % (1, 1, detected)
        if circles is not None:
            msg.data = "%d,%d,%d" % (circles[0, 0]+circles[0, 2] - output_frame.shape[1]/2, circles[0, 1]+circles[0, 2] - output_frame.shape[0]/2, detected)
        else:
            msg.data = "%d,%d,%d" % (0, 0, detected)

        self.publisher_center.publish(msg)
        
        print(msg.data)

        msg = CvBridge().cv2_to_imgmsg(output_frame)
        self.publisher_img.publish(msg)
        self.i += 1

    def timer_callback2(self):
        tic = time.perf_counter()

        check, img = self.webcam.read()
        new_size = (int(img.shape[1] / image_scale), int(img.shape[0] / image_scale))

        toc = time.perf_counter()

        print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")

        img = imutils.resize(img, width=min(400, img.shape[1]))
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        (rects, weights) = self.hog.detectMultiScale(grey, winStride=(8,8))
        
        x, y, w, h = (img.shape[1]/2, img.shape[0]/2, 0, 0)
        if len(rects):
            (x, y, w, h) = rects[0]
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        msg = String()
        detected = 0 if len(rects) == 0 else 1
        msg.data = "%d,%d,%d" % (x+w/2 - img.shape[1]/2, y+h/2 - img.shape[0]/2, detected)
        self.publisher_center.publish(msg)
        
        print(msg.data)

        msg = CvBridge().cv2_to_imgmsg(img)
        self.publisher_img.publish(msg)
        self.i += 1

    def timer_callback(self):
        tic = time.perf_counter()

        check, img = self.webcam.read()
        new_size = (int(img.shape[1] / image_scale), int(img.shape[0] / image_scale))

        toc = time.perf_counter()

        print(f"Image capture time: {toc - tic:0.4f} seconds")

        # convert color input image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        tic = time.perf_counter()
        faces = cascade.detectMultiScale(gray, scaleFactor=1.05,
            minNeighbors=7, minSize=(30, 30),
	        flags=cv2.CASCADE_SCALE_IMAGE
        )
        toc = time.perf_counter()
        print(f"detectMultiScale: {toc - tic:0.4f} seconds")
        #print(faces)
        # Draw the rectangle around each face

        # plt.figure()
        x, y, w, h = (img.shape[1]/2, img.shape[0]/2, 0, 0)
        if len(faces):
            (x, y, w, h) = faces[0]
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        msg = String()
        detected = 0 if len(faces) == 0 else 1
        msg.data = "%d,%d,%d" % (x+w/2 - img.shape[1]/2, y+h/2 - img.shape[0]/2, detected)
        self.publisher_center.publish(msg)
        
        print(msg.data)

        msg = CvBridge().cv2_to_imgmsg(img, "bgr8")
        self.publisher_img.publish(msg)
        self.i += 1

    def jokke(self):
        tic = time.perf_counter()

        check, img = self.webcam.read()
        new_size = (int(img.shape[1] / image_scale), int(img.shape[0] / image_scale))

        toc = time.perf_counter()

        print(f"Image capture time: {toc - tic:0.4f} seconds")

        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        tic = time.perf_counter()
        face_locations = face_recognition.face_locations(rgb_small_frame)
        toc = time.perf_counter()
        print(f"face_recognition {toc - tic:0.4f} seconds")

        for (top, right, bottom, left) in face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
       
        #msg.data = "%d,%d,%d" % (x+w/2 - img.shape[1]/2, y+h/2 - img.shape[0]/2, detected)
        #self.publisher_center.publish(msg)
        
        #print(msg.data)

        msg = CvBridge().cv2_to_imgmsg(img, "bgr8")
        self.publisher_img.publish(msg)
        self.i += 1

def main(args=None):
    print("TISSEMAND")

    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
