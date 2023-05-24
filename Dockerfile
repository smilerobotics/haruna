FROM ros:noetic-ros-base

SHELL ["/bin/bash", "-c"]

RUN <<EOF \
apt update && apt install -y \
    can-utils \
    git \
    iputils-ping \
    net-tools \
    python3-catkin-tools \
    python3-vcstool
mkdir -p /root/catkin_ws/src
cd /root/catkin_ws
catkin init
cd /root/catkin_ws/src
git clone https://github.com/smilerobotics/haruna.git
vcs import < haruna/.rosinstall
rosdep install --from-paths . -y
EOF

RUN catkin build
