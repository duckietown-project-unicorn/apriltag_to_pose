#!/usr/bin/env python
import roslib
import rospy
import math
import tf
import sys
import numpy as np
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from duckietown_msgs.msg import BoolStamped


if __name__ == '__main__':
    if len(sys.argv) < 1:
        ROS_WARN("usage: tf_to_pose.py ID")

    else:
        ID = '/Tag'+ str(sys.argv[1])
    rospy.init_node('tf_to_pose')

    listener = tf.TransformListener()

    switch_pub = rospy.Publisher('apriltag_detector_node/switch', BoolStamped,queue_size=1)
    bool_msg = BoolStamped()
    bool_msg.data=True
    switch_pub.publish(bool_msg)

    pose_pub = rospy.Publisher('/pose', PoseStamped,queue_size=1)
    path_pub = rospy.Publisher('/path', Path,queue_size=1)
    path=Path()
    rate = rospy.Rate(20.0)
    i=0
    while not rospy.is_shutdown():
        i=i+1
        switch_pub.publish(bool_msg)
        try:
                (trans,rot) = listener.lookupTransformFull(ID,rospy.Time(),'/camera', rospy.Time(),'/camera')
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

       	Rotmat = (2*rot[0]**2-1)*np.eye(3)+2*rot[0]*np.matrix([[0,-rot[3],rot[2]], [rot[3],0,-rot[1]], [-rot[2],rot[1],0]])+2*np.matmul(rot[1:3],np.transpose(rot[1:3]))

       	Tmat = np.zeros((4,4))
       	Tmat[:3,:3]=Rotmat
       	Tmat[3,3]=1
       	Tmat[:3,3]=trans

       	Tmat_inv = np.linalg.pinv(Tmat, rcond=0.001)

        print(Tmat)
        print(Tmat_inv)

        #print(trans)
        tag_pose = Pose()
        tag_pose.position.x = trans[0]
        tag_pose.position.y = trans[1]
        tag_pose.position.z = trans[2]
        tag_pose.orientation.x = rot[0]
        tag_pose.orientation.y = rot[1]
        tag_pose.orientation.z = rot[2]
        tag_pose.orientation.w = rot[3]
        tag_pose_stamped = PoseStamped()
        tag_pose_stamped.header.stamp = rospy.Time(0)
        tag_pose_stamped.header.seq= i
        tag_pose_stamped.pose = tag_pose
        tag_pose_stamped.header.frame_id="camera"
        path.header=tag_pose_stamped.header
        path.poses.append(tag_pose_stamped)

        pose_pub.publish(tag_pose_stamped)
        path_pub.publish(path)
        rate.sleep()
