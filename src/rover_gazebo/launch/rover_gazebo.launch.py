import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch_ros.actions import Node

import xacro

def generate_launch_description():
    # Paths to different files and folders
    current_directory = os.getcwd()
    world_file = os.path.join(current_directory, 'src/rover_gazebo/worlds/rover_world.world')
    urdf_file = os.path.join(current_directory, 'src/rover_description/urdf/rover.xacro.urdf')
    control_yaml = os.path.join(current_directory, 'src/rover_control/config/rover_control.yaml')

    # Launch configuration variables
    world = DeclareLaunchArgument(
        'world',
        default_value=world_file,
        description='Path to Gazebo world file'
    )
    
    doc = xacro.parse(open(urdf_file))
    xacro.process_doc(doc)
    params = {'robot_description': doc.toxml()}

    # Start Gazebo server with the specified world file and plugin
    start_gazebo_server = ExecuteProcess(
        cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so', '-s', 'libgazebo_ros_init.so', world_file],
        output='screen'
    )
    state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )
    urdf_spawner = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'rover'],
        output='screen',
    )
    control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        output='screen',
        parameters=[control_yaml]
    )

    # Create a LaunchDescription instance
    ld = LaunchDescription()

    # Add actions to the LaunchDescription instance
    ld.add_action(world)
    ld.add_action(start_gazebo_server)
    ld.add_action(state_publisher)
    ld.add_action(urdf_spawner)
    ld.add_action(control_node)

    return ld
