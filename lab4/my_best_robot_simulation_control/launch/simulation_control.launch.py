
import os
import xacro

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    package_name = 'my_best_robot_simulation_control'
    package_dir = get_package_share_directory(package_name)

    robot_file = os.path.join(
        package_dir, 'urdf', 'robot_model.xacro'
    )

    robot_description = xacro.process_file(robot_file).toxml()

    urdf_file = '/tmp/lab4_robot.urdf'

    with open(urdf_file, 'w') as file:
        file.write(robot_description)

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': '-r empty.sdf'
        }.items()
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }],
        output='screen'
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-file', urdf_file,
            '-name', 'my_best_robot',
            '-z', '0.2'
        ],
        output='screen'
    )

    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen'
    )

    velocity_controller = Node(
    package='controller_manager',
    executable='spawner',
    arguments=[
        'velocity_controller',
        '--controller-manager', '/controller_manager',
        '--param-file',
        os.path.join(package_dir, 'config', 'controllers.yaml')
    ],
    output='screen'
)
    diff_drive = Node(
        package='my_best_robot_simulation_control',
        executable='diff_drive',
        name='diff_drive',
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        TimerAction(
            period=5.0,
            actions=[spawn_robot]
        ),
                TimerAction(
            period=12.0,
            actions=[
                joint_state_broadcaster,
                velocity_controller,
                diff_drive
            ]
        )
    ])
