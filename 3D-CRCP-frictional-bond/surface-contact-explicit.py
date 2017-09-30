mdl.ExplicitDynamicsStep(name='Explicit-Dynamic-Wheel', previous='Initial')

###########
## Define the explicit contact PROPERTIES and interaction to be used for every sbar surface pair
mdl.ContactProperty('explicit_ContProp')
mdl.interactionProperties['explicit_ContProp'].TangentialBehavior(
    formulation=FRICTIONLESS)
mdl.ContactExp(createStepName='Initial', name=
'explicit_Cont')
###########
mdl.interactions['explicit_Cont'].contactPropertyAssignments.appendInStep(
    assignments=((GLOBAL, SELF, 'explicit_ContProp'), ), stepName=
    'Initial')

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
####
mdl.ContactProperty('ConcSubbase-contact-prop')
mdl.interactionProperties['ConcSubbase-contact-prop'].CohesiveBehavior(
    defaultPenalties=OFF, table=((32027.1956, 236.4211, 236.4211), ))
##########
## face sets for frictional contact

## For long-sbar
instances = [k for k in mdl.rootAssembly.instances.keys() if k.startswith('losbar')]
instances.append('concslab')
for i, z_ori in enumerate(model_sbar_location_generator(model_depth, losbar_spacing)):
    conc_surf = None
    sbar_surf = None
    for instance in instances:
        faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(
            yMin=rebar_height-losbar_diameter, yMax=rebar_height+losbar_diameter,
            zMin=z_ori-trsbar_diameter, zMax=z_ori+trsbar_diameter,
            xMin=0, xMax=model_width
            )
        if len(faces) > 0:
            surf_name = 'losbar_face-'+instance+'-'+str(i+1)
            mdl.rootAssembly.Surface(name=surf_name, side1Faces=
                faces)
            if instance == 'concslab':
                conc_surf = surf_name
            else:
                sbar_surf = surf_name
    if conc_surf is None or sbar_surf is None:
        raise AbaqusException("ERROR: sbar surface set not found")

    ##########
    mdl.interactions['explicit_Cont'].includedPairs.setValuesInStep(
        addPairs=((mdl.rootAssembly.surfaces[conc_surf],
        mdl.rootAssembly.surfaces[sbar_surf]), ), stepName=
        'Initial', useAllstar=OFF)
    mdl.interactions['explicit_Cont'].contactPropertyAssignments.appendInStep(
        assignments=((
        mdl.rootAssembly.surfaces[conc_surf],
        mdl.rootAssembly.surfaces[sbar_surf],
        'Conc-losbar-contact-prop'), ), stepName='Initial')
    mdl.interactions['explicit_Cont'].masterSlaveAssignments.appendInStep(
        assignments=((
        mdl.rootAssembly.surfaces[sbar_surf],
        mdl.rootAssembly.surfaces[conc_surf],
        SLAVE), ),
        stepName='Initial')



## For tran-sbar
instances = [k for k in mdl.rootAssembly.instances.keys() if k.startswith('trsbar')]
instances.append('concslab')
for i, x_ori in enumerate(model_sbar_location_generator(model_width, trsbar_spacing)):
    conc_surf = None
    sbar_surf = None
    for instance in instances:
        faces = mdl.rootAssembly.instances[instance].faces.getByBoundingBox(
            yMin=rebar_height-trsbar_diameter, yMax=rebar_height+trsbar_diameter,
            xMin=x_ori-trsbar_diameter, xMax=x_ori+trsbar_diameter,
            zMin=0, zMax=model_depth
            )
        if len(faces) > 0:
            surf_name = 'losbar_face-'+instance+'-'+str(i+1)
            mdl.rootAssembly.Surface(name=surf_name, side1Faces=
                faces)
            if instance == 'concslab':
                conc_surf = surf_name
            else:
                sbar_surf = surf_name
    if conc_surf is None or sbar_surf is None:
        raise AbaqusException("ERROR: sbar surface set not found")

    ######
    mdl.interactions['explicit_Cont'].includedPairs.setValuesInStep(
        addPairs=((mdl.rootAssembly.surfaces[conc_surf],
        mdl.rootAssembly.surfaces[sbar_surf]), ), stepName=
        'Initial', useAllstar=OFF)
    mdl.interactions['explicit_Cont'].contactPropertyAssignments.appendInStep(
        assignments=((
        mdl.rootAssembly.surfaces[conc_surf],
        mdl.rootAssembly.surfaces[sbar_surf],
        'Conc-trsbar-contact-prop'), ), stepName='Initial')
    mdl.interactions['explicit_Cont'].masterSlaveAssignments.appendInStep(
        assignments=((
        mdl.rootAssembly.surfaces[sbar_surf],
        mdl.rootAssembly.surfaces[conc_surf],
        SLAVE), ),
        stepName='Initial')


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

mdl.rootAssembly.Surface(name='concBottomFace', side1Faces=concBottomFace)
mdl.rootAssembly.Surface(name='subbaseTopFace', side1Faces=subbaseTopFace)

mdl.interactions['explicit_Cont'].includedPairs.setValuesInStep(
    addPairs=((mdl.rootAssembly.surfaces['subbaseTopFace'],
    mdl.rootAssembly.surfaces['concBottomFace']), ), stepName=
    'Initial', useAllstar=OFF)
mdl.interactions['explicit_Cont'].contactPropertyAssignments.appendInStep(
    assignments=((
    mdl.rootAssembly.surfaces['concBottomFace'],
    mdl.rootAssembly.surfaces['subbaseTopFace'],
    'ConcSubbase-contact-prop'), ), stepName='Initial')
mdl.interactions['explicit_Cont'].masterSlaveAssignments.appendInStep(
    assignments=((
    mdl.rootAssembly.surfaces['concBottomFace'],
    mdl.rootAssembly.surfaces['subbaseTopFace'],
    SLAVE), ),
    stepName='Initial')


################################################################################
################################################################################
################################################################################
# mdl.steps['Step-1'].setValues(massScaling=((
#     SEMI_AUTOMATIC, MODEL, THROUGHOUT_STEP, 0.0, 0.0001, BELOW_MIN, 1, 0, 0.0,
#     0.0, 0, None), ))

################################################################################
################################################################################
################################################################################
# Surpressing things to combine both model

mdl.steps['Explicit-Dynamic-Wheel'].suppress()

for k in mdl.interactions.keys():
    mdl.interactions[k].suppress()
