import adsk.core, adsk.fusion, traceback

from .Fusion360CommandBase import Fusion360CommandBase

############# Create your Actions Here #################################################

## The following will define a command in a tool bar panel
class Fusion360Command(Fusion360CommandBase):
    
    # Runs when Fusion command would generate a preview after all inputs are valid or changed
    def onPreview(self, command, inputs):
        pass
    
    # Runs when the command is destroyed.  Sometimes useful for cleanup after the fact
    def onDestroy(self, command, inputs, reason_):    
        pass
    
    # Runs when when any input in the command dialog is changed
    def onInputChanged(self, command, inputs, changedInput):
        pass
    
    # Runs when the user presses ok button
    def onExecute(self, command, inputs):
        pass
    
    # Runs when user selects your command from Fusion UI, Build UI here
    def onCreate(self, command, inputs):
        
        # Create a few inputs in the UI
        inputs.addValueInput('valueInput_', '***Sample***Value', 'cm', adsk.core.ValueInput.createByString('0.0 cm'))
        inputs.addBoolValueInput('boolvalueInput_', '***Sample***Checked', True)
        inputs.addStringValueInput('stringValueInput_', '***Sample***String Value', 'Default value')
        inputs.addSelectionInput('selectionInput', '***Sample***Selection', 'Select one')
        
        
        