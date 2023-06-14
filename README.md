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

### Run on a physical machine

```bash
roslaunch haruna main.launch
```

If your Haruna is using EPOS4 motor drivers

```bash
roslaunch haruna main.launch motor_driver:=epos4
```

(The default value for `motor_driver` arg is `zlac8015`)

### Run on simulaters

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

#### On robot master (Laptop or Desktop or else)

```bash
roslaunch haruna_navigation mapping_auto_rviz.launch
```

## Launch files

For more descriptions of the launch file, please check [here](./docs/launch.md)
