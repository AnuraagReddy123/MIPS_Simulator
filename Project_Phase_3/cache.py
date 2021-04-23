import math
class Block:
    # valid bit
    # lru
    # tag

    # Function
    # Find Data
    # Store memory

    def __init__(self,blockSize):
        self.blockSize = blockSize
        self.block = [] # declare empty list for storing the tags later
        pass

    def storeAddresses(self,tag):
        self.block.clear() # clear up the block to store the new addresses
        for i in range(self.blockSize): # referring to every byte the block will store
            self.block.append(tag) # store the tag bits into the list
    pass

class Set:
    # Number of blocks
    # List of block objects

    # Function
    # Find Block

    pass

class Cache:
    # Number of sets
    # List of set objects


    pass


'''

li $v0, 4


0x10010000      0b10000000000010000000000   000    000
0x10010001                                         001 
0x10010002
0x10010003

0x10010004      0b10000000000010000000000   000    100
0x10010005
0x10010006
0x10010007

0x10010008      0b10000000000010000000000   001    000

0x1001000c      0b10000000000010000000000   001    100

0x10010010      0b10000000000010000000000   010    000      

00
01
02
03

tag index offset

128B
2 way assoc
8B block size


offset 3
index 3
tag 26 

set 0       set 1        set 2              ...             set 7
1   2       
1   4





0x10010004


tag 0b10000000000010000000000   
index 000    
offset 100

tag 0b10000000000010000000000000 000 111
'''