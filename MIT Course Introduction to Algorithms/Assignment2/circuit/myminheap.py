# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 13:18:27 2020

@author: malyr
"""

#MyMinHeap

class PriorityQueue:
    """Heap-based priority queue implementation."""
  
    def __init__(self): 
        self.heap = [None]
        
    def __len__(self):
        return len(self.heap) - 1
    

    def append(self, key):
        
        if key == None:
            raise ValueError("Bad key")

        i = len(self.heap)        
        self.heap.append(key)
        
        while i > 1:
            nodeParent = self.parent(i)
            
            if key < self.heap[nodeParent]:
#                tmp = self.heap[i]
#                self.heap[i] = self.heap[nodeParent]
#                self.heap[nodeParent] = tmp
                
                self.heap[i], self.heap[nodeParent] = self.heap[nodeParent], key
                i = nodeParent
            else:
                break
                       
        
    def parent(self, pos): 
         return pos//2
     
    def pop(self):
        """Removes the minimum element in the queue.
    
        Returns:
            The value of the removed element.
        """
        heap = self.heap
        popped_key = heap[1]
        if len(heap) == 2:
            return heap.pop()
        heap[1] = key = heap.pop()
        
        i = 1
        while True:
            left = i * 2
            if len(heap) <= left:
                break
            left_key = heap[left]
            right = i * 2 + 1
            right_key = right < len(heap) and heap[right]
            if right_key and right_key < left_key:
                child_key = right_key
                child = right
            else:
                child_key = left_key
                child = left
            if key <= child_key:
                break
            self.heap[i], self.heap[child] = child_key, key
            i = child
        return popped_key
    

    def min(self):
        """The smallest element in the queue."""
        return self.heap[1]
    
    
    def print(self):
        for i in range(len(self.heap)):
            print(self.heap[i])
            
        
        







#Test 1
            
print("-----------------------------")
a = PriorityQueue()
A = [100, 70 , 50 , 125 , 45 , 60 , 10]
for i in range(len(A)):
    a.append(A[i])
print(a.heap)
C = [None, 10, 50, 45, 125, 100, 70, 60]
print(C)
assert a.heap == C

print("-----------------------------")
print()



q = PriorityQueue()


for i in range(len(A)):
    q.append(A[i])

#print(q.pop())
q.print()

print(q.pop(), "pop")


#print(q.pop() , "pop")
#q.print()
#
#print(q.pop() , "pop")
#q.print()
#
#print(q.pop() , "pop")
#q.print()

#q.pop()
#q.pop()


