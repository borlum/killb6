import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from cv_bridge import CvBridge
import cv2

import pyserial

import matplotlib.pyplot as plt

min_size      = (50, 100) #(10, 10) # (50, 100)#
image_scale   = 2
haar_scale    = 1.1 #1.2 #1.1
min_neighbors = 5 #2 #5
haar_flags    = cv2.CASCADE_SCALE_IMAGE #0 #cv2.CASCADE_SCALE_IMAGE

haarfile = '/usr/share/opencv4/haarcascades/haarcascade_upperbody.xml'

cascade = cv2.CascadeClassifier()
cascade.load(haarfile)
br = CvBridge()


# Serial
#motor1 = serial.Serial("/dev/ttyUSB0")
#motor2 = serial.Serial("/dev/ttyUSB1")

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

        # scale input image for faster processing
        small_img = cv2.resize(gray, new_size, interpolation = cv2.INTER_LINEAR)

        small_img = cv2.equalizeHist(small_img)
        
        if(cascade):
            faces = cascade.detectMultiScale(small_img, haar_scale, min_neighbors, haar_flags, min_size)
            if faces is not None:
                for (x, y, w, h) in faces:
                    # the input to detectMultiScale was resized, so scale the
                    # bounding box of each face and convert it to two CvPoints
                    pt1 = (int(x * image_scale), int(y * image_scale))
                    pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                    cv2.rectangle(img, pt1, pt2, (255, 0, 0), 3, 8, 0)

        plt.figure()
        plt.imshow(img)
        plt.show()
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