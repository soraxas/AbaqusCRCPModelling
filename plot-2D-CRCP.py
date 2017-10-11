##########################################################
#### IMPORTANT
##########################################################
####
#### THESE DATA SHOULD BE THE SAME AS FROM THE MAIN SCRIPT
####
##########################################################

CONCSLAB_NAME = 'concslab'

mdl = mdb.models[model_name]

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
    idx = None
    try:
        idx = mdl.rootAssembly.instances[instanceName].vertices.findAt((pointOn,), )[0].index + 1
    #### IMPORTANT the +1 is workaround for the weird syntax where plot's id is +1 of edge index
    except IndexError:
        pass
    return idx

def templatePlotEntireWidth(instanceName, height):
    pathName = instanceName+'@'+str(height)
    expr = []
    for i in range(int(model_width/partition_size) + 1):
        nodeidx = pointOnToPlotNodeIdx(instanceName, (i * partition_size, height, 0))
        if nodeidx is not None:
            expr.append(nodeidx)
    newPath = session.Path(name=pathName,type=NODE_LIST,expression=(instanceName.upper(),tuple(expr)))
    ## plot XY DATA
    newXYData=session.XYDataFromPath(name=pathName,path=newPath,
                                     includeIntersections=FALSE,
                                     shape=DEFORMED,
                                     labelType=TRUE_DISTANCE)

def main():
    session.viewports[session.viewports.keys()[0]].odbDisplay.setPrimaryVariable(
        variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(COMPONENT,
        'S11'))

    for i in range(int(model_height/partition_size) + 1):
        templatePlotEntireWidth(CONCSLAB_NAME, i*partition_size)

    ## plot sbar
    for rebar_y in rebar_heights:
        templatePlotEntireWidth(losbar(rebar_y), rebar_y)

main()
