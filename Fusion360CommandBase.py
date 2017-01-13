import traceback

import adsk.core
import adsk.fusion

handlers = [] 


# Returns a dictionary for all inputs. Very useful for creating quick Fusion 360 Add-ins
def get_inputs(command_inputs):

    value_types = [adsk.core.BoolValueCommandInput.classType(), adsk.core.DistanceValueCommandInput.classType(),
                   adsk.core.FloatSliderCommandInput.classType(), adsk.core.FloatSpinnerCommandInput.classType(),
                   adsk.core.IntegerSliderCommandInput.classType(), adsk.core.IntegerSpinnerCommandInput.classType(),
                   adsk.core.ValueCommandInput.classType(), adsk.core.SliderCommandInput.classType()]

    list_types = [adsk.core.ButtonRowCommandInput.classType(), adsk.core.DropDownCommandInput.classType(),
                  adsk.core.RadioButtonGroupCommandInput.classType()]

    selection_types = [adsk.core.SelectionCommandInput.classType()]

    input_values = {}
    input_values.clear()

    for command_input in command_inputs:

        # If the input type is in this list the value of the input is returned
        if command_input.objectType in value_types:
            input_values[command_input.id] = command_input.value
            input_values[command_input.id + '_input'] = command_input

        # If the input type is in this list the name of the selected list item is returned
        elif command_input.objectType in list_types:
            input_values[command_input.id] = command_input.selectedItem.name
            input_values[command_input.id + '_input'] = command_input

        # If the input type is a selection an array of entities is returned
        elif command_input.objectType in selection_types:
            if command_input.selectionCount > 0:
                selections = []
                for i in range(0, command_input.selectionCount):
                    selections.append(command_input.selection(i).entity)

                input_values[command_input.id] = selections
                input_values[command_input.id + '_input'] = command_input

        else:
            input_values[command_input.id] = command_input.name
            input_values[command_input.id + '_input'] = command_input

    return input_values

# Removes the command control and definition 
def clean_up_nav_drop_down_command(cmd_id, dc_cmd_id):
    
    obj_array_nav = []
    drop_down_control = command_control_by_id_in_nav_bar(dc_cmd_id)
    command_control_nav = command_control_by_id_in_drop_down(cmd_id, drop_down_control)
        
    if command_control_nav:
        obj_array_nav.append(command_control_nav)
    
    command_definition_nav = command_definition_by_id(cmd_id)
    if command_definition_nav:
        obj_array_nav.append(command_definition_nav)
        
    for obj in obj_array_nav:
        destroy_object(obj)


