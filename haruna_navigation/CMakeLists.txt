cmake_minimum_required(VERSION 3.0.2)
project(haruna_navigation)

find_package(catkin REQUIRED)

#catkin_python_setup()

catkin_package()

install(DIRECTORY config launch maps DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})