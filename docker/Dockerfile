FROM ros:noetic-ros-base

SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt-get install -y \
        can-utils \
        git \
        python3-catkin-tools \
        python3-vcstool && \
    mkdir -p /root/canopen_ws/src && \
    cd /root/canopen_ws && \
    catkin init && \
    cd src && \
    git clone -b melodic-devel https://github.com/smilerobotics/ros_canopen.git && \
    rosdep install --from-paths . -i -y && \
    source /opt/ros/noetic/setup.bash && \
    catkin config --install && \
    catkin build && \
    catkin clean -bdL -y && \
    mkdir -p /root/catkin_ws/src && \
    cd /root/catkin_ws && \
    catkin init

WORKDIR /root/catkin_ws/

COPY ./docker/ws_entrypoint.sh ./
COPY ./haruna/package.xml src/haruna/haruna/

RUN cd src && \
    rosdep install --from-paths . -i -y && \
    rm -rf /var/lib/apt/lists/*

COPY ./ src/haruna/

RUN cd src && \
    source /root/canopen_ws/install/setup.bash && \
    catkin config --install && \
    catkin build

ENTRYPOINT ["./ws_entrypoint.sh"]

