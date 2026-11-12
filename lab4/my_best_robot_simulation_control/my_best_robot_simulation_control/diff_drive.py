
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray


class DiffDrive(Node):

    def __init__(self):
        super().__init__('diff_drive')

        self.wheel_radius = 0.1
        self.wheel_separation = 0.164

        self.publisher = self.create_publisher(
            Float64MultiArray,
            '/velocity_controller/commands',
            10
        )

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        self.get_logger().info(
            'DiffDrive iniciado - Variante 2'
        )

    def cmd_vel_callback(self, msg):
        v = msg.linear.x
        omega = msg.angular.z

        left = (
            v - omega * self.wheel_separation / 2
        ) / self.wheel_radius

        right = (
            v + omega * self.wheel_separation / 2
        ) / self.wheel_radius

        command = Float64MultiArray()
        command.data = [left, right]

        self.publisher.publish(command)


def main(args=None):
    rclpy.init(args=args)

    node = DiffDrive()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

