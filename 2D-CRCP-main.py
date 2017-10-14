##################################################
##### MDOEL SETTINGS
##################################################

PARTITION_SIZE_MODIFER = 0.5
# PARTITION_SIZE_MODIFER = 1

model_name = '2D_CRCP'
# model_width = 1524.0
# model_width = 1828.8
model_width = 3600
model_width = 1800
model_height = 300
rebar_location = model_height/2

partition_size = 30 * PARTITION_SIZE_MODIFER
mesh_size_global = partition_size #* 0.2
# mesh related to nearby trsbar
mesh_size_trsbar = mesh_size_global * 0.3
mesh_size_trsbar_nearby_diagonals = mesh_size_trsbar * 1.4
mesh_size_trsbar_nearby_outer_edges = mesh_size_trsbar * 1.8

# rebar_heights = [model_height * 2/8, model_height * 6/8]
rebar_heights = [model_height * 1/2]

losbar_diameter = 19.05
trsbar_diameter = 15.875

# losbar_spacing = 152.4
trsbar_spacing = 900
############################################
## TEMPERATURE
TEMP_INITIAL = '-2e-4*pow(Y,2) + 6.44e-2*pow(Y,1) + 37.72'

# temp_0130 = ' 3e-9*pow(Y,4) - 2e-6*pow(Y,3) +   4e-4*pow(Y,2) -   2.9e-3*pow(Y,1) + 31.384'
# temp_0430 = '-1e-9*pow(Y,4) + 6e-7*pow(Y,3) -   1e-4*pow(Y,2) +  3.05e-2*pow(Y,1) + 29.299'
# temp_0730 = ' 2e-9*pow(Y,4) - 1e-6*pow(Y,3) +   3e-4*pow(Y,2) -   9.5e-3*pow(Y,1) + 29.563'
# temp_1030 = ' 2e-9*pow(Y,4) - 1e-6*pow(Y,3) +   5e-4*pow(Y,2) - 7.377e-2*pow(Y,1) + 36.052'
# temp_1330 = ' 6e-9*pow(Y,4) - 4e-6*pow(Y,3) + 1.1e-3*pow(Y,2) - 1.344e-1*pow(Y,1) + 41.746'
# temp_1630 = ' 2e-9*pow(Y,4) - 2e-6*pow(Y,3) +   5e-4*pow(Y,2) -  9.36e-2*pow(Y,1) + 44.083'
# temp_1930 = '8e-10*pow(Y,4) - 2e-6*pow(Y,3) +   5e-5*pow(Y,2) -   3.3e-3*pow(Y,1) + 37.575'
# temp_2230 = ' 2e-9*pow(Y,4) - 2e-6*pow(Y,3) +   4e-4*pow(Y,2) -  2.63e-2*pow(Y,1) + 34.388'

temp_0730 = '1.65e-9*pow(Y,4)-1.27e-6*pow(Y,3)+2.92e-4*pow(Y,2)-9.46e-3*pow(Y,1)+29.5'
temp_1630 = '1.86e-9*pow(Y,4)-1.51e-6*pow(Y,3)+4.63e-4*pow(Y,2)-9.36e-2*pow(Y,1)+44.1'

conc_elastic_modulus_before_crack = 14800
conc_elastic_modulus_after_crack  = 23000
CONC_ELASTIC_MODULUS = conc_elastic_modulus_before_crack

shrinkage_as_temp_0730_before_crack = [
    (0,     23.80555556),
    (15,    26.0718195 ),
    (30,    26.25201872),
    (45,    26.3626095 ),
    (60,    26.53663622),
    (75,    26.755398  ),
    (90,    27.00219872),
    (105,   27.262347  ),
    (120,   27.52315622),
    (135,   27.7739445 ),
    (150,   28.00603472),
    (165,   28.2127545 ),
    (180,   28.38943622),
    (195,   28.533417  ),
    (210,   28.64403872),
    (225,   28.722648  ),
    (240,   28.77259622),
    (255,   28.7992395 ),
    (270,   28.80993872),
    (285,   28.8140595 ),
    (300,   28.82297222)
    ]

shrinkage_as_temp_1630_before_crack = [
    (0	,   38.40555556),
    (15	,   39.44739513),
    (30	,   38.47540882),
    (45	,   37.50157563),
    (60	,   36.65471782),
    (75	,   35.91216753),
    (90	,   35.25351682),
    (105,   34.66061763),
    (120,   34.11758182),
    (135,   33.61078113),
    (150,   33.12884722),
    (165,   32.66267163),
    (180,   32.20540582),
    (195,   31.75246113),
    (210,   31.30150882),
    (225,   30.85248003),
    (240,   30.40756582),
    (255,   29.97121713),
    (270,   29.55014482),
    (285,   29.15331963),
    (300,   28.79197222)
    ]

shrinkage_as_temp_0730_after_crack = [
    (0	,   16.02888889),
    (15	,   21.99973617),
    (30	,   23.78993539),
    (45	,   24.47052617),
    (60	,   24.64455289),
    (75	,   24.86331467),
    (90	,   25.11011539),
    (105,	25.37026367),
    (120,	25.63107289),
    (135,	25.88186117),
    (150,	26.11395139),
    (165,	26.32067117),
    (180,	26.49735289),
    (195,	26.64133367),
    (210,	26.75195539),
    (225,	26.83056467),
    (240,	26.88051289),
    (255,	26.90715617),
    (270,	26.91785539),
    (285,	26.92197617),
    (300,	26.93088889)
    ]

