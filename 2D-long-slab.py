##################################################
##### MDOEL SETTINGS
##################################################

PARTITION_SIZE_MODIFER = 0.25

model_name = '2D_CRCP'
model_width = 1524.0 * 2
model_height = 304.8
rebar_location = model_height/2
partition_size = 38.1 * PARTITION_SIZE_MODIFER


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

################################################################################

mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
mdl.sketches['__profile__'].rectangle(point1=(0.0, 0.0),
    point2=(model_width, model_height))
mdl.Part(dimensionality=TWO_D_PLANAR, name=
    'concslabPart', type=DEFORMABLE_BODY)
mdl.parts['concslabPart'].BaseShell(sketch=
    mdl.sketches['__profile__'])
del mdl.sketches['__profile__']
mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
mdl.sketches['__profile__'].Line(point1=(0.0, rebar_location), point2=(
    model_width, rebar_location))
mdl.sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdl.sketches['__profile__'].geometry[2])
mdl.Part(dimensionality=TWO_D_PLANAR, name='steelbarPart', type=
    DEFORMABLE_BODY)
mdl.parts['steelbarPart'].BaseWire(sketch=
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
mdl.rootAssembly.Instance(dependent=ON, name='sbar', part=
    mdl.parts['steelbarPart'])



### Create datum plane

for i in range(int(model_width/partition_size)-1):
    mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=partition_size * (i+1)
        , principalPlane=YZPLANE)
for i in range(int(model_height/partition_size)-1):
    mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=partition_size * (i+1)
        , principalPlane=XZPLANE)
#### Partition by datum plane
for k,v in mdl.parts['concslabPart'].datums.items():
    mdl.parts['concslabPart'].PartitionFaceByDatumPlane(faces=
        mdl.parts['concslabPart'].faces, datumPlane=v)
mdl.rootAssembly.regenerate()

## Partioning Longitudinal and Transverse steel bar in Part
    ##Creating DatumPointBy
for i in range(int(model_width/partition_size)-1):
    mdl.parts['steelbarPart'].DatumPointByCoordinate(coords=(
        partition_size*(i+1), rebar_location, 0.0))
    ## Partitioning the steel bar
for i in range(int(model_width/partition_size)-1):
    mdl.parts['steelbarPart'].PartitionEdgeByPoint(edge=
    mdl.parts['steelbarPart'].edges[i], point=
    mdl.parts['steelbarPart'].datums[i+2])


## Define Connector behavior
    ## ConcStbar-BondSp behavior of a whole element
mdl.ConnectorSection(name='ConcStbar-BondSp interior-HORZ',
     translationalType=AXIAL)
mdl.sections['ConcStbar-BondSp interior-HORZ'].setValues(behaviorOptions=
    (ConnectorElasticity(behavior=NONLINEAR, table=((0.0, -0.2032), (
    -4241.1416, -0.1016), (-12107.77521, -0.0508), (-11013.28706, -0.0254), (
    0.0, 0.0), (11013.28706, 0.0254), (12107.77521, 0.0508), (4241.1416,
    0.1016), (0.0, 0.2032)), independentComponents=(), components=(1, )), ))
    ## ConcStbar-BondSp behavior of a whole element
mdl.ConnectorSection(name='ConcStbar-BondSp corner-HORZ',
    translationalType=AXIAL)
mdl.sections['ConcStbar-BondSp corner-HORZ'].setValues(
    behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR, table=((0.0,
    -0.2032), (-2120.5708, -0.1016), (-6053.887607, -0.0508), (-5506.643529,
    -0.0254), (0.0, 0.0), (5506.643529, 0.0254), (6053.887607, 0.0508), (
    2120.5708, 0.1016), (0.0, 0.2032)), independentComponents=(), components=(
    1, )), ))
mdl.ConnectorSection(name='ConcStbar-BondSp all-VERT',
    translationalType=CARTESIAN)
mdl.sections['ConcStbar-BondSp all-VERT'].setValues(
    behaviorOptions=(ConnectorElasticity(table=((1e+15, ), ),
    independentComponents=(), components=(2, )), ))

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

# iterate all steel bar to get its vertices and connect to concrete slab
stbarInstances = []
for i in mdl.rootAssembly.instances.keys():
    if 'sbar' in i:
        stbarInstances.append(i)

## store the wire in lists
stbarBondVert = []
stbarBondHort = []

for stbar in stbarInstances:
    vertices = mdl.rootAssembly.instances[stbar].vertices
    for stbarV in vertices:
        concV = mdl.rootAssembly.instances['concslab'].vertices.findAt(stbarV.pointOn[0])
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
#### make each surfacec in y axis as node set
lvl = model_height
j = 0
while lvl >= 0:
    vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(yMax=lvl, yMin=lvl)
    mdl.rootAssembly.Set(name='SurfaceSet'+str(j), vertices=vertices)
    j += 1
    lvl -= partition_size
    lvl = round(lvl,10) # force rounding

# Set "All"
v = mdl.rootAssembly.instances['concslab'].vertices + mdl.rootAssembly.instances['sbar'].vertices

mdl.rootAssembly.Set(name='All', vertices=v)

####### Create Step
mdl.ViscoStep(cetol=10.0, name='Visco', previous='Initial')
mdl.steps['Visco'].setValues(cetol=10.0, initialInc=4.0,
    timeIncrementationMethod=FIXED, timePeriod=12.0)
####### Create Predefined Field
mdl.Temperature(createStepName='Initial',
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, magnitudes=(48.9, ), name='All', region=
    mdl.rootAssembly.sets['All'])

