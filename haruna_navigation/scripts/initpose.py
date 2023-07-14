#!/usr/bin/env python3

import rospy
import tf
import tf2_ros
from std_msgs.msg import Header
from geometry_msgs.msg import Transform
from geometry_msgs.msg import PoseWithCovarianceStamped

def transform_to_homogeneous_matrix(tfobj: Transform):
    tfeul= tf.transformations.euler_from_quaternion(
        [
            tfobj.rotation.x,
            tfobj.rotation.y,
            tfobj.rotation.z,
            tfobj.rotation.w
            ],
        axes='sxyz')

    tftrans = [ tfobj.translation.x,tfobj.translation.y,tfobj.translation.z]
    tfobjmatrix = tf.transformations.compose_matrix(angles=tfeul,translate=tftrans)

    return  tfobjmatrix

def homogeneous_to_transform(Mat):
    scale, shear, angles, trans, persp = tf.transformations.decompose_matrix(Mat)
    quat = tf.transformations.quaternion_from_euler(angles[0],angles[1],angles[2])
    tfobj = Transform()
    tfobj.rotation.x = quat[0]
    tfobj.rotation.y = quat[1]
    tfobj.rotation.z = quat[2]
    tfobj.rotation.w = quat[3]
    tfobj.translation.x = trans[0]
    tfobj.translation.y = trans[1]
    tfobj.translation.z = trans[2]
    return tfobj

def transform_dot(tf1: Transform, tf2: Transform):
    tf1M = transform_to_homogeneous_matrix(tf1)
    tf2M = transform_to_homogeneous_matrix(tf2)
    return  homogeneous_to_transform(tf2M.dot(tf1M))


if __name__ == '__main__':
    rospy.init_node('aruco_initializer')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=10)

    while not rospy.is_shutdown():
        try: 
            trans_aruco_to_base = tfBuffer.lookup_transform('base_link', 'aruco_marker_frame', rospy.Time.now(), rospy.Duration(1.0))
        except (
            tf2_ros.LookupException,
            tf2_ros.ConnectivityException,
            tf2_ros.ExtrapolationException,
        ):
            continue

        try: 
            trans_aruco_init = tfBuffer.lookup_transform('aruco_init_frame', 'map', rospy.Time.now(), rospy.Duration(1.0))
        except (
            tf2_ros.LookupException,
            tf2_ros.ConnectivityException,
            tf2_ros.ExtrapolationException,
        ):
            continue

        initial_pose = PoseWithCovarianceStamped()
        initial_pose.header = Header()
        initial_pose.header.stamp = rospy.Time.now()
        initial_pose.header.frame_id = 'map'

        initial_trans = transform_dot(trans_aruco_init.transform, trans_aruco_to_base.transform)

        initial_pose.pose.pose.position.x = initial_trans.translation.x
        initial_pose.pose.pose.position.y = initial_trans.translation.y
        initial_pose.pose.pose.position.z = initial_trans.translation.z
        initial_pose.pose.pose.orientation.x = initial_trans.rotation.x
        initial_pose.pose.pose.orientation.y = initial_trans.rotation.y
        initial_pose.pose.pose.orientation.z = initial_trans.rotation.z
        initial_pose.pose.pose.orientation.w = initial_trans.rotation.w
        initial_pose.pose.covariance = [
            pow(0.00017, 2), 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, pow(0.00017, 2), 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, pow(0.00017, 2), 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, pow(0.00017, 2), 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, pow(0.00017, 2), 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, pow(0.00017, 2)
        ]

        print(initial_pose)
        pub.publish(initial_pose)
