##################################################
##### MDOEL SETTINGS
##################################################
model_name = '3D_CRCP'
model_width = 1524.0
model_height = 304.8
model_depth = 1828.8
partition_size = 76.2

sbar_diameter = 19.05 
trsbar_diameter = 15.875

sbar_spacing = 152.4
trsbar_spacing = 914.4

# delete existing if exists
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

EDGE_NAME_LOOKUP_TABLE = None
def updateEdgeLookupTable():
    global EDGE_NAME_LOOKUP_TABLE
    print('Updating lookup table')
    del EDGE_NAME_LOOKUP_TABLE
    EDGE_NAME_LOOKUP_TABLE = {}
    # build a lookup table on demand:
    for i in mdl.rootAssembly.edges:
        EDGE_NAME_LOOKUP_TABLE[i.featureName] = i

def edgeNameToEdge(edgeName):
    global EDGE_NAME_LOOKUP_TABLE
    # given the name of an edge, return an edge repo containing that edge
    if EDGE_NAME_LOOKUP_TABLE is None:
        updateEdgeLookupTable()
    ## EXTREMELY SLOW but a work around for not being able to construct repo by demand
    return EDGE_NAME_LOOKUP_TABLE[edgeName]

def edgeNameToEdgeArrayFilter(edgeNames, filter, filter2=None):
    # given a list of edge names, it will return a list of edge array with a filter
    # It will return a tuple of two list, the first list if when the optional filter return true
    # if filter2 exists, it will also return _c list
    _a = []
    _b = []
    _c = []
    if filter2 is None:
        for i in [edgeNameToEdge(j.name) for j in edgeNames]:
            if i is None:
                continue
            if filter(i):
                _a.append(edgeToArray(i))
            else:
                _b.append(edgeToArray(i))
        return _a, _b
    else:
        for i in [edgeNameToEdge(j.name) for j in edgeNames]:
            if i is None:
                continue
            if filter(i):
                _a.append(edgeToArray(i))
            elif filter2(i):
                _b.append(edgeToArray(i))
            else:
                _c.append(edgeToArray(i))
        return _a, _b, _c

def conArray(array):
    # given a list of array, return a concentrated array
    _tmp = array[0]
    for i in range(1, len(array)):
        _tmp += array[i]
    return _tmp
################################################################################

print('>--------------------')
##################################################
##### SETUP PART DIMENSIONS
##################################################
# Concrete
mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
mdl.sketches['__profile__'].rectangle(point1=(0.0, 0.0),
    point2=(model_width, model_height))
# trsbar hollow
for i in range(int(model_width/trsbar_spacing) + 1):
	x = trsbar_spacing/2 + trsbar_spacing * i
	y_offset = trsbar_diameter/2
	y = model_height/2
	mdb.models['3D_CRCP'].sketches['__profile__'].CircleByCenterPerimeter(center=(
		x, y), point1=(x + trsbar_diameter/2, y))	
mdl.Part(dimensionality=THREE_D, name='concslabPart', type=
    DEFORMABLE_BODY)
mdl.parts['concslabPart'].BaseSolidExtrude(depth=model_depth, sketch=
    mdl.sketches['__profile__'])
# sbar hollow
mdb.models['3D_CRCP'].ConstrainedSketch(gridSpacing=119.99, name='__profile__', 
    sheetSize=4799.99, transform=
    mdb.models['3D_CRCP'].parts['concslabPart'].MakeSketchTransform(
    sketchPlane=mdb.models['3D_CRCP'].parts['concslabPart'].faces[2], 
    sketchPlaneSide=SIDE1, 
    sketchUpEdge=mdb.models['3D_CRCP'].parts['concslabPart'].edges[9], 
    sketchOrientation=RIGHT, origin=(1524.0, 0, model_depth)))
mdb.models['3D_CRCP'].parts['concslabPart'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['3D_CRCP'].sketches['__profile__'])
for i in range(int(model_depth/sbar_spacing)):
	x = sbar_spacing/2 + sbar_spacing * i
	y = model_height/2
	mdb.models['3D_CRCP'].sketches['__profile__'].CircleByCenterPerimeter(center=(
		x, y), point1=(x + sbar_diameter/2, y))
