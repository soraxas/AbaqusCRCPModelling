##################################################
##### MDOEL SETTINGS
##################################################

PARTITION_SIZE_MODIFER = 0.5
# PARTITION_SIZE_MODIFER = 1

model_name = '2D_CRCP'
# model_width = 1524.0
model_width = 1828.8
model_height = 304.8
rebar_location = model_height/2

partition_size = 38.1 * PARTITION_SIZE_MODIFER
mesh_size = partition_size #* 0.2
trsbar_mesh_size = mesh_size * 0.4

# rebar_heights = [model_height * 2/8, model_height * 6/8]
rebar_heights = [model_height * 1/2]

losbar_diameter = 19.05
trsbar_diameter = 15.875

# losbar_spacing = 152.4
trsbar_spacing = 914.4

TEMP_INITIAL = 48.9
TEMP_TOPSURFACE = 29.4
TEMP_BOTSURFACE = 37.8

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
mdl.materials['Concrete'].Elastic(table=((13780.0, 0.15), ))
mdl.materials['Concrete'].Expansion(table=((1.08e-05, ), ))
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


mdl.Temperature(createStepName='Initial',
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, magnitudes=(TEMP_INITIAL, ), name='Initial-temp', region=TEMP_REGION)

expression = '(({1}-{0})/{2}*Y+{0})'.format(TEMP_BOTSURFACE, TEMP_TOPSURFACE, model_height)
mdl.ExpressionField(description=
    'The temperature gradient for concslab, from top surface as ', expression=
    expression, localCsys=None, name='Temperature Gradient of concslab')
mdl.Temperature(createStepName='Static-thermal',
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=FIELD
    , field='Temperature Gradient of concslab', magnitudes=(1, ), name='Conc-gradient-field',
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

############# Set boundary condition
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
    _instance_mesh_size = mesh_size
    if 'trsbar' in i:
        _instance_mesh_size = trsbar_mesh_size
    mdl.rootAssembly.seedPartInstance(deviationFactor=0.1,
        minSizeFactor=0.1, regions=(mdl.rootAssembly.instances[i],), size=_instance_mesh_size)

# seed the parameter of the trsbar
for rebar_y in rebar_heights:
    for x in model_sbar_location_generator(model_width, trsbar_spacing):
        concslab_trsbar_outer_edges = mdl.rootAssembly.instances['concslab'].edges.getByBoundingBox(xMin=x-trsbar_diameter/2,
                                                                          xMax=x+trsbar_diameter/2,
                                                                          yMin=rebar_y-trsbar_diameter/2,
                                                                          yMax=rebar_y+trsbar_diameter/2)
        mdl.rootAssembly.seedEdgeBySize(constraint=FINER,
            deviationFactor=0.1, edges=concslab_trsbar_outer_edges, minSizeFactor=0.1, size=trsbar_mesh_size)

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
