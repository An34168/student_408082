#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import math
from lab2_interfaces.srv import A408082

class ServiceServer(Node):
    def __init__(self):
        super().__init__('service_server')
        self.srv = self.create_service(A408082, 'calculate_navigation', self.navigation_callback)
        self.targets = [(3.0, 3.0), (8.0, 3.0), (8.0, 8.0), (3.0, 8.0)]
        self.current_target_index = 0
        self.get_logger().info(f"Servidor listo. Primer objetivo: {self.targets[self.current_target_index]}")

    def navigation_callback(self, request, response):
        if self.current_target_index >= len(self.targets):
            response.distance = 0.0
            response.angle = 0.0
            response.success = True
            return response
        target_x, target_y = self.targets[self.current_target_index]
        dx = target_x - request.x_current
        dy = target_y - request.y_current
        distance = math.sqrt(dx**2 + dy**2)
        response.distance = distance
        response.angle = math.atan2(dy, dx)
        if distance < 0.1:
            response.success = True
            self.current_target_index += 1
        else:
            response.success = False
        return response

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(ServiceServer())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
