import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

# MoveIt 2.0 Helpers
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_move_group_launch

def generate_launch_description():
    # 1. 定义配置信息和路径
    robot_name = "humanoid" 
    package_name = 'TK_moveit_config'
    moveit_config_path = get_package_share_directory(package_name)
    launch_path = os.path.join(moveit_config_path, 'launch')
    config_path = os.path.join(moveit_config_path, 'config')

    # 2. 加载 MoveIt 配置
    # 这将加载 robot_description, srdf, kinematics.yaml, controllers.yaml 等文件
    moveit_config = MoveItConfigsBuilder(robot_name, package_name=package_name).to_moveit_configs()

    # 3. ROS 2 Control 核心文件路径
    ros2_controllers_file = os.path.join(config_path, "ros2_controllers.yaml")

    # --- ROS 2 Control 启动 (解决执行失败问题) ---

    # 4. 启动 Controller Manager 节点
    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[moveit_config.robot_description, ros2_controllers_file],
        output="screen",
    )

    # 5. 定义控制器启动列表
    # V.I.P: 请根据您的 ros2_controllers.yaml 文件修改此列表!
    controller_names = [
        "joint_state_broadcaster",
        "left_arm_controller",
        "right_arm_controller"
    ]

    # 6. 使用 spawner 启动所有控制器
    controller_spawners = []
    for controller in controller_names:
        controller_spawners.append(
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[controller, "-c", "/controller_manager"],
                output="screen",
            )
        )

    # --- MoveIt / RViz 启动 ---

    # A. 机器人状态发布器 (加载 URDF 并发布TF)
    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_path, 'rsp.launch.py'))
    )

    # B. Move Group 核心节点 (使用 moveit_configs_utils 生成 Node 实例)
    move_group_node = generate_move_group_launch(moveit_config)

    # C. RViz 可视化 (包含原始的 moveit_rviz.launch.py)
    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_path, 'moveit_rviz.launch.py'))
    )

    # D. 引入 TimerAction (解决 RViz 服务连接失败问题)
    # 延迟 5 秒，确保 move_group 及其服务完全注册
    rviz_delay_action = TimerAction(
        period=5.0,
        actions=[rviz_launch]
    )


    # 7. 组合 LaunchDescription
    # 启动顺序: control_node -> rsp -> 控制器 -> move_group -> (延迟) -> rviz
    return LaunchDescription([
        # 核心 ROS 2 Control 节点
        control_node,
        
        # 机器人描述/状态发布
        rsp_launch,
        
        # 启动所有控制器
        *controller_spawners,
        
        # MoveIt 核心
        move_group_node,
        
        # 可视化 (延迟启动)
        rviz_delay_action,
    ])