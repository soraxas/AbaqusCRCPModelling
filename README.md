# Folder Download Link
[3D Frictional CRCP](https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/soraxas/AbaqusCRCPModelling/tree/master/3D-CRCP-frictional-bond)

# Abaqus CRCP Script

Python scripting interface for building a 2D/3D CRCP model in Abaqus.

## Script Status

### 3D-CRCP-embedded-sbar.py
Creating a 3D model with embedded bond (via embedded constraint) and shear layer at bottom (via connectors).

### 3D-sbar-concslab-FrictionalBond.py
Creating a 3D model with frictional bond (via surface friction) and shear layer at bottom (via surface friction). INCOMPLETED

### 3D-crcp-script.py
Creating a 3D model with non-linear bond-slip (via connectors) and shear layer at bottom (via connectors)

### 2D-long-slab.py
Creating a 2D model with non-linear bond-slip (via connectors) and shear layer at bottom (via connectors). It has a parameter to control the slab length.

### plot-2D-CRCP.py
This is the script for automatically creating path and XY data in the 2D model. Compatible with the 2D script

## Prerequisites

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
