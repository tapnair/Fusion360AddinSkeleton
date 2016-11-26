# Importing sample Fusion Command
# Could import multiple Command definitions here
from .Fusion360Command import Fusion360Command

commands = []
command_defs =[]

#### Define parameters for 1st command #####
cmd = {
        'commandName' : 'Demo Command 1',
        'commandDescription' : 'Demo Command 1 Description',
        'commandResources' : './resources',
        'cmdId' : 'cmdID_Demo_1',
        'workspace' : 'FusionSolidEnvironment',
        'toolbarPanelID' : 'SolidScriptsAddinsPanel',
        'class' : Fusion360Command
}
command_defs.append(cmd)

#### Define parameters for 2nd command #####
cmd = {
        'commandName' : 'Demo Command 2',
        'commandDescription' : 'Demo Command 2 Description',
        'commandResources' : './resources',
        'cmdId' : 'cmdID_Demo_2',
        'workspace' : 'FusionSurfaceEnvironment',
        'toolbarPanelID' : 'SurfaceCreatePanel',
        'class' : Fusion360Command
}
command_defs.append(cmd)

# Set to True to display various useful messages when debugging your app
debug = False


#### Don't change anything below here:
for cmd_def in command_defs:
    command = cmd_def['class'](cmd_def['commandName'], cmd_def['commandDescription'], cmd_def['commandResources'], cmd_def['cmdId'], cmd_def['workspace'], cmd_def['toolbarPanelID'], debug)
    commands.append(command)

def run(context):
    for command in commands:
        command.onRun()


def stop(context):
    for command in commands:
        command.onStop()