T = (37.8-29.4)/(model_height/partition_size)
for i in range(int(model_height/partition_size)+1):
    mdl.Temperature(createStepName='Visco',
        crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
        UNIFORM, magnitudes=(29.4+i*T, ), name='TempLvl_'+str(i), region=
        mdl.rootAssembly.sets['SurfaceSet'+str(i)])

############# Set boundary condition
mdl.rootAssembly.Set(name='SBLeft', vertices=
    mdl.rootAssembly.instances['sbar'].vertices.findAt(((0, rebar_location, 0.0),), ))
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial'
    , distributionType=UNIFORM, fieldName='', localCsys=None, name='SbarLeft',
    region=mdl.rootAssembly.sets['SBLeft'], u1=SET, u2=UNSET,
    ur3=SET)
mdl.rootAssembly.Set(name='SbRight', vertices=
    mdl.rootAssembly.instances['sbar'].vertices.findAt(((model_width, rebar_location, 0.0),), ))
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial'
    , distributionType=UNIFORM, fieldName='', localCsys=None, name='SbarRight',
    region=mdl.rootAssembly.sets['SbRight'], u1=SET, u2=UNSET,
    ur3=SET)


############# Assign material properties to section
## Assign concrete properties
mdl.HomogeneousSolidSection(material='Concrete', name=
    'ConcSection', thickness=None)

    # Create set
f = mdl.parts['concslabPart'].faces
mdl.parts['concslabPart'].Set(name='Side', faces= f)

mdl.parts['concslabPart'].SectionAssignment(offset=    0.0,
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdl.parts['concslabPart'].sets['Side'], sectionName=
    'ConcSection', thicknessAssignment=FROM_SECTION)

# Add thickness to slab
mdl.sections['ConcSection'].setValues(material='Concrete', thickness=model_height/2)

## Assign steel properties
mdl.CircularProfile(name='Sbar_diameter', r=9.525)
mdl.BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='Steel', name='SteelSection', poissonRatio=0.0,
    profile='Sbar_diameter', temperatureVar=LINEAR)

e = mdl.parts['steelbarPart'].edges
mdl.parts['steelbarPart'].Set(name='LongSteel', edges= e)

mdl.parts['steelbarPart'].SectionAssignment(offset=0.0,
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdl.parts['steelbarPart'].sets['LongSteel'],
    sectionName='SteelSection', thicknessAssignment=FROM_SECTION)
    # Assign material orientation
mdl.parts['steelbarPart'].MaterialOrientation(
    additionalRotationType=ROTATION_NONE, axis=AXIS_3, fieldName='', localCsys=
    None, orientationType=GLOBAL, region=
    mdl.parts['steelbarPart'].sets['LongSteel'],
    stackDirection=STACK_3)
mdl.parts['steelbarPart'].assignBeamSectionOrientation(
    method=N1_COSINES, n1=(0.0, 0.0, -1.0), region=
    mdl.parts['steelbarPart'].sets['LongSteel'])

############### Mesh the sections

## Define mesh size
e = mdl.rootAssembly.instances['concslab'].edges + mdl.rootAssembly.instances['sbar'].edges
mdl.rootAssembly.seedEdgeBySize(constraint=FINER,
    deviationFactor=0.1, edges= e, size=partition_size)
## Make instances independent
mdl.rootAssembly.makeIndependent(instances=(
    mdl.rootAssembly.instances['concslab'], ))
mdl.rootAssembly.makeIndependent(instances=(
    mdl.rootAssembly.instances['sbar'], ))
## Mesh
mdl.rootAssembly.generateMesh(regions=(
    mdl.rootAssembly.instances['concslab'],
    mdl.rootAssembly.instances['sbar']))


######### Assign connector section to wire

## Assigning for bond slip between stbar and concrete

##  Vertical
stbarCorner, stbarInterior = edgeNameToEdgeArrayFilter(stbarBondHort,
                               lambda x: eql(x.pointOn[0][0], 0) or
                                         eql(x.pointOn[0][0], model_width))

mdl.rootAssembly.Set(name='STCONC-Interior', edges=conArray(stbarInterior))
mdl.rootAssembly.SectionAssignment(region=
    mdl.rootAssembly.sets['STCONC-Interior'], sectionName=
    'ConcStbar-BondSp interior-HORZ')
mdl.rootAssembly.ConnectorOrientation(localCsys1=
    mdl.rootAssembly.datums[1], region=
    mdl.rootAssembly.allSets['STCONC-Interior'])

mdl.rootAssembly.Set(name='STCONC-corner', edges=conArray(stbarCorner))
mdl.rootAssembly.SectionAssignment(region=
    mdl.rootAssembly.sets['STCONC-corner'], sectionName=
    'ConcStbar-BondSp corner-HORZ')
mdl.rootAssembly.ConnectorOrientation(localCsys1=
    mdl.rootAssembly.datums[1], region=
    mdl.rootAssembly.allSets['STCONC-corner'])

##  Horziontal
stbarVert, _ = edgeNameToEdgeArrayFilter(stbarBondVert,
                               lambda x: True)

mdl.rootAssembly.Set(name='STCONC-VERT', edges=conArray(stbarVert))
mdl.rootAssembly.SectionAssignment(region=
    mdl.rootAssembly.sets['STCONC-VERT'], sectionName=
    'ConcStbar-BondSp all-VERT')
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



############## Static Analysis
mdl.StaticStep(maintainAttributes=True, name='Visco',
    previous='Initial')
# mdl.ViscoStep(cetol=0.001, name='Visco', nlgeom=ON,
#     previous='Initial')
# del mdl.materials['Concrete'].viscoelastic
