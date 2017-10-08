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

def array_append(array, new_item):
    if array is None:
        return new_item
    else:
        return array + new_item
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
for x in model_sbar_location_generator(model_width, trsbar_spacing):
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
for x in model_sbar_location_generator(model_depth, losbar_spacing):
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
    point2=(model_width * num_pavements, subbase_thickness))
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
mdl.parts['loSteelbarPart'].BaseSolidExtrude(depth=model_width * num_pavements, sketch=
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
mdl.materials['Concrete'].Density(table=((2.4e-6, ), ))


# subbase
mdl.Material(name='Subbase')
mdl.materials['Subbase'].Elastic(table=((305, 0.35), ))
mdl.materials['Subbase'].Expansion(table=((9e-06, ), ))
mdl.materials['Subbase'].Density(table=((2.6e-6, ), ))

# Steel
mdl.Material(name='LoSteel')
mdl.materials['LoSteel'].Elastic(table=((200000.0, 0.0), ))
mdl.materials['LoSteel'].Expansion(table=((1.08e-05, ), ))
mdl.materials['LoSteel'].Density(table=((7.85e-6, ), ))
# TrSteel
mdl.Material(name='TrSteel')
mdl.materials['TrSteel'].Elastic(table=((200000.0, 0.0), ))
mdl.materials['TrSteel'].Expansion(table=((1.08e-05, ), ))
mdl.materials['TrSteel'].Density(table=((7.85e-6, ), ))


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
    model_height, 0.0), axisPoint=(model_width * num_pavements , 0.0, 0.0), instanceList=('losbar', ))
mdl.rootAssembly.translate(instanceList=('losbar', ),
    vector=(0.0, rebar_height, model_width * num_pavements + losbar_spacing/2))
# clone by increments
mdl.rootAssembly.LinearInstancePattern(direction1=(-1.0, 0.0,
    0.0), direction2=(0.0, 0.0, 1.0), instanceList=('losbar', ), number1=1,
    number2=12, spacing1=0, spacing2=losbar_spacing)
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
    model_depth-trsbar_spacing/2, rebar_height, 0.0))
# clone by increments
mdl.rootAssembly.LinearInstancePattern(direction1=(-1.0, 0.0,
    0.0), direction2=(0.0, 1.0, 0.0), instanceList=('trsbar', ), number1=2,
    number2=1, spacing1=trsbar_spacing, spacing2=1.0)
# rename to better names
mdl.rootAssembly.features.changeKey(fromName='trsbar', toName='trsbar1')
mdl.rootAssembly.features.changeKey(fromName='trsbar-lin-2-1', toName='trsbar2')

#### translate wheel
# mdl.rootAssembly.translate(instanceList=('Wheel-1', ), vector=(
#     323.85, 454.8, -61.9))
# mdl.rootAssembly.rotate(angle=90.0, axisDirection=(0.0, 150.0,
#     0.0), axisPoint=(323.85, 304.8, 38.1), instanceList=('Wheel-1', ))


# ##################################################
# ##### CREATE DATUM PLANE FOR PARTITIONS
# ##################################################
# offset = model_height/3/2
# print('> Creating Datum Planes')
# # up and down of steelbar
# mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=rebar_height - offset
# 	, principalPlane=XZPLANE)
# mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=rebar_height + offset
# 	, principalPlane=XZPLANE)
# mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=rebar_height
# 	, principalPlane=XZPLANE)
#
# for _,v in mdl.parts['concslabPart'].datums.items():
# 	mdl.parts['concslabPart'].PartitionCellByDatumPlane(cells=
# 		mdl.parts['concslabPart'].cells, datumPlane=v)
#
# datums = []
# # left and right of steelbar
# for i, x_ori in enumerate(model_sbar_location_generator(model_width, trsbar_spacing)):
#     datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=x_ori - offset
# 	   , principalPlane=YZPLANE))
#     datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=x_ori + offset
# 	   , principalPlane=YZPLANE))
#     datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=x_ori
# 	   , principalPlane=YZPLANE))
#
# for i, z_ori in enumerate(model_sbar_location_generator(model_depth, losbar_spacing)):
#     datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=z_ori - offset
# 	   , principalPlane=XYPLANE))
#     datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=z_ori + offset
# 	   , principalPlane=XYPLANE))
#     datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=z_ori
# 	   , principalPlane=XYPLANE))
#
#
# #########################################################
# # partition directly next to hole
# # for i, x_ori in enumerate(model_sbar_location_generator(model_width, trsbar_spacing)):
# #     datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=x_ori
# # 	   , principalPlane=YZPLANE))
#     # datums.append(mdl.parts['concslabPart'].DatumPlaneByPrincipalPlane(offset=x_ori + trsbar_diameter/2
# 	#    , principalPlane=YZPLANE))
# #########################################################
# print('> Partitioning by datum plane')
# # convert fetaures to datum item
# datums = [mdl.parts['concslabPart'].datums[d.id] for d in datums]
# for d in datums:
# 	mdl.parts['concslabPart'].PartitionCellByDatumPlane(cells=
# 		mdl.parts['concslabPart'].cells.getByBoundingBox(
#         yMin=rebar_height - offset, yMax=rebar_height + offset), datumPlane=d)





