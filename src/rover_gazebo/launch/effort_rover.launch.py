import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit

from launch_ros.actions import Node

import xacro

def generate_launch_description():
  current_directory = os.getcwd()
  world_file = os.path.join(current_directory, 'src/rover_gazebo/worlds/rover_world.world')
  gazebo = ExecuteProcess(
    cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so', '-s', 'libgazebo_ros_init.so', world_file],
    output='screen'
  )
  
  xacro_file = os.path.join(get_package_share_directory('rover_description'), 'effort_rover.xacro.urdf')

  doc = xacro.parse(open(xacro_file))
  xacro.process_doc(doc)
  params = {'robot_description': doc.toxml()}

  node_robot_state_publisher = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    output='screen',
    parameters=[params]
  )

  spawn_entity = Node(
    package='gazebo_ros',
    executable='spawn_entity.py',
    arguments=['-topic', 'robot_description', '-entity', 'rover'],
    output='screen'
  )
  
  load_joint_state_broadcaster = ExecuteProcess(
    cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
          'joint_state_broadcaster'],
    output='screen'
  )

  start_effort_controller = ExecuteProcess(
    cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
          'effort_controller'],
    output='screen'
  )

  return LaunchDescription([
      RegisterEventHandler(
          event_handler=OnProcessExit(
              target_action=spawn_entity,
              on_exit=[load_joint_state_broadcaster],
          )
      ),
      RegisterEventHandler(
          event_handler=OnProcessExit(
              target_action=load_joint_state_broadcaster,
              on_exit=[start_effort_controller],
          )
      ),
      gazebo,
      node_robot_state_publisher,
      spawn_entity,
  ])
