# delete existing if exists
if DELETE_EXISTING_MODEL and model_name in mdb.models.keys():
    del mdb.models[model_name]

mdb.Model(modelType=STANDARD_EXPLICIT, name=model_name)
mdl = mdb.models[model_name]


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


##################################################
##### CHECK for all partition coor must be rational
##################################################
MAX_DECIMAL_PLACE = 5
for dimension in [model_width, model_height, model_depth]:
    for i in range(int(dimension/partition_size)):
        coordinate = str(float(partition_size * i))
        if coordinate[::-1].find('.') > MAX_DECIMAL_PLACE:
            msg = "ERROR: Dimension '{0}' divided by partition_size'{1}' produced result = '{2}', which does not produce a number within decimal place of '{3}'".format(
            dimension, partition_size, coordinate, MAX_DECIMAL_PLACE)
            print(msg)
            raise AbaqusException(msg)


##################################################
##### SETUP PART DIMENSIONS
##################################################
# Concrete
mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
mdl.sketches['__profile__'].rectangle(point1=(0.0, 0.0),
    point2=(model_width, model_height))
mdl.Part(dimensionality=THREE_D, name='concslabPart', type=
    DEFORMABLE_BODY)
mdl.parts['concslabPart'].BaseSolidExtrude(depth=model_depth, sketch=
    mdl.sketches['__profile__'])
del mdl.sketches['__profile__']
# subbase
mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
mdl.sketches['__profile__'].rectangle(point1=(0.0, 0.0),
    point2=(model_width, subbase_thickness))
mdl.Part(dimensionality=THREE_D, name='subbasePart', type=
    DEFORMABLE_BODY)
mdl.parts['subbasePart'].BaseSolidExtrude(depth=model_depth, sketch=
    mdl.sketches['__profile__'])
del mdl.sketches['__profile__']
# Steel bar
mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
mdl.sketches['__profile__'].Line(point1=(0.0, 0.0), point2=(
    model_width, 0.0))
mdl.Part(dimensionality=THREE_D, name='steelBarPart', type=
    DEFORMABLE_BODY)
mdl.parts['steelBarPart'].BaseWire(sketch=
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
#### Creating Wheel
mdl.ConstrainedSketch(name='__profile__', sheetSize=1000.0)
mdl.sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 0.0), point1=(0.0, 150.0))
# mdl.Part(dimensionality=THREE_D, name='wheelPart', type=
#     DEFORMABLE_BODY)
# mdl.parts['wheelPart'].BaseSolidExtrude(depth=100.0, sketch=
#     mdl.sketches['__profile__'])
# del mdl.sketches['__profile__']


##################################################
##### SETUP MATERIAL PROPERTIES
##################################################
# Concrete
mdl.Material(name='Concrete')
mdl.materials['Concrete'].Elastic(table=((13780.0, 0.15), ))
mdl.materials['Concrete'].Expansion(table=((1.08e-05, ), ))
mdl.materials['Concrete'].Viscoelastic(domain=TIME, table=((
    0.45, 0.45, 48.0), ), time=PRONY)
# mdl.materials['Concrete'].ConcreteDamagedPlasticity(table=((
#     15, 0.1, 1.16, 0.67, 0.000001), ))
# mdl.materials['Concrete'].concreteDamagedPlasticity.ConcreteCompressionHardening(
#     table=((12.8, 0.0), (14.4, 6.59536e-05), (16.0, 0.00013498), (17.6,
#     0.000207553), (19.2, 0.000284282), (20.8, 0.000365977), (22.4,
#     0.000453748), (24.0, 0.000549193), (25.6, 0.000654766), (27.2,
#     0.000774597), (28.8, 0.000916738), (30.4, 0.00110198), (32.0, 0.001549193),
#     (30.4, 0.001686556), (28.8, 0.001823919), (27.2, 0.001961281), (25.6,
#     0.002098644), (24.0, 0.002236007), (22.4, 0.002373369), (20.8,
#     0.002510732), (19.2, 0.002648094), (17.6, 0.002785457), (16.0, 0.00292282),
#     (14.4, 0.003060182), (12.8, 0.003197545), (11.2, 0.003334908), (9.6,
#     0.00347227), (8.0, 0.003609633), (6.4, 0.003746996), (4.8, 0.003884358), (
#     3.2, 0.004021721), (1.6, 0.004159083), (0.0, 0.004296446)))
# mdl.materials['Concrete'].concreteDamagedPlasticity.ConcreteTensionStiffening(
#     table=((3.39411255, 0.0), (3.00603442, 3.72112e-05), (2.755850108,
#     7.44224e-05), (2.570196969, 0.000112761), (2.367909957, 0.000169142), (
#     2.212216452, 0.000225522), (1.970719701, 0.000338284), (1.775816456,
#     0.000451045), (1.604209964, 0.000563806), (1.445915903, 0.000676567), (
#     1.295942111, 0.000789328), (1.151515165, 0.00090209), (1.010971011,
#     0.001014851), (0.873250705, 0.001127612), (0.737648287, 0.001240373), (
#     0.603675012, 0.001353135), (0.470981778, 0.001465896), (0.339312578,
#     0.001578657), (0.208475405, 0.001691418), (0.07832343, 0.001804179)))

