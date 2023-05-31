FROM ros:noetic-ros-base

SHELL ["/bin/bash", "-c"]

RUN apt update && apt install -y \
    can-utils \
    git \
    python3-catkin-tools \
    python3-vcstool
RUN mkdir -p /root/catkin_ws/src
RUN cd /root/catkin_ws && catkin init
RUN cd /root/catkin_ws/src && git clone https://github.com/smilerobotics/haruna.git

WORKDIR /root/catkin_ws/src
RUN vcs import < haruna/.rosinstall
RUN rosdep install --from-paths . -y
RUN catkin build

WORKDIR /root