shrinkage_as_temp_1630_after_crack = [
    (0  ,   30.62888889),
    (15 ,   35.3753118),
    (30 ,   36.01332549),
    (45 ,   35.6094923),
    (60 ,   34.76263449),
    (75 ,   34.0200842),
    (90 ,   33.36143349),
    (105,	32.7685343),
    (120,	32.22549849),
    (135,	31.7186978),
    (150,	31.23676389),
    (165,	30.7705883),
    (180,	30.31332249),
    (195,	29.8603778),
    (210,	29.40942549),
    (225,	28.9603967),
    (240,	28.51548249),
    (255,	28.0791338),
    (270,	27.65806149),
    (285,	27.2612363),
    (300,	26.89988889),
    ]

TEMP_ANALYSIS_STAGE = temp_0730
SHRINKAGE_ANALYSIS_STAGE = shrinkage_as_temp_0730_before_crack

# TEMP_INITIAL = 48.9
# TEMP_TOPSURFACE = 29.4
# TEMP_BOTSURFACE = 37.8
#########################
# for submitting job
NUM_OF_CPUS = 4
NUM_OF_GPUS = 0
#########################

if model_name in mdb.models.keys():
    del mdb.models[model_name]
mdb.Model(modelType=STANDARD_EXPLICIT, name=model_name)

mdl = mdb.models[model_name]

##################################################
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

################################################################################
#### HELPER METHODS
################################################################################
import itertools
FLOAT_TOLERANCE = 0.001
def eql(a, b):
    # A comparasion method with tolerance
    return abs(a - b) <= FLOAT_TOLERANCE

def edgeToArray(edge):
    # Convert an edge to edge array
    return mdl.rootAssembly.edges[edge.index:edge.index+1]

def edgeNameToEdge(edgeName):
    # given the name of an edge, return an edge repo containing that edge
    ## EXTREMELY SLOW but a work around for not being able to construct repo by demand
    for i in mdl.rootAssembly.edges:
        if i.featureName == edgeName:
            return i

def edgeNameToEdgeArrayFilter(edgeNames, filter):
    # given a list of edge names, it will return a list of edge array with a filter
    # It will return a tuple of two list, the first list if when the optional filter return true
    _a = []
    _b = []
    for i in [edgeNameToEdge(j.name) for j in edgeNames]:
        if i is None:
            continue
        if filter(i):
            _a.append(edgeToArray(i))
        else:
            _b.append(edgeToArray(i))
    return _a, _b

def conArray(array):
    # given a list of array, return a concentrated array
    _tmp = array[0]
    for i in range(1, len(array)):
        _tmp += array[i]
    return _tmp

def array_append(array, new_item):
    if new_item is None:
        return array
    if array is None:
        return new_item
    else:
        return array + new_item

def model_sbar_location_generator(dimension, spacing):
    # given the sbar spacing and the dimension of the block,
    # return the location of sbar that lies within the model.
    return (spacing/2+x*spacing for x in range(int(1+(dimension-spacing/2)/spacing)))

def losbar(height):
    # return a formatted rebar name
    return 'losbar-{0}'.format(int(height))
def trsbar(height, x):
    # return a formatted rebar name
    return 'trsbar-{0}-x{1}'.format(int(height), int(x))
################################################################################

mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
mdl.sketches['__profile__'].rectangle(point1=(0.0, 0.0),
    point2=(model_width, model_height))
for rebar_y in rebar_heights:
    for x in model_sbar_location_generator(model_width, trsbar_spacing):
    	mdl.sketches['__profile__'].CircleByCenterPerimeter(center=(
    		x, rebar_y), point1=(x + trsbar_diameter/2, rebar_y))
mdl.Part(dimensionality=TWO_D_PLANAR, name=
    'concslabPart', type=DEFORMABLE_BODY)
mdl.parts['concslabPart'].BaseShell(sketch=
    mdl.sketches['__profile__'])
del mdl.sketches['__profile__']

for rebar_y in rebar_heights:
    # make a hollow hole in concslab
    mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
    mdl.sketches['__profile__'].Line(point1=(0.0, rebar_y), point2=(
        model_width, rebar_y))
    mdl.sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdl.sketches['__profile__'].geometry[2])
    mdl.Part(dimensionality=TWO_D_PLANAR, name=losbar(rebar_y), type=
        DEFORMABLE_BODY)
    mdl.parts[losbar(rebar_y)].BaseWire(sketch=
        mdl.sketches['__profile__'])
    del mdl.sketches['__profile__']

    # make a plane stress trsbar
    for x in model_sbar_location_generator(model_width, trsbar_spacing):
        mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
    	mdl.sketches['__profile__'].CircleByCenterPerimeter(center=(
    		x, rebar_y), point1=(x + trsbar_diameter/2, rebar_y))
        mdl.Part(dimensionality=TWO_D_PLANAR, name=trsbar(rebar_y, x), type=
            DEFORMABLE_BODY)
        mdl.parts[trsbar(rebar_y, x)].BaseShell(sketch=
            mdl.sketches['__profile__'])
        del mdl.sketches['__profile__']