# subbase
mdl.Material(name='Subbase')
mdl.materials['Subbase'].Elastic(table=((305, 0.35), ))
mdl.materials['Subbase'].Expansion(table=((9e-06, ), ))

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
mdl.rootAssembly.Instance(dependent=ON, name='subbase',
    part=mdl.parts['subbasePart'])
mdl.rootAssembly.Instance(dependent=ON, name='sbar', part=
    mdl.parts['steelBarPart'])
mdl.rootAssembly.Instance(dependent=ON, name='trsbar',
    part=mdl.parts['trSteelBarPart'])
# mdl.rootAssembly.Instance(dependent=ON, name='wheel-1',
#     part=mdl.parts['wheelPart'])

##################################################
##### TRANSLATE INSTANCES TO CORRECT POS
##################################################
### subbase
mdl.rootAssembly.translate(instanceList=('subbase', ),
    vector=(0.0, -subbase_thickness, 0))
### Lognitudial steel bar
mdl.rootAssembly.translate(instanceList=('sbar', ),
    vector=(0.0, rebar_height, 76.2))
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
    vector=(-152.4, rebar_height, -182.88))
# clone by increments
mdl.rootAssembly.LinearInstancePattern(direction1=(-1.0, 0.0,
    0.0), direction2=(0.0, 1.0, 0.0), instanceList=('trsbar', ), number1=2,
    number2=1, spacing1=914.4, spacing2=1.0)
# rename to better names
mdl.rootAssembly.features.changeKey(fromName='trsbar', toName='trsbar1')
mdl.rootAssembly.features.changeKey(fromName='trsbar-lin-2-1', toName='trsbar2')




##################################################
##### ASSIGN SECTIONS
##################################################
mdl.HomogeneousSolidSection(material='Concrete', name=
    'ConcSection', thickness=None)
mdl.HomogeneousSolidSection(material='Subbase', name=
    'SubbaseSection', thickness=None)
mdl.CircularProfile(name='sbar', r=sbar_diameter/2)
mdl.BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='Steel', name='sbarSection', poissonRatio=0.0,
    profile='sbar', temperatureVar=LINEAR)
mdl.CircularProfile(name='trsbar', r=trsbar_diameter/2)
mdl.BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='TrSteel', name='trsbarSection', poissonRatio=0.0,
    profile='trsbar', temperatureVar=LINEAR)

mdl.parts['concslabPart'].SectionAssignment(offset=0.0,
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdl.parts['concslabPart'].cells),
    sectionName='ConcSection', thicknessAssignment=
    FROM_SECTION)
mdl.parts['subbasePart'].SectionAssignment(offset=0.0,
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdl.parts['subbasePart'].cells),
    sectionName='SubbaseSection', thicknessAssignment=
    FROM_SECTION)
mdl.parts['steelBarPart'].SectionAssignment(offset=0.0,
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    edges=mdl.parts['steelBarPart'].edges),
    sectionName='sbarSection', thicknessAssignment=
    FROM_SECTION)
mdl.parts['steelBarPart'].assignBeamSectionOrientation(
    method=N1_COSINES, n1=(0.0, 0.0, -1.0), region=Region(
    edges=mdl.parts['steelBarPart'].edges))
mdl.parts['trSteelBarPart'].SectionAssignment(offset=0.0,
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    edges=mdl.parts['trSteelBarPart'].edges),
    sectionName='trsbarSection', thicknessAssignment=
    FROM_SECTION)
mdl.parts['trSteelBarPart'].assignBeamSectionOrientation(
    method=N1_COSINES, n1=(0.0, 0.0, -1.0), region=Region(
    edges=mdl.parts['trSteelBarPart'].edges))



# ##################################################
# ##### CREATE DATUM PLANE FOR PARTITIONS
# ##################################################
print('> Creating Datum Planes')
for i in range(int(model_depth/partition_size)-1):
	mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=partition_size * (i+1)
		, principalPlane=XYPLANE)
for i in range(int(model_width/partition_size)-1):
	mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=partition_size * (i+1)
		, principalPlane=YZPLANE)
for i in range(int(model_height/vertical_partition_size)-1):
	mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=vertical_partition_size * (i+1)
		, principalPlane=XZPLANE)
