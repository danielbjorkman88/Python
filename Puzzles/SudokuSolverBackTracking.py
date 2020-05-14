# -*- coding: utf-8 -*-
"""
Created on Wed May  6 18:09:49 2020

@author: malyr
"""

#Sudoku solver

import numpy as np

grid = np.array([[5,3,0,0,7,0,0,0,0],
                 [6,0,0,1,9,5,0,0,0],
                 [0,9,8,0,0,0,0,6,0],
                 [8,0,0,0,6,0,0,0,3],
                 [4,0,0,8,0,3,0,0,1],
                 [7,0,0,0,2,0,0,0,6],
                 [0,6,0,0,0,0,2,8,0],
                 [0,0,0,4,1,9,0,0,5],
                 [0,0,0,0,8,0,0,7,9]])

guess = 6
row = 1
col = 6

def possible(row,col,guess):

    global grid
    #print(grid[row,col])
    if guess in grid[:,col]:
        return False
    if guess in grid[row,:]:
        return False
    
    row0 = (row//3)*3
    col0 = (col//3)*3
    
    for i in range(3):
        for j in range(3):
            if grid[row0 + i, col0 + j] == guess:
                return False
    return True

possible(row,col,guess)

def solver():
    global grid
    for row in range(9):
        for col in range(9):
            if grid[row,col] == 0:
                for guess in range(1,10):
                    if possible(row,col,guess):  
                        grid[row,col] = guess
                        solver()
                        grid[row,col] = 0
                return 
    print(np.matrix(grid))

solver()

        
        
        
        
        

