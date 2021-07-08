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
            "motor/motor_speed_rpm",
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        motor1_rpm, motor2_rpm = msg.data.split(",")

        print(f"MOTOR 1 RPM: {motor1_rpm}")
        print(f"MOTOR 2 RPM: {motor2_rpm}")

        motor1.write(f"{motor1_rpm}\n".encode())
        motor2.write(f"{motor2_rpm}\n".encode())


def main(args=None):
    rclpy.init(args=args)

    control = Control()

    rclpy.spin(control)

    control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
