# -*- coding: mbcs -*-
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

# MDOEL SETTINGS
model_name = 'CRCP'
model_width = 1524.0
model_height = 304.8
model_depth = 1828.0


partition_size = 38.1

# delete existing if exists
if model_name in mdb.models.keys():
    del mdb.models[model_name]
mdb.Model(modelType=STANDARD_EXPLICIT, name=model_name)
mdl = mdb.models[model_name]



#####################################################
### Setup concrete model dimension PART
#####################################################
# Concrete
mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
mdl.sketches['__profile__'].rectangle(point1=(0.0, 0.0),
    point2=(model_width, model_height))
mdl.Part(dimensionality=THREE_D, name='concslabPart', type=
    DEFORMABLE_BODY)
mdl.parts['concslabPart'].BaseSolidExtrude(depth=model_depth, sketch=
    mdl.sketches['__profile__'])
del mdl.sketches['__profile__']
# Steel bar
mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
mdl.sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
    model_width, 0.0))
mdl.Part(dimensionality=THREE_D, name='steelbarPart', type=
    DEFORMABLE_BODY)
mdl.parts['steelbarPart'].BaseWire(sketch=
    mdl.sketches['__profile__'])
del mdl.sketches['__profile__']
# Transverse Steel bar
mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
mdl.sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
    model_depth, 0.0))
mdl.Part(dimensionality=THREE_D, name='trSteelBarPart', type=
    DEFORMABLE_BODY)
mdl.parts['trSteelBarPart'].BaseWire(sketch=
    mdl.sketches['__profile__'])
del mdl.sketches['__profile__']



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
# TrSteel
mdl.Material(name='TrSteel')
mdl.materials['TrSteel'].Elastic(table=((200000.0, 0.0), ))
mdl.materials['TrSteel'].Expansion(table=((1.08e-05, ), ))



#####################################################
### Create Instances
#####################################################
# Create Instance
mdl.rootAssembly.DatumCsysByDefault(CARTESIAN)
mdl.rootAssembly.Instance(dependent=ON, name='concslab',
    part=mdl.parts['concslabPart'])
mdl.rootAssembly.Instance(dependent=ON, name='sbar', part=
    mdl.parts['steelbarPart'])
mdl.rootAssembly.Instance(dependent=ON, name='trsbar',
    part=mdl.parts['trSteelBarPart'])

##### Create each Steel Bar instances at correct pos

### Lognitudial steel bar
mdl.rootAssembly.translate(instanceList=('sbar', ),
    vector=(0.0, 152.4, 76.2))
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
    1706.88, 0.0, 0.0))
mdl.rootAssembly.rotate(angle=270.0, axisDirection=(0.0,
    model_height, 0.0), axisPoint=(model_width, 0.0, 0.0), instanceList=('trsbar', ))
mdl.rootAssembly.translate(instanceList=('trsbar', ),
    vector=(-152.4, 152.4, -182.88))
# clone by increments
mdl.rootAssembly.LinearInstancePattern(direction1=(-1.0, 0.0,
    0.0), direction2=(0.0, 1.0, 0.0), instanceList=('trsbar', ), number1=2,
    number2=1, spacing1=914.4, spacing2=1.0)
# rename to better names
mdl.rootAssembly.features.changeKey(fromName='trsbar', toName='trsbar1')
mdl.rootAssembly.features.changeKey(fromName='trsbar-lin-2-1', toName='trsbar2')







### Create datum plane
for i in range(48-1):
	mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=partition_size * (i+1)
		, principalPlane=XYPLANE)
for i in range(40-1):
	mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=partition_size * (i+1)
		, principalPlane=YZPLANE)
for i in range(8-1):
	mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=partition_size * (i+1)
		, principalPlane=XZPLANE)

# ### Partition by datum plane
for k,v in mdl.parts['concslabPart'].datums.items():
	mdl.parts['concslabPart'].PartitionCellByDatumPlane(cells=
		mdl.parts['concslabPart'].cells, datumPlane=v)


## Define Connector behavior
	## NonLinear-BondSp behavior of a whole element
mdl.ConnectorSection(extrapolation=LINEAR, name=
    'NonLinear-BondSp 1', rotationalType=ALIGN, translationalType=AXIAL)
mdl.sections['NonLinear-BondSp 1'].setValues(behaviorOptions=
    (ConnectorElasticity(behavior=NONLINEAR, table=((0.0, -0.2032), (
    -424.11416, -0.1016), (-1210.777521, -0.0508), (-1101.328706, -0.0254), (
    0.0, 0.0), (1101.328706, 0.0254), (1210.777521, 0.0508), (424.11416,
    0.1016), (0.0, 0.2032)), independentComponents=(), components=(1, )), ))
	## NonLinear-BondSp behavior of a whole element
