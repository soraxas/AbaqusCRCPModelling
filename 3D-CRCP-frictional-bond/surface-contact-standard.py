mdl.StaticStep(name='Static-thermal', previous='Initial')

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
instances = [k for k in mdl.rootAssembly.instances.keys() if k.startswith('losbar') or k.startswith('concslab')]
for i, z_ori in enumerate(model_sbar_location_generator(model_depth, losbar_spacing)):
    conc_set = None
    sbar_set = None
    for instance in instances:
        faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(
            yMin=rebar_heights-losbar_diameter, yMax=rebar_heights+losbar_diameter,
            zMin=z_ori-trsbar_diameter, zMax=z_ori+trsbar_diameter,
            xMin=0, xMax=model_width*num_pavements
            )
        if len(faces) > 0:
            if instance.startswith('concslab'):
                conc_set = array_append(conc_set, faces)
            else:
                sbar_set = faces
    if conc_set is None or sbar_set is None:
        raise AbaqusException("ERROR: sbar surface set not found")

    mdl.rootAssembly.Set(name='losbar_face-concslab-'+str(i+1), faces=conc_set)
    mdl.rootAssembly.Set(name='losbar_face-sbar-'+str(i+1), faces=sbar_set)

    mdl.SurfaceToSurfaceContactStd(adjustMethod=NONE,
        clearanceRegion=None, createStepName='Initial', datumAxis=None,
        initialClearance=OMIT, interactionProperty='Conc-losbar-contact-prop',
        master=Region(side1Faces=mdl.rootAssembly.sets['losbar_face-concslab-'+str(i+1)].faces),
        slave=Region(side1Faces=mdl.rootAssembly.sets['losbar_face-sbar-'+str(i+1)].faces),
        name='Conc-losbar-contact'+str(i+1), sliding=SMALL, thickness=ON)


## For tran-sbar
instances = [k for k in mdl.rootAssembly.instances.keys() if k.startswith('trsbar') or k.startswith('concslab')]
for i, x_ori in enumerate(model_sbar_location_generator(model_width*num_pavements, trsbar_spacing)):
    conc_set = None
    sbar_set = None

    for instance in instances:
        faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(
            yMin=rebar_heights-trsbar_diameter, yMax=rebar_heights+trsbar_diameter,
            xMin=x_ori-trsbar_diameter, xMax=x_ori+trsbar_diameter,
            zMin=0, zMax=model_depth
            )
        if len(faces) > 0:
            if instance.startswith('concslab'):
                conc_set = array_append(conc_set, faces)
            else:
                sbar_set = faces
    if conc_set is None or sbar_set is None:
        raise AbaqusException("ERROR: sbar surface set not found")

    mdl.rootAssembly.Set(name='trsbar_face-concslab-'+str(i+1), faces=conc_set)
    mdl.rootAssembly.Set(name='trsbar_face-sbar-'+str(i+1), faces=sbar_set)

    mdl.SurfaceToSurfaceContactStd(adjustMethod=NONE,
        clearanceRegion=None, createStepName='Initial', datumAxis=None,
        initialClearance=OMIT, interactionProperty='Conc-trsbar-contact-prop',
        master=Region(side1Faces=mdl.rootAssembly.sets['trsbar_face-concslab-'+str(i+1)].faces),
        slave=Region(side1Faces=mdl.rootAssembly.sets['trsbar_face-sbar-'+str(i+1)].faces),
        name='Conc-trsbar-contact'+str(i+1), sliding=SMALL, thickness=ON)


##################################################
##### CONNECT CONCRETE TO SUBBASE
##################################################
concBottomFace = None
for instance in [i for i in mdl.rootAssembly.instances.keys() if i.startswith('concslab')]:
    _tmp = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(
        xMin=0, xMax=model_width*num_pavements,
        zMin=0, zMax=model_depth,
        yMin=0, yMax=0)
    concBottomFace = array_append(concBottomFace, _tmp)
subbaseTopFace = mdl.rootAssembly.instances['subbase'].faces.getByBoundingBox(
    xMin=0, xMax=model_width*num_pavements,
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

################################################################################
################################################################################
################################################################################
# Surpressing things to combine both model
#
# mdl.steps['Static-thermal'].suppress()
#
# for k in mdl.interactions.keys():
#     mdl.interactions[k].suppress()
