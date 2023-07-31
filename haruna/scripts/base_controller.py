#!/usr/bin/env python3

import math
import rospy
import tf2_ros
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64


TOPIC_NAME_CMD_VEL = '/cmd_vel'
TIMEOUT_CMD_VEL_SEC = 0.3

TOPIC_NAME_JOINT_STATES = '/joint_states'

PARAM_NAME_RATE = '~rate'
DEFAULT_RATE = 50

PARAM_NAME_VEL_LIMIT_LINEAR = '~vel_limit_linear'
DEFAULT_VEL_LIMIT_LINEAR = float("inf")

PARAM_NAME_VEL_LIMIT_ANGULAR = '~vel_limit_angular'
DEFAULT_VEL_LIMIT_ANGULAR = float("inf")

PARAM_NAME_ACC_LIMIT_LINEAR = '~acc_limit_linear'
DEFAULT_ACC_LIMIT_LINEAR = 2.0

PARAM_NAME_ACC_LIMIT_ANGULAR = '~acc_limit_angular'
DEFAULT_ACC_LIMIT_ANGULAR = 4.0

TREAD_WIDTH = 0.3441
WHEEL_RADIUS = 0.17 / 2.0

class BaseController:
    def __init__(self, lim_vel_linear, lim_vel_angular, lim_acc_linear, lim_acc_angular):
        self._vel_linear = 0.0
        self._vel_angular = 0.0
        self._last_vel_linear = 0.0
        self._last_vel_angular = 0.0
        self._velocity_updated_timestamp = rospy.Time()
        self._left_wheel_motor_velocity_publisher = rospy.Publisher('/left_wheel_motor_velocity_controller/command', Float64, queue_size=1)
        self._right_wheel_motor_velocity_publisher = rospy.Publisher('/right_wheel_motor_velocity_controller/command', Float64, queue_size=1)
        self._lim_vel_linear = lim_vel_linear
        self._lim_vel_angular = lim_vel_angular
        self._lim_acc_linear = lim_acc_linear
        self._lim_acc_angular = lim_acc_angular

    def update_velocity(self, vel_linear: float, vel_angular: float):
        self._vel_linear = clamp(vel_linear, -self._lim_vel_linear, self._lim_vel_linear)
        self._vel_angular = clamp(vel_angular, -self._lim_vel_angular, self._lim_vel_angular)

        self._velocity_updated_timestamp = rospy.Time.now()

    def proc(self, dt: float):
        vel_linear = self._vel_linear
        vel_angular = self._vel_angular

        if (rospy.Time.now() - self._velocity_updated_timestamp >= rospy.Duration.from_sec(TIMEOUT_CMD_VEL_SEC)):
            self._vel_linear = 0.0
            self._vel_angular = 0.0
            vel_linear = 0.0
            vel_angular = 0.0

        vel_linear = clamp(vel_linear, self._last_vel_linear - self._lim_acc_linear * dt, self._last_vel_linear + self._lim_acc_linear * dt)
        vel_angular = clamp(vel_angular, self._last_vel_angular - self._lim_acc_angular * dt, self._last_vel_angular + self._lim_acc_angular * dt)

        vel_left = vel_linear - vel_angular * TREAD_WIDTH / 2
        vel_right = vel_linear + vel_angular * TREAD_WIDTH / 2
        self._left_wheel_motor_velocity_publisher.publish(Float64(vel_left / WHEEL_RADIUS))
        self._right_wheel_motor_velocity_publisher.publish(Float64(-vel_right / WHEEL_RADIUS))

        self._last_vel_linear = vel_linear
        self._last_vel_angular = vel_angular


