import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from cv_bridge import CvBridge
import cv2

import matplotlib.pyplot as plt

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
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        webcam = cv2.VideoCapture(0)
        check, img = webcam.read()
        webcam.release()

        #imgmsg = br.cv2_to_imgmsg(frame)
        #img = br.imgmsg_to_cv2(imgmsg, "bgr8")

        new_size = (int(img.shape[1] / image_scale), int(img.shape[0] / image_scale))

        # convert color input image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        plt.figure()
        plt.imshow(img)
        plt.pause(1)
        plt.show(block=False)
        plt.close()
        #cv2.imshow("result", img)

        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
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
