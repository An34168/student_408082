
import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'my_best_robot_simulation_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')
        ),
        (
            os.path.join('share', package_name, 'urdf'),
            glob('urdf/*')
        ),
        (
            os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='An34168',
    maintainer_email='anahicoraquilla234@gmail.com',
    description='ROS 2 robot simulation and control - Lab 4',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'diff_drive = my_best_robot_simulation_control.diff_drive:main',
        ],
    },
)