class Odom:
    def __init__(self):
        self._tf_broadcaster = tf2_ros.TransformBroadcaster()
        self._odom_publisher = rospy.Publisher('/odom', Odometry, queue_size=1)
        self._frame_id = 'odom'
        self._child_frame_id = 'base_link'

        self._dist_left = 0.0
        self._dist_right = 0.0
        self._vel_left = 0.0
        self._vel_right = 0.0
        self._vel_linear = 0.0
        self._vel_angular = 0.0

        self._pos_x = 0.0
        self._pos_y = 0.0
        self._orientation_yaw = 0.0

    def update_state(self, dist_left: float, dist_right: float, vel_left: float, vel_right: float):
        self._dist_left = dist_left
        self._dist_right = dist_right
        self._vel_left = vel_left
        self._vel_right = vel_right

    def proc(self, dt: float):
        self._orientation_yaw = -(self._dist_left + self._dist_right) * WHEEL_RADIUS / TREAD_WIDTH
        self._vel_linear = (self._vel_left - self._vel_right) / 2 * WHEEL_RADIUS
        self._vel_angular = -(self._vel_left + self._vel_right) * WHEEL_RADIUS / TREAD_WIDTH
        self._pos_x += self._vel_linear * math.cos(self._orientation_yaw) * dt
        self._pos_y += self._vel_linear * math.sin(self._orientation_yaw) * dt

        self._send_transform()
        self._send_odom()
    
    def _send_transform(self):
        tf = TransformStamped()
        tf.header.frame_id = self._frame_id
        tf.header.stamp = rospy.Time.now()
        tf.child_frame_id = 'hoge_link'
        tf.transform.translation.x = self._pos_x
        tf.transform.translation.y = self._pos_y
        tf.transform.rotation.z = math.sin(self._orientation_yaw / 2)
        tf.transform.rotation.w = math.cos(self._orientation_yaw / 2)
        self._tf_broadcaster.sendTransform(tf)

    def _send_odom(self):
        odom_quat = quaternion_from_euler(0.0, 0.0, self._orientation_yaw)
        odom = Odometry()
        odom.header.stamp = rospy.Time.now()
        odom.header.frame_id = self._frame_id
        odom.child_frame_id = self._child_frame_id
        odom.pose.pose.position.x = self._pos_x
        odom.pose.pose.position.y = self._pos_y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.x = odom_quat[0]
        odom.pose.pose.orientation.y = odom_quat[1]
        odom.pose.pose.orientation.z = odom_quat[2]
        odom.pose.pose.orientation.w = odom_quat[3]
        odom.pose.covariance = [
            pow(0.00017, 2), 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, pow(0.00017, 2), 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, pow(0.00017, 2), 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 1000000.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 1000000.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 1000.0
        ]
        odom.twist.twist.linear.x = self._vel_linear * math.cos(self._orientation_yaw)
        odom.twist.twist.linear.y = self._vel_linear * math.sin(self._orientation_yaw)
        odom.twist.twist.angular.z = self._vel_angular
        odom.twist.covariance = [
            pow(0.00017, 2), 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, pow(0.00017, 2), 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, pow(0.00017, 2), 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, pow(0.00017, 2), 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, pow(0.00017, 2), 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.001,
        ]
        self._odom_publisher.publish(odom)


def clamp(n, smallest, largest):
        return max(smallest, min(n, largest))

if __name__ == '__main__':
    rospy.init_node('controller')

    rate_hz = float(rospy.get_param(PARAM_NAME_RATE, DEFAULT_RATE))

    lim_vel_linear = float(rospy.get_param(PARAM_NAME_VEL_LIMIT_LINEAR, DEFAULT_VEL_LIMIT_LINEAR))
    lim_vel_angular = float(rospy.get_param(PARAM_NAME_VEL_LIMIT_ANGULAR, DEFAULT_VEL_LIMIT_ANGULAR))

    lim_acc_linear = float(rospy.get_param(PARAM_NAME_ACC_LIMIT_LINEAR, DEFAULT_ACC_LIMIT_LINEAR))
    lim_acc_angular = float(rospy.get_param(PARAM_NAME_ACC_LIMIT_ANGULAR, DEFAULT_ACC_LIMIT_ANGULAR))

    base = BaseController(lim_vel_linear, lim_vel_angular, lim_acc_linear, lim_acc_angular)
    odom = Odom()

    cmd_vel_subscriber = rospy.Subscriber(
        TOPIC_NAME_CMD_VEL, Twist,
        lambda cmd_vel: base.update_velocity(cmd_vel.linear.x, cmd_vel.angular.z))

    joint_states_subscriber = rospy.Subscriber(
        TOPIC_NAME_JOINT_STATES, JointState,
        lambda joint_state: odom.update_state(joint_state.position[0], joint_state.position[1], joint_state.velocity[0], joint_state.velocity[1]))

    rate = rospy.Rate(rate_hz)
    while not rospy.is_shutdown():
        base.proc(1.0 / rate_hz)
        odom.proc(1.0 / rate_hz)
        rate.sleep()
