# Importing sample Fusion Command
# Could import multiple Command definitions here
from .Fusion360Command import Fusion360Command

#### Define parameters for 1st command #####
commandName1 = 'Demo Command 1'
commandDescription1 = 'Demo Command 1 Description'
commandResources1 = './resources'
cmdId1 = 'cmdID_Demo_1'
myWorkspace1 = 'FusionSolidEnvironment'
myToolbarPanelID1 = 'SolidScriptsAddinsPanel'

#### Define parameters for 2nd command #####
commandName2 = 'Demo Command 2'
commandDescription2 = 'Demo Command 1 Description'
commandResources2 = './resources'
cmdId2 = 'cmdID_Demo_2'
myWorkspace2 = 'FusionSurfaceEnvironment'
myToolbarPanelID2 = 'SurfaceCreatePanel'

# Set to True to display various useful messages when debugging your app
debug = False

# Creates the commands for use in the Fusion 360 UI
newCommand1 = Fusion360Command(commandName1, commandDescription1, commandResources1, cmdId1, myWorkspace1, myToolbarPanelID1, debug)
newCommand2 = Fusion360Command(commandName2, commandDescription2, commandResources2, cmdId2, myWorkspace2, myToolbarPanelID2, debug)


def run(context):
    newCommand1.onRun()
    newCommand2.onRun()
def stop(context):
    newCommand1.onStop()
    newCommand2.onStop()
    