mdb.models['3D_CRCP'].parts['concslabPart'].CutExtrude(flipExtrudeDirection=OFF
    , sketch=mdb.models['3D_CRCP'].sketches['__profile__'], sketchOrientation=
    RIGHT, sketchPlane=mdb.models['3D_CRCP'].parts['concslabPart'].faces[2], 
    sketchPlaneSide=SIDE1, sketchUpEdge=
    mdb.models['3D_CRCP'].parts['concslabPart'].edges[9])
del mdl.sketches['__profile__']

# Steel bar
mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
mdl.sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 0.0), point1=(sbar_diameter/2, 0.0))
mdl.Part(dimensionality=THREE_D, name='steelbarPart', type=
    DEFORMABLE_BODY)
mdl.parts['steelbarPart'].BaseSolidExtrude(depth=model_width, sketch=
    mdb.models['3D_CRCP'].sketches['__profile__'])
del mdl.sketches['__profile__']
# Transverse Steel bar
mdb.models['3D_CRCP'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
mdl.sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 0.0), point1=(trsbar_diameter/2, 0.0))
mdl.Part(dimensionality=THREE_D, name='trSteelBarPart', type=
    DEFORMABLE_BODY)
mdl.parts['trSteelBarPart'].BaseSolidExtrude(depth=model_depth, sketch=
    mdb.models['3D_CRCP'].sketches['__profile__'])
del mdl.sketches['__profile__']


##################################################
##### SETUP MATERIAL PROPERTIES
##################################################
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
# TrSteel
mdl.Material(name='TrSteel')
mdl.materials['TrSteel'].Elastic(table=((200000.0, 0.0), ))
mdl.materials['TrSteel'].Expansion(table=((1.08e-05, ), ))


##################################################
##### CREATE INSTANCES
##################################################
# Create Instance
mdl.rootAssembly.DatumCsysByDefault(CARTESIAN)
mdl.rootAssembly.Instance(dependent=ON, name='concslab',
    part=mdl.parts['concslabPart'])
mdl.rootAssembly.Instance(dependent=ON, name='sbar', part=
    mdl.parts['steelbarPart'])
mdl.rootAssembly.Instance(dependent=ON, name='trsbar',
    part=mdl.parts['trSteelBarPart'])
# mdl.rootAssembly.Instance(dependent=ON, name='wheel-1',
#     part=mdl.parts['wheelPart'])

##################################################
##### TRANSLATE INSTANCES TO CORRECT POS
##################################################
### Lognitudial steel bar
mdl.rootAssembly.rotate(angle=270.0, axisDirection=(0.0,
    model_height, 0.0), axisPoint=(model_width, 0.0, 0.0), instanceList=('sbar', ))
mdl.rootAssembly.translate(instanceList=('sbar', ),
    vector=(0.0, 152.4, 1600.2))
# clone by increments
mdl.rootAssembly.LinearInstancePattern(direction1=(-1.0, 0.0,
    0.0), direction2=(0.0, 0.0, 1.0), instanceList=('sbar', ), number1=1,
    number2=12, spacing1=model_width, spacing2=152.4)
# rename to better names
mdl.rootAssembly.features.changeKey(fromName='sbar', toName='sbar1')
mdl.rootAssembly.features.changeKey(fromName='sbar-lin-1-2', toName='sbar2')
mdl.rootAssembly.features.changeKey(fromName='sbar-lin-1-3', toName='sbar3')
mdl.rootAssembly.features.changeKey(fromName='sbar-lin-1-4', toName='sbar4')
mdl.rootAssembly.features.changeKey(fromName='sbar-lin-1-5', toName='sbar5')
mdl.rootAssembly.features.changeKey(fromName='sbar-lin-1-6', toName='sbar6')
mdl.rootAssembly.features.changeKey(fromName='sbar-lin-1-7', toName='sbar7')
mdl.rootAssembly.features.changeKey(fromName='sbar-lin-1-8', toName='sbar8')
mdl.rootAssembly.features.changeKey(fromName='sbar-lin-1-9', toName='sbar9')
mdl.rootAssembly.features.changeKey(fromName='sbar-lin-1-10', toName='sbar10')
mdl.rootAssembly.features.changeKey(fromName='sbar-lin-1-11', toName='sbar11')
mdl.rootAssembly.features.changeKey(fromName='sbar-lin-1-12', toName='sbar12')
### Transverse steel bar
mdl.rootAssembly.instances['trsbar'].translate(vector=(
    1371.6, 152.4, 0.0))
