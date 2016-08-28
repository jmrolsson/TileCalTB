def get_dict():
    "parses file and returns dictionary of all preset positions"
    
    dPos = {}
    with open("/home/table/TileMoveTable/table_positions.txt", 'r') as f:
        for sLine in f:
            sLine = sLine.strip()
            lLine = sLine.split(" ")
            lLine = [s.strip() for s in lLine if s!=""]
            dPos[lLine[0]] = {
                "Z": int(float(lLine[1].split("Z=")[1])),
                "Theta": round(float(lLine[2].split("Theta=")[1]), 2)
            }

    return dPos







