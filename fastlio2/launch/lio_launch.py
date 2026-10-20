from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    share = FindPackageShare('fastlio2')
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('config_path', default_value=PathJoinSubstitution(
            [share, 'config', 'lio.yaml'])),
        Node(package='fastlio2', namespace='fastlio2', executable='lio_node',
             name='lio_node', output='screen', parameters=[{
                 'config_path': LaunchConfiguration('config_path'),
                 'use_sim_time': LaunchConfiguration('use_sim_time')}]),
        Node(package='rviz2', namespace='fastlio2', executable='rviz2',
             name='rviz2', output='screen', condition=IfCondition(LaunchConfiguration('rviz')),
             arguments=['-d', PathJoinSubstitution([share, 'rviz', 'fastlio2.rviz'])],
             parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]),
    ])
