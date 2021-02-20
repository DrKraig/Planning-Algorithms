<h1>Project 1 - 15 Puzzle Challenge!</h1>

  <h2>Pre-requisites to run the code:</h2>

    1. Python 3 should be installed on your system.
    2. Numpy - Install it using 'pip install numpy'

Note:  Other libraries used are inbuilt.</br>

  <h2>Instructions to run the code:</h2>
  
    1. Clone the repository by clicking the big green button located here: https://github.com/SamPusegaonkar/ENPM661
    2. Open command prompt or terminal.
    3. Navigate to this directory using 'cd ENPM661/Project1'
    4. If OS is windows, type 'python FinalCode.py'
    4. If OS is Ubuntu, type 'python3 FinalCode.py'
    5. Check the generated file in the current directory called 'output.txt'
    6. For running other test cases, uncomment the lines (184-200) from the FinalCode.py file.

## A few instresting things about this prorgam.
  1. No List has been created to store parent child information. Instead a completely seperate data structure is built to store this.
  2. For each state a parent node has been created so that once the final state is found, a solution could be backtracked.
  3. Because there is no list, solution for each test case is generated within milliseconds! - Optimal Time is obtained & is discussed in detail in the code itself.

Note: Outputs of all test cases are located below.</br>

<h2> Test Case 5 </h2>

<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/108575657-f0a11600-72e8-11eb-9ad0-51d2b3d44d03.png" alt="Logo"/>
</p>

<h2> Test Case 1 </h2>
<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/108576241-db2ceb80-72ea-11eb-8932-a335f08760fd.PNG" alt="Logo"/>
</p>

<h2> Test Case 2 </h2>
<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/108576249-e6801700-72ea-11eb-96fd-a0dd42eafeaf.PNG" alt="Logo"/>
</p>

<h2> Test Case 3 </h2>
<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/108576254-ea139e00-72ea-11eb-888e-6425606dd171.PNG" alt="Logo"/>
</p>

<h2> Test Case 4 </h2>
<p align="center">
  <img src="https://user-images.githubusercontent.com/12711480/108576265-eed85200-72ea-11eb-9bfc-0ef54e37b683.PNG" alt="Logo"/>
</p>
