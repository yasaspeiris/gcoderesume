import uuid
import re

from argparse import ArgumentParser
import os.path


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg  # return an open file handle


parser = ArgumentParser(description="Modify GCODE Files to start from given layer")
parser.add_argument("-i", dest="filename", required=True,
                    help="input GCODE file",
                    type=lambda x: is_valid_file(parser, x))
parser.add_argument('-z',dest="z_lookup",required=True , type=str,
                    help='Layer height. Eg : 4 to start at Z4, 5.6 to start at Z5.6')
args = parser.parse_args()

z_lookup = args.z_lookup
target_line = 0

inputFile = open(args.filename, "r")
lines = inputFile.readlines()
for num, line in enumerate(lines):
    if "Z"+(z_lookup)+"\n" in line:
        target_line = num
        for i in range(target_line,len(lines)):
            eFound = re.search(r'(?:[, ])E(\d+\.\d+)', lines[i])
            if eFound:
                eValue_str = eFound.group(1)
                break
        break

inputFile.close()

outputFile_name = "output_" + str(uuid.uuid4())[:8] +".gcode"
outputFile =  open(outputFile_name, "w")

outputFile.write("""M82 ;absolute extrusion mode
M201 X500.00 Y500.00 Z100.00 E5000.00 ;Setup machine max acceleration
M203 X500.00 Y500.00 Z10.00 E50.00 ;Setup machine max feedrate
M204 P500.00 R1000.00 T500.00 ;Setup Print/Retract/Travel acceleration
M205 X8.00 Y8.00 Z0.40 E5.00 ;Setup Jerk
M220 S100 ;Reset Feedrate
M221 S100 ;Reset Flowrate
M140 S60 ; start preheating the bed
M104 S200 ?T0 ; start preheating hotend
M190 S60 ; heat to bed setting in Cura and WAIT
M109 S210 ?T0 ; heat hotend to setting in Cura and WAIT
G92 Z0; set Z to 0
G1 Z10.0 F3000 ; Move Z Axis up little to prevent hitting printed parts
G28 X Y ; home X Y
G1 Z0 F3000 ; Move Z Axis down again
G92 E0 ; Reset Extruder
M300 S1000 P500 ; chirp to indicate starting to print
M104 S210 ; turn on cooling fan\n"""+
"G92 E"+eValue_str+"; set extruder to value found in starting layer\n"+
"G92 Z"+(z_lookup)+"; set Z to starting layer\n\n")

for linenumber in range(target_line,len(lines)):
    outputLine = lines[linenumber]
    outputFile.write(outputLine)
        
print("Generated "+outputFile_name)
outputFile.close()
