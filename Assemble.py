import sys
import csv
opCodes = {}

with open('DLXPairs.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #Add instruction name with its number (decimal)
        opCodes[row['Instruction']] = int(row['Decimal'])

# Check opcodes
# for opCode in opCodes:
#     print(f"{opCode}: {opCodes[opCode]}")

def writeHeader(file, depth, width):
    file.write(f"DEPTH = {depth};\n")
    file.write(f"WIDTH = {width};\n")
    file.write("ADDRESS_RADIX = HEX;\n")
    file.write("DATA_RADIX = HEX;\n")
    file.write("CONTENT\nBEGIN\n\n")

if len(sys.argv) == 4:
    sourceFile = sys.argv[1]
    dataFile = sys.argv[2]
    codeFile = sys.argv[3]
else:
    sourceFile = sys.argv[1]
    dataFile = sys.argv[2]
    print("Usage: python Assemble.py <sourceFile>.dlx <dataFile>.mif <codeFile>.mif")
    #sys.exit(1)
    #Later add auto file name gen for only one parameter

#Track when we are in data or text section
data = 0
text = 0
dataInst = []
codeInst = []
labels = []

#Check the file was correct
try:
    with open(sourceFile, 'r') as file:
        print(f"File '{sourceFile}' opened successfully.")

except FileNotFoundError:
    print(f"Error: The file '{sourceFile}' was not found.")
    exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)

with open(sourceFile, 'r') as file:
        address = 0
        # Loop through each line
        for line in file:
            # Strip whitespace from the end of the line
            lineC = line.strip()
            #Dont do nothing with comments
            if lineC.startswith(';'):
                continue

            # Skip any empty lines
            if not lineC:
                continue

            #Check for section changes
            if lineC == ".data":
                address = 0
                data = 1
                text = 0
                continue
            elif lineC == ".text":
                address = 0
                data = 0
                text = 1
                continue

            # Replace all Parenthese with a single space
            lineCmd = lineC.replace('(', ' ')
            lineCmd = lineCmd.replace(')', ' ')
            # Replace all commas with a single space
            lineCmd = lineCmd.replace(',', ' ')
            #Is label if there was no whitespace at beginning
            if len(lineC.split()) == 1 and text == 1:
                #Means it is a simple label
                #Store current address as label
                labels.append([lineC, address])
                continue
            elif data == 1:
                #If more stuff Store in data and do increment
                dataInst.append(lineCmd.split())
                #Add variables to label as well!!!
                labels.append([lineCmd.split()[0], address])
                address += 1
                continue

            # Split the line into a list of items
            instructions = (lineCmd.split())
            #Store in data or text variables
            codeInst.append(instructions)
            address += 1

#Testing
print("Data Instructions:\n")
for line in dataInst:
    print(line)
print("\nCode Instructions:\n")
for line in codeInst:
    print(line)
print("\nLabels:\n")
for line in labels:
    print(line)

#Write out
with open(dataFile, 'w') as dataOut:
    address = 0
    #Write header
    writeHeader(dataOut, 1024, 32)
    #write all the stuff
    for index, line in enumerate(dataInst):
        #Loop through size of var
        length = int(line[1])
        for i in range(length):
            #Loops through size of array
            #Print out each line
            dataOut.write(f'{address:03X}')
            dataOut.write(" : ")
            dataOut.write(f'{int(line[i+2]):08X}')
            dataOut.write(";")
            dataOut.write(" --" + line[0] + "[" + str(i) + "]\n")
            address += 1
    dataOut.write(f"\nEND;")

