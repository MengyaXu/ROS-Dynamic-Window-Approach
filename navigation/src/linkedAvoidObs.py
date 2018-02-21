#! /usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from std_msgs.msg import *
from math import atan2
from sensor_msgs.msg import LaserScan

obstacle = False

# Callback for scan
def callback(msg):

    minDistance = 31 # max laser range is 30
    obsDirection = 0 # angle of obstacle from robot
    global obstacle

    # range of robot laser 180:540 to include a large span but not the extreme
    # edges - 360 is directly in front of the robot
    #PHYSICAL BOT HAS DEGREES OF 512
    #SIMULATION HAS DEGREES OF 720
    #UNCOMMENT LINE BELOW AND COMMENT NEXT LINE TO USE SIMULATION
    for angle, distance in enumerate(msg.ranges[113:398]):
    #for angle, distance in enumerate(msg.ranges[160:560]):
        if distance < minDistance:
            minDistance = distance
            obsDirection = angle

    if (minDistance < 0.3):
        obstacle = True
        # Obstacle in front
        # Too close: stop.
        speed.linear.x = 0
        # Checks if obstacle infront of robot and which direction to go
        # enum checks between 200 -> 520, 160 is 360 between these
            # Turn right
        #UNCOMMENT LINE BELOW AND COMMENT NEXT LINE TO USE SIMULATION
        if (obsDirection < 184):
        #if (obsDirection < 100):
            speed.angular.z = -0.2
        elif (obsDirection < 256):
        #elif (obsDirection < 200):
            speed.angular.z = -0.4
            # Turn left
        elif (obsDirection < 327):
        #elif (obsDirection < 300):
            speed.angular.z = 0.4
        else:
            speed.angular.z = 0.2
    else:
        # No obstacle in front. Move forward
        speed.angular.z = 0
        speed.linear.x = 0.3
        # Checks to see if obstacle is at side
        #UNCOMMENT LINE BELOW AND COMMENT NEXT LINE TO USE SIMULATION
        if (msg.ranges[0] < 0.4 or msg.ranges[511] < 0.4):
        #if (msg.ranges[0] < 0.4 or msg.ranges[719] < 0.4):
            obstacle = True
        else:
            obstacle = False

    pubLaser.publish(obstacle)

rospy.init_node("obstacles")
pub = rospy.Publisher("cmd_vel_mux/input/teleop", Twist, queue_size=1)
pubLaser = rospy.Publisher("/obstacle", Bool, queue_size=10)
subScan = rospy.Subscriber("/scan", LaserScan, callback)

speed = Twist()
r = rospy.Rate(2)

while not rospy.is_shutdown():
    if(obstacle):
        pub.publish(speed)
    r.sleep()
