# haruna_test_bench

## Prerequirements

* Raspberry Pi 4 Model B
* Ubuntu 20.04
* ROS Noetic

### CAN Interface

Prepare either of the following

* [USB-to-CAN V2 (Ixxat)](./docs/ixxat.md)
* [2-CH CAN HAT (Waveshare)](./docs/can_hat.md)
* etc

### Joy Controller

DualSense or something

## Build

```
~$ mkdir -p catkin_ws/src
~$ cd catkin_ws
~/catkin_ws$ catkin init
~/catkin_ws$ cd src
~/catkin_ws/src$ git clone git@github.com:smilerobotics/haruna_test_bench.git
~/catkin_ws/src$ vcs import < haruna_test_bench/.rosinstall
~/catkin_ws/src$ rosdep install --from-paths .
~/catkin_ws/src$ catkin build
~/catkin_ws/src$ source ~/catkin_ws/devel/setup.bash
```

## Run

```
$ roslaunch haruna main.launch
```