# clone by increments
mdl.rootAssembly.LinearInstancePattern(direction1=(-1.0, 0.0,
    0.0), direction2=(0.0, 1.0, 0.0), instanceList=('trsbar', ), number1=2,
    number2=1, spacing1=914.4, spacing2=1.0)
# rename to better names
mdl.rootAssembly.features.changeKey(fromName='trsbar', toName='trsbar1')
mdl.rootAssembly.features.changeKey(fromName='trsbar-lin-2-1', toName='trsbar2')

#### translate wheel
# mdl.rootAssembly.translate(instanceList=('Wheel-1', ), vector=(
#     323.85, 454.8, -61.9))
# mdl.rootAssembly.rotate(angle=90.0, axisDirection=(0.0, 150.0,
#     0.0), axisPoint=(323.85, 304.8, 38.1), instanceList=('Wheel-1', ))

##################################################
##### ASSIGN SECTIONS
##################################################
mdb.models['3D_CRCP'].HomogeneousSolidSection(material='Concrete', name=
    'ConcSection', thickness=None)
mdb.models['3D_CRCP'].HomogeneousSolidSection(material='Steel', name=
    'sbarSection', thickness=None)
mdb.models['3D_CRCP'].HomogeneousSolidSection(material='TrSteel', name=
    'trsbarSection', thickness=None)
mdb.models['3D_CRCP'].parts['concslabPart'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdb.models['3D_CRCP'].parts['concslabPart'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), )), sectionName='ConcSection', thicknessAssignment=
    FROM_SECTION)
mdb.models['3D_CRCP'].parts['steelbarPart'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdb.models['3D_CRCP'].parts['steelbarPart'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), )), sectionName='sbarSection', thicknessAssignment=
    FROM_SECTION)
mdb.models['3D_CRCP'].parts['trSteelBarPart'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdb.models['3D_CRCP'].parts['trSteelBarPart'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), )), sectionName='trsbarSection', thicknessAssignment=
    FROM_SECTION)
	

	
	
##################################################
##### DEFINE SETS (NODES & SURFACES)
##################################################
print('> Defining Sets')
#### make each surfacec in y axis as node set
lvl = model_height
j = 0
while lvl >= 0:
    vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(yMax=lvl, yMin=lvl)
    mdl.rootAssembly.Set(name='NodeSetLvl_'+str(j), vertices=vertices)
    j += 1
    lvl -= partition_size
    lvl = round(lvl,10) # force rounding



# create the other four side node set
vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(xMax=0, xMin=0)
mdl.rootAssembly.Set(name='NodeSet_xMin', vertices=vertices)
vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(xMax=model_width, xMin=model_width)
mdl.rootAssembly.Set(name='NodeSet_xMax', vertices=vertices)
vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(zMax=0, zMin=0)
mdl.rootAssembly.Set(name='NodeSet_zMin', vertices=vertices)
vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(zMax=model_depth, zMin=model_depth)
mdl.rootAssembly.Set(name='NodeSet_zMax', vertices=vertices)

## create the steel bar node set
sbarXMin = []
sbarXMax = []
for k in mdl.rootAssembly.instances.keys():
    if k.startswith('sbar'):
        sbarXMin.append(mdl.rootAssembly.instances[k].vertices.getByBoundingBox(xMax=0, xMin=0))
        sbarXMax.append(mdl.rootAssembly.instances[k].vertices.getByBoundingBox(xMax=model_width, xMin=model_width))
mdl.rootAssembly.Set(name='sbarNodeSet_xMin', vertices=conArray(sbarXMin))
mdl.rootAssembly.Set(name='sbarNodeSet_xMax', vertices=conArray(sbarXMax))