mdl.ConnectorSection(name='NonLinear-BondSp edge',
    rotationalType=ALIGN, translationalType=AXIAL)
mdl.sections['NonLinear-BondSp edge'].setValues(
    behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR, table=((0.0,
    -0.2032), (-212.05708, -0.1016), (-605.3887607, -0.0508), (-550.6643529,
    -0.0254), (0.0, 0.0), (550.6643529, 0.0254), (605.3887607, 0.0508), (
    212.05708, 0.1016), (0.0, 0.2032)), independentComponents=(), components=(
    1, )), ))

## Partioning Longitudinal and Transverse steel bar in Part
	##Creating DatumPointBy

for i in range(48-1):
	mdl.parts['trSteelBarPart'].DatumPointByCoordinate(coords=(
		partition_size*(i+1), 0.0, 0.0))
for i in range(40-1):
	mdl.parts['steelbarPart'].DatumPointByCoordinate(coords=(
		partition_size*(i+1), 0.0, 0.0))
	## Partitioning the steel bar
for i in range(40-1):
	mdl.parts['steelbarPart'].PartitionEdgeByPoint(edge=
    mdl.parts['steelbarPart'].edges[i], point=
    mdl.parts['steelbarPart'].datums[i+2])
for i in range(48-1):
	mdl.parts['trSteelBarPart'].PartitionEdgeByPoint(edge=
    mdl.parts['trSteelBarPart'].edges[i], point=
    mdl.parts['trSteelBarPart'].datums[i+2])


############# Connect steel bar with concrete

# iterate all steel bar to get its vertices and connect to concrete slab
stbarInstances = []
for i in mdl.rootAssembly.instances.keys():
	if 'sbar' in i:
		stbarInstances.append(i)

for stbar in stbarInstances:
	vertices = mdl.rootAssembly.instances[stbar].vertices
	for stbarV in vertices:
		concV = mdl.rootAssembly.instances['concslab'].vertices.findAt(stbarV.pointOn[0])

		# connect these two point
		mdl.rootAssembly.WirePolyLine(mergeType=IMPRINT, meshable=OFF
			, points=((stbarV, concV), ))


### shear layer connector section properties

mdl.ConnectorSection(name='Conc and base friction-interior',
    translationalType=CARTESIAN)
mdl.sections['Conc and base friction-interior'].setValues(
    behaviorOptions=(ConnectorElasticity(table=((59.080527, 59.080527), ),
    independentComponents=(), components=(1, 2)), ))

mdl.ConnectorSection(name='Conc and base friction-edge',
    translationalType=CARTESIAN)
mdl.sections['Conc and base friction-edge'].setValues(
    behaviorOptions=(ConnectorElasticity(table=((29.5402635, 29.5402635), ),
    independentComponents=(), components=(1, 2)), ))

mdl.ConnectorSection(name='Conc and base friction-corner',
    translationalType=CARTESIAN)
mdl.sections['Conc and base friction-corner'].setValues(
    behaviorOptions=(ConnectorElasticity(table=((14.77013175, 14.77013175), ),
    independentComponents=(), components=(1, 2)), ))



############# Connect concrete slab with shear layer
# iterate all concrete slab vertices and only apply connector for the one with constraints y=0

vertices = mdl.rootAssembly.instances['concslab'].vertices

for v in vertices:
	if int(v.pointOn[0][1]) == 0: # at y=0
		mdl.rootAssembly.WirePolyLine(mergeType=IMPRINT, meshable=OFF
			, points=((None, v), ))


########## Defining node sets
#### make each surfacec in y axis as node set
lvl = model_height
j = 0
while lvl >= 0:
    vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(yMax=lvl, yMin=lvl)
    mdl.rootAssembly.Set(name='NodeSetLvl_'+str(j), vertices=vertices)
    j += 1
    lvl -= partition_size
    lvl = round(lvl,10) # force rounding

## create the other four side node set
vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(xMax=0, xMin=0)
mdl.rootAssembly.Set(name='NodeSet_xMin', vertices=vertices)
vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(xMax=model_width, xMin=model_width)
mdl.rootAssembly.Set(name='NodeSet_xMax', vertices=vertices)
vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(zMax=0, zMin=0)
mdl.rootAssembly.Set(name='NodeSet_zMin', vertices=vertices)
vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(zMax=model_depth, zMin=model_depth)
mdl.rootAssembly.Set(name='NodeSet_zMax', vertices=vertices)


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


