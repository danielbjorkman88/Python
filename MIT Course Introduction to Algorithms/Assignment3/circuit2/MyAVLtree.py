# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 19:44:03 2020

@author: malyr
"""

#MyAVLtree.py

class Node(object):
    
    def __init__(self, key = None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

    def insert(self, node):
        """Inserts a node into the subtree rooted at this node.
        
        Args:
          node: the node to be inserted
          
        Returns the node argument, if the node was inserted in the tree. If a node
        with the same key was found, that node is returned instead.
        """
        if node.key < self.key:
          if self.left is not None:
            return self.left.insert(node)
          node.parent = self
          self.left = node
          return node
        elif node.key > self.key:
          if self.right is not None:
            return self.right.insert(node)
          node.parent = self
          self.right = node
          return node
        return self
    
    
    def find(self, key):
      
        if self.key == key:
            return self
        elif self.key < key:
            if self.right != None:
                return self.right.find(key)
            else:
                return None
        elif self.key > key:
            if self.left != None:
                return self.left.find(key)
            else:
                return None
        
        return None

    def successor(self):
        """The node with the next larger key (the successor) in the BST.
        
        Returns a BSTNode instance, or None if this node has no successor.
        """
        if self.right is not None:
          return self.right.find_min()
        current = self
        while current.parent is not None and current is current.parent.right:
          current = current.parent
        return current.parent
   
    def delete(self):
        
        
        if self.left is None or self.right is None:
            
            if self.parent.right == self:
                if self.left is not None:
                    self.parent.right = self.left
                else:
                    self.parent.right = self.right
            else:
                if self.right is not None:
                    self.parent.left = self.right
                else:
                    self.parent.left = self.left               
            
        else:
          
          s = self.successor()
          deleted_node = s.delete()
          self.key, s.key = s.key, self.key
          return deleted_node
          
        return self
          
        
    
    def find_min(self):
      
        if self.left == None:
            return self
        else:
            return self.left.find_min()
        
    def find_max(self):
      
        if self.right == None:
            return self
        else:
            return self.right.find_max()
  
    


class BST(object):
    
    def __init__(self, node_class = Node):
        """Creates an empty BST.
        
        Args:
          node_class (optional): the class of nodes in the tree, defaults to BSTNode
        """
        self.node_class = node_class
        self.root = None
        
        

    def insert(self, key):
        """Inserts a node into the subtree rooted at this node.
        
        Args:
          key: the key of the node to be inserted
            
        Returns a BSTNode with the given key that belongs to this tree.
        """
        node = self.node_class(key)
        if self.root is None:
          self.root = node
          return node
        return self.root.insert(node)
    
    def find(self, key):
        
        if self.root is None:
            return None       
    
        return self.root.find(key)
    
    def min(self):
        
        if self.root is None:
            return None
        
        return self.root.find_min()
    
    def max(self):
        
        if self.root is None:
            return None
        
        return self.root.find_max()
    
    def delete(self, key):

        if self.root is None:
            return None     
        
        node = self.find(key)
        if node is None:
          return None
        if node is self.root:
          pseudo_root = self.node_class(None)
          pseudo_root.left = self.root
          self.root.parent = pseudo_root
          deleted_node = self.root.delete()
          self.root = pseudo_root.left
          if self.root is not None:
            self.root.parent = None
          return deleted_node
        else:
          return node.delete() 
        
        

class AVLNode(Node):
  """A node in an AVL."""
  
  def __init__(self, key):
    Node.__init__(self, key)
    self.height = 0  
    
  def update_height(self):
    """Updates pre-computed fields such as the node's subtree height."""
    self.height = self._compute_height()

  def _compute_height(self):
    """Re-computes the node's height based on the children's heights."""
    if self.left == None and self.right == None:
        return 0
    elif self.left == None:
        return 1 + self.right.height
    elif self.right == None:
        return 1 + self.left.height
    else:
        return 1 + max(self.left.height , self.right.height)


