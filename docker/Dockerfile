FROM ros:noetic-ros-base

SHELL ["/bin/bash", "-c"]

RUN apt-get update \
 && apt-get install -y \
    can-utils \
    git \
    python3-catkin-tools \
    python3-vcstool \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /root/catkin_ws/src \
 && cd /root/catkin_ws \
 && catkin init \
 && cd /root/catkin_ws/src \
 && git clone https://github.com/smilerobotics/haruna.git \
 && vcs import < haruna/.rosinstall \
 && rosdep install --from-paths . -y \
 && source /opt/ros/noetic/setup.bash \
 && catkin build \
 && source /root/catkin_ws/devel/setup.bash

WORKDIR /root
