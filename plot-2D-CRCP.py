##########################################################
#### IMPORTANT
##########################################################
####
#### THESE DATA SHOULD BE THE SAME AS FROM THE MAIN SCRIPT
####
##########################################################
tolerance = 0.005

CONCSLAB_NAME = 'concslab'
SBAR_NAME = 'sbar'

mdl = mdb.models[model_name]
print('>>>>>>>>>>>>>>>>')
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

def getNodesFromBox(instancename, yMin=None, yMax=None):
    # given the options, return a tuple of the instancename and the resultant list of node index
    MINIMUM_NUM_OF_NODE_TO_CONSIDER_AS_PATH = 2
    options = {}
    if yMin is not None:
        options['yMin'] = yMin-tolerance
    if yMax is not None:
        options['yMax'] = yMax+tolerance
    if instancename == SBAR_NAME:
        # Special case andling for steel bar
        for k in mdl.rootAssembly.instances.keys():
            if SBAR_NAME in k: # is a steel bar
                instance = mdl.rootAssembly.instances[k]
                nodes = instance.nodes.getByBoundingBox(**options)
                # print nodes
                if len(nodes) > MINIMUM_NUM_OF_NODE_TO_CONSIDER_AS_PATH: # we got something from this instance, return the resultant nodes.
                    return k, nodes
    else:
        return instancename, mdl.rootAssembly.instances[instancename].nodes.getByBoundingBox(**options)


# def pointOnToPlotNodeIdx(instanceName, pointOn):
#     # given a tuple of coordinate, return the vertices index of the given instance name
#     idx = None
#     try:
#         idx = mdl.rootAssembly.instances[instanceName].vertices.findAt((pointOn,), )[0].index + 1
#     #### IMPORTANT the +1 is workaround for the weird syntax where plot's id is +1 of edge index
#     except IndexError:
#         pass
#     return idx
#
# def templatePlotEntireWidth2(instanceName, height):
#     pathName = instanceName+'@'+str(height)
#     expr = []
#     for i in range(int(model_width/partition_size) + 1):
#         nodeidx = pointOnToPlotNodeIdx(instanceName, (i * partition_size, height, 0))
#         if nodeidx is not None:
#             expr.append(nodeidx)
#     print(str(expr))
#     newPath = session.Path(name=pathName,type=NODE_LIST,expression=(instanceName.upper(),tuple(expr)))
#     ## plot XY DATA
#     newXYData=session.XYDataFromPath(name=pathName,path=newPath,
#                                      includeIntersections=FALSE,
#                                      shape=UNDEFORMED,
#                                      labelType=TRUE_DISTANCE)
def templatePlotEntireWidth(instance, height):
    instanceName, expr = getNodesFromBox(instance, yMin=height,yMax=height)
    # turn to list first (to sort)
    expr = list(expr)
    # Special case for concslab, also include the nodes around trsbar
    if instance == 'concslab' and height in rebar_heights:
        for x in model_sbar_location_generator(model_width, trsbar_spacing):
            sbar_center_1 = (x, height, -1)
            sbar_center_2 = (x, height, 1)
            sbar_nodes = mdl.rootAssembly.instances[instance].nodes.getByBoundingCylinder(sbar_center_1, sbar_center_2, trsbar_diameter/2 + tolerance)
            # filter out nodes that are below steelbar height
            sbar_nodes = list(filter(lambda x : x.coordinates[1] > height + tolerance, list(sbar_nodes)))
            expr.extend(sbar_nodes)
    pathName = instanceName+'@'+str(height)

    # sort it to increasing sequence
    expr.sort(key=lambda x : x.coordinates[0])
    # extract the index number
    idxs = [x.label for x in expr]
    print('> Found path with {0} nodes, named as: {1}'.format(len(idxs), pathName))
    # print('> Found path :' + str([x.coordinates[0] for x in expr]))
    newPath = session.Path(name=pathName,type=NODE_LIST,expression=(instanceName.upper(),tuple(idxs)))
    ## plot XY DATA
    newXYData=session.XYDataFromPath(name=pathName,path=newPath,
                                     includeIntersections=FALSE,
                                     shape=UNDEFORMED,
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
