cmake_minimum_required(VERSION 3.0.2)
project(haruna)

find_package(catkin REQUIRED)

#catkin_python_setup()

catkin_package()

install(
    DIRECTORY config dcf eds launch tools urdf
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

install(
    DIRECTORY scripts
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
    PATTERN "scripts/*.py"
    PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ)