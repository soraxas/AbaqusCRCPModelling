##################################################
##### MDOEL SETTINGS
##################################################
STIFFNESS_BASE_VALUE = 38.1 # This is what our stiffness value is based upon. If partition_size
                            # is changed, the stiffness value will be changed proportionally
                            # so the value will be correct
model_name = '3D_CRCP_frictional'
# model_width = 1524.0
model_width = 1828.8
model_height = 304.8
model_depth = 1828.8

num_pavements = 1

# rebar_heights = model_height/2

rebar_heights = [ model_height * 1/4, model_height * 3/4]

losbar_diameter = 19.05
trsbar_diameter = 15.875

partition_size = 38.1
mesh_size = 10
mesh_size = 38.1
sbar_mesh_size_factor = 0.8
vertical_partition_size = 38.1

losbar_spacing = 152.4
trsbar_spacing = 914.4
# vertical_partition_size = model_height

TEMP_INITIAL = 48.9
TEMP_TOPSURFACE = 29.4
TEMP_BOTSURFACE = 37.8

subbase_thickness = model_height * 2

if model_name in mdb.models.keys():
    mdl = mdb.models[model_name]
else:
    print('> INFO: Note that the model "'+model_name+'" does not exists yet.')
