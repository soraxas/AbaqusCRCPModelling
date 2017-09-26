print('> Saving XY plot to file')
# x0 = session.xyDataObjects['concslab@x=762.0 ; @y=0.0']
# x1 = session.xyDataObjects['concslab@x=762.0 ; @y=76.2']
# x2 = session.xyDataObjects['concslab@x=762.0 ; @y=152.4']
# x3 = session.xyDataObjects['concslab@x=762.0 ; @y=228.6']
# x4 = session.xyDataObjects['concslab@x=762.0 ; @y=304.8']
# x5 = session.xyDataObjects['concslab@z=914.4 ; @y=0.0']
# x6 = session.xyDataObjects['concslab@z=914.4 ; @y=76.2']
# x7 = session.xyDataObjects['concslab@z=914.4 ; @y=152.4']
# x8 = session.xyDataObjects['concslab@z=914.4 ; @y=228.6']
# x9 = session.xyDataObjects['concslab@z=914.4 ; @y=304.8']
filename = SCRIPT_PATH_DIRECTORY+model_name+'_XYPlot.rpt'
session.writeXYReport(fileName=filename, xyData=tuple(session.xyDataObjects.values()), appendMode=False)
print('>> Saved as "'+model_name+'_XYPlot.rpt"')
# print()
