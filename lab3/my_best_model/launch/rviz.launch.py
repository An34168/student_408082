import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    package_dir = get_package_share_directory('my_best_model')

    xacro_file = os.path.join(
        package_dir, 'urdf', 'robot_model.xacro'
    )

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description
            }],
            output='screen'
        ),

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            output='screen'
        ),

	Node(
    	    package='rviz2',
    	    executable='rviz2',
            output='screen',
            arguments=[
                '-d',
                '/home/user/ROS_2026/student_408082/lab3/my_best_model/config/robot_view.rviz'
            ]
        )
])