class AVL(BST):

  
    def __init__(self, node_class = AVLNode):
        BST.__init__(self, node_class)
        
    def insert(self, key):
        """Inserts a node into the subtree rooted at this node.
        
        Args:
          key: the key of the node to be inserted
            
        Returns an AVLNode with the given key that belongs to this tree.
        """
        inserted_node = BST.insert(self, key)
        self._rebalance(inserted_node)
        return inserted_node

    def delete(self, key):

        deleted_node = BST.delete(self, key)
        # NOTE: deleted_node still has its parent set, and it happens to be the
        #       first potentially out-of-balance node.
        self._rebalance(deleted_node.parent)
        return deleted_node
  
    def _rebalance(self, node):
        while node is not None:
          # NOTE: rebalance is called after an insertion or a deletion; asides from
          #       fixing the imbalance, it is also responsible for updating the
          #       cached sub-tree information in each node on the path to the root 
          node.update_height()
          
          if AVL._height(node.left) >= 2 + AVL._height(node.right):
            if AVL._height(node.left.left) < AVL._height(node.left.right):
              self._left_rotate(node.left)
            self._right_rotate(node)
          elif AVL._height(node.right) >= 2 + AVL._height(node.left):
            if AVL._height(node.right.right) < AVL._height(node.right.left):
              self._right_rotate(node.right)
            self._left_rotate(node)
          node = node.parent

    @staticmethod
    def _height(node):
        if node is not None:
          return node.height
        else:
          return -1

    def _left_rotate(self, x):
        y = x.right
        y.parent = x.parent
        if y.parent is None:
          self.root = y
        else:
          if y.parent.left is x:
            y.parent.left = y
          else:  # y.parent.right is x
            y.parent.right = y
        x.right = y.left
        if x.right is not None:
          x.right.parent = x
        y.left = x
        x.parent = y
        x.update_height()
        y.update_height()

    def _right_rotate(self, x):
        y = x.left
        y.parent = x.parent
        if y.parent is None:
          self.root = y
        else:
          if y.parent.left is x:
            y.parent.left = y
          else:  # y.parent.right is x
            y.parent.right = y
        x.left = y.right
        if x.left is not None:
            x.left.parent = x
        y.right = x
        x.parent = y
        x.update_height()
        y.update_height()
        
#    def preOrder(self, root): 
#          
#          
#            print("{0} ".format(root.key), end="") 
#            self.preOrder(root.left) 
#            self.preOrder(root.right) 
    #  
#  def add(self, key):
#    """Inserts a key in the range index."""
#    if key is None:
#        raise ValueError('Cannot insert None in the index')    
#        
#    self.insert(self.root, key)
#
#    
#  def insert(self, root, key): 
#      
#
#        
#        # Step 1 - Perform normal BST 
#        if not root: 
#            return Node(key) 
#        elif key < root.key: 
#            root.left = self.insert(root.left, key) 
#        else: 
#            root.right = self.insert(root.right, key)
            
            
#        root.height =
            
#    cont = True
#    curr = self.tree
#    while cont:
#        
#        if curr.key > key:
#            if curr.left == None:
#                curr.left = Node(key)
#                cont = False
#            else:
#                curr = curr.left
#        else:
#            if curr.right == None:
#                curr.right = Node(key)
#                cont = False
#            else:
#                curr = curr.right


    
#  def rebalance(self):
#      pass
#  
#  def remove(self, key):
#    """Removes a key from the range index."""
#    self.data.remove(key)
#  
#  def list(self, first_key, last_key):
#    """List of values for the keys that fall within [first_key, last_key]."""
#    return [key for key in self.data if first_key <= key <= last_key]
#  
#  def count(self, first_key, last_key):
#    """Number of keys that fall within [first_key, last_key]."""
#    result = 0
#    for key in self.data:
#      if first_key <= key <= last_key:
#        result += 1
#    return result
#
#  def preOrder(self, root): 
#      
#        if not root: 
#            return
#      
#        print("{0} ".format(root.val), end="") 
#        self.preOrder(root.left) 
#        self.preOrder(root.right) 
  
  
# Driver program to test above function 
#myTree = AVLtree() 
#root = None
#  
#root = myTree.insert(root, 10) 
#root = myTree.insert(root, 20) 



q = BST()
q.insert(5)
q.insert(2)
q.insert(7)
q.insert(3)
q.insert(0)
q.insert(-1)
q.insert(9)
deletedNode = q.delete(7)

assert q.root.left.key == 2
assert q.root.left.left.key == 0
assert q.root.left.left.left.key == -1
assert q.root.left.right.key == 3
assert q.min().key == -1
assert q.max().key == 9
assert q.find(-1).key == -1
assert q.find(10) == None
assert deletedNode.key == 7




q = AVL()
q.insert(5)
q.insert(2)
q.insert(7)
q.insert(3)
q.insert(0)
q.insert(10)
q.insert(11)
q.insert(4)
q.insert(6)
q.insert(1)
q.insert(51)
q.insert(8)
q.insert(9)
q.insert(-1)
q.insert(-2)
deletedNode = q.delete(7)

assert q.root.key == 5
assert q.root.left.key == 2