trsbarZMin = []
trsbarZMax = []
for k in mdl.rootAssembly.instances.keys():
    if k.startswith('trsbar'):
        trsbarZMin.append(mdl.rootAssembly.instances[k].vertices.getByBoundingBox(zMax=0, zMin=0))
        trsbarZMax.append(mdl.rootAssembly.instances[k].vertices.getByBoundingBox(zMax=model_depth, zMin=model_depth))
mdl.rootAssembly.Set(name='sbarNodeSet_zMin', vertices=conArray(trsbarZMin))
mdl.rootAssembly.Set(name='sbarNodeSet_zMax', vertices=conArray(trsbarZMax))

####### Create Surface set on all six faces
faces = mdl.rootAssembly.instances['concslab'].faces.getByBoundingBox(xMax=0, xMin=0)
mdl.rootAssembly.Set(name='SurfaceSet_xMin', faces=faces)
faces = mdl.rootAssembly.instances['concslab'].faces.getByBoundingBox(xMax=model_width, xMin=model_width)
mdl.rootAssembly.Set(name='SurfaceSet_xMax', faces=faces)
faces = mdl.rootAssembly.instances['concslab'].faces.getByBoundingBox(yMax=0, yMin=0)
mdl.rootAssembly.Set(name='SurfaceSet_yMin', faces=faces)
faces = mdl.rootAssembly.instances['concslab'].faces.getByBoundingBox(yMax=model_height, yMin=model_height)
mdl.rootAssembly.Set(name='SurfaceSet_yMax', faces=faces)
faces = mdl.rootAssembly.instances['concslab'].faces.getByBoundingBox(zMax=0, zMin=0)
mdl.rootAssembly.Set(name='SurfaceSet_zMin', faces=faces)
faces = mdl.rootAssembly.instances['concslab'].faces.getByBoundingBox(zMax=model_depth, zMin=model_depth)
mdl.rootAssembly.Set(name='SurfaceSet_zMax', faces=faces)

##################################################
##### BOUNDARY CONDITION
##################################################
print('> Defining Boundary Conditions')
# conc
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial',
    distributionType=UNIFORM, fieldName='', localCsys=None, name='FrontBC',
    region=mdl.rootAssembly.sets['SurfaceSet_zMin'], u1=UNSET, u2=
    UNSET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
# sbar
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial',
    distributionType=UNIFORM, fieldName='', localCsys=None, name='sbarXMinBC',
    region=mdl.rootAssembly.sets['sbarNodeSet_xMin'], u1=SET, u2=
    UNSET, u3=UNSET, ur1=SET, ur2=UNSET, ur3=SET)
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial',
    distributionType=UNIFORM, fieldName='', localCsys=None, name='sbarXMaxBC',
    region=mdl.rootAssembly.sets['sbarNodeSet_xMax'], u1=SET, u2=
    UNSET, u3=UNSET, ur1=SET, ur2=UNSET, ur3=SET)
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial',
    distributionType=UNIFORM, fieldName='', localCsys=None, name='trsbarZMinBC',
    region=mdl.rootAssembly.sets['sbarNodeSet_zMin'], u1=UNSET, u2=
    UNSET, u3=SET, ur1=SET, ur2=UNSET, ur3=SET)
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial',
    distributionType=UNIFORM, fieldName='', localCsys=None, name='trsbarZMaxBC',
    region=mdl.rootAssembly.sets['sbarNodeSet_zMax'], u1=UNSET, u2=
    UNSET, u3=SET, ur1=SET, ur2=UNSET, ur3=SET)

	
########## SEEDING MESH ################
	
mdl.parts['concslabPart'].seedPart(deviationFactor=0.1,
    minSizeFactor=0.1, size=38.1)
mdl.parts['concslabPart'].generateMesh()

mdl.parts['steelbarPart'].seedPart(deviationFactor=0.1,
    minSizeFactor=0.1, size=38.1)
mdl.parts['steelbarPart'].generateMesh()

mdl.parts['trSteelBarPart'].seedPart(deviationFactor=0.1,
    minSizeFactor=0.1, size=38.1)
mdl.parts['trSteelBarPart'].generateMesh()


mdl.rootAssembly.regenerate()
print('--------------------<')
