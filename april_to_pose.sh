#!/bin/bash
source /home/software/docker/env.sh

roslaunch apriltag_to_pose april_to_pose.launch duckiebot:=gyrogearloose id:=14

