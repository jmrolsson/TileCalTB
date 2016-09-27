#!/usr/bin/env python

#Roman Hartmann



import signal
import sys

def exit_handler(signal, frame):
    print('^C')
    sys.exit(0)


signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)
#signal.signal(signal.SIGKILL, exit_handler)


# sPC = "pc7600nr3"
# sIP = "137.138.209.74"
# sCommand = "ssh -t -t {0} cat /home/table/TileMoveTable/logBook.txt".format(sIP)
# sCommand = "ssh {0} cat /home/table/TileMoveTable/logBook.txt".format(sIP)             #run this when execting manually

def parse_log(sLogFilePath):
    "parse table log file and return dictionary that will be pushed to IS"
    sCommand = "/bin/cat {0}".format(sLogFilePath)

    from subprocess import Popen, PIPE
    oProc = Popen(sCommand, stdin=PIPE, stdout=PIPE, shell=True)
    (sStdout, sErr) = oProc.communicate()

    try:
        sLastLine = sStdout.split("\n")[-2]         #[-1] is '' because of last \n
        lLastLine = sLastLine.split()


        return lLastLine
    except IndexError:
        return None







while True:
    #parse the log from the remote control table
    lTableLog = parse_log("/mnt/TableRemoteControl/logBook.txt")

    if lTableLog:
        dTableMeta = {
            "sTimeStamp": lTableLog[0:2],
            "sAction": lTableLog[2],
            "sTableSetup": lTableLog[3],
            "lEncoded": lTableLog[4:8],
            "sEncodedMeta": " ".join(lTableLog[8::]) if len(lTableLog)>8 else "",
            "lPosition": [None, None, None]      #TODO (z,theta,phi)
        }
    else:
        dTableMeta = {
            "sTimeStamp": None,
            "sAction": None,
            "sTableSetup": None,
            "lEncoded": [None, None, None, None],
            "sEncodedMeta": None,
            "lPosition": [None, None, None]
        }


    sTableSetup = dTableMeta['sTableSetup']



    # #move the muon wall
    # if sTableSetup:
    #     from subprocess import Popen, PIPE
    #     # sPC = "pc7600nr3"
    #     sIP = "137.138.209.74"
    #     sMoveCommand = "ssh {0} python /home/table/TileMoveTable/muon_wall_controller.py {1}".format(sIP, sTableSetup)
    #     #ssh 137.138.209.74 python /home/table/TileMoveTable/muon_wall_controller.py M0_20deg_A-3
    #     Popen(sMoveCommand, stdin=PIPE, stdout=PIPE, shell=True)



    #log the muon wall position
    lMuonLog = parse_log("/mnt/TableRemoteControl/logBookMuonWall.txt")

    if lMuonLog:
        dMuonMeta = {
            'sTimeStamp': lMuonLog[0:2],
            'sAction': lMuonLog[2],
            'rMuonPosition': lMuonLog[4],
            'sPositionMeta': " ".join(lTableLog[5::]) if len(lTableLog)>5 else ""
        }
    else:
        dMuonMeta = {
            'sTimeStamp': None,
            'sAction': None,
            'rMuonPosition': None,
            'sPositionMeta': None
        }





    #set the metadata in the IS
    import ispy
    import json

    #get object
    oPartition = ispy.IPCPartition("TileTB")
    oIS = ispy.ISObject(oPartition, 'RunParams.UserMetaData', 'UserMetaData')

    #write
    lsInput = [
        'TableSetup:={0}'.format(json.dumps(dTableMeta['sTableSetup'])),
        'TileTableTimeStamp:={0}'.format(json.dumps(dTableMeta['sTimeStamp'])),
        'TileTableLastAction:={0}'.format(json.dumps(dTableMeta['sAction'])),
        'TileTableEncoders:={0}'.format(json.dumps(dTableMeta['lEncoded'])),
        'MuonTimeStamp:={0}'.format(json.dumps(dMuonMeta['sTimeStamp'])),
        'MuonLastAction:={0}'.format(json.dumps(dMuonMeta['sAction'])),
        'MuonPosition:={0}'.format(json.dumps(dMuonMeta['rMuonPosition'])),
    ]
    oIS.RunTags = lsInput

    oIS.checkin()


    import time
    time.sleep(125)