#
print('> Partitioning by datum plane')
# ### Partition by datum plane
for _,v in mdl.parts['concslabPart'].datums.items():
	mdl.parts['concslabPart'].PartitionCellByDatumPlane(cells=
		mdl.parts['concslabPart'].cells, datumPlane=v)

print('> Partitioning Steelbars')
## Partioning Longitudinal and Transverse steel bar in Part
## first create datum points
for i in range(int(model_width/partition_size)-1):
    mdl.parts['steelBarPart'].DatumPointByCoordinate(coords=(
    partition_size*(i+1), 0.0, 0.0))
for i in range(int(model_depth/partition_size)-1):
	mdl.parts['trSteelBarPart'].DatumPointByCoordinate(coords=(
		partition_size*(i+1), 0.0, 0.0))

## Partitioning the steel bar
for part in ['steelBarPart', 'trSteelBarPart']:
    for _,v in mdl.parts[part].datums.items():
        for e in mdl.parts[part].edges:
            try:
                mdl.parts[part].PartitionEdgeByPoint(
                edge=e, point=v)
            except AbaqusException as e:
                if str(e) != "The selected point does not lie within the edge.":
                    raise e # only catch the datum point exception
#
##################################################
##### CONNECT STEEL BAR TO CONCRETE
##################################################
print('> Connecting Steel bar to Concrete')
## Define Connector behavior

mdl.ConnectorSection(name='ConcStbar-BondSp interior-HORZ',
     translationalType=SLOT)
mdl.sections['ConcStbar-BondSp interior-HORZ'].setValues(behaviorOptions=
    (ConnectorElasticity(behavior=NONLINEAR, table=((0.0, -0.2032), (
    -4241.1416, -0.1016), (-12107.77521, -0.0508), (-11013.28706, -0.0254), (
    0.0, 0.0), (11013.28706, 0.0254), (12107.77521, 0.0508), (4241.1416,
    0.1016), (0.0, 0.2032)), independentComponents=(), components=(1, )), ))
mdl.ConnectorSection(name='ConcStbar-BondSp corner-HORZ',
    translationalType=SLOT)
mdl.sections['ConcStbar-BondSp corner-HORZ'].setValues(
    behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR, table=((0.0,
    -0.2032), (-1060.2854, -0.1016), (-3026.9438035, -0.0508), (-2753.3217645,
    -0.0254), (0.0, 0.0), (2753.3217645, 0.0254), (3026.9438035, 0.0508),
    (1060.2854, 0.1016), (0.0, 0.2032)), independentComponents=(), components=(
    1, )), ))
# mdl.ConnectorSection(name='ConcStbar-BondSp all-VERT',
#     translationalType=CARTESIAN)
# mdl.sections['ConcStbar-BondSp all-VERT'].setValues(
#     behaviorOptions=(ConnectorElasticity(table=((1e+15, ), ),
#     independentComponents=(), components=(2, )), ))

## Connect steel bar with concrete

# iterate all steel bar to get its vertices and connect to concrete slab
stbarInstances = []
for i in mdl.rootAssembly.instances.keys():
    if i.startswith('sbar'):
        stbarInstances.append(i)
trstbarInstances = []
for i in mdl.rootAssembly.instances.keys():
    if i.startswith('trsbar'):
        trstbarInstances.append(i)

sbarConnectorCSYS = mdl.rootAssembly.DatumCsysByThreePoints(
    coordSysType=CARTESIAN, name='sbarConnectorCSYS', origin=(0.0, 0.0, 0.0),
    point1=(1.0, 0.0, 0.0), point2=(1.0, 1.0, 0.0))
sbarConnectorCSYS = mdl.rootAssembly.datums[sbarConnectorCSYS.id]
trSbarConnectorCSYS = mdl.rootAssembly.DatumCsysByThreePoints(
    coordSysType=CARTESIAN, name='trSbarConnectorCSYS', origin=(0.0, 0.0, 0.0),
    point1=(0.0, 0.0, 1.0), point2=(0.0, 1.0, 1.0))
print(mdl.rootAssembly.datums)
print(trSbarConnectorCSYS.id)
trSbarConnectorCSYS = mdl.rootAssembly.datums[trSbarConnectorCSYS.id]

