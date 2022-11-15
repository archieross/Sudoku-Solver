import numpy as np

domains = [1, 2, 3, 4, 5, 6, 7, 8, 9]



#Checks whether a state satisfies some given constraints
def MinimumCellFinder(sudoku, numOfDomains):
    
    blankCellOrder = []

    for i in [0,1,2,3,4,5,6,7,8]:

        for j in [0,1,2,3,4,5,6,7,8]:

            if sudoku[i][j] == 0:
                blankCellOrder.append([numOfDomains[i][j], [i, j]])
                
    minimum = 99
    
    blankCellLength = len(blankCellOrder)
    
    if blankCellLength == 0:
        return False

    for i in range(blankCellLength):
        
        blankCellHeuristic = blankCellOrder[i][0]
        
        if blankCellHeuristic < minimum:
            
            minimum = blankCellHeuristic
            minimumCoordinates = blankCellOrder[i][1]
        
            
    return minimumCoordinates

def DomainFinder(sudoku, minimumCell):
    

        rowSet = set(domains)
        columnSet = set(domains)
        regionSet = set(domains)


        for elementRow in sudoku[minimumCell[0]]:
            
            try:
                rowSet.remove(elementRow)
            except:
              continue

        for elementColumn in [0,1,2,3,4,5,6,7,8]:
            
            try:
                columnSet.remove(sudoku[elementColumn][minimumCell[1]])
            except:
              continue

        neededValueRow = (minimumCell[0] // 3) * 3  #Reduces computation time as only need to do calculation once and not twice.
        neededValueColumn = (minimumCell[1] // 3) * 3

        for row in range(neededValueRow, neededValueRow + 3):

            for column in range(neededValueColumn, neededValueColumn + 3):

              try:
                regionSet.remove(sudoku[row][column])
              except:
                continue

        #Now we have all our domain sets, we need to find the overlap between all the sets - this tells us which domains are possible in row, column and region.


        possibleDomains = set.intersection(rowSet, columnSet, regionSet)

        possibleDomains = list(possibleDomains)
        
        return possibleDomains


def CSP(sudoku):

    global goalFound
    global solution
    
    #Num of domains is a heuristic sudoku board. It uses a variation of possible domains in row, column and region. 
    numOfDomains = HeuristicCalculator(sudoku)

    
    #Finds the order in which blank cells will be propagated.
    minimumCell = MinimumCellFinder(sudoku, numOfDomains)
    
    if minimumCell == False:
        return False
    

    #We now have our coordinates for least possible domains
    #Now we have to find possible domains and explore them all.
    
    nextSudoku = []
    
    for row in [0,1,2,3,4,5,6,7,8]:
        
        theRow = []
        
        for column in [0,1,2,3,4,5,6,7,8]:
            
            theRow.append(sudoku[row][column])
        
        nextSudoku.append(theRow)
        


    possibleDomains = DomainFinder(sudoku, minimumCell)

    for domain in possibleDomains:

        nextSudoku[minimumCell[0]][minimumCell[1]] = domain

        if goalFound:
            return True

        elif isGoal(nextSudoku):
            goalFound = True
            return True

        elif CSP(nextSudoku):
            return True


    return False
    


def HeuristicCalculator(sudoku):
    
    numOfDomains = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    stop = False
    
    #Looking at number of empty on a row (corresponds to number of available domains)
    for row in [0,1,2,3,4,5,6,7,8]:

        numOfEmpty = sudoku[row].count(0)
        
        if numOfEmpty == 1:
            numOfEmpty = -1
            stop = True

        for element in [0,1,2,3,4,5,6,7,8]:

            numOfDomains[row][element] += numOfEmpty
            
            
        if stop:
            return numOfDomains
        

    #Columns - num of domains
    for column in [0,1,2,3,4,5,6,7,8]:

        numOfEmpty = 0

        for row in [0,1,2,3,4,5,6,7,8]:

            if sudoku[row][column] == 0:
                numOfEmpty += 1
        
        if numOfEmpty == 1:
            stop = True
            numOfEmpty = -99

        for row in [0,1,2,3,4,5,6,7,8]:

            numOfDomains[row][column] += numOfEmpty
        
        if stop:
            return numOfDomains
        
    

    #Add number of possibles domains from regions
    for regionRow in [0,1,2]:

        for regionColumn in [0,1,2]:

            blankCount = 0

            for row in [0,1,2]:

                for column in [0,1,2]:

                    if sudoku[(row + (3 * regionRow))][(column +(3 * regionColumn))] == 0:
                        blankCount += 1
            
            if blankCount == 1:
                blankCount = -99
                stop = True
            

            for row in [0,1,2]:

                for column in [0,1,2]:

                    numOfDomains[row + (3 * regionRow)][column + (3 * regionColumn)] += blankCount
            
            if stop:
                return numOfDomains
    
    
    return numOfDomains






def BlankCellChecker(row):

  if row.count(0) != 0:

    return True

  
  return False




def isGoal(sudoku):
    
    global solution


    #If all cell are also filled in continue <-- We are checking this proposition first as it has a lower time compledity than the ConstraintChecker. This is also a situation which is only ever true for a consistent solution so will be false most of the algorithm.
    for row in sudoku:
      
      if BlankCellChecker(row):
        return False
      
    solution = sudoku
    return True

def SameOnRows(sudoku):
    
    for row in sudoku:
        
        for domain in domains:
        
            if row.count(domains) > 1:
                return True

def SameOnColumn(sudoku):
    
    for column in [0,1,2,3,4,5,6,7,8]:
        
        theColumn = []
        
        for row in [0,1,2,3,4,5,6,7,8]:
            
            theColumn.append(sudoku[row][column])
        
        for domain in domains:
            
            if theColumn.count(domain) > 1:
                return True
            
def SameOnRegion(sudoku):
    
    for regionRow in [0,1,2]:

        for regionColumn in [0,1,2]:
            
            region = []
            
            for row in [0,1,2]:

                for column in [0,1,2]:

                     region.append(sudoku[(row + (3 * regionRow))][(column +(3 * regionColumn))])
            
            for domain in domains:
                
                if region.count(domain) > 1:
                    return True
    
    return False
                        

def initialLegalityChecker(sudoku):

        if SameOnRows(sudoku):
            return True
        
        if SameOnColumn(sudoku):
            return True
        
        if SameOnRegion(sudoku):
            return True
        
        return False


def sudoku_solver(sudoku):
    
    global goalFound
    global solution
    
    goalFound = False
    
    sudoku = sudoku.tolist()


    #setting solution to -1 sudoku board so that should no solution be found, it will be returned.
    solution = [[-1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1]]
    
    if initialLegalityChecker(sudoku):
        return solution
    
    
    
    #The given sudoku is entered into the CSP. A solution will then be returned.
    CSP(sudoku)
    
    solution = np.array(solution)
    return solution
