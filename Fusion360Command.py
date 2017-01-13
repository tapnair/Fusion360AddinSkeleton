import adsk.core, adsk.fusion, traceback

from .Fusion360CommandBase import Fusion360CommandBase

# The following will define a command in a tool bar panel
class Fusion360Command(Fusion360CommandBase):
    
    # Runs when Fusion command would generate a preview after all inputs are valid or changed
    def on_preview(self, command, command_inputs, args, input_values):
        pass
    
    # Runs when the command is destroyed.  Sometimes useful for cleanup after the fact
    def on_destroy(self, command, command_inputs, reason, input_values):    
        pass
    
    # Runs when when any input in the command dialog is changed
    def on_inputChanged(self, command, command_inputs, changed_input, input_values):
        pass
    
    # Runs when the user presses ok button
    def on_execute(self, command, command_inputs, args, input_values):
        pass
    
    # Runs when user selects your command from Fusion UI, Build UI here
    def on_create(self, command, command_inputs):
        
        # Create a few inputs in the UI
        command_inputs.addValueInput('valueInput_', '***Sample***Value', 'cm', adsk.core.ValueInput.createByString('0.0 cm'))
        command_inputs.addBoolValueInput('boolvalueInput_', '***Sample***Checked', True)
        command_inputs.addStringValueInput('stringValueInput_', '***Sample***String Value', 'Default value')
        command_inputs.addSelectionInput('selectionInput', '***Sample***Selection', 'Select one')
        
        
        