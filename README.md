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
Base Address for the data segment = 0x10010000\
PC = 0x40000000\
We have used little endian architecture to store data

We have used the operations
- Add
- Sub
- Load
- Load_Int
- Store
- Bne
- Jump
- Move
- Sub_Int
- Beq
- Slt
- syscall

The output format in the terminal is as follows\
  (i): Sorted Array\
  (ii): Registers List\
  (iii): Data Segment\
  (iv): PC

Some **Warnings**
- We have **not** used .globl as a keyword
- Strings are not yet accepted
- bubblesort.s is made according to our instruction set
- **Input values must be changed for different test cases and so must the value of n change**
