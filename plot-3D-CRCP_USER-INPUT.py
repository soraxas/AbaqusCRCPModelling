##########################################################
#### IMPORTANT
##########################################################
####
#### THESE DATA SHOULD BE THE SAME AS FROM THE MAIN SCRIPT
####
##########################################################
tolerance = 0.05
model_name = '3D_CRCP_frictional'
mdl = mdb.models[model_name]

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

tolerance = 0.1
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

def templatePlot(instance, atX=None, atZ=None):
    # get all height
    instance, expr_height = getNodesFromBox(instance, xMin=0, xMax=0, zMin=atZ, zMax=atZ)
    expr_height = list(expr_height)
    expr_height.sort(key=lambda x : x.coordinates[1])
    heights = [i.coordinates[1] for i in expr_height]
    for height in heights:
        # atX and atZ should be one or the other being None, cannot be both
        if atX == atZ or (atX and atZ):
            raise Exception("ERROR: one and only one of the variable atX and atZ should be provided.")
        if atX:
            plotname = '@x='+str(atX)+'_@y='+str(height)
            sortIdx = 2
        else:
            plotname = '@z='+str(atZ)+'_@y='+str(height)
            sortIdx = 0

        instance, expr = getNodesFromBox(instance, yMin=height,yMax=height, xMin=atX, xMax=atX, zMin=atZ, zMax=atZ)

        pathName = instance+plotname

        # turn to list first (to sort)
        expr = list(expr)
        # sort it to increasing sequence
        expr.sort(key=lambda x : x.coordinates[sortIdx])
        # extract the index number
        idxs = [i.label for i in expr]
        print('> For ['+plotname+'] Found path :' + str(idxs))
        newPath = session.Path(name=pathName,type=NODE_LIST,expression=(instance.upper(),tuple(idxs)))
        ## plot XY DATA
        newXYData=session.XYDataFromPath(name=pathName,path=newPath,includeIntersections=False,
                                         projectOntoMesh=True, pathStyle=PATH_POINTS, numIntervals=10,
                                         projectionTolerance=0, shape=UNDEFORMED, labelType=TRUE_DISTANCE)


def getInputbox(msg):
    import pywin.mfc.dialog
    return pywin.mfc.dialog.GetSimpleInput(str(msg))
def confirm(s):
    import win32api
    result = win32api.MessageBox(None, s, "Abaqus Script",1)
    if result == 1:
        return True
    elif result == 2:
        return False
    # else:
    #     raise SystemExit


atX = None
atZ = None
# ask if plotting along x or z
if confirm("Plotting along x direction? (X is variable, and Z is fixed)"):
    atZ = float(getInputbox("Input z coordinates:"))
elif confirm("Plotting along z direction? (X is fixed, and Z is variable)"):
    atX = float(getInputbox("Input x coordinates:"))

print(atX)
print(atZ)
if atX is not None or atZ is not None:
    templatePlot(CONCSLAB_NAME, atX=atX, atZ=atZ)



## plot sbar

# templatePlotEntireWidth(SBAR_NAME, rebar_location)s

print('------------------<')
