#!/usr/bin/env python3
"""
trajectory_bridge.py

Bridges MoveIt FollowJointTrajectory actions to the real robot's
bodyctrl_msgs topics (/arm/cmd_pos).

Action servers provided:
  /left_arm_controller/follow_joint_trajectory
  /right_arm_controller/follow_joint_trajectory
"""
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from control_msgs.action import FollowJointTrajectory
from bodyctrl_msgs.msg import CmdSetMotorPosition, SetMotorPosition

# Joint name → motor ID (arms only)
JOINT_TO_MOTOR_ID = {
    'shoulder_pitch_l_joint': 11, 'shoulder_roll_l_joint': 12, 'shoulder_yaw_l_joint': 13,
    'elbow_pitch_l_joint': 14,    'elbow_yaw_l_joint': 15,
    'wrist_pitch_l_joint': 16,    'wrist_roll_l_joint': 17,
    'shoulder_pitch_r_joint': 21, 'shoulder_roll_r_joint': 22, 'shoulder_yaw_r_joint': 23,
    'elbow_pitch_r_joint': 24,    'elbow_yaw_r_joint': 25,
    'wrist_pitch_r_joint': 26,    'wrist_roll_r_joint': 27,
}

# Per-joint speed (rad/s) and current (A) limits sent to hardware
DEFAULT_SPD = 0.2
DEFAULT_CUR = 8.0


class TrajectoryBridge(Node):
    def __init__(self):
        super().__init__('trajectory_bridge')
        self.arm_pub = self.create_publisher(CmdSetMotorPosition, '/arm/cmd_pos', 10)

        self._left_server = ActionServer(
            self, FollowJointTrajectory,
            '/left_arm_controller/follow_joint_trajectory',
            execute_callback=self._execute,
            goal_callback=lambda _: GoalResponse.ACCEPT,
            cancel_callback=lambda _: CancelResponse.ACCEPT,
        )
        self._right_server = ActionServer(
            self, FollowJointTrajectory,
            '/right_arm_controller/follow_joint_trajectory',
            execute_callback=self._execute,
            goal_callback=lambda _: GoalResponse.ACCEPT,
            cancel_callback=lambda _: CancelResponse.ACCEPT,
        )
        self.get_logger().info('TrajectoryBridge ready.')

    def _execute(self, goal_handle):
        traj = goal_handle.request.trajectory
        joint_names = traj.joint_trajectory.joint_names
        points = traj.joint_trajectory.points

        t_start = time.monotonic()
        for i, point in enumerate(points):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return FollowJointTrajectory.Result()

            # Sleep until this point's time_from_start
            t_target = t_start + point.time_from_start.sec + point.time_from_start.nanosec * 1e-9
            sleep_dur = t_target - time.monotonic()
            if sleep_dur > 0:
                time.sleep(sleep_dur)

            # Build and publish motor command
            msg = CmdSetMotorPosition()
            msg.header.stamp = self.get_clock().now().to_msg()
            for name, pos in zip(joint_names, point.positions):
                if name in JOINT_TO_MOTOR_ID:
                    cmd = SetMotorPosition()
                    cmd.name = JOINT_TO_MOTOR_ID[name]
                    cmd.pos = float(pos)
                    cmd.spd = DEFAULT_SPD
                    cmd.cur = DEFAULT_CUR
                    msg.cmds.append(cmd)
            self.arm_pub.publish(msg)

            # Publish feedback
            fb = FollowJointTrajectory.Feedback()
            fb.joint_names = joint_names
            fb.desired = point
            goal_handle.publish_feedback(fb)

        goal_handle.succeed()
        return FollowJointTrajectory.Result()


def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