# boundary Condition
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial',
    distributionType=UNIFORM, fieldName='', localCsys=None, name='FrontBC',
    region=mdl.rootAssembly.sets['SurfaceSet_zMin'], u1=UNSET, u2=
    UNSET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)


#### Creating Wheel
mdl.ConstrainedSketch(name='__profile__', sheetSize=1000.0)
mdl.sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 0.0), point1=(0.0, 150.0))
mdl.Part(dimensionality=THREE_D, name='WheelPart', type=
    DEFORMABLE_BODY)
mdl.parts['WheelPart'].BaseSolidExtrude(depth=100.0, sketch=
    mdl.sketches['__profile__'])
del mdl.sketches['__profile__']

### instance of wheels
mdl.rootAssembly.Instance(dependent=ON, name='Wheel-1',
    part=mdl.parts['WheelPart'])

# translate wheel
mdl.rootAssembly.translate(instanceList=('Wheel-1', ), vector=(
    323.85, 454.8, -61.9))
mdl.rootAssembly.rotate(angle=90.0, axisDirection=(0.0, 150.0,
    0.0), axisPoint=(323.85, 304.8, 38.1), instanceList=('Wheel-1', ))

# Define contact surfaces
mdl.rootAssembly.Surface(name='WheelSurface', side1Faces=
    mdl.rootAssembly.instances['Wheel-1'].faces.getSequenceFromMask(
    ('[#1 ]', ), ))
mdl.rootAssembly.Surface(name='TopSurface', side1Faces=
    mdl.rootAssembly.sets['SurfaceSet_yMax'].faces)

# Contect properties
mdl.ContactProperty('IntProp-1')
mdl.interactionProperties['IntProp-1'].TangentialBehavior(
    dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None,
    formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION,
    pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF,
    table=((0.3, ), ), temperatureDependency=OFF)
mdl.SurfaceToSurfaceContactExp(clearanceRegion=None,
    createStepName='Initial', datumAxis=None, initialClearance=OMIT,
    interactionProperty='IntProp-1', master=
    mdl.rootAssembly.surfaces['TopSurface'],
    mechanicalConstraint=KINEMATIC, name='Int-1', slave=
    mdl.rootAssembly.surfaces['WheelSurface'], sliding=FINITE)
mdl.parts['WheelPart'].ReferencePoint(point=
    mdl.parts['WheelPart'].InterestingPoint(
    mdl.parts['WheelPart'].edges[0], CENTER))
mdl.Velocity(distributionType=MAGNITUDE, field='', name=
    'Predefined Field-1', omega=0.0, region=Region(
    cells=mdl.rootAssembly.instances['Wheel-1'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), ),
    faces=mdl.rootAssembly.instances['Wheel-1'].faces.getSequenceFromMask(
    mask=('[#7 ]', ), ),
    edges=mdl.rootAssembly.instances['Wheel-1'].edges.getSequenceFromMask(
    mask=('[#3 ]', ), ),
    vertices=mdl.rootAssembly.instances['Wheel-1'].vertices.getSequenceFromMask(
    mask=('[#3 ]', ), ), referencePoints=(
    mdl.rootAssembly.instances['Wheel-1'].referencePoints[2], ))
    , velocity1=0.0, velocity2=0.0, velocity3=10.0)
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial',
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-2',
    region=Region(referencePoints=(
    mdl.rootAssembly.instances['Wheel-1'].referencePoints[2], ))
    , u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=SET, ur3=SET)
mdl.ExplicitDynamicsStep(massScaling=((SEMI_AUTOMATIC, MODEL,
    AT_BEGINNING, 0.0, 5.55e-07, BELOW_MIN, 0, 0, 0.0, 0.0, 0, None), ), name=
    'Step-1', previous='Initial', timePeriod=4.0)
mdl.VelocityBC(amplitude=UNSET, createStepName='Step-1',
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-3',
    region=Region(referencePoints=(
    mdl.rootAssembly.instances['Wheel-1'].referencePoints[2], ))
    , v1=UNSET, v2=UNSET, v3=UNSET, vr1=-5.0, vr2=UNSET, vr3=UNSET)


########## SEEDING MESH ################

# mdl.parts['concslabPart'].seedPart(deviationFactor=0.1,
#     minSizeFactor=0.1, size=3.8)
# mdl.parts['concslabPart'].generateMesh()


mdl.rootAssembly.regenerate()
