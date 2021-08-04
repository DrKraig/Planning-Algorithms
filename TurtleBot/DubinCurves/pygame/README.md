<h1>Implementation of AStar Algorithm for a rigid robot with Dublin Curves in PyGame!</h1>

  <h2>Pre-requisites to run the code:</h2>

    1. Python 3 should be installed on your system.
    2. PyGame - Install it using 'pip install pygame'

Note:  Other libraries used are inbuilt.</br>

  <h2>Instructions to run the code:</h2>
  
    1. Clone the repository by clicking the big green button located here: https://github.com/DrKraig/Planning-Algorithms
    2. Open command prompt or terminal.
    3. Navigate to this directory using 'cd Planning-Algorithms/TurtleBot/DubinCurves/'
    4. To Run AStar, Navigate to 'cd pygame'. If OS is Ubuntu, type 'python3 AStar.py'
    5. Enter the parameters of the  robot
    6. Enjoy!


<h1>Videos are present in the 'Output Videos' folder. The output can also be viewed below in GIF format.</h2>

<h1> Radius = 0.105, Clerance = 0.2 </h1>

<h2> Test Case 1: Starting Coordinate = (1, 1, 60), Ending Coordinate = (9, 1)</h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/116008967-f23ad300-a5e4-11eb-9978-c3e69eb130fb.gif" alt="Logo"/>
</p>
<h2> Test Case 2: Starting Coordinate = (9, 9, 385), Ending Coordinate = (1, 1)</h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/116008636-9ae83300-a5e3-11eb-9221-c0474deada17.gif" alt="Logo"/>
</p>

<h2> Test Case 3: Starting Coordinate = (6, 9, 30), Ending Coordinate = (1, 1) </h2>

<p align="center">
  
  <img src="https://user-images.githubusercontent.com/12711480/116008620-8f950780-a5e3-11eb-9bff-6c893eb0f777.gif" alt="Logo"/>
</p>

<h2> Test Case 4: Starting Coordinate = (1, 9, 0), Ending Coordinate = (9, 1) </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/116008617-8c018080-a5e3-11eb-8fc9-09f06d77351b.gif" alt="Logo"/>
</p>

<h2> Test Case 5: Starting Coordinate = (6, 8, 0), Ending Coordinate = (8, 8) </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/116008619-8dcb4400-a5e3-11eb-9c6c-6637638703fd.gif" alt="Logo"/>
</p>




## A few instresting things about this prorgam.
  1. For each and every node, its co-ordinates, neighbours, parent and the distance to reach that node is being stored.
  2. The parent node has been created so that once the final state is found, a solution could be backtracked.
  3. The math for finding out the line, rectangle, circle and ellipse equations was found by plotting the map on GeoGebra.
  4. The program will let you know if the starting point or ending point is inside the obstacle or outside the arena
  5. All the equations for the algebraic planes are defined in their approppriate methods.