from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    rviz_config = PathJoinSubstitution(
        [FindPackageShare('pgo'), 'rviz', 'pgo.rviz']
    )
    pgo_config = PathJoinSubstitution(
        [FindPackageShare('pgo'), 'config', 'pgo.yaml']
    )
    lio_config = PathJoinSubstitution(
        [FindPackageShare('fastlio2'), 'config', 'lio.yaml']
    )

    use_sim_time = LaunchConfiguration('use_sim_time')
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('rviz', default_value='false'),
        Node(
            package='fastlio2',
            namespace='fastlio2',
            executable='lio_node',
            name='lio_node',
            output='screen',
            parameters=[{
                'config_path': lio_config,
                'use_sim_time': use_sim_time,
            }],
        ),
        Node(
            package='pgo',
            namespace='pgo',
            executable='pgo_node',
            name='pgo_node',
            output='screen',
            parameters=[{
                'config_path': pgo_config,
                'use_sim_time': use_sim_time,
            }],
        ),
        Node(
            package='rviz2',
            namespace='pgo',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': use_sim_time}],
            condition=IfCondition(LaunchConfiguration('rviz')),
        ),
    ])
