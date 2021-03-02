import globals
from operations import *

globals.initialize()

def find_label (instr, instr_num):
    label_index = instr.find(":")
    if label_index != -1:
        label = instr[:label_index]
        globals.label_dict[label] = instr_num
        instr = instr.replace(instr[:label_index+1], "")
    return instr

def clean_instruction(instr, instr_num):
    instr = instr.strip()
    instr = instr.replace("\n", "")
    
    #Searching for comments
    comment_index = instr.find('#')
    if comment_index != -1:
        globals.comments[instr[comment_index:]] = instr_num
        instr = instr.replace(instr[comment_index:], "")
        instr = instr.strip()
    
    return instr


if __name__ == "__main__":
    instr_num = 0
    with open('instructions.txt', 'r') as file:
        for instr in file:
            instr = find_label(instr, instr_num)
            instr = clean_instruction(instr, instr_num)
            
            if (instr != ""):
                globals.instructions.append(instr)
                instr_num += 1