import re
import numpy as np
import copy 


class Tree:
    def __init__(self, node):
        self.node = node
        self.parent = None

    def backTrack(self, child):
        print("Entereted Tree class")
        print(type(child))
        print(child)
        print(child.parent)
        # child = child.parent
        # while child != None:
        #     print(child)
        #     child = child.parent
            

        # return True
class TileGame(Tree):

    def __init__(self, initialState):
        self.initialState = initialState
        self.rows = len(self.initialState)
        self.cols = len(self.initialState[0])
        self.visited = {}
        self.matchingNumToString = {1:"One", 2:"Two", 3:"Three", 0:"Zero", 4:"Four", 5:"Five", 6:"Six", 7:"Seven", 8:"Eight"}
        self.matchingStringToNum = {"One":1, "Two":2, "Three":3, "Zero":0, "Four":4, "Five":5, "Six":6, "Seven":7, "Eight":8}
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
    def dfs(self,matrixA):

        currentStateString = self.convertMatrixToString(matrixA)
        statesToExplore = [currentStateString]

        while len(statesToExplore):

            currentStateString = statesToExplore.pop()
            if currentStateString in self.visited:
                continue
            self.visited[currentStateString] = True
            print(currentStateString)
            if currentStateString == self.targetStateString:
                print("Answer Found!")
                # leaf = Tree(currentStateString)
                # print(leaf.parent, "this is the parent")
                # Tree.backTrack(self, leaf)
                return True

            children = self.getNewStates(currentStateString)
            for child in children:
                print(child, "child of", currentStateString)
                statesToExplore.append(child)
                obj = Tree(child)
                obj.parent = currentStateString
            print("---------------------------------------")
        return False



    def getNewStates(self, currentStateString):

        currentState = self.convertStringToMatrix(currentStateString)
        result = []
        i,j = self.getBlankTile(currentState)
        print(currentState)
        deepCopyState = copy.deepcopy(currentState) 
        print("Blank tile located at,",i,j)
        if i > 0:
            newState = self.swapTiles(i, j, currentState, mode = 0)
            newStateString = self.convertMatrixToString(newState)
            if newStateString not in self.visited:
                result.append(newStateString)

        currentState = deepCopyState
        if j > 0:
            newState = self.swapTiles(i, j, currentState, mode = 1)
            newStateString = self.convertMatrixToString(newState)
            if newStateString not in self.visited:
                result.append(newStateString)

        currentState = deepCopyState
        if i < len(currentState) - 1:
            newState = self.swapTiles(i, j, currentState, mode = 2)
            newStateString = self.convertMatrixToString(newState)
            if newStateString not in self.visited:
                result.append(newStateString)        

        currentState = deepCopyState
        if j < len(currentState[0]) - 1:
            newState = self.swapTiles(i, j, currentState, mode = 3)
            newStateString = self.convertMatrixToString(newState)
            if newStateString not in self.visited:
                result.append(newStateString)
        
        return result

    def swapTiles(self, i,j, matrix, mode):
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
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    return i,j

    def convertMatrixToString(self, matrix):
        string = ""

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                num = matrix[i][j]
                string += self.matchingNumToString[num]

        return string
    
    def convertStringToMatrix(self, string):
        matrix = []

        listOfWords = re.sub( r"([A-Z])", r" \1", string).split()
        for word in listOfWords:
            matrix.append(self.matchingStringToNum[word])           

        matrix = np.array(matrix)
        matrix = np.reshape(matrix, (self.rows,self.cols))

        return matrix




matrixA = [[3,1,4],[5,2,0], [8,7,6]]
start = TileGame(matrixA)
print(start.dfs(matrixA))