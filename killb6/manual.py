import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import time

from curtsies import Input

# Define controls
speed = 200
turn_speed = 100
fire = 1000

controls = {}
controls['KEY_UP'] = '%d, %d' % (speed, speed)
controls['KEY_DOWN'] = '%d, %d' % (-speed, -speed)
controls['KEY_RIGHT'] = '%d, %d' % (turn_speed, -turn_speed)
controls['KEY_LEFT'] = '%d, %d' % (-turn_speed,  turn_speed)
controls['f'] = '%d, %d' % (fire, fire)
controls['s'] = '%d, %d' % (0, 0)

class ManualControl(Node):

    def __init__(self):
        super().__init__("killb6_manual_control")
        self.publisher_ = self.create_publisher(String, "motor/motor_speed_rpm", 1)
        self.i = 0

        self.run()


    def run(self):
        with Input(keynames='curses') as input_generator:
            for e in input_generator:
                if e in controls.keys():
                    msg = String()
                    msg.data = controls[e]
                    print("sending:")
                    print(msg.data)
                    self.publisher_.publish(msg)

            time.sleep(1)

def main(args=None):
    rclpy.init(args=args)

    manual_control = ManualControl()

    rclpy.spin(manual_control)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    manual_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
