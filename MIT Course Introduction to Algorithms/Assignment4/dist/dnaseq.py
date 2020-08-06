#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *
import time

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.dict = dict()
        for pair in pairs:
            self.put(pair[0], pair[1] )
        
    # Associates the value v with the key k.
    def put(self, k, v):
        
        if k not in self.dict:
            self.dict[k] = [v]
        else:
            self.dict[k].append(v)
 
       
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        
        if k not in self.dict:
            return []
        
        return self.dict[k]
    

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    
    try:
        assert k > 0
        
        sub = ""
        
        for i in range(k):
            sub = sub + next(seq)
        rh = RollingHash(sub)
        
        pos = 0
        
        while True:
            yield (rh.current_hash(), (pos, sub))
            
            pos += 1
            previtm = sub[0]
            nextitm = next(seq)
            rh.slide(previtm, nextitm)
            sub = sub[1:] + nextitm
    except StopIteration:
        return
        
    


# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
        
    try:
        assert k > 0
        
        sub = ""
        
        for i in range(k):
            sub = sub + next(seq)
        rh = RollingHash(sub)
        
        pos = 0
        
        while True:
            yield (rh.current_hash(), (pos, sub))
            
            pos += m
            for i in range(m):
                previtm = sub[0]
                nextitm = next(seq)
                rh.slide(previtm, nextitm)
                sub = sub[1:] + nextitm
    except StopIteration:
        return

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):

    start_time = time.time()

 
    out = []
       
    genA = intervalSubsequenceHashes(a, k, m)
    genB = subsequenceHashes(b, k)
    tableA = Multidict()
    
    cont = True
    while cont:
        try:
            hashA, (posA, subA) = next(genA)    
        except:
            cont = False
            break
        tableA.put(hashA, (posA, subA))    
    
    print("Table constructed")
    
    
    cont = True
    while cont:
        try:
            hashB, (posB, subB) = next(genB)    
        except:
            cont = False
            break
        
        for (posA, subA) in tableA.get(hashB):
            if subA == subB:
                out.append((posA,posB))




    print("--- %s seconds for execution ---" % (time.time() - start_time))
   
                
    return out


            
    
    
    





if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print('Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0]))
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
