# tk_moveit_config

该项目为天工人形机器人 MoveIt 配置包，运行时依赖 `walker_tienkung_ei_description` 项目中的机器人描述文件。

## 依赖说明

- 依赖项目：`walker_tienkung_ei_description`
- 获取地址：https://github.com/Open-X-Humanoid/TienKung_URDF

## 构建与运行

在工作空间根目录执行：

```bash
cd <your_ws>
colcon build

# 实际启动前，需要依次加载两个工作空间环境
cd ~/lsy_ws/Humanoid/UBitech/Walker-TienKung-URDF
source install/setup.bash

cd ~/lsy_ws/Humanoid/UBitech/Walker-TienKung-URDF/ros
source install/setup.bash

ros2 launch tk_moveit_config start.launch.py
```

执行后将启动 MoveIt。

## 快速获取依赖仓库（可选）

如果你还没有 `walker_tienkung_ei_description`，可在 `src` 目录中克隆：

```bash
cd <your_ws>/src
git clone https://github.com/Open-X-Humanoid/TienKung_URDF.git
```


## Walker-TienKung-URDF 文件夹结构

路径：`~/lsy_ws/Humanoid/UBitech/Walker-TienKung-URDF`

### 工作空间目录

```text
Walker-TienKung-URDF/
├── ros/tk_moveit_config/
│   ├── config/
│   └── launch/
└── walker_tienkung_ei_description/
	├── urdf/
	├── meshes/
	└── launch/
```

## Troubleshooting

### 1) MoveIt 启动后看不到 MotionPlanning 或只能在仿真中动

- 问题
	- 直接启动后，MotionPlanning 模块可能未正常加载，或者只能通过运动学方法看到关节角控制。
- 原因
	- 启动顺序问题：move_group 启动时间过长，rviz 界面先加载完成，导致参数没有被正确传入。
- 解决方案
	- 在 RViz 的 Displays 中删除 MotionPlanning 项。
	- 点击 Add 重新加载 MotionPlanning。
	- 维持当前启动顺序控制思路（先核心节点，后 RViz）。

### 2) Plan 能看到轨迹，但 Execute 无法执行

- 问题
	- 点击 Plan 可以看到规划轨迹，但规划速度很慢，点击 Execute 无法执行轨迹。
- 原因
	- MoveIt 与 ros2_control 配置不匹配，导致 controller 启动失败，无法建立正常控制器通信。
- 解决方案
	- 检查 config/moveit_controllers.yaml：控制器类型应为 FollowJointTrajectory，action_ns 设为 follow_joint_trajectory。
	- 检查 config/humanoid.urdf.xacro：xacro:humanoid_ros2_control 的 name 与 mode 设置应与实际硬件/仿真一致。
	- 检查 config/ros2_controllers.yaml：controller type 与参数需匹配；command_interfaces 应包含 position，state_interfaces 应至少包含 position 和 velocity。
