#!/usr/bin/env python
import roslib
import rospy
import math
import tf
import numpy as np
import sys
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import CameraInfo
from image_geometry import PinholeCameraModel

cam_inf_ros = CameraInfo()
duckiebot = ""

def imgcb(image):
    bridge = CvBridge()
    cv_image = bridge.compressed_imgmsg_to_cv2(image, desired_encoding="mono8")
    cv_image_rectified = np.zeros(np.shape(cv_image))
    cam_inf = PinholeCameraModel()
    global cam_inf_ros
    cam_inf.fromCameraInfo(cam_inf_ros)
    #print(cam_inf.K, cam_inf.D, cam_inf.R, cam_inf.P, (cam_inf.width, cam_inf.height))
    mapx = np.ndarray(shape=(cam_inf.height, cam_inf.width, 1), dtype='float32')
    mapy = np.ndarray(shape=(cam_inf.height, cam_inf.width, 1), dtype='float32')
    mapx, mapy = cv2.initUndistortRectifyMap(cam_inf.K, cam_inf.D, cam_inf.R, cam_inf.P, (cam_inf.width, cam_inf.height), cv2.CV_32FC1, mapx, mapy)
    rect_cv= cv2.remap(cv_image, mapx, mapy, cv2.INTER_CUBIC, cv_image_rectified)
    rect_img = bridge.cv2_to_imgmsg(rect_cv, encoding="mono8")
    rect_img.header = cam_inf_ros.header
    global duckiebot
    topic_rect = str('/'+duckiebot+'/camera_node/rect')
    #topic_info = str('/'+duckiebot+'camera_info')
    pub = rospy.Publisher(topic_rect, Image, queue_size=1000)
    pub.publish(rect_img)
    #info_pub = rospy.Publisher(topic_info,CameraInfo,queue_size=1000)

def camcb(cam_info):
    global cam_inf_ros
    cam_inf_ros = cam_info

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: rect.py duckiebot_name")

    else:
        global duckiebot
        duckiebot=sys.argv[1]
    rospy.init_node('rectify_image')


    listener = tf.TransformListener()
    global duckiebot
    topic = str('/'+duckiebot+'/camera_node/camera_info')
    cam_sub = rospy.Subscriber(topic,CameraInfo,camcb)
    im_topic = str('/'+duckiebot+'/camera_node/image/compressed')
    img_sub = rospy.Subscriber(im_topic,CompressedImage,imgcb)

    rate = rospy.Rate(200.0)
    i=0
    while not rospy.is_shutdown():
        rate.sleep()
