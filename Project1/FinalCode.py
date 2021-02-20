#https://github.com/SamPusegaonkar/ENPM661/tree/main/Project1

###########################################
#Worst Case Time complexity is O(N) - Where N is the number of states visited to reach the target state.

#Explnation: A while loop is been run to store all the possible states to be explored.
###########################################
#Space Complexity is O(N) - Where N is the number of states.

#Explnation: A hash table has been used to store all the visited states.
###########################################


import re
import numpy as np
import copy 

class Tree:
    """
    Tree class : This class is built to store the parent property for every state that is being generated.
    """
    def __init__(self, node):
        self.name = node
        self.parent = ""

class TileGame(Tree):
    """
    TileGame class : This class defines all the functions required to play the tile game given an initial state.
    """
    def __init__(self, initialState):
        
        """
        Description: Defining initial constants - Visited array, Rows, Cols, Target String.
        """
        self.initialState = initialState
        self.rows = len(self.initialState)
        self.cols = len(self.initialState[0])
        self.visited = {}
        self.matchingNumToString = {1:"One", 2:"Two", 3:"Three", 0:"Zero", 4:"Four", 5:"Five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine", 10:"Ten", 11:"Eleven", 12:"Twel", 13:"Thir", 14:"Fourt", 15:"Fif"}
        self.matchingStringToNum = {"One":1, "Two":2, "Three":3, "Zero":0, "Four":4, "Five":5, "Six":6, "Seven":7, "Eight":8, "Nine":9, "Ten":10, "Eleven":11, "Twel":12, "Thir":13, "Fourt":14, "Fif":15}
        self.targetState = self.generateTargetState(self.initialState)
        self.targetStateString = self.convertMatrixToString(self.targetState)

    def generateTargetState(self, initialState):

        matrix = [[0 for j in range(len(self.initialState[0]))] for i in range(len(self.initialState))]

        counter = 1
        for i in range(self.rows):
            for j in range(self.cols):
                matrix[i][j] = counter 
                counter += 1
        matrix[self.rows-1][self.cols-1] = 0
        return matrix

    def bfs(self,matrixA):
        """
        Input: A given matrix/ initial state of any size. (nxn)
        Output: A text file generated with the path from the initial state to the final state.

        """
        currentStateString = self.convertMatrixToString(matrixA)
        node = Tree(currentStateString)
        statesToExplore = [node]

        while len(statesToExplore):
            currentState = statesToExplore.pop(0)
            currentStateString = currentState.name

            if currentStateString == self.targetStateString:
                print("Answer Found!")
                result = []
                while currentState != "":
                    result.append(str(self.convertStringToMatrix(currentState.name)))
                    currentState = currentState.parent
                f = open("output.txt", "w")
                f.write('Test Case 5 - Given Start State\n')
                for matrix in reversed(result):
                    f.write('----------------------------\n')
                    f.write(matrix)
                    f.write('\n')
                f.write('Goal state')
                f.close()

                return True

            if currentStateString in self.visited:
                continue
            self.visited[currentStateString] = True
            
            children = self.getNewStates(currentStateString)
            for child in children:
                obj = Tree(child)
                obj.name = child
                obj.parent = currentState
                statesToExplore.append(obj)
            
        return False

    def getNewStates(self, currentStateString):
        """
        Input: The hashed state of the matrix.
        Output: New possible states of the matrix.

        """
        currentState = self.convertStringToMatrix(currentStateString)
        result = []
        i,j = self.getBlankTile(currentState)
        
        deepCopyState1 = copy.deepcopy(currentState) 
        deepCopyState2 = copy.deepcopy(currentState) 
        deepCopyState3 = copy.deepcopy(currentState) 
        deepCopyState4 = copy.deepcopy(currentState) 

        if i > 0:
            newState = self.swapTiles(i, j, deepCopyState1, 0)
            newStateString = self.convertMatrixToString(newState)
            if newStateString not in self.visited:
                result.append(newStateString)

        if j > 0:
            newState = self.swapTiles(i, j, deepCopyState2, 1)
            newStateString = self.convertMatrixToString(newState)
            if newStateString not in self.visited:
                result.append(newStateString)

        if i < (self.rows - 1):
            newState = self.swapTiles(i, j, deepCopyState3, 2)
            newStateString = self.convertMatrixToString(newState)
            if newStateString not in self.visited:
                result.append(newStateString) 

        if j < (self.cols - 1):
            newState = self.swapTiles(i, j, deepCopyState4, 3)
            newStateString = self.convertMatrixToString(newState)
            if newStateString not in self.visited:
                result.append(newStateString)
        
        return result

    def swapTiles(self, i,j, matrix, mode):
        """
        Description: Swapping the number with 0 position
        """
        if mode == 0:   
            matrix[i][j], matrix[i-1][j] = matrix[i-1][j], matrix[i][j]
        elif mode == 1:
            matrix[i][j], matrix[i][j-1] = matrix[i][j-1], matrix[i][j]
        elif mode == 2:
            matrix[i][j], matrix[i+1][j] = matrix[i+1][j], matrix[i][j]
        elif mode == 3:
            matrix[i][j], matrix[i][j+1] = matrix[i][j+1], matrix[i][j]
        return matrix

    def getBlankTile(self, matrix):
        """
        Description: Getting the position of the blank Tile
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if matrix[i][j] == 0:
                    return i,j

    def convertMatrixToString(self, matrix):
        """
        Description: Hashing the matrix to string.
        """
        string = ""

        for i in range(self.rows):
            for j in range(self.cols):
                num = matrix[i][j]
                string += self.matchingNumToString[num]

        return string
    
    def convertStringToMatrix(self, string):
        """
        Description: UnHashing the string to matrix.
        """
        matrix = []

        listOfWords = re.sub( r"([A-Z])", r" \1", string).split()
        for word in listOfWords:
            matrix.append(self.matchingStringToNum[word])           

        matrix = np.array(matrix)
        matrix = np.reshape(matrix, (self.rows,self.cols))

        return matrix


#################################################
#Uncomment any of these below chunks of line to run the code for a test case.

#Test Case 1:
# matrixA = [[1,2,3,4],[5,6,0,8], [9,10,7,12], [13,14,11,15]]
# start = TileGame(matrixA)
# print(start.bfs(matrixA))

#Test Case 2:
# matrixB = [[1,0,3,4],[5,2,7,8], [9,6,10,11], [13,14,15,12]]
# start = TileGame(matrixB)
# print(start.bfs(matrixB))

#Test Case 3:
# matrixC = [[0,2,3,4],[1,5,7,8], [9,6,11,12], [13,10,14,15]]
# start = TileGame(matrixC)
# print(start.bfs(matrixC))

#Test Case 4:
matrixD = [[5,1,2,3],[0,6,7,4], [9,10,11,8], [13,14,15,12]]
start = TileGame(matrixD)
print(start.bfs(matrixD))

#Test Case 5:
# matrixE = [[1,6,2,3],[9,5,7,4], [0,10,11,8], [13,14,15,12]]
# start = TileGame(matrixE)
# print(start.bfs(matrixE))



