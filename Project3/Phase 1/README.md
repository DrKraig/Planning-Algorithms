<h1>Project 3 - Implementation of Dijkstra's Algorithm on a rigid robot with Animation!</h1>

  <h2>Pre-requisites to run the code:</h2>

    1. Python 3 should be installed on your system.
    2. PyGame - Install it using 'pip install pygame'

Note:  Other libraries used are inbuilt.</br>

  <h2>Instructions to run the code:</h2>
  
    1. Clone the repository by clicking the big green button located here: https://github.com/SamPusegaonkar/ENPM661
    2. Open command prompt or terminal.
    3. Navigate to this directory using 'cd ENPM661/Project3'
    4. If OS is windows, type 'python Dijkstra.py'
    4. If OS is Ubuntu, type 'python3 Dijkstra.py'
    5. Input the co-ordinates for starting & ending point
    6. Enjoy!


<h1>Videos are present in the 'Output' folder. </h1>

<h2> Test Case 1: Starting Coordinate = (15, 15), Ending Coordinate = (385, 285)</h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/113612762-3ce8b100-961e-11eb-9db2-fd85530d3585.gif" alt="Logo"/>
</p>
<h2> Test Case 2: Starting Coordinate = (250, 199), Ending Coordinate = (15, 285) </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/113612767-3eb27480-961e-11eb-9612-0d98faf19dac.gif" alt="Logo"/>
</p>

<h2> Test Case 3: Starting Coordinate = (385, 15), Ending Coordinate = (15, 285) </h2>

<p align="center">
  
  <img src="https://user-images.githubusercontent.com/12711480/113613848-c51b8600-961f-11eb-982d-1990732cbbfc.gif" alt="Logo"/>
</p>

<h2> Test Case 4: Starting Coordinate = (24, 199), Ending Coordinate = (350, 199) </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/113613974-e11f2780-961f-11eb-820a-8e67ba34903e.gif" alt="Logo"/>
</p>

<h2> Test Case 5: Starting Coordinate = (270, 285), Ending Coordinate = (50, 15) </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/113614005-ebd9bc80-961f-11eb-9e7c-809b94667cde.gif" alt="Logo"/>
</p>

<h2> Test Case 6: Starting Coordinate = (120, 15), Ending Coordinate = (280, 285) </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/113614311-54289e00-9620-11eb-9bbc-f7a7d019781b.gif" alt="Logo"/>
</p>

<h2> Test Case 7: Starting Coordinate = (250, 240), Ending Coordinate = (15, 15) </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/113614973-40ca0280-9621-11eb-9313-2a3461d87ab3.gif" alt="Logo"/>
</p>




## A few instresting things about this prorgam.
  1. For each and every node, its co-ordinates, neighbours, parent and the distance to reach that node is being stored.
  2. The parent node has been created so that once the final state is found, a solution could be backtracked.
  3. The math for finding out the line, rectangle, circle and ellipse equations was found by plotting the map on GeoGebra.
  4. The program will let you know if the starting point or ending point is inside the obstacle.
  5. All the equations for the algebraic planes are defined in their approppriate methods in the file 'Dijkstra.py'.
