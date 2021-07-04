import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image

from cv_bridge import CvBridge
import cv2

import base64
import numpy as np
min_size      = (50, 100) #(10, 10) # (50, 100)#
image_scale   = 2
haar_scale    = 1.1 #1.2 #1.1
min_neighbors = 2 #5
haar_flags    = cv2.CASCADE_SCALE_IMAGE #0 #cv2.CASCADE_SCALE_IMAGE

haarfile = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'

cascade = cv2.CascadeClassifier()
cascade.load(haarfile)
br = CvBridge()

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_img = self.create_publisher(Image, 'facial_detection/img', 1)
        self.publisher_center = self.create_publisher(String, 'facial_detection/center_point', 1)
        timer_period = 0.05  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        self.webcam = cv2.VideoCapture(0)


    def timer_callback(self):
        check, img = self.webcam.read()
        new_size = (int(img.shape[1] / image_scale), int(img.shape[0] / image_scale))

        # convert color input image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = cascade.detectMultiScale(gray, 1.1, 4)
        #print(faces)
        # Draw the rectangle around each face

        # plt.figure()
        x, y, w, h = (img.shape[1]/2, img.shape[0]/2, 0, 0)
        if len(faces):
            (x, y, w, h) = faces[0]
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        msg = String()
        msg.data = "%d,%d" % (x+w/2 - img.shape[1]/2, y+h/2 - img.shape[0]/2)
        print(msg.data)
        self.publisher_center.publish(msg)

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
