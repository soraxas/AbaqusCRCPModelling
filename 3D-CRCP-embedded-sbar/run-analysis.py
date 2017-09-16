import datetime
jobname = model_name+'_@_'+datetime.datetime.now().strftime("%d%m%y_%I-%M%p")
print('> Submitting analysis now with name "'+jobname+'"')
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF,
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF,
    memory=90, memoryUnits=PERCENTAGE, model=model_name, modelPrint=OFF,
    multiprocessingMode=DEFAULT, name=jobname, nodalOutputPrecision=SINGLE,
    numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', type=
    ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs[jobname].submit(consistencyChecking=OFF)