# Finds command definition in active UI
def command_definition_by_id(cmd_id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    
    if not cmd_id:
        ui.messageBox('Command Definition:  ' + cmd_id + '  is not specified')
        return None
    command_definitions = ui.commandDefinitions
    command_definition = command_definitions.itemById(cmd_id)
    return command_definition


# Find command control by id in nav bar
def command_control_by_id_in_nav_bar(cmd_id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    
    if not cmd_id:
        ui.messageBox('Command Control:  ' + cmd_id + '  is not specified')
        return None
    
    toolbars_ = ui.toolbars
    nav_toolbar = toolbars_.itemById('NavToolbar')
    nav_toolbar_controls = nav_toolbar.controls
    cmd_control = nav_toolbar_controls.itemById(cmd_id)
    
    if cmd_control is not None:
        return cmd_control


# Get a command control in a Nav Bar Drop Down
def command_control_by_id_in_drop_down(cmd_id, drop_down_control):
    cmd_control = drop_down_control.controls.itemById(cmd_id)
    
    if cmd_control is not None:
        return cmd_control


# Destroys a given object
def destroy_object(obj_to_be_deleted):
    app = adsk.core.Application.get()
    ui = app.userInterface
    
    if ui and obj_to_be_deleted:
        if obj_to_be_deleted.isValid:
            obj_to_be_deleted.deleteMe()
        else:
            ui.messageBox(obj_to_be_deleted.id + 'is not a valid object')


# Returns the id of a Toolbar Panel in the given Workspace
def toolbar_panel_by_id_in_workspace(workspace_id, toolbar_panel_id):
    app = adsk.core.Application.get()
    ui = app.userInterface
        
    all_workspaces = ui.workspaces
    this_workspace = all_workspaces.itemById(workspace_id)
    all_toolbar_panels = this_workspace.toolbarPanels
    toolbar_panel = all_toolbar_panels.itemById(toolbar_panel_id)
    
    return toolbar_panel


# Returns the Command Control from the given panel
def command_control_by_id_in_panel(cmd_id, toolbar_panel):
    
    app = adsk.core.Application.get()
    ui = app.userInterface
    
    if not cmd_id:
        ui.messageBox('Command Control:  ' + cmd_id + '  is not specified')
        return None
    
    cmd_control = toolbar_panel.controls.itemById(cmd_id)
    
    if cmd_control is not None:
        return cmd_control


# Base Class for creating Fusion 360 Commands
class Fusion360CommandBase:
    
    def __init__(self, cmd_def, debug):

        self.commandName = cmd_def.get('commandName', 'Default Command Name')
        self.commandDescription = cmd_def.get('commandDescription', 'Default Command Description')
        self.commandResources = cmd_def.get('commandResources', './resources')
        self.cmdId = cmd_def.get('cmdId', 'Default Command ID')
        self.workspace = cmd_def.get('workspace', 'FusionSolidEnvironment')
        self.toolbarPanelID = cmd_def.get('toolbarPanelID', 'SolidScriptsAddinsPanel')
        self.DC_CmdId = cmd_def.get('DC_CmdId', 'Default_DC_CmdId')
        self.DC_Resources = cmd_def.get('DC_Resources', './resources')
        self.command_in_nav_bar = cmd_def.get('command_in_nav_bar', False)
        self.debug = debug

        # global set of event handlers to keep them referenced for the duration of the command
        self.handlers = []
        
        try:
            self.app = adsk.core.Application.get()
            self.ui = self.app.userInterface

        except RuntimeError:
            if self.ui:
                self.ui.messageBox('Could not get app or ui: {}'.format(traceback.format_exc()))
    
    def on_preview(self, command, inputs, args, input_values):
        pass 

    def on_destroy(self, command, inputs, reason, input_values):
        pass   

    def on_input_changed(self, command_, command_inputs, changed_input, input_values):
        pass

    def on_execute(self, command, inputs, args, input_values):
        pass

    def on_create(self, command, inputs):
        pass

    # TODO Continue variable cleanup from here
    def on_run(self):
        global handlers

        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            command_definitions = ui.commandDefinitions
            
            # Add command to drop down in nav bar
            if self.command_in_nav_bar:
                
                toolbars_ = ui.toolbars
                nav_bar = toolbars_.itemById('NavToolbar')
                toolbar_controls_nav = nav_bar.controls
                
                drop_control = toolbar_controls_nav.itemById(self.DC_CmdId) 
                
                if not drop_control:             
                    drop_control = toolbar_controls_nav.addDropDown(self.DC_CmdId, self.DC_Resources, self.DC_CmdId) 
                
                controls_to_add_to = drop_control.controls
                
                new_control = toolbar_controls_nav.itemById(self.cmdId)
            
            # Add command to workspace panel
            else:
                toolbar_panel = toolbar_panel_by_id_in_workspace(self.workspace, self.toolbarPanelID)
                controls_to_add_to = toolbar_panel.controls               
                new_control = controls_to_add_to.itemById(self.cmdId)
            
            # If control does not exist, create it
            if not new_control:
                command_definition = command_definitions.itemById(self.cmdId)
                if not command_definition:
                    command_definition = command_definitions.addButtonDefinition(self.cmdId, 
                                                                                 self.commandName, 
                                                                                 self.commandDescription, 
                                                                                 self.commandResources)
                
                on_command_created_handler = CommandCreatedEventHandler(self)
                command_definition.commandCreated.add(on_command_created_handler)
                handlers.append(on_command_created_handler)
                
                new_control = controls_to_add_to.addCommand(command_definition)
                new_control.isVisible = True
        
        except:
            if ui:
                ui.messageBox('AddIn Start Failed: {}'.format(traceback.format_exc()))

    def on_stop(self):
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface

            # Remove command from nav bar
            if self.command_in_nav_bar:
                drop_down_control = command_control_by_id_in_nav_bar(self.DC_CmdId)
                command_control_nav = command_control_by_id_in_drop_down(self.cmdId, drop_down_control)
                command_definition_nav = command_definition_by_id(self.cmdId)
                destroy_object(command_control_nav)
                destroy_object(command_definition_nav)
                
                if drop_down_control.controls.count == 0:
                    command_definition_drop_down = command_definition_by_id(self.DC_CmdId)
                    destroy_object(drop_down_control)
                    destroy_object(command_definition_drop_down)
            
            # Remove command from workspace panel
            else:
                toolbar_panel = toolbar_panel_by_id_in_workspace(self.workspace, self.toolbarPanelID)
                command_control_panel = command_control_by_id_in_panel(self.cmdId, toolbar_panel)
                command_definition_panel = command_definition_by_id(self.cmdId)
                destroy_object(command_control_panel)
                destroy_object(command_definition_panel)

        except:
            if ui:
                ui.messageBox('AddIn Stop Failed: {}'.format(traceback.format_exc()))


class ExecutePreviewHandler(adsk.core.CommandEventHandler):
    def __init__(self, cmd_object):
        super().__init__()
        self.cmd_object_ = cmd_object
        self.args = None

    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            command_ = args.firingEvent.sender
            command_inputs = command_.commandInputs
            if self.cmd_object_.debug:
                ui.messageBox('***Debug *** Preview: {} execute preview event triggered'.
                              format(command_.parentCommandDefinition.id))
            input_values = get_inputs(command_inputs)
            self.cmd_object_.on_preview(command_, command_inputs, args, input_values)

        except:
            if ui:
                ui.messageBox('Input changed event failed: {}'.format(traceback.format_exc()))


class DestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self, cmd_object):
        super().__init__()
        self.cmd_object_ = cmd_object

    def notify(self, args):
        # Code to react to the event.
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            command_ = args.firingEvent.sender
            command_inputs = command_.commandInputs
            reason_ = args.terminationReason

            if self.cmd_object_.debug:
                ui.messageBox('***Debug ***Command: {} destroyed'.format(command_.parentCommandDefinition.id))
                ui.messageBox("***Debug ***Reason for termination= " + str(reason_))

            input_values = get_inputs(command_inputs)

            self.cmd_object_.on_destroy(command_, command_inputs, reason_, input_values)
            
        except:
            if ui:
                ui.messageBox('Input changed event failed: {}'.format(traceback.format_exc()))


class InputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self, cmd_object):
        super().__init__()
        self.cmd_object_ = cmd_object

    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            command_ = args.firingEvent.sender
            command_inputs = command_.commandInputs
            changed_input = args.input

            if self.cmd_object_.debug:
                ui.messageBox('***Debug ***Input: {} changed event triggered'.format(command_.parentCommandDefinition.id))
                ui.messageBox('***Debug ***The Input: {} was the command'.format(changedInput_.id))

            input_values = get_inputs(command_inputs)

            self.cmd_object_.on_input_changed(command_, command_inputs, changed_input, input_values)

        except:
            if ui:
                ui.messageBox('Input changed event failed: {}'.format(traceback.format_exc()))