##################################################
##### LINEAR PATTERNS FOR MULTIPLE PAVEMENT SLABS
##################################################
if num_pavements > 1:
    mdl.rootAssembly.LinearInstancePattern(direction1=(1.0, 0.0, 0.0),
        direction2=(0.0, 1.0, 0.0), instanceList=('concslab', 'trsbar1', 'trsbar2'),
        number1=num_pavements, number2=1, spacing1=model_width, spacing2=0)


##################################################
##### ASSIGN SECTIONS
##################################################
mdl.HomogeneousSolidSection(material='Concrete', name=
    'ConcSection', thickness=None)
mdl.HomogeneousSolidSection(material='Subbase', name=
    'SubbaseSection', thickness=None)
mdl.HomogeneousSolidSection(material='Concrete', name=
    'ConcSection', thickness=None)
mdl.HomogeneousSolidSection(material='LoSteel', name=
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
# lvl = model_height
# j = 0
# while lvl >= 0:
#     vertices = mdl.rootAssembly.instances['concslab'].vertices.getByBoundingBox(yMax=lvl, yMin=lvl)
#     mdl.rootAssembly.Set(name='NodeSetLvl_'+str(j), vertices=vertices)
#     j += 1
#     lvl -= partition_size
#     lvl = round(lvl,10) # force rounding

combinations = [('xMin', {'xMin':0, 'xMax':0}), \
                ('xMax', {'xMin':model_width*num_pavements, 'xMax':model_width*num_pavements}), \
                ('zMin', {'zMin':0, 'zMax':0}), \
                ('zMax', {'zMin':model_depth, 'zMax':model_depth}) ]

# create the other four side node set
for combination in combinations:
    vertices = None
    faces    = None
    for k in mdl.rootAssembly.instances.keys():
        if k.startswith('concslab'):
            vertices = array_append(vertices, mdl.rootAssembly.instances[k].vertices.getByBoundingBox( **combination[1] ))
            faces = array_append(faces, mdl.rootAssembly.instances[k].faces.getByBoundingBox( **combination[1] ))
    mdl.rootAssembly.Set(name='concslabSurfaceSet_'+combination[0], faces=faces)
    mdl.rootAssembly.Set(name='concslabNodeSet_'+combination[0], vertices=vertices)


####### Create Surface set on all six faces for subbase
faces = mdl.rootAssembly.instances['subbase'].faces.getByBoundingBox(xMax=0, xMin=0)
mdl.rootAssembly.Set(name='subbaseSurfaceSet_xMin', faces=faces)
faces = mdl.rootAssembly.instances['subbase'].faces.getByBoundingBox(xMax=model_width*num_pavements, xMin=model_width*num_pavements)
mdl.rootAssembly.Set(name='subbaseSurfaceSet_xMax', faces=faces)
faces = mdl.rootAssembly.instances['subbase'].faces.getByBoundingBox(zMax=0, zMin=0)
mdl.rootAssembly.Set(name='subbaseSurfaceSet_zMin', faces=faces)
faces = mdl.rootAssembly.instances['subbase'].faces.getByBoundingBox(zMax=model_depth, zMin=model_depth)
mdl.rootAssembly.Set(name='subbaseSurfaceSet_zMax', faces=faces)
faces = mdl.rootAssembly.instances['subbase'].faces.getByBoundingBox(yMax=-subbase_thickness, yMin=-subbase_thickness)
mdl.rootAssembly.Set(name='subbaseSurfaceSet_yMin', faces=faces)
faces = mdl.rootAssembly.instances['subbase'].faces.getByBoundingBox(yMax=0, yMin=0)
mdl.rootAssembly.Set(name='subbaseSurfaceSet_yMax', faces=faces)

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
        losbarXMax_vertices.append(mdl.rootAssembly.instances[k].vertices.getByBoundingBox(xMax=model_width*num_pavements, xMin=model_width*num_pavements))
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









##################################################
##### SURFACE INTERACTION
##################################################
run('surface-contact-standard.py')
# run('surface-contact-explicit.py')


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

# Save by Oscar on 2017_09_30-14.01.24; build 6.14-
# exit()










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