# Save by kyue3641 on 2017_08_16-11.47.36; build 6.14-1 2014_06_05-08.11.02 134264
#####################################################
### Setup Material Property
#####################################################
# Concrete
mdl.Material(name='Concrete')
mdl.materials['Concrete'].Elastic(table=((CONC_ELASTIC_MODULUS, 0.15), ))
mdl.materials['Concrete'].Expansion(table=((7.2e-6, ), ))
mdl.materials['Concrete'].Density(table=((2.4e-06, ), ))
mdl.materials['Concrete'].Viscoelastic(domain=TIME, table=((
    0.45, 0.45, 48.0), ), time=PRONY)
# Steel
mdl.Material(name='Steel')
mdl.materials['Steel'].Elastic(table=((200000.0, 0.0), ))
mdl.materials['Steel'].Expansion(table=((1.08e-05, ), ))
#####################################################
### Create Instances
#####################################################
# Create Instance
mdl.rootAssembly.DatumCsysByDefault(CARTESIAN)
mdl.rootAssembly.Instance(dependent=ON, name='concslab',
    part=mdl.parts['concslabPart'])
mdl.rootAssembly.makeIndependent(instances=(
mdl.rootAssembly.instances['concslab'], ))

for rebar_y in rebar_heights:
    mdl.rootAssembly.Instance(dependent=OFF, name=losbar(rebar_y), part=
        mdl.parts[losbar(rebar_y)])
    for x in model_sbar_location_generator(model_width, trsbar_spacing):
        mdl.rootAssembly.Instance(dependent=OFF, name=trsbar(rebar_y, x), part=
            mdl.parts[trsbar(rebar_y, x)])
# mdl.rootAssembly.translate(instanceList=('sbar',),
#                            vector=(0.0, rebar_location, 0.0))
## Make instances independent

# ### Create datum plane
#
# for i in range(int(model_width/partition_size)-1):
#     mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=partition_size * (i+1)
#         , principalPlane=YZPLANE)
# for i in range(int(model_height/partition_size)-1):
#     mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=partition_size * (i+1)
#         , principalPlane=XZPLANE)
# #### Partition by datum plane
# for k,v in mdl.parts['concslabPart'].datums.items():
#     mdl.parts['concslabPart'].PartitionFaceByDatumPlane(faces=
#         mdl.parts['concslabPart'].faces, datumPlane=v)
# mdl.rootAssembly.regenerate()
    # partition trsbar
mdl.ConstrainedSketch(gridSpacing=1.11, name='__profile__',
        sheetSize=44.77, transform=
        mdl.rootAssembly.MakeSketchTransform(
        sketchPlane=mdl.rootAssembly.instances['concslab'].faces[0],
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0,0,0)))
# partition vert and Horziontal
for i in range(int(model_width/partition_size)-1):
    mdl.sketches['__profile__'].Line(point1=(partition_size * (i+1), 0),
                                     point2=(partition_size * (i+1), model_height))
for i in range(int(model_height/partition_size)-1):
    mdl.sketches['__profile__'].Line(point1=(0,           partition_size * (i+1)),
                                     point2=(model_width, partition_size * (i+1)))
mdl.rootAssembly.PartitionFaceBySketch(faces=
        mdl.rootAssembly.instances['concslab'].faces, sketch=mdl.sketches['__profile__'])
del mdl.sketches['__profile__']

## Partioning Longitudinal and Transverse steel bar in Part
    ##Creating DatumPointBy
for rebar_y in rebar_heights:
    datums_pts = []
    for i in range(int(model_width/partition_size)-1):
        datums_pts.append(mdl.rootAssembly.DatumPointByCoordinate(coords=(
            partition_size*(i+1), rebar_y, 0.0)))
        ## Partitioning the steel bar
    i = 0
    for p in [mdl.rootAssembly.datums[d.id] for d in datums_pts]:

        mdl.rootAssembly.PartitionEdgeByPoint(edge=
        mdl.rootAssembly.instances[losbar(rebar_y)].edges[i], point=p)
        i += 1

    # partition trsbar
    for x in model_sbar_location_generator(model_width, trsbar_spacing):
        for i in [trsbar(rebar_y, x), 'concslab']:
            mdl.ConstrainedSketch(gridSpacing=1.11, name='__profile__',
            sheetSize=44.77, transform=
            mdl.rootAssembly.MakeSketchTransform(
            sketchPlane=mdl.rootAssembly.instances[i].faces[0],
            sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0,0,0)))
            # partition vert and Horziontal
            mdl.sketches['__profile__'].Line(point1=(x - partition_size, rebar_y),
                                             point2=(x + partition_size, rebar_y))
            mdl.sketches['__profile__'].Line(point1=(x, rebar_y - partition_size),
                                             point2=(x, rebar_y + partition_size))
            # partition diagonal
            mdl.sketches['__profile__'].Line(point1=(x - partition_size, rebar_y - partition_size),
                                             point2=(x + partition_size, rebar_y + partition_size))
            mdl.sketches['__profile__'].Line(point1=(x - partition_size, rebar_y + partition_size),
                                             point2=(x + partition_size, rebar_y - partition_size))
            mdl.rootAssembly.PartitionFaceBySketch(faces=
                    mdl.rootAssembly.instances[i].faces, sketch=mdl.sketches['__profile__'])
            del mdl.sketches['__profile__']


