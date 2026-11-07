
#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node
from turtlesim_msgs.msg import Pose
from geometry_msgs.msg import Twist
from lab2_interfaces.srv import A408082


class ServiceClient(Node):
    def __init__(self):
        super().__init__('service_client')

        self.client = self.create_client(
            A408082, 'calculate_navigation'
        )

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando al servidor...')

        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10
        )

        self.cmd_pub = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )

        self.current_pose = None
        self.target_distance = 0.0
        self.target_angle = 0.0
        self.goal_reached = False
        self.state = "REQUEST"

        self.timer = self.create_timer(0.1, self.control_loop)

    def pose_callback(self, msg):
        self.current_pose = msg

    def send_request(self):
        self.cmd_pub.publish(Twist())

        req = A408082.Request()
        req.x_current = self.current_pose.x
        req.y_current = self.current_pose.y

        self.state = "WAITING"
        future = self.client.call_async(req)
        future.add_done_callback(self.handle_response)

    def handle_response(self, future):
        try:
            res = future.result()
        except Exception as e:
            self.get_logger().error(f'Error del servicio: {e}')
            self.state = "REQUEST"
            return

        self.target_distance = res.distance
        self.target_angle = res.angle
        self.goal_reached = res.success

        if self.goal_reached and self.target_distance == 0.0:
            self.state = "FINISHED"
            self.get_logger().info('Mision completada')
        elif self.goal_reached:
            self.state = "REQUEST"
        else:
            self.state = "ROTATE"

    def control_loop(self):
        if self.current_pose is None:
            return

        if self.state == "REQUEST":
            self.send_request()

        elif self.state == "WAITING":
            return

        elif self.state == "ROTATE":
            err = self.target_angle - self.current_pose.theta
            err = math.atan2(math.sin(err), math.cos(err))

            twist = Twist()

            if abs(err) > 0.05:
                twist.angular.z = max(-2.0, min(2.0, 4.0 * err))
                self.cmd_pub.publish(twist)
            else:
                self.cmd_pub.publish(Twist())
                self.state = "MOVE"

        elif self.state == "MOVE":
            twist = Twist()

            if self.target_distance > 0.1:
                twist.linear.x = 1.5 * min(
                    self.target_distance, 1.0
                )
                self.cmd_pub.publish(twist)

            self.state = "REQUEST"

        elif self.state == "FINISHED":
            self.cmd_pub.publish(Twist())
            self.timer.cancel()


def main(args=None):
    rclpy.init(args=args)
    node = ServiceClient()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
