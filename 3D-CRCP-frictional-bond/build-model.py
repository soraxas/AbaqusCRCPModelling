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

def model_sbar_location_generator(dimension, spacing):
    # given the sbar spacing and the dimension of the block,
    # return the location of sbar that lies within the model.
    return (spacing/2+x*spacing for x in range(int(1+(dimension-spacing/2)/spacing)))

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

rebar_height
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
	mdl.sketches['__profile__'].CircleByCenterPerimeter(center=(
		x, y), point1=(x + trsbar_diameter/2, y))
mdl.Part(dimensionality=THREE_D, name='concslabPart', type=
    DEFORMABLE_BODY)
mdl.parts['concslabPart'].BaseSolidExtrude(depth=model_depth, sketch=
    mdl.sketches['__profile__'])
# losbar hollow
mdl.ConstrainedSketch(gridSpacing=119.99, name='__profile__',
    sheetSize=4799.99, transform=
    mdl.parts['concslabPart'].MakeSketchTransform(
    sketchPlane=mdl.parts['concslabPart'].faces[2],
    sketchPlaneSide=SIDE1,
    sketchUpEdge=mdl.parts['concslabPart'].edges[9],
    sketchOrientation=RIGHT, origin=(1524.0, 0, model_depth)))
mdl.parts['concslabPart'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdl.sketches['__profile__'])
for i in range(int(model_depth/losbar_spacing)):
	x = losbar_spacing/2 + losbar_spacing * i
	y = model_height/2
	mdl.sketches['__profile__'].CircleByCenterPerimeter(center=(
		x, y), point1=(x + losbar_diameter/2, y))
mdl.parts['concslabPart'].CutExtrude(flipExtrudeDirection=OFF
    , sketch=mdl.sketches['__profile__'], sketchOrientation=
    RIGHT, sketchPlane=mdl.parts['concslabPart'].faces[2],
    sketchPlaneSide=SIDE1, sketchUpEdge=
    mdl.parts['concslabPart'].edges[9])
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
mdl.sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 0.0), point1=(losbar_diameter/2, 0.0))
mdl.Part(dimensionality=THREE_D, name='loSteelbarPart', type=
    DEFORMABLE_BODY)
mdl.parts['loSteelbarPart'].BaseSolidExtrude(depth=model_width, sketch=
    mdl.sketches['__profile__'])
del mdl.sketches['__profile__']
# Transverse Steel bar
mdl.ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdl.ConstrainedSketch(name='__profile__', sheetSize=3000.0)
mdl.sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 0.0), point1=(trsbar_diameter/2, 0.0))
mdl.Part(dimensionality=THREE_D, name='trSteelBarPart', type=
    DEFORMABLE_BODY)
mdl.parts['trSteelBarPart'].BaseSolidExtrude(depth=model_depth, sketch=
    mdl.sketches['__profile__'])
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
mdl.rootAssembly.Instance(dependent=ON, name='losbar', part=
    mdl.parts['loSteelbarPart'])
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
mdl.rootAssembly.rotate(angle=270.0, axisDirection=(0.0,
    model_height, 0.0), axisPoint=(model_width, 0.0, 0.0), instanceList=('losbar', ))
mdl.rootAssembly.translate(instanceList=('losbar', ),
    vector=(0.0, 152.4, 1600.2))
# clone by increments
mdl.rootAssembly.LinearInstancePattern(direction1=(-1.0, 0.0,
    0.0), direction2=(0.0, 0.0, 1.0), instanceList=('losbar', ), number1=1,
    number2=12, spacing1=model_width, spacing2=152.4)
# rename to better names
mdl.rootAssembly.features.changeKey(fromName='losbar', toName='losbar1')
mdl.rootAssembly.features.changeKey(fromName='losbar-lin-1-2', toName='losbar2')
mdl.rootAssembly.features.changeKey(fromName='losbar-lin-1-3', toName='losbar3')
mdl.rootAssembly.features.changeKey(fromName='losbar-lin-1-4', toName='losbar4')
mdl.rootAssembly.features.changeKey(fromName='losbar-lin-1-5', toName='losbar5')
mdl.rootAssembly.features.changeKey(fromName='losbar-lin-1-6', toName='losbar6')
mdl.rootAssembly.features.changeKey(fromName='losbar-lin-1-7', toName='losbar7')
mdl.rootAssembly.features.changeKey(fromName='losbar-lin-1-8', toName='losbar8')
mdl.rootAssembly.features.changeKey(fromName='losbar-lin-1-9', toName='losbar9')
mdl.rootAssembly.features.changeKey(fromName='losbar-lin-1-10', toName='losbar10')
mdl.rootAssembly.features.changeKey(fromName='losbar-lin-1-11', toName='losbar11')
mdl.rootAssembly.features.changeKey(fromName='losbar-lin-1-12', toName='losbar12')
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
##### CREATE DATUM PLANE FOR PARTITIONS
##################################################
offset = model_height/3/2
print('> Creating Datum Planes')
# up and down of steelbar
mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=rebar_height - offset
	, principalPlane=XZPLANE)
mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=rebar_height + offset
	, principalPlane=XZPLANE)
mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=rebar_height
	, principalPlane=XZPLANE)

for _,v in mdl.parts['concslabPart'].datums.items():
	mdl.parts['concslabPart'].PartitionCellByDatumPlane(cells=
		mdl.parts['concslabPart'].cells, datumPlane=v)

datums = []
# left and right of steelbar
for i, x_ori in enumerate(model_sbar_location_generator(model_width, trsbar_spacing)):
    datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=x_ori - offset
	   , principalPlane=YZPLANE))
    datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=x_ori + offset
	   , principalPlane=YZPLANE))
    datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=x_ori
	   , principalPlane=YZPLANE))

for i, z_ori in enumerate(model_sbar_location_generator(model_depth, losbar_spacing)):
    datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=z_ori - offset
	   , principalPlane=XYPLANE))
    datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=z_ori + offset
	   , principalPlane=XYPLANE))
    datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=z_ori
	   , principalPlane=XYPLANE))


#########################################################
# partition directly next to hole
# for i, x_ori in enumerate(model_sbar_location_generator(model_width, trsbar_spacing)):
#     datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=x_ori
# 	   , principalPlane=YZPLANE))
    # datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=x_ori + trsbar_diameter/2
	#    , principalPlane=YZPLANE))
#########################################################
print('> Partitioning by datum plane')
# convert fetaures to datum item
datums = [mdl.parts['concslabPart'].datums[d.id] for d in datums]
for d in datums:
	mdl.parts['concslabPart'].PartitionCellByDatumPlane(cells=
		mdl.parts['concslabPart'].cells.getByBoundingBox(
        yMin=rebar_height - offset, yMax=rebar_height + offset), datumPlane=d)









##################################################
##### ASSIGN SECTIONS
##################################################
mdl.HomogeneousSolidSection(material='Concrete', name=
    'ConcSection', thickness=None)
mdl.HomogeneousSolidSection(material='Subbase', name=
    'SubbaseSection', thickness=None)
mdl.HomogeneousSolidSection(material='Concrete', name=
    'ConcSection', thickness=None)
mdl.HomogeneousSolidSection(material='Steel', name=
    'sbarSection', thickness=None)
mdl.HomogeneousSolidSection(material='TrSteel', name=
    'trsbarSection', thickness=None)
mdl.parts['concslabPart'].SectionAssignment(offset=0.0,
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdl.parts['concslabPart'].cells),
    sectionName='ConcSection', thicknessAssignment=
    FROM_SECTION)
mdl.parts['subbasePart'].SectionAssignment(
    offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdl.parts['subbasePart'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), )), sectionName='SubbaseSection', thicknessAssignment=
    FROM_SECTION)
mdl.parts['loSteelbarPart'].SectionAssignment(offset=0.0,
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdl.parts['loSteelbarPart'].cells.getSequenceFromMask(
    mask=('[#1 ]', ), )), sectionName='sbarSection', thicknessAssignment=
    FROM_SECTION)