## Define Connector behavior
    ## losbar-BondSp behavior of a whole element
mdl.ConnectorSection(name='losbar-BondSp interior-HORZ',
     translationalType=AXIAL)
mdl.sections['losbar-BondSp interior-HORZ'].setValues(behaviorOptions=
    (ConnectorElasticity(behavior=NONLINEAR, table=((0.0, -0.2032), (
    -4241.1416, -0.1016), (-12107.77521, -0.0508), (-11013.28706, -0.0254), (
    0.0, 0.0), (11013.28706, 0.0254), (12107.77521, 0.0508), (4241.1416,
    0.1016), (0.0, 0.2032)), independentComponents=(), components=(1, )), ))
    ## losbar-BondSp behavior of a whole element
mdl.ConnectorSection(name='losbar-BondSp corner-HORZ',
    translationalType=AXIAL)
mdl.sections['losbar-BondSp corner-HORZ'].setValues(
    behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR, table=((0.0,
    -0.2032), (-2120.5708, -0.1016), (-6053.887607, -0.0508), (-5506.643529,
    -0.0254), (0.0, 0.0), (5506.643529, 0.0254), (6053.887607, 0.0508), (
    2120.5708, 0.1016), (0.0, 0.2032)), independentComponents=(), components=(
    1, )), ))
mdl.ConnectorSection(name='losbar-BondSp all-VERT',
    translationalType=CARTESIAN)
mdl.sections['losbar-BondSp all-VERT'].setValues(
    behaviorOptions=(ConnectorElasticity(table=((1e+15,  ), ),
    independentComponents=(), components=(2, )), ))
mdl.ConnectorSection(name='trsbar-ALL-RIGID',
    translationalType=CARTESIAN)
mdl.sections['trsbar-ALL-RIGID'].setValues(
    behaviorOptions=(ConnectorElasticity(table=((1e+15,1e+15  ), ),
    independentComponents=(), components=(1,2 )), ))


######## SHEAR LAYERS:

### shear layer connector section properties
CONC_BASE_FRICTION_STIFFNESS_VERT_FORCE = 32027.1956 * PARTITION_SIZE_MODIFER
CONC_BASE_FRICTION_STIFFNESS_VERT_DISPLACEMENT = 50.8

mdl.ConnectorSection(name='ConcBase-Friction interior-VERT',
    translationalType=CARTESIAN)
mdl.sections['ConcBase-Friction interior-VERT'].setValues(
    behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR, table=((0.0, 0.0),
    (CONC_BASE_FRICTION_STIFFNESS_VERT_FORCE, CONC_BASE_FRICTION_STIFFNESS_VERT_DISPLACEMENT)
    ), independentComponents=(), components=(2, )), ))

mdl.ConnectorSection(name='ConcBase-Friction corner-VERT',
    translationalType=CARTESIAN)
mdl.sections['ConcBase-Friction corner-VERT'].setValues(
    behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR, table=((0.0, 0.0),
    (CONC_BASE_FRICTION_STIFFNESS_VERT_FORCE / 2, CONC_BASE_FRICTION_STIFFNESS_VERT_DISPLACEMENT)
    ), independentComponents=(), components=(2, )), ))

CONC_BASE_FRICTION_STIFFNESS_HORZ = 236.4211 * PARTITION_SIZE_MODIFER

mdl.ConnectorSection(name='ConcBase-Friction interior-HORZ',
    translationalType=CARTESIAN)
mdl.sections['ConcBase-Friction interior-HORZ'].setValues(
    behaviorOptions=(ConnectorElasticity(table=((CONC_BASE_FRICTION_STIFFNESS_HORZ, ), ),
    independentComponents=(), components=(1, )), ))

mdl.ConnectorSection(name='ConcBase-Friction corner-HORZ',
    translationalType=CARTESIAN)
mdl.sections['ConcBase-Friction corner-HORZ'].setValues(
    behaviorOptions=(ConnectorElasticity(table=((CONC_BASE_FRICTION_STIFFNESS_HORZ / 2, ), ),
    independentComponents=(), components=(1, )), ))


############# Connect steel bar with concrete
########## FOR trsbar
trsbarBond = []
for stbar in [i for i in mdl.rootAssembly.instances.keys() if 'trsbar' in i]:
    vertices = mdl.rootAssembly.instances[stbar].vertices
    for stbarV in vertices:
        concV = mdl.rootAssembly.instances['concslab'].vertices.findAt(stbarV.pointOn[0])
        if concV is None:
            continue
        ## connect these two point
        _tmp = mdl.rootAssembly.WirePolyLine(mergeType=IMPRINT, meshable=OFF
            , points=((stbarV, concV), ))
        trsbarBond.append(_tmp)

