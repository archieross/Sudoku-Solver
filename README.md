# Sudoku-Solver
Year 1 Coursework - Using the theory behind Constraint Satisfaction Problems to solve 9x9 Sudoku

My solution uses a Constraint Satisfaction Problem (CSP) approach. However, instead of checking whether a particular sudoku satisfies the constraints, only sudoku states that satisfy the constraints are propagated. The only time my solution checks whether or not the constraints have been satisfied is when process_sudoku(sudoku) runs with the entered sudoku to check whether or not the sudoku is even solvable to begin with. 

I find the empty cell to propagate based on a 9x9 heuristic board called numOfDomains whose elements correspond to the respective cells on the sudoku board. The heuristic varies with each cell assignment. The heuristic checks whether any cells have only one possible domain when checking a row, then column, and then region (3x3 box). If at any point only one domain is available in a row, column or region, the heuristic will stop calculating values as this cell will always be the quickest to fill (for the given entered sudoku) because it limits branching. Therefore the heuristic is always a variation in the sum of the row, column and region's possible domains. 

The sudoku is copied by value to a variable currentSudoku. The algorithm will then fill currentSudoku in the cell with the lowest heuristic with that cell's possible domain(s) (by looking at its row, column and region). This process happens recursively until either it must backtrack, a solution has been found or no solution exists.

I also found that my solution ran faster when using python lists instead of numpy arrays. So, I converted the numpy sudoku to a 2D array first and then converted the solution to a numpy array before returning it.

To conclude, my solution uses a CSP approach which uses a variable heuristic to decide which of the cells to propagate next.
