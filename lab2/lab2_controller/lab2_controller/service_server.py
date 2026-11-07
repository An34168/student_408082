
#!/usr/bin/env python3

import math

import rclpy
from lab2_interfaces.srv import A408082
from rclpy.node import Node


class ServiceServer(Node):

    def __init__(self):
        super().__init__('service_server')

        self.srv = self.create_service(
            A408082,
            'calculate_navigation',
            self.navigation_callback
        )

        self.targets = [
            (2.0, 3.0),
            (4.0, 2.0),
            (5.0, 4.0)
        ]

        self.current_target_index = 0

        self.get_logger().info(
            'Servidor listo. Primer objetivo: '
            f'{self.targets[self.current_target_index]}'
        )

    def navigation_callback(self, request, response):
        if self.current_target_index >= len(self.targets):
            response.distance = 0.0
            response.angle = 0.0
            response.success = True
            return response

        target_x, target_y = self.targets[self.current_target_index]

        dx = target_x - request.x_current
        dy = target_y - request.y_current

        distance = math.sqrt(dx ** 2 + dy ** 2)

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

    node = ServiceServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
