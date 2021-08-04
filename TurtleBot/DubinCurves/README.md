<h1>Project 3 - Implementation of AStar Algorithm with Animation! - Dublin Curves</h1>

  <h2>Pre-requisites to run the code:</h2>

    1. Python 3 should be installed on your system.
    2. PyGame - Install it using 'pip install pygame'

Note:  Other libraries used are inbuilt.</br>

<h2>Instructions to run the code:</h2>
  
    1. Part1 Folder includes: Animation of Dublin curves in pygame
    2. Part2 Folder includes: Animation of Dublin curves in ROS

  <h2>Instructions to run the code:</h2>
  
    1. Clone the repository by clicking the big green button located here: https://github.com/SamPusegaonkar/ENPM661
    2. Open command prompt or terminal.
    3. Navigate to this directory using 'cd ENPM661/Project3/'
    4. To Run AStar - Part 1, Navigate to 'cd Phase 3/Part1'. If OS is Ubuntu, type 'python3 AStar.py'
    5. Enter the parameters of the  robot
    6. Enjoy!


<h2>Videos are present in the 'Output Videos' folder. </h2>

## A few instresting things about this prorgam.
  1. For each and every node, its co-ordinates, neighbours, parent and the cost that node is being stored.
  2. The parent node has been created so that once the final state is found, a solution could be backtracked.
  3. The math for finding out the line, rectangle, circle and ellipse equations was found by plotting the map on GeoGebra.
  4. The program will let you know if the starting point or ending point is inside the obstacle or outside the arena
  5. All the equations for the algebraic planes are defined in their approppriate methods.