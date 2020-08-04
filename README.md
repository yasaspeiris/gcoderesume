# GCODE Resume!
A small python script to edit GCODE files to resume 3D prints after power loss.

1. Measure the height from the hot bed to the top of the existing print. (Preferably using a vernier caliper)
2. Find the closest Z value. Eg : For a print with a layer hieght of 0.2mm, layers will be in increments of 0.2mm.
3. Run the script,
    Syntax : 
    
    python gcoderesume.py -i [input gcode file] -z [layer height]

    Eg : If your print failed at Z26.8,
    
    python gcoderesume.py -i EBA3_004.gcode -z 26.8
    
4. Use the generated gcode file to start the print.
