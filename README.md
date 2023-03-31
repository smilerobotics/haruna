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
~/catkin_ws/src$ git clone git@github.com:smilerobotics/haruna.git
~/catkin_ws/src$ vcs import < haruna/.rosinstall
~/catkin_ws/src$ rosdep install --from-paths .
~/catkin_ws/src$ catkin build
~/catkin_ws/src$ source ~/catkin_ws/devel/setup.bash
```

## Run

```bash
roslaunch haruna main.launch
```

### Run to create a map

Please set `ROS_MASTER_URI` and `ROS_IP`.

#### Robot client (Raspberry Pi)

```bash
roslaunch haruna_navigation mapping_auto.launch
```

#### Robot master (Laptop or Desktop or else)

```bash
roslaunch haruna_navigation mapping_auto_rviz.launch
```

### Launch file

The description of the launch file is [here](./docs/launch.md)
