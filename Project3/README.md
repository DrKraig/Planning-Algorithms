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


<h2>Videos are present in the 'Output Videos' folder. The output can also be viewed below in GIF format.</h2>

<h2> Test Case 1 </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/110245177-1e649c80-7f30-11eb-8c37-7e5da186f337.gif" alt="Logo"/>
</p>
<h2> Test Case 2 </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/110245227-46540000-7f30-11eb-9fa4-c52f53260e6e.gif" alt="Logo"/>
</p>

<h2> Test Case 3 </h2>

<p align="center">
  
  <img src="https://user-images.githubusercontent.com/12711480/110245347-acd91e00-7f30-11eb-861e-2782e4ff6dc6.gif" alt="Logo"/>
</p>

<h2> Test Case 4 </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/110245494-5d472200-7f31-11eb-87c2-6eeacfd0eff6.gif" alt="Logo"/>
</p>

<h2> Test Case 5 </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/110245230-481dc380-7f30-11eb-877a-bbdd6b1f8560.gif" alt="Logo"/>
</p>


## A few instresting things about this prorgam.
  1. For each and every node, its co-ordinates, neighbours, parent and the distance to reach that node is being stored.
  2. The parent node has been created so that once the final state is found, a solution could be backtracked.
  3. The math for finding out the line, rectangle, circle and ellipse equations was found by plotting the map on GeoGebra.
  4. The program will let you know if the starting point or ending point is inside the obstacle.
  5. All the equations for the algebraic planes are defined in their approppriate methods in the file 'Dijkstra_point.py'.