## store the wire in lists
for sbar_type in ['long-sbar', 'tran-sbar']:
    stbarBondHort = []
    if sbar_type == 'long-sbar':
        instances = stbarInstances
        csys = sbarConnectorCSYS
    elif sbar_type == 'tran-sbar':
        instances = trstbarInstances
        csys = trSbarConnectorCSYS

    for stbar in instances:
        print('> Connecting {0} wire for {1}'.format(sbar_type, stbar))
        vertices = mdl.rootAssembly.instances[stbar].vertices
        for stbarV in vertices:
            print('>> Connecting vertex of '+str(stbarV))
            concV = mdl.rootAssembly.instances['concslab'].vertices.findAt(stbarV.pointOn[0])
            _tmp = mdl.rootAssembly.WirePolyLine(mergeType=IMPRINT, meshable=OFF
                , points=((stbarV, concV), ))
            stbarBondHort.append(_tmp)

    #### Assign connector section to wire
    updateEdgeLookupTable()
    print(stbarBondHort)
    ##  Horziontal
    stbarCorner, stbarInterior = edgeNameToEdgeArrayFilter(stbarBondHort,
           lambda x: eql(x.pointOn[0][0], 0) or eql(x.pointOn[0][0], model_width)
                  or eql(x.pointOn[0][2], 0) or eql(x.pointOn[0][2], model_depth))

    mdl.rootAssembly.Set(name='STCONC-{0}-Interior'.format(sbar_type), edges=conArray(stbarInterior))
    mdl.rootAssembly.SectionAssignment(region=
        mdl.rootAssembly.sets['STCONC-{0}-Interior'.format(sbar_type)], sectionName=
        'ConcStbar-BondSp interior-HORZ')
    mdl.rootAssembly.ConnectorOrientation(localCsys1=
        csys, region=
        mdl.rootAssembly.allSets['STCONC-{0}-Interior'.format(sbar_type)])

    mdl.rootAssembly.Set(name='STCONC-{0}-Corner'.format(sbar_type), edges=conArray(stbarCorner))
    mdl.rootAssembly.SectionAssignment(region=
        mdl.rootAssembly.sets['STCONC-{0}-Corner'.format(sbar_type)], sectionName=
        'ConcStbar-BondSp corner-HORZ')
    mdl.rootAssembly.ConnectorOrientation(localCsys1=
        csys, region=
        mdl.rootAssembly.allSets['STCONC-{0}-Corner'.format(sbar_type)])

# ##  Vertical
# stbarVert, _ = edgeNameToEdgeArrayFilter(stbarBondVert,
#                                lambda x: True)
#
# mdl.rootAssembly.Set(name='STCONC-VERT', edges=conArray(stbarVert))
# mdl.rootAssembly.SectionAssignment(region=
#     mdl.rootAssembly.sets['STCONC-VERT'], sectionName=
#     'ConcStbar-BondSp all-VERT')
# mdl.rootAssembly.ConnectorOrientation(localCsys1=
#     mdl.rootAssembly.datums[1], region=
#     mdl.rootAssembly.allSets['STCONC-VERT'])



##################################################
##### CONNECT CONCRETE TO SHEAR LAYER
##################################################
concBottomFace = mdl.rootAssembly.instances['concslab'].faces.getByBoundingBox(
    xMin=0, xMax=model_width,
    zMin=0, zMax=model_depth,
    yMin=0, yMax=0)
subbaseTopFace = mdl.rootAssembly.instances['subbase'].faces.getByBoundingBox(
    xMin=0, xMax=model_width,
    zMin=0, zMax=model_depth,
    yMin=0, yMax=0)
mdl.ContactProperty('ConcSubbase-contact')
mdl.interactionProperties['ConcSubbase-contact'].CohesiveBehavior(
    defaultPenalties=OFF, table=((32027.1956, 236.4211, 236.4211), ))
mdl.SurfaceToSurfaceContactStd(adjustMethod=NONE,
    clearanceRegion=None, createStepName='Initial', datumAxis=None,
    initialClearance=OMIT, interactionProperty='ConcSubbase-contact', master=Region(
    side1Faces=concBottomFace), name='Int-1', slave=Region(
    side1Faces=subbaseTopFace), sliding=SMALL, thickness=ON)

