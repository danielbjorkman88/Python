
import rubik
from collections import deque

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    
    
    if start == end:
        return []
    
    
    
    queueF = deque([start])
    queueB = deque([end])
    visited = {}
    forwardParents = {}
    backwardParents = {}
    intersection = []
    counter = 0
    queuedItemsF = {}
    queuedItemsB = {}
    queuedItemsF[start] = 1
    queuedItemsB[end] = 1

    forward_moves = {}
    for move in rubik.quarter_twists:
        forward_moves[move] = move

    
    while len(intersection) == 0 and counter < 3047:
        currF = queueF.popleft()
        currB = queueB.popleft()
        queuedItemsF.pop(currF)
        queuedItemsB.pop(currB)


        #Forwards
        for twist in forward_moves:
            config = rubik.perm_apply(twist, currF)
            if config not in visited and config not in queuedItemsF:
                forwardParents[config] = (twist, currF)
                if config == end:
                    intersection.append(config)
                    break

                queueF.append(config)
                queuedItemsF[config] = 1
        
        #Backwards
        for twist in forward_moves:
            config = rubik.perm_apply(twist, currB)
            if config not in visited and config not in queuedItemsB:
                backwardParents[config] = (twist, currB)
                queueB.append(config)   
                queuedItemsB[config] = 1                
                    
        visited[currF] = 1
        visited[currB] = 1
        
        intersect = list(set(queueF).intersection(queueB))
        
        if len(intersect) != 0: 
            intersection.append( intersect[0])
            
        counter += 1
        
        
    if len(intersection) == 0:
        return None
    
    ans = []
    curr = intersection[0]
    while start != curr:
        twist, curr = forwardParents[curr]
        ans.insert(0,twist)
        
    curr = intersection[0]
    while end != curr:        
        twist, curr = backwardParents[curr]
        ans.append(rubik.perm_inverse(twist))
        
    
    
    return ans


