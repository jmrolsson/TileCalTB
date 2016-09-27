# TileCalTB

This repository contains various scripts that I used during the ATLAS Tile Calorimeter test beams between October 2015 and October 2016. Each part is documented below.

For questions please contact: joakim.olsson[at]cern.ch

## TBAnalysis

Code for offline test beam data analysis.

## MuonWall

Scripts to automatically move the muon wall into the best position, based on the position of the table. 

## TriggerAndCalib

Scripts related to the trigger, beam elements and beam chamber calibration.

### BeamChambersCalib

To setup (if you don't have the numpy, root_numpy, and matplotlib Python packages installed already):

```
pip install numpy
pip install root_numpy
pip install matplotlib
```

Usage:
```
python CalibrateBeamChambers.py -bc BC_NUMBER -r LEFT_UP_CALIB_RUN CENTER_CALIB_RUN RIGHT_DOWN_CALIB_RUN --plots
```

Example:
```
python CalibrateBeamChambers.py -bc 1 -r 611274 611276 611278 --path tiletb_September2016 --plots
```

### ScopeTraces

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

