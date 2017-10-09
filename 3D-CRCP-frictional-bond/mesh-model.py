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

# mdl.parts['Wheel'].seedPart(deviationFactor=0.1,
#     minSizeFactor=0.1, size=25.0)

## mesh subbase
mdl.parts['subbasePart'].seedPart(deviationFactor=0.1,
    minSizeFactor=0.1, size=381)


print('> Generating Mesh...')
for part in mdl.parts.keys():
    mdl.parts[part].generateMesh()
