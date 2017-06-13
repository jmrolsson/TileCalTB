# BeamElements

This repository contains various scrupts that I used during the ATLAS Tile Calorimeter test beams between October 2015 and October 2016. Each part is documented below.

For questions please contact: joakim.olsson[at]cern.ch

## MuonWall

Scripts to automatically move the muon wall into an optimal position, based on the position of the table. 

### Script for moving the muon wall
The main script for communication with the Arduino to move the muon wall is called 'muon_wall_controller.py'. It takes a table position string (such as "LB_eta-0.35") as input and translates that into a z-coordinate for the muon wall (which can move between z=0 and z=400 cm). You can also give it a z-coordinate directly with the "-z" option (see example below).

Usage:
```
python muon_wall_controller.py "TABLE_POSITION_STRING"
python muon_wall_controller.py -z Z_POSITION
```
Example:
```
python muon_wall_controller.py "LB_eta-0.35"
python muon_wall_controller.py -z 150
```

This script is stored and executed on the 'table' computer:
```
table@pc7600nr3.cern.ch:/home/table/TileMoveTable/muon_wall_controller.py 
```

### Cronjob for automatically updating the position of the muon wall
A shell script (meant to be run as a cronjob) automatically reads the log file of the table and the log file for the muon wall, compares the last known positions, and updates the position of the muon wall if necessary. 

The cronjob is setup as follows:

```
[table@pc7600nr3]~% crontab -ls
* * * * * /home/table/TileMoveTable/muwall_cronjob.py >> /home/table/TileMoveTable/log/muwall_cronjob.log 2>&1
```

### Script to parse the position of the table and the muon wall from the log files into the IS database

This script is called 'table_position_parser.py' and is stored in: 
```
/afs/cern.ch/user/t/tiledemo/public/Prometeo/Prometeo-1.0.1/TablePositionParser/share
```

## BeamChambersCalibration

To setup (if you don't have the numpy, root_numpy, and matplotlib Python packages installed already):

```
pip install numpy
pip install root_numpy
pip install matplotlib
```

Usage:
```
python CalibrateBeamChambers.py --beam-chamber <bc_number> -l <left_up_run> -c <center_run> -r <right_down_run> --plots
```

Examples:
```
python CalibrateBeamChambers.py --beam-chamber 1 -l 611274 -c 611276 -r 611278 --plots
```
```
python -b CalibrateBeamChambers.py --beam-chamber 1 -l 611274 611275 -c 611276 611277 -r 611278 611279 --plots
```



## ScopeTraces

Simple script for plotting scope traces (ASCII input) with nice colors ;)

To setup (if you don't have the numpy, matplotlib, and/or seaborn Python packages installed already):

```
pip install numpy
pip install matplotlib
pip install seaborn
```

To run:

```
python plot_scope.py
```

