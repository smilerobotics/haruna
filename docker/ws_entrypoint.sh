#!/bin/bash
set -e

# setup ros environment
source "${HOME}/catkin_ws/install/setup.bash" --
exec "$@"
