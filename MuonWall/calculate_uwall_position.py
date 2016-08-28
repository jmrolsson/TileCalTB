#!/usr/bin/env python

#romhartmann@gmail.com

def get_muon_position(sTableSetup=None):
    """
    accpets optional string argument, for which it returns integer Z position
    for the argument setup.  If no String provided, returns all positions
    """

    #table width in mm
    rTableWidth = 2750

    #offset between center of table to middle of uWall
    rCenterOffset = 2820-1360

    import table_positions
    dTablePos = table_positions.get_dict()


    def muon_pos(sTablePos):
        "calculate the position of the muon wall based of table position"
        import math
        rMuonMin = 0
        rMuonMax = 4000
        if sTablePos not in dTablePos.keys():
            print "Table position not one of predefined positions"
            #return (rMuonMax-rMuonMin)/20   #half of max in cm
            return sTablePos 
        rThetaDeg = dTablePos[sTablePos]['Theta']
        rTheta = rThetaDeg * math.pi /180
        rTableZ = dTablePos[sTablePos]['Z']
        rMuonPos = rTableZ + (rTableWidth* math.tan(rTheta)) + rCenterOffset
        #check that its between limits, else set to limits
        rMuonPos = rMuonPos if (rMuonPos>=rMuonMin and rMuonPos<=rMuonMax) else rMuonMin if rMuonPos<rMuonMin else rMuonMax

        return int(rMuonPos/10)   #to convert to cm



    #calculate muon position for each table position
    dMuonPos = {}
    for sKey in dTablePos.keys():
        dMuonPos[sKey] = {
            'Z': muon_pos(sKey),
            'Theta': dTablePos[sKey]['Theta']
        }


    if sTableSetup not in dTablePos.keys() and sTableSetup!=None:
        #return 200   #half of max in cm
        return "Undefined" 
    elif sTableSetup != None:
        return dMuonPos[sTableSetup]['Z']
    else:
        return dMuonPos



# def print_dict(d):
#     for i in range(len(d.keys())):
#         print "{0}:  {1}".format(d.keys()[i], d.values()[i])


# print_dict(get_muon_position())



if __name__ == '__main__':
    import sys
    if len(sys.argv) >1:
        print get_muon_position(sys.argv[1])
    else:
        print get_muon_position()
