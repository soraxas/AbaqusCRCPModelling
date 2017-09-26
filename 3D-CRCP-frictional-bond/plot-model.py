tolerance = 0.05

CONCSLAB_NAME = 'concslab'
SBAR_NAME = 'sbar'

paths = []

def getNodesFromBox(instancename, xMin=None, xMax=None, yMin=None, yMax=None, zMin=None, zMax=None):
    # given the options, return a tuple of the instancename and the resultant list of node index
    MINIMUM_NUM_OF_NODE_TO_CONSIDER_AS_PATH = 2
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


def templatePlotEntireWidthMid(instance, height, atZ):
    instanceName, expr = getNodesFromBox(instance, yMin=height,yMax=height, zMin=atZ, zMax=atZ)
    pathName = instanceName+'@z='+str(model_depth/2)+' ; @y='+str(height)

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
                                     shape=UNDEFORMED,
                                     labelType=TRUE_DISTANCE)

def templatePlotEntireDepthMid(instanceName, height, atX):
    pathName = instanceName+'@x='+str(model_width/2)+' ; @y='+str(height)
    expr = getNodesFromBox(instanceName, yMin=height,yMax=height, xMin=atX, xMax=atX)

    # turn to list first (to sort)
    expr = list(expr)
    # sort it to increasing sequence
    expr.sort(key=lambda x : x.coordinates[2])
    # extract the index number
    # print(expr[0].label)
    idxs = [x.label for x in expr]
    print('> Found path :' + str(idxs))
    newPath = session.Path(name=pathName,type=NODE_LIST,expression=(instanceName.upper(),tuple(idxs)))
    global paths
    paths.append(newPath)


def templatePlot(instance, height, atX=None, atZ=None):
    # atX and atZ should be one or the other being None, cannot be both
    if atX == atZ or (atX and atZ):
        raise Exception("ERROR: one and only one of the variable atX and atZ should be provided.")
    if atX:
        plotname = '@x='+str(atX)+'_@y='+str(height)
        sortIdx = 2
    else:
        plotname = '@z='+str(atZ)+'_@y='+str(height)
        sortIdx = 0

    instanceName, expr = getNodesFromBox(instance, yMin=height,yMax=height, xMin=atX, xMax=atX, zMin=atZ, zMax=atZ)

    pathName = instanceName+plotname

    # turn to list first (to sort)
    expr = list(expr)
    # sort it to increasing sequence
    expr.sort(key=lambda x : x.coordinates[sortIdx])
    # extract the index number
    idxs = [i.label for i in expr]
    print('> For ['+plotname+'] Found path :' + str(idxs))
    newPath = session.Path(name=pathName,type=NODE_LIST,expression=(instanceName.upper(),tuple(idxs)))
    ## plot XY DATA
    newXYData=session.XYDataFromPath(name=pathName,path=newPath,includeIntersections=False,
                                     projectOntoMesh=True, pathStyle=PATH_POINTS, numIntervals=10,
                                     projectionTolerance=0, shape=UNDEFORMED, labelType=TRUE_DISTANCE)

# name=pathName,path=newPath,
#                                  includeIntersections=FALSE,
#                                  shape=UNDEFORMED,
#                                  labelType=TRUE_DISTANCE)
## plot concslab

# # surface
# templatePlotEntireWidth('concslab', model_height)
# # rebar location
# templatePlotEntireWidth('concslab', rebar_height)
# # bottom
# templatePlotEntireWidth('concslab', 0)

########################################
# Plot along the width
########################################
# # slab mid point
# for i in range(int(model_height/mesh_size) + 1):
#     templatePlot(CONCSLAB_NAME, i*mesh_size, atZ=model_depth/2)
# in line with steelbar
for i in range(int(model_height/mesh_size) + 1):
    templatePlot(CONCSLAB_NAME, i*mesh_size, atZ=990.6)
templatePlot(SBAR_NAME, rebar_height, atZ=990.6)
# in between 2 steelbar
for i in range(int(model_height/mesh_size) + 1):
    templatePlot(CONCSLAB_NAME, i*mesh_size, atZ=838.2 + (990.6-838.2)/2)


########################################
# Plot along the depth
########################################
# # slab mid point
# for i in range(int(model_height/mesh_size) + 1):
#     templatePlot(CONCSLAB_NAME, i*mesh_size, atX=model_width/2)
# in line with steelbar
for i in range(int(model_height/mesh_size) + 1):
    templatePlot(CONCSLAB_NAME, i*mesh_size, atX=457.2)
templatePlot(SBAR_NAME, rebar_height, atX=457.2)
# in between 2 steelbar
for i in range(int(model_height/mesh_size) + 1):
    templatePlot(CONCSLAB_NAME, i*mesh_size, atX=457.2 + (1371.6-457.2)/2)



################################################################################
## plot XY DATA
for path in paths:
    session.XYDataFromPath(name=path,path=newPath,
                                 includeIntersections=FALSE,
                                 shape=UNDEFORMED,
                                 labelType=TRUE_DISTANCE)