# # ##################################################
# # ##### CONNECT CONCRETE TO SHEAR LAYER
# # ##################################################
# print('> Connecting Concrete to Shear Layer')
# ### shear layer connector section properties
#
# CONC_BASE_FRICTION_STIFFNESS_VERT_FORCE = 32027.1956 * (partition_size/STIFFNESS_BASE_VALUE)
# CONC_BASE_FRICTION_STIFFNESS_VERT_DISPLACEMENT = 50.8
#
# mdl.ConnectorSection(name='ConcBase-Friction interior-VERT',
#     translationalType=CARTESIAN)
# mdl.sections['ConcBase-Friction interior-VERT'].setValues(
#     behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR, table=((0.0, 0.0),
#     (CONC_BASE_FRICTION_STIFFNESS_VERT_FORCE, CONC_BASE_FRICTION_STIFFNESS_VERT_DISPLACEMENT)
#     ), independentComponents=(), components=(2, )), ))
#
# mdl.ConnectorSection(name='ConcBase-Friction edge-VERT',
#     translationalType=CARTESIAN)
# mdl.sections['ConcBase-Friction edge-VERT'].setValues(
#     behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR, table=((0.0, 0.0),
#     (CONC_BASE_FRICTION_STIFFNESS_VERT_FORCE / 2, CONC_BASE_FRICTION_STIFFNESS_VERT_DISPLACEMENT)
#     ), independentComponents=(), components=(2, )), ))
#
# mdl.ConnectorSection(name='ConcBase-Friction corner-VERT',
#     translationalType=CARTESIAN)
# mdl.sections['ConcBase-Friction corner-VERT'].setValues(
#     behaviorOptions=(ConnectorElasticity(behavior=NONLINEAR, table=((0.0, 0.0),
#     (CONC_BASE_FRICTION_STIFFNESS_VERT_FORCE / 4, CONC_BASE_FRICTION_STIFFNESS_VERT_DISPLACEMENT)
#     ), independentComponents=(), components=(2, )), ))
#
# CONC_BASE_FRICTION_STIFFNESS_HORZ = 236.4211 * (partition_size/STIFFNESS_BASE_VALUE)
#
# mdl.ConnectorSection(name='ConcBase-Friction interior-HORZ',
#     translationalType=CARTESIAN)
# mdl.sections['ConcBase-Friction interior-HORZ'].setValues(
#     behaviorOptions=(ConnectorElasticity(table=((CONC_BASE_FRICTION_STIFFNESS_HORZ, ), ),
#     independentComponents=(), components=(1, )), ))
#
# mdl.ConnectorSection(name='ConcBase-Friction edge-HORZ',
#     translationalType=CARTESIAN)
# mdl.sections['ConcBase-Friction edge-HORZ'].setValues(
#     behaviorOptions=(ConnectorElasticity(table=((CONC_BASE_FRICTION_STIFFNESS_HORZ / 2, ), ),
#     independentComponents=(), components=(1, )), ))
#
# mdl.ConnectorSection(name='ConcBase-Friction corner-HORZ',
#     translationalType=CARTESIAN)
# mdl.sections['ConcBase-Friction corner-HORZ'].setValues(
#     behaviorOptions=(ConnectorElasticity(table=((CONC_BASE_FRICTION_STIFFNESS_HORZ / 4, ), ),
#     independentComponents=(), components=(1, )), ))
#
# ## Connect steel bar with concrete
#
# # iterate all steel bar to get its vertices and connect to concrete slab
# stbarInstances = []
# for i in mdl.rootAssembly.instances.keys():
#     if 'sbar' in i:
#         stbarInstances.append(i)
## store the wire in lists
# concBaseBondVert = []
# concBaseBondHorz = []
#
# for v in mdl.rootAssembly.instances['concslab'].vertices:
#     if int(v.pointOn[0][1]) == 0: # at y=0
#         print('>> Connecting vertex of '+str(v))
#         # Vertical wire
#         _tmp = mdl.rootAssembly.WirePolyLine(mergeType=IMPRINT, meshable=OFF
#             , points=((None, v), ))
#         concBaseBondVert.append(_tmp)
#         # Horziontal wire
#         _tmp = mdl.rootAssembly.WirePolyLine(mergeType=IMPRINT, meshable=OFF
#             , points=((None, v), ))
#         concBaseBondHorz.append(_tmp)
#
# #### Assign connector section to wire
# updateEdgeLookupTable()
# ##  Horziontal
# concBaseBondCorner, concBaseBondEdge, concBaseBondInterior = edgeNameToEdgeArrayFilter(concBaseBondHorz,
#         lambda x: (eql(x.pointOn[0][0], 0) or eql(x.pointOn[0][0], model_width))
#               and (eql(x.pointOn[0][2], 0) or eql(x.pointOn[0][2], model_depth)),
#         lambda x: eql(x.pointOn[0][0], 0) or eql(x.pointOn[0][0], model_width)
#                or eql(x.pointOn[0][2], 0) or eql(x.pointOn[0][2], model_depth))
#
# mdl.rootAssembly.Set(name='CONCBASE-Interior-HORZ', edges=conArray(concBaseBondInterior))
# mdl.rootAssembly.SectionAssignment(region=
#     mdl.rootAssembly.sets['CONCBASE-Interior-HORZ'],
#     sectionName='ConcBase-Friction interior-HORZ')
# mdl.rootAssembly.ConnectorOrientation(localCsys1=
#     mdl.rootAssembly.datums[1], region=
#     mdl.rootAssembly.allSets['CONCBASE-Interior-HORZ'])
#
# mdl.rootAssembly.Set(name='CONCBASE-edge-HORZ', edges=conArray(concBaseBondEdge))
# mdl.rootAssembly.SectionAssignment(region=
#     mdl.rootAssembly.sets['CONCBASE-edge-HORZ'], sectionName=
#     'ConcBase-Friction edge-HORZ')
# mdl.rootAssembly.ConnectorOrientation(localCsys1=
#     mdl.rootAssembly.datums[1], region=
#     mdl.rootAssembly.allSets['CONCBASE-edge-HORZ'])
#
# mdl.rootAssembly.Set(name='CONCBASE-corner-HORZ', edges=conArray(concBaseBondCorner))
# mdl.rootAssembly.SectionAssignment(region=
#     mdl.rootAssembly.sets['CONCBASE-corner-HORZ'], sectionName=
#     'ConcBase-Friction corner-HORZ')
# mdl.rootAssembly.ConnectorOrientation(localCsys1=
#     mdl.rootAssembly.datums[1], region=
#     mdl.rootAssembly.allSets['CONCBASE-corner-HORZ'])
#
#
# # Vertical
#
# concBaseBondCorner, concBaseBondEdge, concBaseBondInterior = edgeNameToEdgeArrayFilter(concBaseBondVert,
#         lambda x: (eql(x.pointOn[0][0], 0) or eql(x.pointOn[0][0], model_width))
#               and (eql(x.pointOn[0][2], 0) or eql(x.pointOn[0][2], model_depth)),
#         lambda x: eql(x.pointOn[0][0], 0) or eql(x.pointOn[0][0], model_width)
#                or eql(x.pointOn[0][2], 0) or eql(x.pointOn[0][2], model_depth))
#
# mdl.rootAssembly.Set(name='CONCBASE-Interior-VERT', edges=conArray(concBaseBondInterior))
# mdl.rootAssembly.SectionAssignment(region=
#     mdl.rootAssembly.sets['CONCBASE-Interior-VERT'],
#     sectionName='ConcBase-Friction interior-VERT')
# mdl.rootAssembly.ConnectorOrientation(localCsys1=
#     mdl.rootAssembly.datums[1], region=
#     mdl.rootAssembly.allSets['CONCBASE-Interior-VERT'])
#
# mdl.rootAssembly.Set(name='CONCBASE-edge-VERT', edges=conArray(concBaseBondEdge))
# mdl.rootAssembly.SectionAssignment(region=
#     mdl.rootAssembly.sets['CONCBASE-edge-VERT'], sectionName=
#     'ConcBase-Friction edge-VERT')
# mdl.rootAssembly.ConnectorOrientation(localCsys1=
#     mdl.rootAssembly.datums[1], region=
#     mdl.rootAssembly.allSets['CONCBASE-edge-VERT'])
#
# mdl.rootAssembly.Set(name='CONCBASE-corner-VERT', edges=conArray(concBaseBondCorner))
# mdl.rootAssembly.SectionAssignment(region=
#     mdl.rootAssembly.sets['CONCBASE-corner-VERT'], sectionName=
#     'ConcBase-Friction corner-VERT')
# mdl.rootAssembly.ConnectorOrientation(localCsys1=
#     mdl.rootAssembly.datums[1], region=
#     mdl.rootAssembly.allSets['CONCBASE-corner-VERT'])



