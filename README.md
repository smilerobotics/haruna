# haruna

## Prerequirements

* Raspberry Pi 4 Model B
* Ubuntu 20.04
* ROS Noetic

### CAN Interface

Prepare either of the following

* [USB2CAN-Cable](./docs/innomaker.md)
* [USB-to-CAN V2 (Ixxat)](./docs/ixxat.md)
* [2-CH CAN HAT (Waveshare)](./docs/can_hat.md)
* etc

### Camera

Realsense D435 or D435i

### Joy Controller

DualSense or something

## Build

```bash
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

### Run on a real robot

```bash
roslaunch haruna main.launch
```

If your Haruna is using EPOS4 motor drivers

```bash
roslaunch haruna main.launch motor_driver:=epos4
```

(The default value for `motor_driver` arg is `zlac8015`)

More details on other options, including LiDAR, [here](./docs/argument.md)

### Run on simulators

#### Gazebo

```bash
roslaunch haruna_simulations gazebo.launch
```

## Create a map

Please set `ROS_MASTER_URI` and `ROS_IP`.

### On robot client (Raspberry Pi)

```bash
roslaunch haruna_navigation mapping_auto.launch
```

### On robot master (Laptop or Desktop or else)

```bash
roslaunch haruna_navigation mapping_auto_rviz.launch
```

## Navigation

```bash
roslaunch haruna_navigation navigation.launch
```

Use arg `map` to set the map file.

### Initialize Pose with ArUco marker

Before using this feature, you need to confirm the robot is running either real or sim and navigation is also running.
And set the tf named `aruco_init_frame` that looked up from `map`.
In the launch file below, that frame is defined by `static_transform_publisher`.

```bash
roslaunch haruna_navigation detect_aruco.launch
```

Use arg `markerId` and `markerSize` to set the marker's info.

## Launch files

For more descriptions of the launch file, please check [here](./docs/launch.md)
