from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument(
            'map_path',
            default_value=PathJoinSubstitution([
                FindPackageShare('pgo'), 'maps', 'map.pcd'
            ]),
        ),
        Node(
            package='fastlio2',
            namespace='fastlio2',
            executable='lio_node',
            name='lio_node',
            output='screen',
            parameters=[{
                'config_path': PathJoinSubstitution([
                    FindPackageShare('fastlio2'), 'config', 'lio.yaml'
                ]),
                'use_sim_time': use_sim_time,
            }],
        ),
        Node(
            package='localizer',
            namespace='localizer',
            executable='localizer_node',
            name='localizer_node',
            output='screen',
            parameters=[
                {'config_path': PathJoinSubstitution([
                    FindPackageShare('localizer'), 'config', 'localizer.yaml'
                ])},
                {'map_path': LaunchConfiguration('map_path')},
                {'use_sim_time': use_sim_time},
            ],
        ),
        Node(
            package='rviz2',
            namespace='localizer',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', PathJoinSubstitution([
                FindPackageShare('localizer'), 'rviz', 'localizer.rviz'
            ])],
            parameters=[{'use_sim_time': use_sim_time}],
            condition=IfCondition(LaunchConfiguration('rviz')),
        ),
    ])