##################################################
##### DEFINE SETS (NODES & SURFACES)
##################################################
print('> Defining Sets')
#### make each surfacec in y axis as node set
lvl = model_height
j = 0
while lvl >= 0:
    vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(yMax=lvl, yMin=lvl)
    # faces = mdl.rootAssembly.instances['concslab'].faces.getByBoundingBox(yMax=lvl, yMin=lvl)
    # mdl.rootAssembly.Set(name='NodeSurfaceSetLvl_'+str(j), vertices=vertices, faces=faces)
    mdl.rootAssembly.Set(name='NodeSurfaceSetLvl_'+str(j), vertices=vertices)
    j += 1
    lvl -= vertical_partition_size
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

##################################################
##### CREATE STEPS
##################################################

mdl.rootAssembly.Set(edges=
    mdl.rootAssembly.instances['sbar1'].edges+\
    mdl.rootAssembly.instances['sbar2'].edges+\
    mdl.rootAssembly.instances['sbar3'].edges+\
    mdl.rootAssembly.instances['sbar4'].edges+\
    mdl.rootAssembly.instances['sbar5'].edges+\
    mdl.rootAssembly.instances['sbar6'].edges+\
    mdl.rootAssembly.instances['sbar7'].edges+\
    mdl.rootAssembly.instances['sbar8'].edges+\
    mdl.rootAssembly.instances['sbar9'].edges+\
    mdl.rootAssembly.instances['sbar10'].edges+\
    mdl.rootAssembly.instances['sbar11'].edges+\
    mdl.rootAssembly.instances['sbar12'].edges+\
    mdl.rootAssembly.instances['trsbar1'].edges+\
    mdl.rootAssembly.instances['trsbar2'].edges,
    vertices=
    mdl.rootAssembly.instances['sbar1'].vertices+\
    mdl.rootAssembly.instances['sbar2'].vertices+\
    mdl.rootAssembly.instances['sbar3'].vertices+\
    mdl.rootAssembly.instances['sbar4'].vertices+\
    mdl.rootAssembly.instances['sbar5'].vertices+\
    mdl.rootAssembly.instances['sbar6'].vertices+\
    mdl.rootAssembly.instances['sbar7'].vertices+\
    mdl.rootAssembly.instances['sbar8'].vertices+\
    mdl.rootAssembly.instances['sbar9'].vertices+\
    mdl.rootAssembly.instances['sbar10'].vertices+\
    mdl.rootAssembly.instances['sbar11'].vertices+\
    mdl.rootAssembly.instances['sbar12'].vertices+\
    mdl.rootAssembly.instances['trsbar1'].vertices+\
    mdl.rootAssembly.instances['trsbar2'].vertices,
    name='steelbars-set')

