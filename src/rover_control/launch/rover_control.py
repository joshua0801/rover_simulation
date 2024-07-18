import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Paths to different files and folders
    current_directory = os.getcwd()
    control_yaml = os.path.join(current_directory, 'src/rover_control/config/control.yaml')
    urdf_file = os.path.join(current_directory, 'src/rover_description/urdf/rover.urdf')

    # Start the robot state publisher
    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': urdf_file}]
    )

    # Start the controller manager
    controller_manager_cmd = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[control_yaml],
        output='screen'
    )

    # Load the joint state controller
    load_joint_state_controller_cmd = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_controller'],
        output='screen'
    )

    # Load the differential drive controller
    load_diff_drive_controller_cmd = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['diff_drive_controller'],
        output='screen'
    )

    # Create a LaunchDescription instance
    ld = LaunchDescription()

    # Add actions to the LaunchDescription instance
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(controller_manager_cmd)
    ld.add_action(load_joint_state_controller_cmd)
    ld.add_action(load_diff_drive_controller_cmd)

    return ld
