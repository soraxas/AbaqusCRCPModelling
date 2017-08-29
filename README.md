# Abaqus CRCP Script

Python scripting interface for building a 2D/3D CRCP model in Abaqus.

## plot.py

This is the script for automatically creating path and XY data in the 2D model

### Prerequisites

Make sure the data within..

```
##########################################################
#### IMPORTANT
##########################################################
####
#### THESE DATA SHOULD BE THE SAME AS FROM THE MAIN SCRIPT
####
##########################################################
```
..are the same as the one in the main script. 


### Plotting

This plot script can be run after the model had been analysed during the visualise stage. It will create XY data of S11 in each level for concrete, and also for steel bar.
