#!/usr/bin/env python3

import math
import rospy
import tf2_ros
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64
from base_controller import Odometry, BaseController


TOPIC_NAME_CMD_VEL = '/cmd_vel'
TIMEOUT_CMD_VEL_SEC = 0.3

TOPIC_NAME_JOINT_STATES = '/joint_states'

PARAM_NAME_RATE = '~rate'
DEFAULT_RATE = 50

ACCELERATION_LIMIT_LINEAR = 1.0
ACCELERATION_LIMIT_ANGULAR = 2.0

VELOCITY_LIMIT_LINEAR = 0.1
VELOCITY_LIMIT_ANGULAR = 0.2

TREAD_WIDTH = 0.3441
WHEEL_RADIUS = 0.17 / 2.0


class LimitedBaseController(BaseController):
    def update_limited_velocity(self, vel_linear: float, vel_angular: float):
        self.update_velocity(vel_linear, vel_angular)
        if self._vel_linear > VELOCITY_LIMIT_LINEAR:
            self._vel_linear = VELOCITY_LIMIT_LINEAR
        elif self._vel_linear < -VELOCITY_LIMIT_LINEAR:
            self._vel_linear = -VELOCITY_LIMIT_LINEAR
        if self._vel_angular > VELOCITY_LIMIT_ANGULAR:
            self._vel_angular = VELOCITY_LIMIT_ANGULAR
        elif self._vel_angular < -VELOCITY_LIMIT_ANGULAR:
            self._vel_angular = -VELOCITY_LIMIT_ANGULAR


if __name__ == '__main__':
    rospy.init_node('controller')

    rate_hz = float(rospy.get_param(PARAM_NAME_RATE, DEFAULT_RATE))

    base = LimitedBaseController()
    odom = Odometry()

    cmd_vel_subscriber = rospy.Subscriber(
        TOPIC_NAME_CMD_VEL, Twist,
        lambda cmd_vel: base.update_limited_velocity(cmd_vel.linear.x, cmd_vel.angular.z))

    joint_states_subscriber = rospy.Subscriber(
        TOPIC_NAME_JOINT_STATES, JointState,
        lambda joint_state: odom.update_state(joint_state.position[0], joint_state.position[1], joint_state.velocity[0], joint_state.velocity[1]))

    rate = rospy.Rate(rate_hz)
    while not rospy.is_shutdown():
        base.proc(1.0 / rate_hz)
        odom.proc(1.0 / rate_hz)
        rate.sleep()
