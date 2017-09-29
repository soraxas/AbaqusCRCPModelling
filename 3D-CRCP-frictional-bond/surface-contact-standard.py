mdl.StaticStep(name='Step-1', previous='Initial')

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
