#!/usr/bin/env python
# coding=utf-8

# 指令部分在judge函数中(^_^)

import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
# 导入mgs到pkg中
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from math import pi


# 创建发布者及订阅者
class Image_converter:
    def __init__(self):
        rospy.init_node('hole_detecting', anonymous=True)
        rospy.loginfo("start")
        # 定义退出
        rospy.on_shutdown(self.shutdown)
        # 发布者定义
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(1)
        # ros_image 转换为 cv图像格式
        self.bridge = CvBridge()
        # 订阅者定义
        # Subscriber函数第一个参数是topic的名称，第二个参数是接受的数据类型 第三个参数是回调函数的名称
        self.image_sub = rospy.Subscriber('/front_cam/camera/image', Image, self.callback)
        # 至此进入回调函数

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print e
        final_image, cx, cy, wid, hei = self.hole_detecting(cv_image)
        self.judge(cx, cy, wid, hei)


    def hole_detecting(self, src):
        # edge = canny(src) 图像处理
        blur = cv2.GaussianBlur(src, (3, 3), 0)
        edge = cv2.Canny(blur, 50, 150)
        # dil = dilate(edge) 膨胀
        g = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
        dil = cv2.dilate(edge, g)
        # final = judge_rectangle(dil) 判断矩形
        cnt = cv2.findContours(dil, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = cnt[1]
        output = np.ones(src.shape, np.uint8) * 255
        # width, height = center() 计算原图中点
        width = src.shape[1] / 2
        height = src.shape[0] / 2
        print(width, height)
        cX, cY = width, height
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.01*peri, True)
            if len(approx) == 4:
                cv2.drawContours(output, c, -1, (0, 255, 0))
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                print(cX, cY)
        cv2.imshow("final", output)
        return output, cX, cY, width, height

    def judge(self, cX, cY, width, height):
        linear_speed = 0.2
        goal_distance = 1.0
        linear_duration = goal_distance / linear_speed
        angular_speed = 1.0
        goal_angle = pi
        angular_duration = goal_angle / angular_speed
        move_cmd = Twist()
        move_cmd.linear.x = linear_speed
        if cX < width:
            self.cmd_vel.publish(move_cmd)
        elif cX > width:
            self.cmd_vel.publish(move_cmd)
        else:
            self.cmd_vel.publish(move_cmd)
        if cY < height:
            self.cmd_vel.publish(move_cmd)
        elif cY > height:
            self.cmd_vel.publish(move_cmd)
        else:
            self.cmd_vel.publish(move_cmd)
        self.rate.sleep()

    def shutdown(self):
        # Always stop the robot when shutting down the node.
        rospy.loginfo("Stopping the robot...")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)


if __name__ == '__main__':
    Image_converter()
    rospy.spin()

