# CSI-CAMERA
Directory for csi cameras with jetson nano

This will have sample codes for testing MIPI-CSI(2) camera with Jetson Nano. The SDK image can be found here: https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write
The metal pins face the inside of the board. The Jetson has 2 CSI Camera slots.

Simple test:


gst-launch-1.0 nvarguscamerasrc sensor_id=0 ! \
   'video/x-raw(memory:NVMM),width=3280, height=2464, framerate=30/1' ! \
   nvvidconv flip-method=0 ! 'video/x-raw(memory:NVMM),width=1920, height=1080' ! \
   nvegltransform ! nveglglessink -e

You can use v4l2-ctl to determine the camera capabilities. v4l2-ctl is in the v4l-utils: ``` $ sudo apt-get install v4l-utils ``` For the Raspberry Pi V2 camera, a typical output is (assuming the camera is /dev/video0):
$ v4l2-ctl --list-formats-ext