########## FOR losbar
## store the wire in lists
stbarBondVert = []
stbarBondHort = []

for stbar in [i for i in mdl.rootAssembly.instances.keys() if 'losbar' in i]:
    vertices = mdl.rootAssembly.instances[stbar].vertices
    for stbarV in vertices:
        concV = mdl.rootAssembly.instances['concslab'].vertices.findAt(stbarV.pointOn[0])
        if concV is None:
            continue
        ## connect these two point
        # Vertical wire
        _tmp = mdl.rootAssembly.WirePolyLine(mergeType=IMPRINT, meshable=OFF
            , points=((stbarV, concV), ))
        stbarBondVert.append(_tmp)
        ## Horziontal wire
        _tmp = mdl.rootAssembly.WirePolyLine(mergeType=IMPRINT, meshable=OFF
            , points=((stbarV, concV), ))
        stbarBondHort.append(_tmp)


############# Connect concrete slab with shear layer
# iterate all concrete slab vertices and only apply connector for the one with constraints y=0

concBaseBondVert = []
concBaseBondHorz = []

for v in mdl.rootAssembly.instances['concslab'].vertices:
    if int(v.pointOn[0][1]) == 0: # at y=0
        # Vertical wire
        _tmp = mdl.rootAssembly.WirePolyLine(mergeType=IMPRINT, meshable=OFF
            , points=((None, v), ))
        concBaseBondVert.append(_tmp)
        # Horziontal wire
        _tmp = mdl.rootAssembly.WirePolyLine(mergeType=IMPRINT, meshable=OFF
            , points=((None, v), ))
        concBaseBondHorz.append(_tmp)

########## Defining node sets
mdl.StaticStep(name='Static-thermal', previous='Initial')
mdl.steps['Static-thermal'].setValues(initialInc=4.0,
    timeIncrementationMethod=FIXED, timePeriod=12.0)
# mdl.(maintainAttributes=True, name='Static-thermal',
#     previous='Initial')

faces = None
cells = None
edges = None
vertices = None
for k in mdl.rootAssembly.instances.keys():
    faces = array_append(faces, mdl.rootAssembly.instances[k].faces)
    cells = array_append(cells, mdl.rootAssembly.instances[k].cells)
    edges = array_append(edges, mdl.rootAssembly.instances[k].edges)
    vertices = array_append(vertices, mdl.rootAssembly.instances[k].vertices)

TEMP_REGION = Region(
faces=faces,
cells=cells,
edges=edges,
vertices=vertices
)

temp_csys = mdl.rootAssembly.DatumCsysByThreePoints(origin=(0,model_height,0),
                                        point1=(model_width,model_height,0),
                                        point2=(0,0,0),
                                        name='Temp-field-csys', coordSysType=CARTESIAN)
temp_csys = mdl.rootAssembly.datums[temp_csys.id]

# mdl.Temperature(createStepName='Initial',
#     crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
#     UNIFORM, magnitudes=(TEMP_INITIAL, ), name='Initial-temp', region=TEMP_REGION)

# expression = '(({1}-{0})/{2}*Y+{0})'.format(TEMP_BOTSURFACE, TEMP_TOPSURFACE, model_height)
# mdl.ExpressionField(description=
#     'The temperature gradient for concslab, from top surface as ', expression=
#     expression, localCsys=None, name='Temperature Gradient of concslab')
mdl.ExpressionField(description=
    'Zero stress temp', expression=
    TEMP_INITIAL, localCsys=temp_csys, name='Zero Stress Temp')
mdl.ExpressionField(description=
    'Afterward temp profile', expression=
    TEMP_ANALYSIS_STAGE, localCsys=temp_csys, name='Temperature profile after exposing')

mdl.Temperature(createStepName='Initial',
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=FIELD
    , field='Zero Stress Temp', magnitudes=(1, ), name='Zero-stress-temp',
    region=TEMP_REGION)
mdl.Temperature(createStepName='Static-thermal',
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=FIELD
    , field='Temperature profile after exposing', magnitudes=(1, ), name='Temp-Profile',
    region=TEMP_REGION)

# #### make each surfacec in y axis as node set
# lvl = model_height
# j = 0
# while lvl >= 0:
#     vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(yMax=lvl, yMin=lvl)
#     mdl.rootAssembly.Set(name='SurfaceSet'+str(j), vertices=vertices)
#     j += 1
#     lvl -= partition_size
#     lvl = round(lvl,10) # force rounding
#
# # Set "All"
# v = mdl.rootAssembly.instances['concslab'].vertices + mdl.rootAssembly.instances['sbar'].vertices
#
# mdl.rootAssembly.Set(name='All', vertices=v)
# ######### TEMPERATURE ################
#
#
# ####### Create Predefined Field
# mdl.Temperature(createStepName='Initial',
#     crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
#     UNIFORM, magnitudes=(48.9, ), name='All', region=
#     mdl.rootAssembly.sets['All'])
#
# T = (37.8-29.4)/(model_height/partition_size)
# for i in range(int(model_height/partition_size)+1):
#     mdl.Temperature(createStepName='Static-thermal',
#         crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
#         UNIFORM, magnitudes=(29.4+i*T, ), name='TempLvl_'+str(i), region=
#         mdl.rootAssembly.sets['SurfaceSet'+str(i)])

