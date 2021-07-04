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
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        m = msg
        np_img = np.reshape(m.data, (m.height, m.width, 3)).astype(np.uint8)
        plt.cla()
        plt.imshow(np_img)
        plt.pause(0.05)
        plt.show(block=False)

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
