FROM ros:noetic-ros-base

SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt-get install -y \
    can-utils \
    git \
    python3-catkin-tools \
    python3-vcstool && \
    mkdir -p /root/catkin_ws/src && \
    cd /root/catkin_ws && \
    catkin init && \
    cd /root/catkin_ws/src && \
    git clone https://github.com/smilerobotics/haruna.git && \
    vcs import < haruna/.rosinstall && \
    rosdep install --from-paths . -y && \
    rm -rf /var/lib/apt/lists/*

RUN cd /root/catkin_ws && \
    source /opt/ros/noetic/setup.bash && \
    catkin config --install && \
    catkin build && \
    catkin clean -bdL -y