##################################################################3
### Shrinkage Stage
##################################################################3
mdl.StaticStep(name='Static-Shrinkage', previous='Static-thermal')
mdl.steps['Static-Shrinkage'].setValues(
    timeIncrementationMethod=AUTOMATIC, timePeriod=1.0)
for i in range(int(model_height/partition_size)+1):
    mdl.Temperature(createStepName='Static-Shrinkage',
        crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
        UNIFORM, magnitudes=(SHRINKAGE_ANALYSIS_STAGE[len(SHRINKAGE_ANALYSIS_STAGE)-1-i][1], ), name='ShrinkageLvl_'+str(i), region=
        (mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(yMin=i*partition_size, yMax=i*partition_size),))

############# Set boundary condition
######################
### Concslab
######################
concslab_left_vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(xMin=0, xMax=0)
concslab_left_edges    = mdl.rootAssembly.instances['concslab'].edges.getByBoundingBox(xMin=0, xMax=0)

concslab_right_vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(xMin=model_width, xMax=model_width)
concslab_right_edges    = mdl.rootAssembly.instances['concslab'].edges.getByBoundingBox(xMin=model_width, xMax=model_width)

mdl.rootAssembly.Set(name='ConcLeft', vertices=concslab_left_vertices, edges=concslab_left_edges)
mdl.rootAssembly.Set(name='ConcRight', vertices=concslab_right_vertices, edges=concslab_right_edges)
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial'
    , distributionType=UNIFORM, fieldName='', localCsys=None, name='ConcLeft',
    region=mdl.rootAssembly.sets['ConcLeft'], u1=SET, u2=UNSET,
    ur3=SET)
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial'
    , distributionType=UNIFORM, fieldName='', localCsys=None, name='ConcRight',
    region=mdl.rootAssembly.sets['ConcRight'], u1=SET, u2=UNSET,
    ur3=SET)

######################
### Steel Bar
######################
sbar_left = None
sbar_right = None
for rebar_y in rebar_heights:
    for i in [k for k in mdl.rootAssembly.instances.keys() if 'sbar' in k]:
        sbar_left = array_append(sbar_left, mdl.rootAssembly.instances[i].vertices.findAt(((0, rebar_y, 0.0),), ))
        sbar_right = array_append(sbar_right, mdl.rootAssembly.instances[i].vertices.findAt(((model_width, rebar_y, 0.0),), ))

mdl.rootAssembly.Set(name='SBLeft', vertices=sbar_left)
mdl.rootAssembly.Set(name='SBRight', vertices=sbar_right)
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial'
    , distributionType=UNIFORM, fieldName='', localCsys=None, name='SbarLeft',
    region=mdl.rootAssembly.sets['SBLeft'], u1=SET, u2=UNSET,
    ur3=SET)
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial'
    , distributionType=UNIFORM, fieldName='', localCsys=None, name='SbarRight',
    region=mdl.rootAssembly.sets['SBRight'], u1=SET, u2=UNSET,
    ur3=SET)


############# Assign material properties to section
## Assign concrete properties
mdl.HomogeneousSolidSection(material='Concrete', name=
    'ConcSection', thickness=model_height/2)

    # Create set
f = mdl.parts['concslabPart'].faces
mdl.parts['concslabPart'].Set(name='Side', faces= f)

mdl.parts['concslabPart'].SectionAssignment(offset=0.0,
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdl.parts['concslabPart'].sets['Side'], sectionName=
    'ConcSection', thicknessAssignment=FROM_SECTION)

# Add thickness to slab
# mdl.sections['ConcSection'].setValues(material='Concrete', thickness=model_height/2)

## Assign steel properties
mdl.CircularProfile(name='Sbar_radius', r=losbar_diameter/2)
mdl.BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='Steel', name='losbarSection', poissonRatio=0.0,
    profile='Sbar_radius', temperatureVar=LINEAR)

for rebar_y in rebar_heights:
    # trsbar
    mdl.HomogeneousSolidSection(material='Steel', name=
        'trsbarSection', thickness=None)
    for x in model_sbar_location_generator(model_width, trsbar_spacing):
        mdl.parts[trsbar(rebar_y, x)].SectionAssignment(offset=0.0,
            offsetField='', offsetType=MIDDLE_SURFACE, region=
            (mdl.parts[trsbar(rebar_y, x)].faces,), sectionName=
            'trsbarSection', thicknessAssignment=FROM_SECTION)

    # losbar
    e = mdl.parts[losbar(rebar_y)].edges
    mdl.parts[losbar(rebar_y)].Set(name='LongSteel', edges= e)

    mdl.parts[losbar(rebar_y)].SectionAssignment(offset=0.0,
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdl.parts[losbar(rebar_y)].sets['LongSteel'],
        sectionName='losbarSection', thicknessAssignment=FROM_SECTION)
        # Assign material orientation
    mdl.parts[losbar(rebar_y)].MaterialOrientation(
        additionalRotationType=ROTATION_NONE, axis=AXIS_3, fieldName='', localCsys=
        None, orientationType=GLOBAL, region=
        mdl.parts[losbar(rebar_y)].sets['LongSteel'],
        stackDirection=STACK_3)
    mdl.parts[losbar(rebar_y)].assignBeamSectionOrientation(
        method=N1_COSINES, n1=(0.0, 0.0, -1.0), region=
        mdl.parts[losbar(rebar_y)].sets['LongSteel'])



