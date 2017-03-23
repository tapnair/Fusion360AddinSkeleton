# Fusion360AddinSkeleton
Framework to simplify the creation of Fusion 360 Addin

Documentation to come later. For now:



# Usage
Files in the Fusion360Utilities folder should not be modified.

Rename the following items to your desired addin name: 
* Fusion360AddinSkeleton.py 
* The top level folder
* Fusion360AddinSkeleton.manifest

## Step 1 
Open the newly renamed python file

The current file will create two commands in the Fusion 360 UI in the Addins Drop Down

Change the names and description strings here to your desired naming conventions

Currently each command relies on a separate file called Demo1Command.py and demo2Command.py

If you want to rename the files that define the names of the commands you must do it for each one in 3 places:

![Rename Command](./resources/rename_command.png)


## Step 2

Edit Demo1Command.py and add functionality to the desired methods.  

onCreate: Build your UI components here

onExecute: Will be executed when user selects OK in command dialog.

DemoCommand1 creates a very basic UI and then accesses the input parameters.

###Some helpful extras:

_input_values_

In the on_execute, on_preview, on_input_changed methods there is a parameter called "input_values"

This parameter is a dictionary containing the relevant values for all of the user inputs.

The key is the name of the input.

The value is dependant on the type input:
* Value type inputs will have their actual value stored (string or number depending)
* List type inputs (drop downs, etc) will have the name of the selected item as the value (string)
* Selection inputs regardless of whether they contain one or more selections will be returned as an array of the selected objects

_Note: you can still access the raw command inputs object with the "inputs" variable.  This would behave similar to any of the examples in the API documentation._



_get_app_objects_

This is a helper function that returns a dictionary of many useful fusion 360 application objects.

This is the format of the returned dictionary:
'''
app_objects = {
        'app': app,
        'design': design,
        'import_manager': import_manager,
        'ui': ui,
        'units_manager': units_manager,
        'all_occurrences': all_occurrences,
        'all_components': all_components,
        'root_comp': root_comp,
        'time_line': time_line,
        'export_manager': export_manager,
        'document': document
    }
'''

