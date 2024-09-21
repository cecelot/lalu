# Credit: Mr. Mueller; not written by me
import sys

# valid instructions, case insensitive
instructions = {
    "add": "0010",
    "sub": "0011",
    "subtract": "0011",
    "ldi": "1110",
    "loadimmediate": "1110",
    "ld": "1111",
    "load": "1111",
    "st": "1011",
    "store": "1011",
    "mv": "0110",
    "mov": "0110",
    "move": "0110",
    "jmp": "00",
    "jump": "00",
    "jmpn": "01",
    "jumpn": "01",
    "nop": "0110",
    "halt": "0110",
}

nopBin = "00000110"  # move R0,R0
haltBin = "11110110"  # move R3,R3
fillerHex = "00"

# register number or value 0-3
operands = {"0": "00", "1": "01", "2": "10", "3": "11"}

# map target labels to addresses
fName = sys.argv[1]
fhandle = open(fName)
addr = 0
longestLabelLength = 0
targets = {}
for line in fhandle:
    line = line.lower().strip()
    # skip blank & comment lines
    if line == "" or line.startswith("#"):
        continue
    # remove comments at the end of the line
    if line.find("#") != -1:
        line = line[: line.find("#")].strip()
    if line.find(":") != -1:
        target = line[: line.find(":")].strip()
        targets[target] = format(addr, "06b")
        if len(target) > longestLabelLength:
            longestLabelLength = len(target)
    addr += 1
fhandle.close()


# assemble program
fhandle = open(fName)
lineNum = 0
addr = 0
program = ""
print("\nOriginal Program")
for line in fhandle:
    # print("line1 --> ",line)
    lineNum += 1
    origLine = line.strip()
    # get rid of target label
    if origLine.find(":") != -1:
        origLine = origLine[origLine.find(":") + 1 :].strip()
    line = line.lower().strip()
    # skip empty lines or comment lines
    if line.strip() == "" or line.startswith("#"):
        print("         " + line)
        continue
    # remove comments at the end of the line
    if line.find("#") != -1:
        line = line[: line.find("#")].strip()
    # get rid of target label
    target2Print = ""
    if line.find(":") != -1:
        target2Print = line[: line.find(":")].strip() + ":"
        line = line[line.find(":") + 1 :].strip()
    # print("line2 --> ",line)
    line = line.replace("\t", " ")  # replace tabs with a space
    tokens = line.split(" ", 1)
    # print("tokens --> ",tokens)
    instr = tokens[0]
    if instr == "nop":
        binaryInstr = (
            "1111" + nopBin
        )  # to preserve a leading 0 add '1111'at beginning which results in 'fxx' otherwise '00001110' becomes just e not 0e.
    elif instr == "halt":
        binaryInstr = (
            "1111" + haltBin
        )  # to preserve a leading 0 add '1111'at beginning which results in 'fxx' otherwise '00001110' becomes just e not 0e.
    elif instr not in instructions:
        print(
            "ERROR!!! '"
            + instr
            + "' on line "
            + str(lineNum)
            + " is not a valid instruction"
        )
        sys.exit()
    elif instr == "jumpn" or instr == "jmpn":
        target = tokens[1].strip()
        binaryInstr = (
            "1111" + targets[target] + "01"
        )  # to preserve a leading 0 add '1111'at beginning which results in 'fxx' otherwise '00001110' becomes just e not 0e.
    elif instr == "jump" or instr == "jmp":
        target = tokens[1].strip()
        if target in targets:
            binaryInstr = (
                "1111" + targets[target] + "00"
            )  # to preserve a leading 0 add '1111'at beginning which results in 'fxx' otherwise '00001110' becomes just e not 0e.
        else:
            print(
                "ERROR!!! '"
                + instr
                + "' on line "
                + str(lineNum)
                + " has an invalid target."
            )
            sys.exit()
    else:
        opsRaw = tokens[1].replace(" ", "")
        ops = opsRaw.split(",")
        # rd operand
        rd = ops[0].replace("r", "").strip()
        if rd not in operands:
            print(
                "ERROR!!! '"
                + ops[0]
                + "' on line "
                + str(lineNum)
                + " is not a valid destination operand"
            )
            sys.exit()
        rsOp = ops[1].replace("r", "").strip()
        if rsOp not in operands:
            print(
                "ERROR!!! '"
                + ops[1]
                + "' on line "
                + str(lineNum)
                + " is not a valid source operand"
            )
            sys.exit()
        # to preserve a leading 0 add '1111'at beginning which results in 'fxx' otherwise '00001110' becomes just e not 0e.
        binaryInstr = "1111" + operands[rd] + operands[rsOp] + instructions[instr]
    hexInstr = hex(int(binaryInstr, 2))[3:]
    hexAddr = hex(addr)[3:]
    hexAddr = "{0:#0{1}x}".format(addr, 4)
    print(
        "["
        + hexAddr[-2:]
        + "] "
        + hexInstr
        + "  "
        + target2Print
        + (" " * (longestLabelLength - len(target2Print) + 2))
        + origLine
    )
    program = program + hexInstr + " "
    addr += 1
program = program + ((fillerHex + " ") * int(64 - (len(program) / 3)))
print("\nProgram Memory (copy & paste this into your program memory)")
print(program)
fhandle.close()
