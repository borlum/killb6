import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from curtsies import Input
import serial

# Serial
motor1 = serial.Serial("/dev/ttyUSB0")
motor2 = serial.Serial("/dev/ttyUSB1")

# Define controls
controls = {}
controls['KEY_UP'] = 'F'
controls['KEY_DOWN'] = 'B'
controls['KEY_RIGHT'] = 'R'
controls['KEY_LEFT'] = 'L'

class ManualControl(Node):

    def __init__(self):
        super().__init__("killb6_manual_control")
        self.publisher_ = self.create_publisher(String, "topic", 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        self.run()

    def timer_callback(self):
        msg = String()
        msg.data = "Hello World: %d" % self.i
        self.publisher_.publish(msg)
        self.get_logger().info("Publishing: %s" % msg.data)
        self.i += 1

    def run(self):
        with Input(keynames='curses') as input_generator:
            for e in input_generator:
                if e in controls.keys():
                    if e == "KEY_UP":
                        motor1.write("1".encode())
                        motor2.write("1".encode())
                    if e == "KEY_DOWN":
                        motor1.write("3".encode())
                        motor2.write("3".encode())
                    if e == "KEY_LEFT":
                        motor1.write("1".encode())
                        motor2.write("3".encode())
                    if e == "KEY_RIGHT":
                        motor1.write("3".encode())
                        motor2.write("1".encode())

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