#Bit masks or shifts?
opCodeMask  =   0b11111100000000000000000000000000 # << 26
reg1Mask    =   0b00000011111000000000000000000000 # << 21
reg2Mask    =   0b00000000000111110000000000000000 # << 16
reg3Mask    =   0b00000000000000001111100000000000 # << 11
unusedMask  =   0b00000000000000000000011111111111 # << 0
immMask     =   0b00000000000000001111111111111111 # << 0
absAddrMask =   0b00000011111111111111111111111111 # << 0
opCodeShift  =   26
reg1Shift    =   21
reg2Shift    =   16
reg3Shift    =   11
unusedShift  =   0
immShift     =   0
absAddrShift =   0
baseAddrShift=   0
with open(codeFile, 'w') as codeOut:
    address = 0
    #Write header
    writeHeader(codeOut, 1024, 32)
    #write all the stuff
    for index, line in enumerate(codeInst):
        #Find the Binary for each instruction
        #Get opcode
        opCodeText = line[0]
        opcode = opCodes.get(opCodeText)
        print(opcode)
        #If all are operanda are registers it is Register type
        #If one operand is an emmediate value (number?) it is Immediate type
        #If it modifies the program counter is is Jump type
        #Load/store data, memory to/from register is memory type
        instructionCode = 0
        params = []
        param = 0
        #Need to check for labels and variables(indexed)
        for i in range(len(line) - 1):
            #Figure out if reg number or actual number or label address or variable address
            # isArray = False
            # varName = line[i + 1].split('(')[0]
            # for label in labels:
            #     if varName in label and '(' in line[i + 1]:
            #         isArray = True
            #         break
            # #If array variable with index
            # if isArray:
            #     #If reg value indexed then find val
            #     #And find the address of that index of this var
            #     param = 0
            #Split by '(' to get parameters
            if line[i + 1] in [label[0] for label in labels]:
                #Labels or single variable
                for label in labels:
                    if line[i + 1] == label[0]:
                        param = label[1]
                        break
            elif line[i + 1].startswith('R'):
                #Register
                param = int(line[i + 1][1:])
            elif line[i + 1].isnumeric():# or (line[i + 1][0] == '-' and line[i + 1][1:].isnumeric()):
                #Immediate number
                param = int(line[i + 1])
            params.append(int(param))
        #Everything gets op code
        instructionCode |= (opcode << opCodeShift)
        if opCodeText in ['NOP']:
            #Stays zero
            instructionCode = 0
        #We could check the 2 load/store op codes,
        elif opCodeText in ['LW']:
            #Memeory type has opcode, r_data, r_offset, base_address
            instructionCode |= (params[0] << reg1Shift)  # r_data
            instructionCode |= (params[1] << baseAddrShift)
            if len(params) > 2:
                instructionCode |= (params[2] << reg2Shift)
        elif opCodeText in ['SW']:
            #Memeory type has opcode, r_data, r_offset, base_address
            instructionCode |= (params[0] << baseAddrShift) 
            if len(params) > 2:
                instructionCode |= (params[1] << reg2Shift)  # r_offset
                instructionCode |= (params[2] << reg1Shift)
            else:
                instructionCode |= (params[1] << reg1Shift)  # r_data
        #then check for the 4-6 jump/branch op codes,
        elif opCodeText in ['J', 'JR', 'JAL', 'JALR']:
            #Jump type has opcode, absolute_address
            instructionCode |= (params[0] << absAddrShift)  # absolute_address
        elif opCodeText in ['BEQZ', 'BNEZ']:
                instructionCode |= (params[0] << reg1Shift)  # rs1
                instructionCode |= (params[1] << immShift)  # absolute_address/Immeditate
        #then check for I in code
        elif opCodeText in ['ADDI', 'ADDUI', 'SUBI', 'SUBUI', 'ANDI', 'ORI', 'XORI', 'SLLI', 'SRLI', 'SRAI', 'SLTI', 'SLTUI', 'SGTI', 'SGTUI', 'SLEI', 'SLEUI', 'SGEI', 'SGEUI', 'SEQI', 'SNEI']:
            #Immediate type has opcode, rd, rs1, immediate
            instructionCode |= (params[0] << reg1Shift)  # rd
            instructionCode |= (params[1] << reg2Shift)  # rs1
            instructionCode |= (params[2] << immShift)   # immediate
        #Else assume register type
        else:
            #Register type has opcode, rd, rs1, rs2, unused
            instructionCode |= (params[0] << reg1Shift)  # rd
            if len(params) > 1:
                instructionCode |= (params[1] << reg2Shift)  # rs1
            if len(params) > 2:
                instructionCode |= (params[2] << reg3Shift)  # rs2
            #instructionCode |= (0 << unusedShift)        # unused

        #Print out each line
        codeOut.write(f'{address:03X}')
        codeOut.write(" : ")
        codeOut.write(f'{int(instructionCode):08X}')
        codeOut.write(";")
        codeOut.write(" --")
        for i in range(len(line)):
            codeOut.write(line[i] + " ")
        codeOut.write("\n")
        address += 1
    codeOut.write(f"\nEND;")




