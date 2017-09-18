##########################################################
#### IMPORTANT
##########################################################
####
#### THESE DATA SHOULD BE THE SAME AS FROM THE MAIN SCRIPT
####
##########################################################

model_name = '2D_CRCP'
model_width = 1524.0 * 2
model_height = 304.8
rebar_location = model_height/2
partition_size = 38.1
mdl = mdb.models[model_name]
CONCSLAB_NAME = 'concslab'
SBAR_NAME = 'sbar'


##########################################################
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

def pointOnToPlotNodeIdx(instanceName, pointOn):
    # given a tuple of coordinate, return the vertices index of the given instance name
    return mdl.rootAssembly.instances[instanceName].vertices.findAt((pointOn,), )[0].index + 1
    #### IMPORTANT the +1 is workaround for the weird syntax where plot's id is +1 of edge index


def templatePlotEntireWidth(instanceName, height):
    pathName = instanceName+'@'+str(height)
    expr = []
    for i in range(int(model_width/partition_size) + 1):
        expr.append(pointOnToPlotNodeIdx(instanceName, (i * partition_size, height, 0)))
    newPath = session.Path(name=pathName,type=NODE_LIST,expression=(instanceName.upper(),tuple(expr)))
    ## plot XY DATA
    newXYData=session.XYDataFromPath(name=pathName,path=newPath,
                                     includeIntersections=FALSE,
                                     shape=DEFORMED,
                                     labelType=TRUE_DISTANCE)
                                    #  variable=variable)


## plot concslab

# # surface
# templatePlotEntireWidth('concslab', model_height)
# # rebar location
# templatePlotEntireWidth('concslab', rebar_location)
# # bottom
# templatePlotEntireWidth('concslab', 0)

for i in range(int(model_height/partition_size) + 1):
    templatePlotEntireWidth(CONCSLAB_NAME, i*partition_size)


## plot sbar

templatePlotEntireWidth(SBAR_NAME, rebar_location)