class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, cmd_object):
        super().__init__()
        self.cmd_object_ = cmd_object

    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            command_ = args.firingEvent.sender
            command_inputs = command_.commandInputs

            if self.cmd_object_.debug:
                ui.messageBox('***Debug ***command: {} executed successfully'.format(command_.parentCommandDefinition.id))

            input_values = get_inputs(command_inputs)

            self.cmd_object_.on_execute(command_, command_inputs, args, input_values)
            
        except:
            if ui:
                ui.messageBox('command executed failed: {}'.format(traceback.format_exc()))


class CommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, cmd_object):
        super().__init__()
        self.cmd_object_ = cmd_object
    
    def notify(self, args):
        try:
            global handlers
            
            app = adsk.core.Application.get()
            ui = app.userInterface
            command_ = args.command
            inputs_ = command_.commandInputs
            
            on_execute_handler = CommandExecuteHandler(self.cmd_object_)
            command_.execute.add(on_execute_handler)
            handlers.append(on_execute_handler)
            
            on_input_changed_handler = InputChangedHandler(self.cmd_object_)
            command_.inputChanged.add(on_input_changed_handler)
            handlers.append(on_input_changed_handler)
            
            on_destroy_handler = DestroyHandler(self.cmd_object_)
            command_.destroy.add(on_destroy_handler)
            handlers.append(on_destroy_handler)
            
            on_execute_preview_handler = ExecutePreviewHandler(self.cmd_object_)
            command_.executePreview.add(on_execute_preview_handler)
            handlers.append(on_execute_preview_handler)
            
            if self.cmd_object_.debug:
                ui.messageBox('***Debug ***Panel command created successfully')
            
            self.cmd_object_.on_create(command_, inputs_)

        except:
                if ui:
                    ui.messageBox('Panel command created failed: {}'.format(traceback.format_exc()))