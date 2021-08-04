cmake_minimum_required(VERSION 3.0.2)
project(Astar)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  rospy
  std_msgs
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS src/publisher.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
