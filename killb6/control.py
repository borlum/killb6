import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

# Serial
motor1 = serial.Serial("/dev/ttyUSB0")
motor2 = serial.Serial("/dev/ttyUSB1")

class Control(Node):
    def __init__(self):
        super().__init__("killb6_control")
        
        self.subscription = self.create_subscription(
            String,
            "facial_detection/center_point",
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        x,y = msg.data.split(",")

        dx = float(x)

        if dx == 0:
            motor1.write("3".encode())
            motor2.write("3".encode())
        elif dx > 0:
            motor1.write("1".encode())
            motor2.write("2".encode())
        else:
            motor1.write("2".encode())
            motor2.write("1".encode())

def main(args=None):
    rclpy.init(args=args)

    control = Control()

    rclpy.spin(control)

    control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
