import math
import sim_glob

class Block:
    # valid bit
    # lru
    # tag

    # Function
    # Find Data
    # Store memory

    def __init__(self,blockSize):
        self.validBit = 0
        self.blockSize = blockSize
        self.tag = None # empty block

    def storeAddresses(self,tag,lru):
        self.tag = tag # store the tag bits
        self.lru = lru # store the lru bit

    def searchAddress(self,address,indexBits):
        offset = math.log2(self.blockSize) # get the number of off set bits
        tag = address[:32-indexBits-offset] # get the tag bits of the address
        if self.tag == None or self.tag != tag:
            return None # if the block was empty or the block doesn't have the required tag
        index = int(address,2) - sim_glob.base_address # fetch the index in the memory segment
        return sim_glob.data_segment[index] # return the contents of the memory at the index

class Set:
    # Number of blocks
    # List of block objects
    # Associativity

    def __init__(self, numOfBlksInSet, blockSize, numOfSets):
        self.__numOfBlksInSet = numOfBlksInSet
        self.__blocks = []
        self.__numOfSets = numOfSets
        for i in range(self.__numOfBlksInSet):
            self.blocks.append(Block(blockSize))

    def findBlock (self, addr):
        offset = math.log2(self.__blocks[0].blockSize) # get the number of off set bits
        tag = addr[:32-self.__numOfSets-offset] # get the tag bits of the address
        for i in range(len(self.__blocks)):
            if tag == self.__blocks[i].block[0]:
                return self.__blocks[i]
        return None

    def updateLRU (self, block):
        max = 0
        for blk in self.__blocks:
            if max < blk.lru:
                max = blk.lru
        block.lru = self.findMaxLRU+1
            
class Cache:
    # Number of sets
    # List of set objects

    # Functions
    # extractSetIndex
    def __init__(self,blockSize,associativity,numofBlocks):
        self.blockSize = blockSize # set the blocksize
        self.numofBlocks = numofBlocks # get the number of blocks in the cache
        self.associativity = associativity # set the associativity
        self.offset = math.log2(self.blockSize) # get the number of off set bits
        numberofSets = self.numofBlocks/self.associativity # get the number of sets
        self.indexBits = math.log2(numberofSets) # get the number of indexBits
        self.tagBits = 32 - self.indexBits - self.offset # get the number of tag bits in the cache
        self.sets = [Set(self.numofBlocks,self.blockSize,numberofSets) for i in range(numberofSets)] # make a list of sets

    def extractSetIndex(self,address):
        index = address[self.tagBits:self.tagBits+self.indexBits] # get the indexBits of the address
        return index 

    def access(self,address):
        setNumber = self.extractSetIndex(address) # get the set number
        block = self.sets[setNumber].findBlock(address) # find the block
        if block != None:
            self.sets[setNumber].updateLRU(block)
            return block.searchAddress(address,self.indexBits) # return the data
        return None # if its a cache miss

    def replaceBlock(self,address):
        index = self.extractSetIndex(address) # get the index of the set
        block = Block(self.blockSize,0) # the block to be replaced
        tag = address[:self.tagBits] # get the tag bits for the new block
        block.storeAddresses(tag,0) # make the new block with lru as 0
        self.sets[index].replaceBlock(block) # replace the least recently block in the set

    '''
    char *access (int64_t addr)
    {
        int setNo = extractSetIndex(addr);
        Block *blk = sets[setNo].findBlock(addr)
        if (blk != nullptr)
        {
            sets[setNo].updateLRU(blk);
            return blk->data;
        }
        return nullptr;
    }
    '''
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

0x10010008      0b10000000000010000000000   001    000 001 002 003

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


A B C D A E 

4 block

A(1) NULL NULL NULL
A(1) B(2) NULL NULL
A(1) B(2) C(3) NULL
A(1) B(2) C(3) D(4)
A(5) B(2) C(3) D(4)
A(5) E(6) C(3) D(4)

0x10010004


tag 0b10000000000010000000000   
index 000    
offset 100

tag 0b10000000000010000000000000 000 111



128B
2 way assoc
4B block size

offset 2
index 4
tag 26

0x10010000      0b10000000000010000000000   0000    00

0x10010040      0b10000000000010000000001   0000    00


0x10010004      0b10000000000010000000000   0001    00



set 0       set 1       set 2               ...                 set 15
1    2




'''