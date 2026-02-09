#    constant ADD		: std_logic_vector(5 downto 0) := "001000";
#	 constant ADDI		: std_logic_vector(5 downto 0) := "001100";

import sys
import csv
opCodes = {}
special_names = {"AND", "OR", "XOR", "SLL", "SRL", "SRA"}

with open('DLXPairs.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #Add instruction name with its number (decimal)
        #opCodes[row['Instruction']] = int(row['Decimal'])
        
        #Make it so already used vhdl names are changed
        name = row['Instruction']
        if name in special_names:
            name = name + "c"
        opCodes[name] = int(row['Decimal'])

sourceFile = "opCodes.txt"
# Find the longest instruction name
max_len = max(len(name) for name in opCodes)

with open(sourceFile, 'w') as file:
        address = 0
        # Loop through all op codes
        for opCode in opCodes:
            #Write the line to the file
            # file.write("    constant " + opCode + "      : std_logic_vector(5 downto 0) := ")
            # file.write(format(opCodes[opCode], '06b'))
            # file.write(";\n")
            padded_name = opCode.ljust(max_len)
            vhdl_line = f'    constant {padded_name} : std_logic_vector(5 downto 0) := "{format(opCodes[opCode], "06b")}";\n'
            file.write(vhdl_line)