TEMP_REGION = Region(
# faces=mdl.rootAssembly.instances['concslab'].faces,
# cells=mdl.rootAssembly.instances['concslab'].cells,
# edges=mdl.rootAssembly.instances['sbar1'].edges+\
# mdl.rootAssembly.instances['trsbar1'].edges+\
# mdl.rootAssembly.instances['sbar2'].edges+\
# mdl.rootAssembly.instances['sbar3'].edges+\
# mdl.rootAssembly.instances['sbar4'].edges+\
# mdl.rootAssembly.instances['sbar5'].edges+\
# mdl.rootAssembly.instances['sbar6'].edges+\
# mdl.rootAssembly.instances['sbar7'].edges+\
# mdl.rootAssembly.instances['sbar8'].edges+\
# mdl.rootAssembly.instances['sbar9'].edges+\
# mdl.rootAssembly.instances['sbar10'].edges+\
# mdl.rootAssembly.instances['sbar11'].edges+\
# mdl.rootAssembly.instances['sbar12'].edges+\
# mdl.rootAssembly.instances['trsbar2'].edges,
# vertices=
mdl.rootAssembly.instances['concslab'].vertices
+\
mdl.rootAssembly.instances['sbar1'].vertices+\
mdl.rootAssembly.instances['trsbar1'].vertices+\
mdl.rootAssembly.instances['sbar2'].vertices+\
mdl.rootAssembly.instances['sbar3'].vertices+\
mdl.rootAssembly.instances['sbar4'].vertices+\
mdl.rootAssembly.instances['sbar5'].vertices+\
mdl.rootAssembly.instances['sbar6'].vertices+\
mdl.rootAssembly.instances['sbar7'].vertices+\
mdl.rootAssembly.instances['sbar8'].vertices+\
mdl.rootAssembly.instances['sbar9'].vertices+\
mdl.rootAssembly.instances['sbar10'].vertices+\
mdl.rootAssembly.instances['sbar11'].vertices+\
mdl.rootAssembly.instances['sbar12'].vertices+\
mdl.rootAssembly.instances['trsbar2'].vertices
)


mdl.Temperature(createStepName='Initial',
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, magnitudes=(48.9, ), name='Initial-temp', region=TEMP_REGION)
mdl.StaticStep(name='Step-1', previous='Initial')



# expression = '(({0}-{1})/{2}*Y+{1})/{0}'.format(TEMP_BOTSURFACE, TEMP_TOPSURFACE, model_height)
# mdl.ExpressionField(description=
#     'The temperature gradient for concslab, from top surface as ', expression=
#     expression, localCsys=None, name='Temperature Gradient of concslab')
# mdl.Temperature(createStepName='Step-1',
#     crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=FIELD
#     , field='Temperature Gradient of concslab', magnitudes=(TEMP_BOTSURFACE, ), name='Conc-gradient-field',
#     region=TEMP_REGION)

# mdl.Temperature(createStepName='Step-1',
#     crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
#     UNIFORM, magnitudes=(TEMP_TOPSURFACE, ), name='concslab-topSutfaceTemp', region=
#     mdl.rootAssembly.sets['SurfaceSet_yMax'])
# mdl.Temperature(createStepName='Step-1',
#     crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
#     UNIFORM, magnitudes=(TEMP_BOTSURFACE, ), name='concslab-botSutfaceTemp', region=
#     mdl.rootAssembly.sets['SurfaceSet_yMin'])

mdl.Temperature(createStepName='Step-1',
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, magnitudes=(TEMP_TOPSURFACE + (TEMP_BOTSURFACE-TEMP_TOPSURFACE)/2, ), name='sbar-midTemp', region=
    mdl.rootAssembly.sets['steelbars-set'])
