from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    isu_id = "408082"
    
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            namespace=f'ns1_{isu_id}',
            output='screen'
        ),
        Node(
            package='mybestcontroller',
            executable='lab1_controller',
            namespace=f'ns1_{isu_id}',
            output='screen'
        ),
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            namespace=f'ns2_{isu_id}',
            output='screen'
        ),
        Node(
            package='mybestcontroller',
            executable='lab1_controller',
            namespace=f'ns2_{isu_id}',
            output='screen'
        ),
    ])