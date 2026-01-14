import sys

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
            #Dont do nothing with comments
            if line.startswith(';'):
                continue
            # Strip whitespace from the end of the line
            lineC = line.strip()

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

            #Is label if there was no whitespace at beginning
            if len(lineC.split()) == 1 and text == 1:
                #Means it is a simple label
                #Store current address as label
                labels.append([lineC, address])
                continue
            elif data == 1:
                #If more stuff Store in data and do increment
                lineCmd = lineC.replace(',', ' ')
                dataInst.append(lineCmd.split())
                address += 1
                continue

            # Replace all commas with a single space
            lineCmd = lineC.replace(',', ' ')
            # Split the line into a list of items
            # By default, split() uses any whitespace (spaces, tabs) as a delimiter
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






