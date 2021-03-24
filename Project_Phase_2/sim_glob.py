def initialize():
    global fetched_instr
    global decoded_instr
    global result_of_execution
    global mem_result
    global final_reg_value  #This will be used to check dependencies

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