mdl.parts['trSteelBarPart'].SectionAssignment(offset=0.0,
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdl.parts['trSteelBarPart'].cells.getSequenceFromMask(
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
losbarXMin_faces = []
losbarXMax_faces = []
losbarXMin_vertices = []
losbarXMax_vertices = []
for k in mdl.rootAssembly.instances.keys():
    if k.startswith('losbar'):
        losbarXMin_faces.append(mdl.rootAssembly.instances[k].faces.getByBoundingBox(xMax=0, xMin=0))
        losbarXMax_faces.append(mdl.rootAssembly.instances[k].faces.getByBoundingBox(xMax=model_width, xMin=model_width))
        losbarXMin_vertices.append(mdl.rootAssembly.instances[k].vertices.getByBoundingBox(xMax=0, xMin=0))
        losbarXMax_vertices.append(mdl.rootAssembly.instances[k].vertices.getByBoundingBox(xMax=model_width, xMin=model_width))
mdl.rootAssembly.Set(name='sbarNodeSet_xMin', vertices=conArray(losbarXMin_vertices), faces=conArray(losbarXMin_faces))
mdl.rootAssembly.Set(name='sbarNodeSet_xMax', vertices=conArray(losbarXMax_vertices), faces=conArray(losbarXMax_faces))

trsbarZMin_faces = []
trsbarZMax_faces = []
trsbarZMin_vertices = []
trsbarZMax_vertices = []
for k in mdl.rootAssembly.instances.keys():
    if k.startswith('trsbar'):
        trsbarZMin_faces.append(mdl.rootAssembly.instances[k].faces.getByBoundingBox(zMax=0, zMin=0))
        trsbarZMax_faces.append(mdl.rootAssembly.instances[k].faces.getByBoundingBox(zMax=model_depth, zMin=model_depth))
        trsbarZMin_vertices.append(mdl.rootAssembly.instances[k].vertices.getByBoundingBox(zMax=0, zMin=0))
        trsbarZMax_vertices.append(mdl.rootAssembly.instances[k].vertices.getByBoundingBox(zMax=model_depth, zMin=model_depth))
mdl.rootAssembly.Set(name='sbarNodeSet_zMin', vertices=conArray(trsbarZMin_vertices), faces=conArray(trsbarZMin_faces))
mdl.rootAssembly.Set(name='sbarNodeSet_zMax', vertices=conArray(trsbarZMax_vertices), faces=conArray(trsbarZMax_faces))


####### Create Surface set on all six faces
for instance in ['concslab', 'subbase']:
    faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(xMax=0, xMin=0)
    mdl.rootAssembly.Set(name=instance+'SurfaceSet_xMin', faces=faces)
    faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(xMax=model_width, xMin=model_width)
    mdl.rootAssembly.Set(name=instance+'SurfaceSet_xMax', faces=faces)
    faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(zMax=0, zMin=0)
    mdl.rootAssembly.Set(name=instance+'SurfaceSet_zMin', faces=faces)
    faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(zMax=model_depth, zMin=model_depth)
    mdl.rootAssembly.Set(name=instance+'SurfaceSet_zMax', faces=faces)
    if instance == 'concslab':
        faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(yMax=0, yMin=0)
    elif instance == 'subbase':
        faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(yMax=-subbase_thickness, yMin=-subbase_thickness)
    mdl.rootAssembly.Set(name=instance+'SurfaceSet_yMin', faces=faces)
    if instance == 'concslab':
        faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(yMax=model_height, yMin=model_height)
    elif instance == 'subbase':
        faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(yMax=0, yMin=0)
    mdl.rootAssembly.Set(name=instance+'SurfaceSet_yMax', faces=faces)



##################################################
##### CONNECT CONCRETE TO SBAR SURFACES
##################################################
sbar_instances = [x for x in mdl.rootAssembly.instances.keys() if 'sbar' in x]

mdl.ContactProperty('Conc-losbar-contact-prop')
mdl.interactionProperties['Conc-losbar-contact-prop'].CohesiveBehavior(
    eligibility=INITIAL_NODES,
    defaultPenalties=OFF, table=((1e10, 190, 190), ))
####
mdl.ContactProperty('Conc-trsbar-contact-prop')
mdl.interactionProperties['Conc-trsbar-contact-prop'].CohesiveBehavior(
    eligibility=INITIAL_NODES,
    defaultPenalties=OFF, table=((1e10, 190, 190), ))

##########
## face sets for frictional contact

## For long-sbar
instances = [k for k in mdl.rootAssembly.instances.keys() if k.startswith('losbar')]
instances.append('concslab')
for i, z_ori in enumerate(model_sbar_location_generator(model_depth, losbar_spacing)):
    conc_set = None
    sbar_set = None
    for instance in instances:
        faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(
            yMin=rebar_height-losbar_diameter, yMax=rebar_height+losbar_diameter,
            zMin=z_ori-trsbar_diameter, zMax=z_ori+trsbar_diameter,
            xMin=0, xMax=model_width
            )
        if len(faces) > 0:
            set_name = 'losbar_face-'+instance+'-'+str(i+1)
            mdl.rootAssembly.Set(name=set_name, faces=faces)
            if instance == 'concslab':
                conc_set = set_name
            else:
                sbar_set = set_name
    if conc_set is None or sbar_set is None:
        raise AbaqusException("ERROR: sbar surface set not found")
    mdl.SurfaceToSurfaceContactStd(adjustMethod=NONE,
        clearanceRegion=None, createStepName='Initial', datumAxis=None,
        initialClearance=OMIT, interactionProperty='Conc-losbar-contact-prop',
        master=Region(side1Faces=mdl.rootAssembly.sets[conc_set].faces),
        slave=Region(side1Faces=mdl.rootAssembly.sets[sbar_set].faces),
        name='Conc-losbar-contact'+str(i+1), sliding=SMALL, thickness=ON)


## For tran-sbar
instances = [k for k in mdl.rootAssembly.instances.keys() if k.startswith('trsbar')]
instances.append('concslab')
for i, x_ori in enumerate(model_sbar_location_generator(model_width, trsbar_spacing)):
    conc_set = None
    sbar_set = None
    for instance in instances:
        faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(
            yMin=rebar_height-trsbar_diameter, yMax=rebar_height+trsbar_diameter,
            xMin=x_ori-trsbar_diameter, xMax=x_ori+trsbar_diameter,
            zMin=0, zMax=model_depth
            )
        if len(faces) > 0:
            set_name = 'losbar_face-'+instance+'-'+str(i+1)
            mdl.rootAssembly.Set(name=set_name, faces=faces)
            if instance == 'concslab':
                conc_set = set_name
            else:
                sbar_set = set_name
    if conc_set is None or sbar_set is None:
        raise AbaqusException("ERROR: sbar surface set not found")
    mdl.SurfaceToSurfaceContactStd(adjustMethod=NONE,
        clearanceRegion=None, createStepName='Initial', datumAxis=None,
        initialClearance=OMIT, interactionProperty='Conc-trsbar-contact-prop',
        master=Region(side1Faces=mdl.rootAssembly.sets[conc_set].faces),
        slave=Region(side1Faces=mdl.rootAssembly.sets[sbar_set].faces),
        name='Conc-trsbar-contact'+str(i+1), sliding=SMALL, thickness=ON)



##################################################
##### CONNECT CONCRETE TO SUBBASE
##################################################
concBottomFace = mdl.rootAssembly.instances['concslab'].faces.getByBoundingBox(
    xMin=0, xMax=model_width,
    zMin=0, zMax=model_depth,
    yMin=0, yMax=0)
subbaseTopFace = mdl.rootAssembly.instances['subbase'].faces.getByBoundingBox(
    xMin=0, xMax=model_width,
    zMin=0, zMax=model_depth,
    yMin=0, yMax=0)
mdl.ContactProperty('ConcSubbase-contact-prop')
mdl.interactionProperties['ConcSubbase-contact-prop'].CohesiveBehavior(
    defaultPenalties=OFF, table=((32027.1956, 236.4211, 236.4211), ))
mdl.SurfaceToSurfaceContactStd(adjustMethod=NONE,
    clearanceRegion=None, createStepName='Initial', datumAxis=None,
    enforcement=NODE_TO_SURFACE,
    initialClearance=OMIT, interactionProperty='ConcSubbase-contact-prop',
    master=Region(side1Faces=subbaseTopFace),
    slave=Region(side1Faces=concBottomFace),
    name='ConcSubbase-contact', sliding=SMALL, thickness=ON)

##################################################
##### BOUNDARY CONDITION
##################################################
print('> Defining Boundary Conditions')
# conc
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial',
    distributionType=UNIFORM, fieldName='', localCsys=None, name='FrontBC',
    region=mdl.rootAssembly.sets['concslabSurfaceSet_zMin'], u1=UNSET, u2=
    UNSET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
# subbase
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial',
    distributionType=UNIFORM, fieldName='', localCsys=None, name='SubbaseSideBC',
    region=Region(faces=mdl.rootAssembly.sets['subbaseSurfaceSet_zMin'].faces+\
    mdl.rootAssembly.sets['subbaseSurfaceSet_zMax'].faces+\
    mdl.rootAssembly.sets['subbaseSurfaceSet_xMin'].faces+\
    mdl.rootAssembly.sets['subbaseSurfaceSet_xMax'].faces)
    , u1=SET, u2=
    UNSET, u3=SET, ur1=SET, ur2=SET, ur3=SET)
mdl.DisplacementBC(amplitude=UNSET, createStepName='Initial',
    distributionType=UNIFORM, fieldName='', localCsys=None, name='SubbaseBottomBC',
    region=mdl.rootAssembly.sets['subbaseSurfaceSet_yMin'],
    u1=SET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET)
# losbar
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


########## TEMPERATURE ################
TEMP_REGION = Region(
faces=mdl.rootAssembly.instances['concslab'].faces,
cells=mdl.rootAssembly.instances['concslab'].cells,
edges=mdl.rootAssembly.instances['trsbar1'].edges+\
mdl.rootAssembly.instances['trsbar2'].edges+\
mdl.rootAssembly.instances['losbar1'].edges+\
mdl.rootAssembly.instances['losbar2'].edges+\
mdl.rootAssembly.instances['losbar3'].edges+\
mdl.rootAssembly.instances['losbar4'].edges+\
mdl.rootAssembly.instances['losbar5'].edges+\
mdl.rootAssembly.instances['losbar6'].edges+\
mdl.rootAssembly.instances['losbar7'].edges+\
mdl.rootAssembly.instances['losbar8'].edges+\
mdl.rootAssembly.instances['losbar9'].edges+\
mdl.rootAssembly.instances['losbar10'].edges+\
mdl.rootAssembly.instances['losbar11'].edges+\
mdl.rootAssembly.instances['losbar12'].edges,
vertices=mdl.rootAssembly.instances['concslab'].vertices+\
mdl.rootAssembly.instances['trsbar1'].vertices+\
mdl.rootAssembly.instances['trsbar2'].vertices+\
mdl.rootAssembly.instances['losbar1'].vertices+\
mdl.rootAssembly.instances['losbar2'].vertices+\
mdl.rootAssembly.instances['losbar3'].vertices+\
mdl.rootAssembly.instances['losbar4'].vertices+\
mdl.rootAssembly.instances['losbar5'].vertices+\
mdl.rootAssembly.instances['losbar6'].vertices+\
mdl.rootAssembly.instances['losbar7'].vertices+\
mdl.rootAssembly.instances['losbar8'].vertices+\
mdl.rootAssembly.instances['losbar9'].vertices+\
mdl.rootAssembly.instances['losbar10'].vertices+\
mdl.rootAssembly.instances['losbar11'].vertices+\
mdl.rootAssembly.instances['losbar12'].vertices
)

mdl.Temperature(createStepName='Initial',
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, magnitudes=(TEMP_INITIAL, ), name='Initial-temp', region=TEMP_REGION)
mdl.StaticStep(name='Step-1', previous='Initial')

expression = '(({1}-{0})/{2}*Y+{0})'.format(TEMP_BOTSURFACE, TEMP_TOPSURFACE, model_height)
mdl.ExpressionField(description=
    'The temperature gradient for concslab, from top surface as ', expression=
    expression, localCsys=None, name='Temperature Gradient of concslab')
mdl.Temperature(createStepName='Step-1',
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=FIELD
    , field='Temperature Gradient of concslab', magnitudes=(1, ), name='Conc-gradient-field',
    region=TEMP_REGION)



########## SEEDING MESH ################



for part in ['concslabPart', 'loSteelbarPart', 'trSteelBarPart']:
    _factor = 1.0
    if 'bar' in part:
        _factor = sbar_mesh_size_factor
    mdl.parts[part].seedPart(deviationFactor=0.1,
        minSizeFactor=0.1, size=mesh_size * _factor)

    # mdl.parts[part].setMeshControls(
    #     elemShape=TET, regions=
    #     mdl.parts[part].cells.getSequenceFromMask(
    #     ('[#1 ]', ), ), technique=FREE)
    # mdl.parts[part].setElementType(elemTypes=
    #     (ElemType(elemCode=UNKNOWN_HEX, elemLibrary=EXPLICIT), ElemType(
    #     elemCode=UNKNOWN_WEDGE, elemLibrary=EXPLICIT), ElemType(elemCode=C3D10M,
    #     elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)),
    #     regions=(
    #     mdl.parts[part].cells.getSequenceFromMask(
    #     ('[#1 ]', ), ), ))
    mdl.parts[part].generateMesh()

## mesh subbase
mdl.parts['subbasePart'].seedPart(deviationFactor=0.1,
    minSizeFactor=0.1, size=381)
mdl.parts['subbasePart'].generateMesh()








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
# mdl.parts['concslabPart'].setElementType(elemTypes=(ElemType(
#     elemCode=C3D8, elemLibrary=STANDARD, secondOrderAccuracy=ON,
#     distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD),
#     ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(
#     mdl.parts['concslabPart'].cells, ))

mdl.rootAssembly.regenerate()
