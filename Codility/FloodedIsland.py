# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 10:49:42 2020

@author: malyr
"""

# 1.FloodedIsland
#
# The city of Codicity is located at the seaside. The city area comprises N plots located along a boulevard on one side of the city. Each plot is flat, but different plots have different heights above the sea level. The relative heights of the consecutive plots are given in the form of a non-empty zero-indexed array A of N integers.
# The sea level changes constantly and many plots are sometimes under water. Water levels on consecutive days are given in the form of a non-empty zero-indexed array B of M integers.
# A slice of array A is any pair of integers (P, Q) such that 0 ≤ P ≤ Q < N. An island is a slice of consecutive plots that rise above the water’s surface. The plots on either side of each island are under water. More precisely, if the level of the water is K, then an island is a slice (P, Q) in which the level of each plot A[P], A[P + 1], ..., A[Q] is greater than K. Both of the adjacent plots should also be under water; that is:
# P = 0 or A[P − 1] ≤ K
# Q = N − 1 or A[Q + 1] ≤ K
# The goal is to calculate the number of islands on consecutive days.
# For example, given the following arrays A and B:
#     A[0] = 2    B[0] = 0
#     A[1] = 1    B[1] = 1
#     A[2] = 3    B[2] = 2
#     A[3] = 2    B[3] = 3
#     A[4] = 3    B[4] = 1
# We have the following number of islands on consecutive days:
# on the first day there is only 1 island: (0, 4),
# on the second day there are 2 islands: (0, 0) and (2, 4),
# on the third day there are 2 islands: (2, 2) and (4, 4),
# on the fourth day there aren't any islands,
# on the fifth day there are 2 islands: (0, 0) and (2, 4).
# Write a function:
# def solution(A, B)
# that, given a non-empty zero-indexed array A of N integers and a non-empty zero-indexed array B of M integers, returns a sequence consisting of M integers representing the number of islands on consecutive days.
# The sequence should be returned as:
# a structure Results (in C), or
# a vector of integers (in C++), or
# a record Results (in Pascal), or
# an array of integers (in any other programming language).
# For example, given:
#     A[0] = 2    B[0] = 0
#     A[1] = 1    B[1] = 1
#     A[2] = 3    B[2] = 2
#     A[3] = 2    B[3] = 3
#     A[4] = 3    B[4] = 1
# the function should return the array [1, 2, 2, 0, 2], as explained above.
# Assume that:
# N and M are integers within the range [1..30,000];
# each element of array A is an integer within the range [0..100,000];
# each element of array B is an integer within the range [0..100,000].
# Complexity:
# expected worst-case time complexity is O(N+M+max(A)+max(B));
# expected worst-case space complexity is O(N+M+max(A)+max(B)), beyond input storage (not counting the storage required for input arguments).
# Elements of input arrays can be modified.
from random import randint


def Solution(A,B):
    
    out = [0]*len(B)
    
    for i in range(len(B)):
        count = 0
        water = B[i]
        aboveWater = 0
        for idx in range(len(A)):
            if A[idx] - water > 0 and aboveWater == 0:
                count += 1
                aboveWater = 1
            elif A[idx] - water <= 0:
                aboveWater = 0
        out[i] = count
        
        
    return out

def Solution2(A, B):
    water_levels, current_peak, total_peaks = [1] + [0] * max(max(A),max(B)), None, 0

    for previous_water_level, water_level in zip(A[:-1], A[1:]):
    
        if water_level < previous_water_level:
            current_peak = [water_level, current_peak[1]] if current_peak else [water_level, previous_water_level]

        elif water_level > previous_water_level and current_peak != None:
            water_levels[current_peak[0]] += 1
            water_levels[current_peak[1]] -= 1
            current_peak = None
    
    water_levels[current_peak[1] if current_peak else water_level] -= 1
    
    for i, l in enumerate(water_levels): water_levels[i] = total_peaks = total_peaks + l
    
    return [water_levels[day] for day in B]

A = [2,1,3,2,3]
B = [0,1,2,3,1]
print(Solution(A,B), "Solution1")
print(Solution2(A,B),"Solution2")


 
Solution2([randint(0, 100000) for x in range(30000)],B = [randint(0, 100000) for x in range(30000)]) #Performance test
print( Solution ([9, 6, 10, 10, 1, 9, 6, 10, 2, 2, 8, 6], [3, 9, 2]), "Solution1")
print( Solution ([9, 6, 10, 10, 1, 9, 6, 10, 2, 2, 8, 6], [3, 9, 2]),"Solution2")
print( Solution([2, 1, 3, 2, 3], [0, 1, 2, 3, 1]), "Solution1")
print( Solution([2, 1, 3, 2, 3], [0, 1, 2, 3, 1]),"Solution2")
print( Solution([4, 5, 8, 5, 1, 4, 6, 8, 7, 2, 2, 5], [9, 9, 4]), "Solution1")
print( Solution([4, 5, 8, 5, 1, 4, 6, 8, 7, 2, 2, 5], [9, 9, 4]),"Solution2")





