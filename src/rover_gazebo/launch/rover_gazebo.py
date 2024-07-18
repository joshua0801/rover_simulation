import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    # Paths to different files and folders
    current_directory = os.getcwd()
    world_file = os.path.join(current_directory, 'src/rover_gazebo/worlds/rover_world.world')
    urdf_file = os.path.join(current_directory, 'src/rover_description/urdf/rover.urdf')

    # Launch configuration variables
    world = DeclareLaunchArgument(
        'world',
        default_value=world_file,
        description='Path to Gazebo world file'
    )

    # Start Gazebo server with the specified world file and plugin
    start_gazebo_server = ExecuteProcess(
        cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so', '-s', 'libgazebo_ros_init.so', world_file],
        output='screen'
    )

    # Spawn URDF model into Gazebo
    spawn_urdf = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'rover', '-file', urdf_file, '-x', '0', '-y', '0', '-z', '0.1'],
        output='screen',
    )

    # Create a LaunchDescription instance
    ld = LaunchDescription()

    # Add actions to the LaunchDescription instance
    ld.add_action(world)
    ld.add_action(start_gazebo_server)
    ld.add_action(spawn_urdf)

    return ld
