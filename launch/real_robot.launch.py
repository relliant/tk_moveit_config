import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import TimerAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_move_group_launch


def generate_launch_description():
    package_name = 'tk_moveit_config'
    launch_path = os.path.join(get_package_share_directory(package_name), 'launch')

    moveit_config = MoveItConfigsBuilder("humanoid", package_name=package_name).to_moveit_configs()

    # 1. 实机关节状态发布 (来自 bodyctrl SDK)
    joint_state_publisher = Node(
        package='tiangong2pro_urdf',
        executable='joint_state_publisher',
        output='screen',
    )

    # 2. 轨迹桥接节点 (MoveIt ↔ bodyctrl)
    trajectory_bridge = Node(
        package='tk_moveit_config',
        executable='trajectory_bridge',
        output='screen',
    )

    # 3. 机器人状态发布 (TF)
    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_path, 'rsp.launch.py'))
    )

    # 4. MoveIt move_group
    move_group_node = generate_move_group_launch(moveit_config)

    # 5. RViz (延迟5秒等待 move_group 就绪)
    rviz_launch = TimerAction(
        period=5.0,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_path, 'moveit_rviz.launch.py'))
        )]
    )

    return LaunchDescription([
        joint_state_publisher,
        trajectory_bridge,
        rsp_launch,
        move_group_node,
        rviz_launch,
    ])
