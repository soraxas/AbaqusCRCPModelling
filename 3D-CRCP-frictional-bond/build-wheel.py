# build implicit dynamic step
mdl.ImplicitDynamicsStep(name='Implicit-Dynamic-Wheel', previous=
    'Static-thermal')

wheel_diameter = 175
offset_from_corner = 76.2 * 3
width_of_road = 76.2 * 2
wheel_velocity = 10.0 ## in x direction
wheel_concentrated_force = -10000.0
mesh_road_size = 20.0

print('> Building Wheels')
####################################################
### Modelling a wheel dimension
###################################################
mdl.ConstrainedSketch(name='__profile__',
    sheetSize=200.0)
mdl.sketches['__profile__'].CircleByCenterPerimeter(
    center=(0.0, 0.0), point1=(0.0, wheel_diameter))
mdl.Part(dimensionality=THREE_D, name='Wheel',
    type=DEFORMABLE_BODY)
mdl.parts['Wheel'].BaseSolidExtrude(depth=150.0,
    sketch=mdl.sketches['__profile__'])
del mdl.sketches['__profile__']
mdl.parts['Wheel'].PartitionCellByPlaneThreePoints(
    cells=
    mdl.parts['Wheel'].cells.getSequenceFromMask((
    '[#1 ]', ), ), point1=
    mdl.parts['Wheel'].InterestingPoint(
    mdl.parts['Wheel'].edges[0], MIDDLE), point2=
    mdl.parts['Wheel'].vertices[0], point3=
    mdl.parts['Wheel'].vertices[1])
mdl.parts['Wheel'].PartitionCellByPlaneThreePoints(
    cells=
    mdl.parts['Wheel'].cells.getSequenceFromMask((
    '[#3 ]', ), ), point1=
    mdl.parts['Wheel'].InterestingPoint(
    mdl.parts['Wheel'].edges[6], MIDDLE), point2=
    mdl.parts['Wheel'].InterestingPoint(
    mdl.parts['Wheel'].edges[4], MIDDLE), point3=
    mdl.parts['Wheel'].InterestingPoint(
    mdl.parts['Wheel'].edges[7], MIDDLE))
mdl.parts['Wheel'].DatumPlaneByOffset(flip=SIDE2,
    offset=75.0, plane=
    mdl.parts['Wheel'].faces[4])
mdl.parts['Wheel'].PartitionCellByDatumPlane(
    cells=
    mdl.parts['Wheel'].cells.getSequenceFromMask((
    '[#f ]', ), ), datumPlane=
    mdl.parts['Wheel'].datums[4])
mdl.Material(name='Wheel')
mdl.materials['Wheel'].Density(table=((2000.0, ),
    ))
mdl.materials['Wheel'].Elastic(table=((200000.0,
    0.3), ))
mdl.HomogeneousSolidSection(material='Wheel',
    name='WheelSection', thickness=None)
mdl.parts['Wheel'].Set(cells=
    mdl.parts['Wheel'].cells.getSequenceFromMask((
    '[#ff ]', ), ), name='Set-1')
mdl.parts['Wheel'].SectionAssignment(offset=0.0,
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdl.parts['Wheel'].cells), sectionName=
    'WheelSection', thicknessAssignment=FROM_SECTION)
mdl.rootAssembly.Instance(dependent=ON, name=
    'Wheel-1', part=mdl.parts['Wheel'])

# move to the surface of concrete slab
mdl.rootAssembly.translate(instanceList=(
    'Wheel-1', ), vector=(0.0, wheel_diameter + model_height, 0.0))

# Creating the second wheel
mdl.rootAssembly.translate(instanceList=(
    'Wheel-1', ), vector=(0, 0, offset_from_corner))
mdl.rootAssembly.LinearInstancePattern(direction1=
    (0.0, 0.0, 1.0), direction2=(0.0, 1.0, 0.0), instanceList=('Wheel-1', ),
    number1=2, number2=1, spacing1=model_depth - width_of_road - 2*offset_from_corner,
    spacing2=0)
mdl.rootAssembly.features.changeKey(fromName='Wheel-1-lin-2-1', toName='Wheel-2')

####################################################
### Partitioning wheel
####################################################

datums = []

datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=offset_from_corner
   , principalPlane=XYPLANE))
datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=model_depth - offset_from_corner
   , principalPlane=XYPLANE))

datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=offset_from_corner + width_of_road
   , principalPlane=XYPLANE))
datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=model_depth - offset_from_corner - width_of_road
   , principalPlane=XYPLANE))

# convert fetaures to datum item
datums = [mdl.parts['concslabPart'].datums[d.id] for d in datums]
# partition
for d in datums:
    mdl.parts['concslabPart'].PartitionFaceByDatumPlane(
        datumPlane=d,
        faces=mdl.parts['concslabPart'].faces.getByBoundingBox(yMax=model_height, yMin=model_height))


####################################################
### Creating mesh control
####################################################
# get egdes for mesh control
road_mesh_edges = mdl.parts['concslabPart'].edges.getByBoundingBox(
    yMin=model_height, yMax=model_height,
    zMin=offset_from_corner, zMax=offset_from_corner+width_of_road
    )
road_mesh_edges += mdl.parts['concslabPart'].edges.getByBoundingBox(
    yMin=model_height, yMax=model_height,
    zMin=model_depth - offset_from_corner - width_of_road, zMax=model_depth - offset_from_corner
    )
#### generate mesh for concslab surface road
mdl.parts['concslabPart'].seedEdgeBySize(
    constraint=FINER, deviationFactor=0.1, edges=
    road_mesh_edges, minSizeFactor=0.1, size=mesh_road_size)

####################################################
### Making surface for wheel contact
####################################################
surfaces_road_1 = None
surfaces_road_2 = None
for instance in [i for i in mdl.rootAssembly.instances.keys() if i.startswith('concslab')]:
    f1 = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(
        yMin=model_height, yMax=model_height,
        zMin=offset_from_corner, zMax=offset_from_corner+width_of_road
    )
    f2 = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(
        yMin=model_height, yMax=model_height,
        zMin=model_depth - offset_from_corner - width_of_road, zMax=model_depth - offset_from_corner
    )
    if f1:
        surfaces_road_1 = array_append(surfaces_road_1, f1)
    if f2:
        surfaces_road_2 = array_append(surfaces_road_2, f2)
mdl.rootAssembly.Surface(name='Road Surface 1',
    side1Faces=surfaces_road_1)
mdl.rootAssembly.Surface(name='Road Surface 2',
    side1Faces=surfaces_road_2)


####################################################
### THESE ARE LEAVING IT AS IT IS FOR THE 'get sequence from mash'
####################################################

mdl.rootAssembly.Surface(name='Wheel 1 Surface',
    side1Faces=
    mdl.rootAssembly.instances['Wheel-1'].faces.getSequenceFromMask(
    ('[#3028330 ]', ), ))
mdl.rootAssembly.Surface(name='Wheel 2 Surface',
    side1Faces=
    mdl.rootAssembly.instances['Wheel-2'].faces.getSequenceFromMask(
    ('[#3028330 ]', ), ))

mdl.ContactProperty('wheel-road-contProp')
mdl.interactionProperties['wheel-road-contProp'].TangentialBehavior(
    dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None,
    formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION,
    pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF,
    table=((0.3, ), ), temperatureDependency=OFF)
mdl.interactionProperties['wheel-road-contProp'].NormalBehavior(
    allowSeparation=ON, constraintEnforcementMethod=DEFAULT,
    pressureOverclosure=HARD)
mdl.SurfaceToSurfaceContactStd(adjustMethod=NONE, clearanceRegion=
    None, createStepName='Implicit-Dynamic-Wheel', datumAxis=None, initialClearance=OMIT,
    interactionProperty='wheel-road-contProp', master=
    mdl.rootAssembly.surfaces['Road Surface 1'],
    name='Road-Wheel-1', slave=
    mdl.rootAssembly.surfaces['Wheel 1 Surface'],
    sliding=FINITE, thickness=ON)
mdl.SurfaceToSurfaceContactStd(adjustMethod=NONE, clearanceRegion=
    None, createStepName='Implicit-Dynamic-Wheel', datumAxis=None, initialClearance=OMIT,
    interactionProperty='wheel-road-contProp', master=
    mdl.rootAssembly.surfaces['Road Surface 2'],
    name='Road-Wheel-2', slave=
    mdl.rootAssembly.surfaces['Wheel 2 Surface'],
    sliding=FINITE, thickness=ON)


