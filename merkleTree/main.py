
import numpy as np

import hashlib
import argparse
import string

class MerkleNode():
    def __init__(self, data):
        self.right = None
        self.left  = None
        self.parent = None
        self.data  = data

class MerkleTree():
    def __init__(self):
        self.root = None
    
    def getHash(self,data):
        return hashlib.sha256(data.encode()).hexdigest()
        
    def buildTree(self, data):
        nodes = [MerkleNode(self.getHash(d)) for d in data]
        self.root = self._buildTree(nodes,1)
    
    def _buildTree(self, nodes,level):
        if len(nodes) == 1:
            return nodes[0]
        else:
            new_level =[]
            (depth, isOdd) = divmod(len(nodes),2)
            if (isOdd):
                nodes.append(MerkleNode(''))
                depth = depth + 1

            for i in range(depth):
                left = nodes[2*i]
                right = nodes[2*i+1]
                children_data = (left.data  + right.data)
                node = MerkleNode(self.getHash(children_data)) 
                node.left = left
                node.right = right
                left.parent = node
                right.parent = node
                new_level.append(node)
            return self._buildTree(new_level,level +1)

    def printTree(self):
        self._printTree(self.root,0)
        
    def _printTree(self,node, level):
        print(f"{level}: {node.data}")
        if node.left != None:
            self._printTree(node.left, level+1)
        if node.right != None:
            self._printTree(node.right,level+1)

    def getRoot(self):
        return self.root.data

    def getTrail(self,data):
        self.trail = []
        self.found_trail = []
        self._getTrail(self.root,0,data)

        # Trail not found at self.found_trail
        if len(self.found_trail) ==0:
            return list()
        # Trail found. from parent(root), get the sibilings
        hash_trail = [self.root]
        for idx in range(len(self.found_trail)-1):
            if (self.found_trail[idx].left.data == self.found_trail[idx+1].data):
                hash_trail.append((self.found_trail[idx].right,'left'))
            elif (self.found_trail[idx].right.data == self.found_trail[idx+1].data):
                hash_trail.append((self.found_trail[idx].left,'right'))
        return hash_trail
        
    def _getTrail(self,node, level,data):
        self.trail.append(node)
        if(node.left ==None and node.right == None and data == node.data):
            self.found_trail = list(self.trail)
        if node.left != None:
            self._getTrail(node.left, level+1,data)
        if node.right != None:
            self._getTrail(node.right,level+1,data)
        
        self.trail.pop()

    def verifyTrail(self,trail, data):
        hash = None
        root = trail[0]
        hash = data
        new_trail = list(trail[1:])
        new_trail.reverse()
        for (node,direction) in new_trail:
            if direction == 'left':
                term =  hash + node.data
            else:
                term = node.data + hash
            hash = self.getHash(term)
        return hash == root.data

def main():
    file = "01234567" 
    data = list(file)

    tree = MerkleTree()
    tree.buildTree(data)

    print(f"Root: {tree.getRoot()}")

    tree.printTree()

    trail = tree.getTrail(tree.getHash("3"))
    ret = tree.verifyTrail(trail,tree.getHash("3"))
    print(f"{ret}")

if __name__ == "__main__":
    main()
