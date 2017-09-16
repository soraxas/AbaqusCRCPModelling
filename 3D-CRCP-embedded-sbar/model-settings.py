##################################################
##### MDOEL SETTINGS
##################################################
STIFFNESS_BASE_VALUE = 38.1 # This is what our stiffness value is based upon. If partition_size
                            # is changed, the stiffness value will be changed proportionally
                            # so the value will be correct
model_name = '3D_CRCP'
model_width = 1524.0
model_height = 304.8
model_depth = 1828.8

sbar_diameter = 19.05
trsbar_diameter = 15.875

partition_size = 38.1 * 2
mesh_size = 38.1 * 2
# vertical_partition_size = 38.1 * 2
vertical_partition_size = model_height

TEMP_TOPSURFACE = 29.4
TEMP_BOTSURFACE = 37.8

if model_name in mdb.models.keys():
    mdl = mdb.models[model_name]
else:
    print('> INFO: Note that the model "'+model_name+'" does not exists yet.')
