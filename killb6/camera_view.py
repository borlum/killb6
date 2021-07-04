import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

import matplotlib.pyplot as plt
import base64
import numpy as np

class CameraViewer(Node):

    def __init__(self):
        plt.figure()
        super().__init__("killb6_camera_view")

        self.subscription = self.create_subscription(
            Image,
            "facial_detection/img",
            self.listener_callback,
            1)
        self.subscription  # prevent unused variable warning

        #self.img = np.zeros((480,640,3))

    def listener_callback(self, msg):
        img = np.reshape(msg.data, (msg.height, msg.width, 3)).astype(np.uint8)
        print("msg")

        plt.gca()
        plt.imshow(img)
        plt.show(block=False)
        plt.pause(0.01)

def main(args=None):
    rclpy.init(args=args)

    camera_view = CameraViewer()

    rclpy.spin(camera_view)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    camera_view.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
