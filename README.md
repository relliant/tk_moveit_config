# tk_moveit_config

该项目为天工人形机器人 MoveIt 配置包，运行时依赖 `walker_tienkung_ei_description` 项目中的机器人描述文件。

## 依赖说明

- 依赖项目：`walker_tienkung_ei_description`
- 获取地址：https://github.com/Open-X-Humanoid/TienKung_URDF

请将 `tk_moveit_config` 与 `walker_tienkung_ei_description` 放在同一个 ROS 2 工作空间目录下（同级目录）。

## 目录示例

```text
<your_ws>/
├── src/
│   ├── tk_moveit_config
│   └── walker_tienkung_ei_description
```

## 构建与运行

在工作空间根目录执行：

```bash
cd <your_ws>
colcon build
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

然后确认 `walker_tienkung_ei_description` 位于与 `tk_moveit_config` 同级目录后，再进行 `colcon build`。
