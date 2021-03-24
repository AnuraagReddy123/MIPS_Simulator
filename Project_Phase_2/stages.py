import sim_glob

def ifetch():
    pass

def idrf(clock):
    '''
    check for dependency with prev instr
    if yes:
        check if dep_reg value present in final_reg_value
        if yes:
            enqueue ex(decoded_instr, dependent_reg, clk+1)
        else:
            stall
            enqueue idrf(fetched_string, clk+1)
    else:
        enqueu ex(decoded_instr, dependent_reg, clk+1)
    '''
    
    pass

def ex(clock):
    '''
    
    '''
    
    pass

def mem():
    pass

def wb():
    pass