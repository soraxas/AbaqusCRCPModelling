# IMPORTANT please specific the directory of the script folder
SCRIPT_PATH_DIRECTORY = r"C:\Users\Oscar\GIT\3D-CRCP-connector-sbar/"
# For example, "C:\Users\Oscar\GIT/"
##############################################################

def main():
    global OPT_build, OPT_run, OPT_plot, OPT_save_plot

    if OPT_build:
        global DELETE_EXISTING_MODEL
        DELETE_EXISTING_MODEL = True
        run('build-model.py')

    if OPT_run:
        run('run-analysis.py')

    if OPT_plot:
        run('plot-model.py')

    if OPT_save_plot:
        run('save-plot-to-file.py')


################################################################################
################           DEFINING THE SCRIPT LOGICS           ################
################################################################################
def pre_setup():
    # test the existance of this file to vertify the directory variable
    import os.path
    if not os.path.isfile(SCRIPT_PATH_DIRECTORY+'main.py'):
        import win32api
        win32api.MessageBox(None, "ERROR: Your variable for 'SCRIPT_PATH_DIRECTORY' is invalid, edit it in 'main.py'.\n\nThe files within '"+SCRIPT_PATH_DIRECTORY+"' not found.", "Abaqus Script",0)
        raise SystemExit
    run('imports.py')
    run('model-settings.py')
    global OPT_build, OPT_run, OPT_plot, OPT_save_plot
    OPT_build = True
    OPT_run = True
    OPT_plot = False
    OPT_save_plot = False
    if not confirm("""Run script with DEFAULT settings?\n
(Default: Delete existing model, Build the model, Submit job, Run analysis.)"""):
        OPT_build = confirm("""Delete and build a new model?""")
        OPT_run = confirm("""Submit the job and run analysis afterwards?""")
        OPT_plot = confirm("""Plot the XY Data?\n\n(NOTE: You should run this in the 'Visualization' screen with the desire variable selected)""")
        OPT_save_plot = confirm("""Save the XY Data in the current directory?\n\n(NOTE: You should run this in the 'Visualization' screen with the desire variable selected)""")

def run(s):
    execfile(SCRIPT_PATH_DIRECTORY+s, __main__.__dict__)
def confirm(s):
    import win32api
    result = win32api.MessageBox(None, s, "Abaqus Script",3)
    if result == 6:
        return True
    elif result == 7:
        return False
    else:
        raise SystemExit
##############################################################

try:
    print(">-- Script Started --<")
    pre_setup()
    main()
except SystemExit:
    pass
finally:
    print(">-- Script Exited --<")
