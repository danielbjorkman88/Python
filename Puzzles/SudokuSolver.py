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

guess = 1
x = 0
y = 2

def possible(col,row,guess):

    global grid
    if guess in grid[col,:]:
        return False
    if guess in grid[row,:]:
        return False
    
    row0 = (row//3)*3
    col0 = (col//3)*3
    
    for i in range(3):
        for j in range(3):
            if grid[x0 + i, y0 + j] == guess:
                return False
    return True

possible(7,8,7)

def solver():
    global grid
    for x in range(9):
        for y in range(9):
            if grid[x,y] == 0:
                for guess in range(1,10):
                    if possible(x,y,guess):      
                        grid[x,y] = guess
                        solver()
                        grid[x,y] = 0
                return 

solver()
print(np.matrix(grid))
        
        
        
        
        