######### Assign connector section to wire
if len(trsbarBond) > 0:
    ## Assigning for bond slip between stbar and concrete
    trsbarBond, _ = edgeNameToEdgeArrayFilter(trsbarBond,
                                              lambda x: True)
    ##trsbar
    mdl.rootAssembly.Set(name='STCONC-trsbar', edges=conArray(trsbarBond))
    mdl.rootAssembly.SectionAssignment(region=
        mdl.rootAssembly.sets['STCONC-trsbar'], sectionName=
        'trsbar-ALL-RIGID')
    mdl.rootAssembly.ConnectorOrientation(localCsys1=
        mdl.rootAssembly.datums[1], region=
        mdl.rootAssembly.allSets['STCONC-trsbar'])


##losbar
##  Vertical
stbarCorner, stbarInterior = edgeNameToEdgeArrayFilter(stbarBondHort,
                               lambda x: eql(x.pointOn[0][0], 0) or
                                         eql(x.pointOn[0][0], model_width))

mdl.rootAssembly.Set(name='STCONC-Interior', edges=conArray(stbarInterior))
mdl.rootAssembly.SectionAssignment(region=
    mdl.rootAssembly.sets['STCONC-Interior'], sectionName=
    'losbar-BondSp interior-HORZ')
mdl.rootAssembly.ConnectorOrientation(localCsys1=
    mdl.rootAssembly.datums[1], region=
    mdl.rootAssembly.allSets['STCONC-Interior'])

mdl.rootAssembly.Set(name='STCONC-corner', edges=conArray(stbarCorner))
mdl.rootAssembly.SectionAssignment(region=
    mdl.rootAssembly.sets['STCONC-corner'], sectionName=
    'losbar-BondSp corner-HORZ')
mdl.rootAssembly.ConnectorOrientation(localCsys1=
    mdl.rootAssembly.datums[1], region=
    mdl.rootAssembly.allSets['STCONC-corner'])

##  Horziontal
stbarVert, _ = edgeNameToEdgeArrayFilter(stbarBondVert,
                               lambda x: True)

mdl.rootAssembly.Set(name='STCONC-VERT', edges=conArray(stbarVert))
mdl.rootAssembly.SectionAssignment(region=
    mdl.rootAssembly.sets['STCONC-VERT'], sectionName=
    'losbar-BondSp all-VERT')
mdl.rootAssembly.ConnectorOrientation(localCsys1=
    mdl.rootAssembly.datums[1], region=
    mdl.rootAssembly.allSets['STCONC-VERT'])

######## Assign section for conc base & shear layer wires

# Horziontal

concBaseBondCorner, concBaseBondInterior = edgeNameToEdgeArrayFilter(concBaseBondHorz,
                               lambda x: eql(x.pointOn[0][0], 0) or
                                         eql(x.pointOn[0][0], model_width))

mdl.rootAssembly.Set(name='CONCBASE-Interior-HORZ', edges=conArray(concBaseBondInterior))
mdl.rootAssembly.SectionAssignment(region=
    mdl.rootAssembly.sets['CONCBASE-Interior-HORZ'],
    sectionName='ConcBase-Friction interior-HORZ')
mdl.rootAssembly.ConnectorOrientation(localCsys1=
    mdl.rootAssembly.datums[1], region=
    mdl.rootAssembly.allSets['CONCBASE-Interior-HORZ'])

mdl.rootAssembly.Set(name='CONCBASE-corner-HORZ', edges=conArray(concBaseBondCorner))
mdl.rootAssembly.SectionAssignment(region=
    mdl.rootAssembly.sets['CONCBASE-corner-HORZ'], sectionName=
    'ConcBase-Friction corner-HORZ')
mdl.rootAssembly.ConnectorOrientation(localCsys1=
    mdl.rootAssembly.datums[1], region=
    mdl.rootAssembly.allSets['CONCBASE-corner-HORZ'])


# Vertical

concBaseBondCorner, concBaseBondInterior = edgeNameToEdgeArrayFilter(concBaseBondVert,
                               lambda x: eql(x.pointOn[0][0], 0) or
                                         eql(x.pointOn[0][0], model_width))

mdl.rootAssembly.Set(name='CONCBASE-Interior-VERT', edges=conArray(concBaseBondInterior))
mdl.rootAssembly.SectionAssignment(region=
    mdl.rootAssembly.sets['CONCBASE-Interior-VERT'],
    sectionName='ConcBase-Friction interior-VERT')
mdl.rootAssembly.ConnectorOrientation(localCsys1=
    mdl.rootAssembly.datums[1], region=
    mdl.rootAssembly.allSets['CONCBASE-Interior-VERT'])

mdl.rootAssembly.Set(name='CONCBASE-corner-VERT', edges=conArray(concBaseBondCorner))
mdl.rootAssembly.SectionAssignment(region=
    mdl.rootAssembly.sets['CONCBASE-corner-VERT'], sectionName=
    'ConcBase-Friction corner-VERT')
