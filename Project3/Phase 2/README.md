<h1>Project 3 - Implementation of AStar Algorithm for a rigid robot with Animation!</h1>

  <h2>Pre-requisites to run the code:</h2>

    1. Python 3 should be installed on your system.
    2. PyGame - Install it using 'pip install pygame'

Note:  Other libraries used are inbuilt.</br>

  <h2>Instructions to run the code:</h2>
  
    1. Clone the repository by clicking the big green button located here: https://github.com/SamPusegaonkar/ENPM661
    2. Open command prompt or terminal.
    3. Navigate to this directory using 'cd ENPM661/Project3/'
    4. To Run AStar, Navigate to 'cd Phase 2'. If OS is Ubuntu, type 'python3 AStar.py'
    5. Enter the parameters of the  robot
    6. Enjoy!


<h1>Videos are present in the 'Output Videos' folder. The output can also be viewed below in GIF format.</h2>

<h2> Test Case 1: Starting Coordinate = (15, 15, 0), Ending Coordinate = (385, 285), Step Size = 10 </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/113526317-9f42a280-9587-11eb-8a1a-7a41fb66f769.gif" alt="Logo"/>
</p>
<h2> Test Case 2: Starting Coordinate = (380, 250, 50), Ending Coordinate = (15, 15), Step Size = 10 </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/113526321-a10c6600-9587-11eb-9355-6a076e05deda.gif" alt="Logo"/>
</p>

<h2> Test Case 3: Starting Coordinate = (150, 285, 300), Ending Coordinate = (385, 15), Step Size = 5 </h2>

<p align="center">
  
  <img src="https://user-images.githubusercontent.com/12711480/113526340-b2ee0900-9587-11eb-829e-3b46b1c54de0.gif" alt="Logo"/>
</p>

<h2> Test Case 4: Starting Coordinate = (15, 285, 60), Ending Coordinate = (385, 15), Step Size = 7</h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/113526323-a36ec000-9587-11eb-822a-cc8be7bcae61.gif" alt="Logo"/>
</p>

<h2> Test Case 5: Starting Coordinate = (170, 285, 190), Ending Coordinate = (15, 285), Step Size = 10<</h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/113526837-82a76a00-9589-11eb-8f7e-e11b5eef473b.gif" alt="Logo"/>
</p>

<h2> Test Case 6: Starting Coordinate = (355, 285, 15), Ending Coordinate = (15, 285), Step Size = 10<</h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/113526790-58ee4300-9589-11eb-8071-2a7ebe1989a4.gif" alt="Logo"/>
</p>

<h2> Test Case 7: Starting Coordinate = (245, 250, 180), Ending Coordinate = (15, 15), Step Size = 10<</h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/113526468-2b54ca00-9588-11eb-8b31-99febe575231.gif" alt="Logo"/>
</p>

## A few instresting things about this prorgam.
  1. For each and every node, its co-ordinates, neighbours, parent and the distance to reach that node is being stored.
  2. The parent node has been created so that once the final state is found, a solution could be backtracked.
  3. The math for finding out the line, rectangle, circle and ellipse equations was found by plotting the map on GeoGebra.
  4. The program will let you know if the starting point or ending point is inside the obstacle or outside the arena
  5. All the equations for the algebraic planes are defined in their approppriate methods.