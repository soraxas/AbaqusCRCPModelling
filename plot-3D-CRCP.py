##########################################################
#### IMPORTANT
##########################################################
####
#### THESE DATA SHOULD BE THE SAME AS FROM THE MAIN SCRIPT
####
##########################################################
tolerance = 0.05

model_name = '3D_CRCP'
model_width = 1524.0
model_height = 304.8
model_depth = 1828.8

sbar_diameter = 19.05
trsbar_diameter = 15.875

partition_size = 38.1 * 8
mesh_size = 38.1 * 2

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
print('>------------------')

def getNodesFromBox(instancename, xMin=None, xMax=None, yMin=None, yMax=None, zMin=None, zMax=None):
    options = {}
    if xMin is not None:
        options['xMin'] = xMin-tolerance
    if xMax is not None:
        options['xMax'] = xMax+tolerance
    if yMin is not None:
        options['yMin'] = yMin-tolerance
    if yMax is not None:
        options['yMax'] = yMax+tolerance
    if zMin is not None:
        options['zMin'] = zMin-tolerance
    if zMax is not None:
        options['zMax'] = zMax+tolerance
    return mdl.rootAssembly.instances[instancename].nodes.getByBoundingBox(**options)


# a = getNodesFromBox(CONCSLAB_NAME, yMin=model_height,yMax=model_height, zMin=model_depth/2, zMax=model_depth/2)
# print(a)
# a = list(a)
# print(len(a))
# print(a)
# for i in a:
#     print i
# #     print(i.coordinates[0])
# a.sort(key=lambda x : x.coordinates[0])
# for i in a:
#     print i
# print('-------------')

# def meshFindAt()

# def pointOnToPlotNodeIdx(instanceName, pointOn):
#     # given a tuple of coordinate, return the vertices index of the given instance name
#     print(mdl.rootAssembly.instances[instanceName].vertices.findAt((pointOn,), ))
#     print(mdl.rootAssembly.instances[instanceName].nodes.findAt())
#     print(mdl.rootAssembly.instances[instanceName].vertices.findAt((pointOn,), )[0])
#     print(mdl.rootAssembly.instances[instanceName].vertices.findAt((pointOn,), )[0].__repr__)
#     return mdl.rootAssembly.instances[instanceName].vertices.findAt((pointOn,), )[0].index + 1
    #### IMPORTANT the +1 is workaround for the weird syntax where plot's id is +1 of edge index


def templatePlotEntireWidthMid(instanceName, height):
    pathName = instanceName+'@z='+str(model_depth/2)+' ; @y='+str(height)
    expr = getNodesFromBox(instanceName, yMin=height,yMax=height, zMin=model_depth/2, zMax=model_depth/2)

    # turn to list first (to sort)
    expr = list(expr)
    # sort it to increasing sequence
    expr.sort(key=lambda x : x.coordinates[0])
    # extract the index number
    # print(expr[0].label)
    idxs = [x.label for x in expr]
    print('> Found path :' + str(idxs))
    newPath = session.Path(name=pathName,type=NODE_LIST,expression=(instanceName.upper(),tuple(idxs)))
    ## plot XY DATA
    newXYData=session.XYDataFromPath(name=pathName,path=newPath,
                                     includeIntersections=FALSE,
                                     shape=DEFORMED,
                                     labelType=TRUE_DISTANCE)

def templatePlotEntireDepthMid(instanceName, height):
    pathName = instanceName+'@x='+str(model_width/2)+' ; @y='+str(height)
    expr = getNodesFromBox(instanceName, yMin=height,yMax=height, xMin=model_width/2, xMax=model_width/2)

    # turn to list first (to sort)
    expr = list(expr)
    # sort it to increasing sequence
    expr.sort(key=lambda x : x.coordinates[2])
    # extract the index number
    # print(expr[0].label)
    idxs = [x.label for x in expr]
    print('> Found path :' + str(idxs))
    newPath = session.Path(name=pathName,type=NODE_LIST,expression=(instanceName.upper(),tuple(idxs)))
    ## plot XY DATA
    newXYData=session.XYDataFromPath(name=pathName,path=newPath,
                                     includeIntersections=FALSE,
                                     shape=DEFORMED,
                                     labelType=TRUE_DISTANCE)



## plot concslab

# # surface
# templatePlotEntireWidth('concslab', model_height)
# # rebar location
# templatePlotEntireWidth('concslab', rebar_location)
# # bottom
# templatePlotEntireWidth('concslab', 0)

for i in range(int(model_height/mesh_size) + 1):
    templatePlotEntireWidthMid(CONCSLAB_NAME, i*mesh_size)
#
for i in range(int(model_height/mesh_size) + 1):
    templatePlotEntireDepthMid(CONCSLAB_NAME, i*mesh_size)


## plot sbar

# templatePlotEntireWidth(SBAR_NAME, rebar_location)s

print('------------------<')
