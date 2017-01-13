import adsk.core, adsk.fusion, traceback

from .Fusion360CommandBase import Fusion360CommandBase

class Fusion360Command(Fusion360CommandBase):
    
    def on_preview(self, command, command_inputs, args, input_values):
        pass
    
    def on_destroy(self, command, command_inputs, reason, input_values):    
        pass
    
    def on_inputChanged(self, command, command_inputs, changed_input, input_values):
        pass
    
    def on_execute(self, command, command_inputs, args, input_values):
        pass
    
    def on_create(self, command, command_inputs):
        
        # Create a few inputs in the UI
        command_inputs.addValueInput('valueInput_', '***Sample***Value', 'cm', adsk.core.ValueInput.createByString('0.0 cm'))
        command_inputs.addBoolValueInput('boolvalueInput_', '***Sample***Checked', True)
        command_inputs.addStringValueInput('stringValueInput_', '***Sample***String Value', 'Default value')
        command_inputs.addSelectionInput('selectionInput', '***Sample***Selection', 'Select one')
        
        
        