Wheel_1_datum = mdl.rootAssembly.DatumCsysByThreePoints(
    coordSysType=CARTESIAN, line1=(1.0, 0.0, 0.0), line2=(0.0, 1.0, 0.0), name=
    'Wheel-1-Datum', origin=
    mdl.rootAssembly.instances['Wheel-1'].vertices[1])
Wheel_2_datum = mdl.rootAssembly.DatumCsysByThreePoints(
    coordSysType=CARTESIAN, line1=(1.0, 0.0, 0.0), line2=(0.0, 1.0, 0.0), name=
    'Wheel-2-Datum', origin=
    mdl.rootAssembly.instances['Wheel-2'].vertices[1])

mdl.Coupling(controlPoint=Region(
    vertices=mdl.rootAssembly.instances['Wheel-1'].vertices.getSequenceFromMask(
    mask=('[#2 ]', ), )), couplingType=KINEMATIC, influenceRadius=WHOLE_SURFACE
    , localCsys=mdl.rootAssembly.datums[Wheel_2_datum.id],
    name='Constraint-1', surface=Region(
    side1Faces=mdl.rootAssembly.instances['Wheel-1'].faces.getSequenceFromMask(
    mask=('[#fcfc330 ]', ), )), u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
mdl.Coupling(controlPoint=Region(
    vertices=mdl.rootAssembly.instances['Wheel-2'].vertices.getSequenceFromMask(
    mask=('[#2 ]', ), )), couplingType=KINEMATIC, influenceRadius=WHOLE_SURFACE
    , localCsys=mdl.rootAssembly.datums[Wheel_2_datum.id],
    name='Constraint-2', surface=Region(
    side1Faces=mdl.rootAssembly.instances['Wheel-2'].faces.getSequenceFromMask(
    mask=('[#fcfc330 ]', ), )), u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

mdl.ConcentratedForce(cf2=wheel_concentrated_force,
    createStepName='Implicit-Dynamic-Wheel', distributionType=UNIFORM, field='', localCsys=None
    , name='Load-1', region=Region(
    vertices=mdl.rootAssembly.instances['Wheel-1'].vertices.getSequenceFromMask(
    mask=('[#2 ]', ), )))
mdl.ConcentratedForce(cf2=wheel_concentrated_force,
    createStepName='Implicit-Dynamic-Wheel', distributionType=UNIFORM, field='', localCsys=None
    , name='Load-2', region=Region(
    vertices=mdl.rootAssembly.instances['Wheel-2'].vertices.getSequenceFromMask(
    mask=('[#2 ]', ), )))
mdl.Velocity(distributionType=MAGNITUDE, field='',
    name='Wheel-1 Velocity Field', omega=0.0, region=Region(
    cells=mdl.rootAssembly.instances['Wheel-1'].cells.getSequenceFromMask(
    mask=('[#ff ]', ), ),
    faces=mdl.rootAssembly.instances['Wheel-1'].faces.getSequenceFromMask(
    mask=('[#fffffff ]', ), ),
    edges=mdl.rootAssembly.instances['Wheel-1'].edges.getSequenceFromMask(
    mask=('[#fffdfeff #3 ]', ), ),
    vertices=mdl.rootAssembly.instances['Wheel-1'].vertices.getSequenceFromMask(
    mask=('[#7bd7 ]', ), )), velocity1=wheel_velocity, velocity2=0.0, velocity3=0.0)
mdl.Velocity(distributionType=MAGNITUDE, field='',
    name='Wheel-2 Velocity Field', omega=0.0, region=Region(
    cells=mdl.rootAssembly.instances['Wheel-2'].cells.getSequenceFromMask(
    mask=('[#ff ]', ), ),
    faces=mdl.rootAssembly.instances['Wheel-2'].faces.getSequenceFromMask(
    mask=('[#fffffff ]', ), ),
    edges=mdl.rootAssembly.instances['Wheel-2'].edges.getSequenceFromMask(
    mask=('[#fffdfeff #3 ]', ), ),
    vertices=mdl.rootAssembly.instances['Wheel-2'].vertices.getSequenceFromMask(
    mask=('[#7bd7 ]', ), )), velocity1=wheel_velocity, velocity2=0.0, velocity3=0.0)

####################################################

# mdl.steps['Implicit-Dynamic-Wheel'].suppress()
