Package to publish robot pose and path from detected apriltags.

What's inside?
rect.py : Takes compressed image and publishes rectified version

tf_to_pose.py: Takes tf transforms published from apriltags2_ros and publishes pose and path

How to use:
```roslaunch apriltag_to_pose april_to_pose.launch duckiebot:=duckiebot_name id:=Tag-ID-number```
e.g: ```roslaunch apriltag_to_pose april_to_pose.launch duckiebot:=sebot id:=66```

Pose is published on ```/pose```, path is published on ```/path```.
