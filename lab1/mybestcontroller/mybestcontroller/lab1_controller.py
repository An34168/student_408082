#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Float32
import math
import time

ISU_ID = "408082"

class Lab1Controller(Node):
    def __init__(self):
        super().__init__('lab1_controller')
        
        ns = self.get_namespace()
        self.get_logger().info(f"Iniciado en namespace: {ns}")
        
        if f"ns1_{ISU_ID}" in ns:
            self.turtle_type = "leader"
        elif f"ns2_{ISU_ID}" in ns:
            self.turtle_type = "follower"
        else:
            self.turtle_type = "leader"

        self.current_pose = None
        self.leader_pose = None

        self.pose_sub = self.create_subscription(Pose, 'turtle1/pose', self.pose_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        if self.turtle_type == "follower":
            self.leader_sub = self.create_subscription(
                Pose, f'/ns1_{ISU_ID}/turtle1/pose', self.leader_pose_callback, 10
            )

        if self.turtle_type == "leader":
            self.result_pub = self.create_publisher(Float32, f'/result_{ISU_ID}', 10)
            self.target_points = [(2.0, 2.0), (5.0, 2.0), (5.0, 5.0), (2.0, 5.0)]
            self.current_target_idx = 0
            self.start_time = time.time()
            self.finished = False

        self.timer = self.create_timer(0.05, self.control_loop)

    def pose_callback(self, msg):
        self.current_pose = msg

    def leader_pose_callback(self, msg):
        self.leader_pose = msg

    def control_loop(self):
        if self.current_pose is None:
            return

        twist = Twist()

        if self.turtle_type == "leader" and not self.finished:
            if self.current_target_idx < len(self.target_points):
                target_x, target_y = self.target_points[self.current_target_idx]
                dx = target_x - self.current_pose.x
                dy = target_y - self.current_pose.y
                distance = math.sqrt(dx**2 + dy**2)
                
                angle_to_target = math.atan2(dy, dx)
                angle_diff = angle_to_target - self.current_pose.theta
                angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))

                if distance > 0.2:
                    twist.linear.x = min(1.5, 1.5 * distance)
                    twist.angular.z = 4.0 * angle_diff
                else:
                    self.current_target_idx += 1
            else:
                elapsed_time = time.time() - self.start_time
                res_msg = Float32()
                res_msg.data = float(elapsed_time)
                self.result_pub.publish(res_msg)
                self.get_logger().info(f"Meta alcanzada en {elapsed_time:.2f} segundos.")
                self.finished = True

        elif self.turtle_type == "follower" and self.leader_pose is not None:
            dx = self.leader_pose.x - self.current_pose.x
            dy = self.leader_pose.y - self.current_pose.y
            distance = math.sqrt(dx**2 + dy**2)

            angle_to_leader = math.atan2(dy, dx)
            angle_diff = angle_to_leader - self.current_pose.theta
            angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))

            if distance > 0.8:
                twist.linear.x = min(1.5, 1.2 * (distance - 0.8))
                twist.angular.z = 4.0 * angle_diff
            else:
                twist.linear.x = 0.0
                twist.angular.z = 0.0

        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = Lab1Controller()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()