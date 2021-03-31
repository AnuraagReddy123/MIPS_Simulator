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

We have incorporated pipeline into our simulator in the second phase of our simulator. We have followed the MIPS
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
The program can be run from the main.py file in the PROJECT_PHASE_2 folder. A couple of test files written in MIPS are also
available to test the simulator.To print the data segment which is huge, one can uncomment the commented line in line 66 
in main.py file. 
