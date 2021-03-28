def initialize():
    global instructions
    global label_dict
    global data_dict
    global comments
    global base_address
    global registers
    global data_segment
    instructions = [] # list of the instructions read from the file
    label_dict = {} # To store the indices of where the labels are occurring
    data_dict = {} # storing the indices for data segment
    comments = {}

    base_address = int("0x10010000",16) # address of the first byte

    registers = {'$zero' : '00000000','$at' : '00000000','$v0' : '00000000','$v1' : '00000000',
                    '$a0' : '00000000','$a1' : '00000000','$a2' : '00000000','$a3' : '00000000',
                    '$t0' : '00000000','$t1' : '00000000','$t2' : '00000000','$t3' : '00000000',
                    '$t4' : '00000000','$t5' : '00000000','$t6' : '00000000','$t7' : '00000000',
                    '$s0' : '00000000','$s1' : '00000000','$s2' : '00000000','$s3' : '00000000',
                    '$s4' : '00000000','$s5' : '00000000','$s6' : '00000000','$s7' : '00000000',
                    '$t8' : '00000000','$t9' : '00000000','$k0' : '00000000','$k1' : '00000000',
                    '$gp' : '00000000','$sp' : '00000000','$s8' : '00000000','$ra' : '00000000',}

    data_segment = ['00000000'] * 1024 #data segment (4 Kilobytes)
    global fetched_instr
    global decoded_instr
    global result_of_execution
    global latest_clock # to get the latest clock cycle of a WB that just happened
    global queue
    queue = [] # queue for storing stages of pipeline
    global dic_exe 
    global dic_mem
    dic_exe = {} # dictionary for keeping track of execution operations
    dic_mem = {} # dictionary for keeping track of memory operation
    fetched_instr = ""
    decoded_instr = {"operation": "" } #Fill rest of register values 
    result_of_execution = {}
    mem_result = {}
    final_reg_value = {}
    '''
    if() --> fetched_instr --> idrf() --> decoded_instr --> ex() --> result_of_execution --> (contd below)
                                                                 --> final_reg_value               
                                                                     (in case of add type instr)


    mem() --> mem_result -->            wb() --> final_reg_value
          --> final_reg_value
          (in case of load type instr)
    '''