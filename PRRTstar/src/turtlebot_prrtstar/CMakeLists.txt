cmake_minimum_required(VERSION 3.0.2)
project(turtlebot_prrtstar)


find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  rospy
  std_msgs
  tf2
  tf2_ros
)

catkin_package(CATKIN_DEPENDS geometry_msgs roscpp rospy std_msgs tf2 tf2_ros)

include_directories(${catkin_INCLUDE_DIRS})


add_executable(bot_controller src/bot_controller.cpp)
target_link_libraries(bot_controller ${catkin_LIBRARIES})
catkin_install_python(PROGRAMS scripts/goal_broadcaster.py DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})


