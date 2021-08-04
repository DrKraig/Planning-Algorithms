<h1>PRRT*: RRT* with Potential Fields on ROS!</h1>

  <h2>Pre-requisites to run the code:</h2>

    1. Python 3 should be installed on your system.
    2. ROS melodic should be installed along with Gazebo, turtlebot3

Note:  Other libraries used are inbuilt.</br>

  <h2>Instructions to run the code:</h2>
  
    1. Clone the repository by clicking the big green button located here: https://github.com/DrKraig/Planning-Algorithms
    2. Open command prompt or terminal.
    3. Navigate to this directory using 'cd Planning-Algorithms/PRRTStar/src/'
    4. To Run PRRT* on ROS, clone the ROS package 'turtlebot_prrtstar' to your catkin
       workspace and enter the following script.
      ```bash
         source /opt/ros/melodic/setup.bash
         cd ~/your_workspace/
         catkin build
         source ~/your_workspace/devel/setup.bash
      ```
    5. To change the bot's initial location edit the ./launch/turtlebot3_map.launch
    6. Now run the following commands in 3 different terminal windows
    ```
       roslaunch turtlebot_prrtstar turtlebot3_map
       rosrun turtlebot_prrtstar bot_controller
       rosrun turtlebot_prrtstar goal_broadcaster.py
    ```
    7. Enter goal location and enjoy!


<h2>Videos are present in the 'Output Videos' folder. The output can also be viewed below in GIF format.</h2>

<h2> Test Case 1: Starting Coordinate = (0.3, 0.3), Ending Coordinate = (9, 9), Iterations = 100</h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/117591930-93a54700-b104-11eb-9bda-76593ecc76ab.gif" alt="Logo"/>
</p>
<h2> Test Case 2: Starting Coordinate = (0.3, 9), Ending Coordinate = (0.3, 0.3), Iterations = 500 </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/117591789-03670200-b104-11eb-985d-75b78a4ca7ac.gif" alt="Logo"/>
</p>


## A few instresting things about this prorgam.
  1. For each and every node, its co-ordinates, neighbours, parent and the cost that node is being stored.
  2. The parent node has been created so that once the final state is found, a solution could be backtracked.
  3. The math for finding out the line, rectangle, circle and ellipse equations was found by plotting the map on GeoGebra.
  4. The program will let you know if the starting point or ending point is inside the obstacle or outside the arena
  5. All the equations for the algebraic planes are defined in their approppriate methods.