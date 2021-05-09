# MIPS_Simulator
Simulator for MIPS made by Naman Sharma and P. Anuraag Reddy

Naman Sharma: CS19B029\
P. Anuraag Reddy: CS19B031

We have used **Python** to make our MIPS Simulator\
Basic Folder structure is as follows:\
|\_**Simulator**\
  |\_main.py\
  |\_operations.py\
  |\_utility_functions.py\
  |\_globals.py\
|\_**Testing**\
  |\_bubble_sort.s\
  |\_sub.s\
  |\_test.s

All the operations are stored in operations.py\
Various utility functions are present in utitlity_functions.py\
Global variables such as registers, data_segment are stored in globals.py\
Testing folder contains test assembly files to run our simulator

Data segment is implemented as a list of strings with each string being a hexadecimal number that is 4 bytes long\
The simulator supports 4KB memory\
Base Address for the data segment = 0x10010000\
PC = 0x400000\
We have used little endian architecture to store data\
Output and Input are to the console

We have used the operations
- Add
- Sub
- Load
- Load_Int
- Store
- Bne
- Jump
- Move
- Add_Int
- Sub_Int
- Beq
- Slt
- syscall
- Load_Byte and Store_Byte were also coded but not used in the program. They can be used in the future phases

The output format in the terminal is as follows\
  (i): Sorted Array\
  (ii): Registers List\
  (iii): Data Segment\
  (iv): PC

Some **Warnings**
- We have **not** used .globl as a keyword
- Strings are not yet accepted
- bubblesort.s is made according to our instruction set
- **Please change the value of n in the bubblesort.js to change how many numbers will be present in the array**
- Errors are not handled yet


## Phase 2

We have incorporated pipeline into our simulator in the second phase. We have followed the MIPS
pipeline consisting of six stages: Instruction Fetch(IF), Instruction Decode and Register Fetch(IDRF),Execution(EX),
Memory(MEM) and Write Back(WB). The pipeline has only been incorporated for few instructions right now: 
- ADD
- SUB
- LOAD
- STORE
- BNE
- BEQ
- JUMP

An assembly code written using above instructions can be run on our simulator. The program first asks the user if
the program be executed wit or without forwarding. Once, the user enter the choice, the program is run and at the end
of the program, the following information is provided:
1. Registers List
2. Data Segment
3. IPC (Instructions per Cycle) upto 3 decimal places
4. Number of stalls
5. Number of cycles executed
6. The list of stalled instructions

We have assumed that each stage of the pipeline takes one cycle to complete. For incorporating the pipeline, we have
used a queue in the form of a list. The clock cycle is updated in the WB stage of every instruction. The dependencies
between instructions are checked in IDRF stage. For a branch instruction, we have assumed that the branch will not be taken
and the branch result is known in IDRF stage. So, if we find out that branch is taken , we issue a new instruction fetch 
in the next cycle and a stall occurs. Rest of the instructions also follow the pipeline along similar lines of MIPS
architecture.

### How to run:
The program can be run from the main.py file in the Project_Phase_2 folder. A couple of test files written in MIPS are also
available to test the simulator.To print the data segment which is huge, one can uncomment the commented line in line 66 
in main.py file.


## Phase 3

We have incorporated cache in the third and last phase of our simulator. We have two levels of cache L1 and L2. We have followed
the Least Recently Used cache replacement policy. The L2 cache just stores the block which is kicked out by L1 cache while replacing.
Since, its just a simulator, instead of storing the data along with the address in the cache we have just stored the address using 
the tag , index and offset bits. We have used 32 bits addresses similar to MIPS architecture. Now the the number of cycles for running
the program will increase since now we consider the latency from the memory.

For the two caches L1 and L2, we have tried to follow approximately exclusive caches. When a load or store instruction is executed and 
and some address is requested, we search in L1, if there is a hit, we update the LRU bits and return the data. If there is a miss in L1, we 
search in L2. If there is a hit in L2 now, we push that address into the L1 cache and remove it from the L2 cache. Also, if the L1 cache was
full and some block is kicked out of L1 cache while replacing, then that block is kept into L2 cache by kicking out the LRU block from L2 
if needed. Also, if there is a miss in L1 and L2 both, we fetch the data from data segment(memory) and push that address into L1. If again 
some address is kicked out of L1 to accommodate the pushed address, that address is pushed into L2 similar to what we do in case of hit in L2.

### Input Format for cache_param.txt
1. block size of L1
2. associativity of L1
3. cache size of L1
4. access latency of L1
5. block size of L2
6. associativity of L2
7. cache size of L2
8. access latency of L2
9. access latency of data segment(memory)

To implement the above explained policy more easily, we have assumed that block sizes of both the caches should be equal.The access latency of 
the data segment(memory) is also to be given in the input file. The program can be run from the main.py file in the Project_Phase_3 folder. 
The input format is to be same as in the cache_param.txt file. The input assembly code can be written test.s file. The bubble sort is already written
there. The bubble sort code reads from the data segment and sorts the numbers and puts the sorted array back in the data segment. 
Our simulator will output the following information:
1. Number of total cycles
2. Number of pipeline stalls
3. IPC (Instructions per Cycle) upto 3 decimal places
4. List of stalled instructions due to pipeline(memory instruction always have some stall due to cache access and memory access)
5. Registers
6. Miss rate of L1 cache upto 3 decimal places
7. Miss rate of L2 cache upto 3 decimal places
8. Data Segment(To print it, uncomment the line 83 in main.py file )