tempStep = (TEMP_BOTSURFACE - TEMP_TOPSURFACE)/int(model_height/vertical_partition_size)
for i in range(int(model_height/vertical_partition_size) + 1):
    mdl.Temperature(createStepName='Step-1',
        crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
        UNIFORM, magnitudes=(TEMP_TOPSURFACE + i*tempStep, ), name='TempLvl_'+str(i), region=
        mdl.rootAssembly.sets['NodeSurfaceSetLvl_'+str(i)])

## reset the initial tempStep
# mdl.predefinedFields['Initial-temp'].resetToInitial(stepName='Step-1')

# # Define contact surfaces
# mdl.rootAssembly.Surface(name='WheelSurface', side1Faces=
#     mdl.rootAssembly.instances['wheel-1'].faces.getSequenceFromMask(
#     ('[#1 ]', ), ))
# mdl.rootAssembly.Surface(name='TopSurface', side1Faces=
#     mdl.rootAssembly.sets['SurfaceSet_yMax'].faces)
#
# # Contect properties
# mdl.ContactProperty('IntProp-1')
# mdl.interactionProperties['IntProp-1'].TangentialBehavior(
#     dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None,
#     formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION,
#     pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF,
#     table=((0.3, ), ), temperatureDependency=OFF)
# mdl.SurfaceToSurfaceContactExp(clearanceRegion=None,
#     createStepName='Initial', datumAxis=None, initialClearance=OMIT,
#     interactionProperty='IntProp-1', master=
#     mdl.rootAssembly.surfaces['TopSurface'],
#     mechanicalConstraint=KINEMATIC, name='Int-1', slave=
#     mdl.rootAssembly.surfaces['WheelSurface'], sliding=FINITE)
# mdl.parts['wheelPart'].ReferencePoint(point=
#     mdl.parts['wheelPart'].InterestingPoint(
#     mdl.parts['wheelPart'].edges[0], CENTER))
# mdl.Velocity(distributionType=MAGNITUDE, field='', name=
#     'Initial-temp', omega=0.0, region=Region(
#     cells=mdl.rootAssembly.instances['wheel-1'].cells.getSequenceFromMask(
#     mask=('[#1 ]', ), ),
#     faces=mdl.rootAssembly.instances['wheel-1'].faces.getSequenceFromMask(
#     mask=('[#7 ]', ), ),
#     edges=mdl.rootAssembly.instances['wheel-1'].edges.getSequenceFromMask(
#     mask=('[#3 ]', ), ),
#     vertices=mdl.rootAssembly.instances['wheel-1'].vertices.getSequenceFromMask(
#     mask=('[#3 ]', ), ), referencePoints=(
#     mdl.rootAssembly.instances['wheel-1'].referencePoints[2], ))
#     , velocity1=0.0, velocity2=0.0, velocity3=10.0)
# mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial',
#     distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-2',
#     region=Region(referencePoints=(
#     mdl.rootAssembly.instances['wheel-1'].referencePoints[2], ))
#     , u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=SET, ur3=SET)
# mdl.ExplicitDynamicsStep(massScaling=((SEMI_AUTOMATIC, MODEL,
#     AT_BEGINNING, 0.0, 5.55e-07, BELOW_MIN, 0, 0, 0.0, 0.0, 0, None), ), name=
#     'Step-1', previous='Initial', timePeriod=4.0)
# mdl.VelocityBC(amplitude=UNSET, createStepName='Step-1',
#     distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-3',
#     region=Region(referencePoints=(
#     mdl.rootAssembly.instances['wheel-1'].referencePoints[2], ))
#     , v1=UNSET, v2=UNSET, v3=UNSET, vr1=-5.0, vr2=UNSET, vr3=UNSET)


########## SEEDING MESH ################

for p in mdl.parts.keys():
    mdl.parts[p].seedPart(deviationFactor=0.1,
    minSizeFactor=0.1, size=mesh_size)
    mdl.parts[p].generateMesh()



# mdl.parts['concslabPart'].seedPart(deviationFactor=0.1,
#     minSizeFactor=0.1, size=mesh_size)
# mdl.parts['concslabPart'].generateMesh()
#
# mdl.parts['steelBarPart'].seedPart(deviationFactor=0.1,
#     minSizeFactor=0.1, size=mesh_size)
# mdl.parts['steelBarPart'].generateMesh()
#
# mdl.parts['trSteelBarPart'].seedPart(deviationFactor=0.1,
#     minSizeFactor=0.1, size=mesh_size)
# mdl.parts['trSteelBarPart'].generateMesh()

# set element type
mdl.parts['concslabPart'].setElementType(elemTypes=(ElemType(
    elemCode=C3D8, elemLibrary=STANDARD, secondOrderAccuracy=ON,
    distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD),
    ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(
    mdl.parts['concslabPart'].cells, ))

mdl.rootAssembly.regenerate()