mdl.rootAssembly.ConnectorOrientation(localCsys1=
    mdl.rootAssembly.datums[1], region=
    mdl.rootAssembly.allSets['CONCBASE-corner-VERT'])


############### Mesh the sections
all_instances = [mdl.rootAssembly.instances[i] for i in mdl.rootAssembly.instances.keys()]
all_instances = tuple(all_instances)

for i in mdl.rootAssembly.instances.keys():
    _instance_mesh_size = mesh_size_global
    if 'trsbar' in i:
        _instance_mesh_size = mesh_size_trsbar
    mdl.rootAssembly.seedPartInstance(deviationFactor=0.1,
        minSizeFactor=0.1, regions=(mdl.rootAssembly.instances[i],), size=_instance_mesh_size)

for rebar_y in rebar_heights:
    for x in model_sbar_location_generator(model_width, trsbar_spacing):
        ########################################################################
        #### seed the innear diagonals nearby of trsbar
        ########################################################################
        _edges = mdl.rootAssembly.instances['concslab'].edges.getByBoundingBox(xMin=x-partition_size,
                                                                          xMax=x+partition_size,
                                                                          yMin=rebar_y-partition_size,
                                                                          yMax=rebar_y+partition_size)
        mdl.rootAssembly.seedEdgeBySize(constraint=FINER,
            deviationFactor=0.1, edges=_edges, minSizeFactor=0.1, size=mesh_size_trsbar_nearby_diagonals)
        ########################################################################
        #### seed the outer edge nearby of trsbar
        ########################################################################
        # Left
        _edges = mdl.rootAssembly.instances['concslab'].edges.getByBoundingBox(xMin=x-partition_size,
                                                                          xMax=x-partition_size,
                                                                          yMin=rebar_y-partition_size,
                                                                          yMax=rebar_y+partition_size)
        # Right
        _edges += mdl.rootAssembly.instances['concslab'].edges.getByBoundingBox(xMin=x+partition_size,
                                                                          xMax=x+partition_size,
                                                                          yMin=rebar_y-partition_size,
                                                                          yMax=rebar_y+partition_size)
        # Up
        _edges += mdl.rootAssembly.instances['concslab'].edges.getByBoundingBox(xMin=x-partition_size,
                                                                          xMax=x+partition_size,
                                                                          yMin=rebar_y+partition_size,
                                                                          yMax=rebar_y+partition_size)
        # Down
        _edges += mdl.rootAssembly.instances['concslab'].edges.getByBoundingBox(xMin=x-partition_size,
                                                                          xMax=x+partition_size,
                                                                          yMin=rebar_y-partition_size,
                                                                          yMax=rebar_y-partition_size)
        mdl.rootAssembly.seedEdgeBySize(constraint=FINER,
            deviationFactor=0.1, edges=_edges, minSizeFactor=0.1, size=mesh_size_trsbar_nearby_outer_edges)
        ########################################################################
        #### seed the parameter of the trsbar
        ########################################################################
        _edges = mdl.rootAssembly.instances['concslab'].edges.getByBoundingBox(xMin=x-trsbar_diameter/2,
                                                                          xMax=x+trsbar_diameter/2,
                                                                          yMin=rebar_y-trsbar_diameter/2,
                                                                          yMax=rebar_y+trsbar_diameter/2)
        mdl.rootAssembly.seedEdgeBySize(constraint=FINER,
            deviationFactor=0.1, edges=_edges, minSizeFactor=0.1, size=mesh_size_trsbar)

mdl.rootAssembly.setMeshControls(elemShape=QUAD, technique=STRUCTURED,
    regions=mdl.rootAssembly.instances['concslab'].faces)
mdl.rootAssembly.generateMesh(regions=all_instances)


# ## Define mesh size
# e = mdl.rootAssembly.instances['concslab'].edges + mdl.rootAssembly.instances['sbar'].edges
# mdl.rootAssembly.seedEdgeBySize(constraint=FINER,
#     deviationFactor=0.1, edges= e, size=partition_size)
# ## Mesh
# mdl.rootAssembly.generateMesh(regions=(
#     mdl.rootAssembly.instances['concslab'],
#     mdl.rootAssembly.instances['sbar']))



############## Static Analysis

# mdl.ViscoStep(cetol=0.001, name='Static-thermal', nlgeom=ON,
#     previous='Initial')
# del mdl.materials['Concrete'].viscoelastic

##################################
# exit()
import datetime
jobname = model_name+'_@_'+datetime.datetime.now().strftime("%d%m%y_%I-%M%p")
print('> Submitting analysis now with name "'+jobname+'"')
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF,
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF,
    memory=90, memoryUnits=PERCENTAGE, model=model_name,
    modelPrint=OFF, multiprocessingMode=DEFAULT, name=jobname,
    nodalOutputPrecision=SINGLE, numCpus=NUM_OF_CPUS, numDomains=4, numGPUs=NUM_OF_GPUS, queue=None
    , resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='',
    waitHours=0, waitMinutes=0)
mdb.jobs[jobname].submit(consistencyChecking=OFF)
