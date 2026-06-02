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
