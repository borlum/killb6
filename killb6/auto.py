import rclpy
import numpy as np
from rclpy.node import Node
from std_msgs.msg import String

# Define controls
speed = 200
turn_speed = 100
fire = 1000



class AutoControl(Node):

    def __init__(self):
        super().__init__("killb6_auto_control")
        self.publisher_ = self.create_publisher(String, "motor/motor_speed_rpm", 1)
        
        self.subscription = self.create_subscription(
            String,
            "facial_detection/center_point",
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        
        self.i = 0

    def listener_callback(self, msg):
        x,y,d = msg.data.split(",")
        
        msg = String()
        msg.data = "100,-100"
        
        if int(d) > 0:
            x = float(x)
            if np.abs(x) < 25:
                msg.data = "1000,1000"
            else:
                speed = np.sign(x) * np.minimum(3 * np.abs(x), 150)
                msg.data = f"{speed}, {-speed}"

        print(msg.data)
        self.publisher_.publish(msg)
        

def main(args=None):
    rclpy.init(args=args)

    auto_control = AutoControl()

    rclpy.spin(auto_control)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    auto_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
