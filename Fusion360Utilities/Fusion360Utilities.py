import adsk.core
import adsk.fusion
import adsk.cam
import traceback

from typing import Optional, List


# Class to quickly access Fusion Application Objects
class AppObjects(object):

    def __init__(self):

        self.app = adsk.core.Application.cast(adsk.core.Application.get())

        # Get import manager
        self.import_manager = self.app.importManager

        # Get User Interface
        self.ui = self.app.userInterface

        self.document = self.app.activeDocument
        self.product = self.app.activeProduct

        self._design = self.design

    @property
    def design(self) -> Optional[adsk.fusion.Design]:
        design_ = self.document.products.itemByProductType('DesignProductType')
        if design_ is not None:
            return design_
        else:
            return None

    @property
    def cam(self) -> Optional[adsk.cam.CAM]:
        cam_ = self.document.products.itemByProductType('CAMProductType')
        if cam_ is not None:
            return cam_
        else:
            return None

    @property
    def units_manager(self) -> Optional[adsk.core.UnitsManager]:
        if self.product.productType == 'DesignProductType':
            units_manager_ = self._design.fusionUnitsManager
        else:
            units_manager_ = self.product.unitsManager

        if units_manager_ is not None:
            return units_manager_
        else:
            return None

    @property
    def export_manager(self) -> Optional[adsk.fusion.ExportManager]:
        if self._design is not None:
            export_manager_ = self._design.exportManager
            return export_manager_
        else:
            return None

    @property
    def root_comp(self) -> Optional[adsk.fusion.Component]:
        if self.product.productType == 'DesignProductType':
            root_comp_ = self.design.rootComponent
            return root_comp_
        else:
            return None

    @property
    def time_line(self) -> Optional[adsk.fusion.Timeline]:
        if self.product.productType == 'DesignProductType':
            if self._design.designType == adsk.fusion.DesignTypes.ParametricDesignType:
                time_line_ = self.product.timeline

                return time_line_

        return None


# Externally usable function to get all relevant application objects easily in a dictionary
# Old method, shouldn't use any more
def get_app_objects():
    app = adsk.core.Application.cast(adsk.core.Application.get())

    # Get import manager
    import_manager = app.importManager

    # Get User Interface
    ui = app.userInterface

    # Get active design
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    document = app.activeDocument

    units_manager = None
    export_manager = None
    root_comp = None
    time_line = None

    # Get top level collections
    all_occurrences = None
    all_components = None

    if design is not None:

        # Get Design specific elements
        units_manager = design.fusionUnitsManager
        export_manager = design.exportManager
        root_comp = design.rootComponent

        if design.designType == adsk.fusion.DesignTypes.ParametricDesignType:
            time_line = product.timeline

        # Get top level collections
        all_occurrences = root_comp.allOccurrences
        all_components = design.allComponents

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
    return app_objects


def start_group() -> int:
    """
    Starts a time line group
    :return: The index of the time line
    :rtype: int
    """
    # Gets necessary application objects
    app_objects = get_app_objects()

    # Start time line group
    start_index = app_objects['time_line'].markerPosition

    return start_index


def end_group(start_index: int):
    """
    Ends a time line group
    :param start_index: Time line index
    :type start_index: int
    :return:
    :rtype:
    """

    # Gets necessary application objects
    app_objects = get_app_objects()

    end_index = app_objects['time_line'].markerPosition - 1

    app_objects['time_line'].timelineGroups.add(start_index, end_index)


def import_dxf(dxf_file, component, plane) -> adsk.fusion.Sketches:
    """
    Import dxf file with one sketch per layer.
    :param dxf_file: The full path to the dxf file
    :type dxf_file: str
    :param component: The target component for the new sketch(es)
    :type component: adsk.fusion.Component
    :param plane: The plane on which to import the DXF file.
    :type plane: adsk.fusion.ConstructionPlane or adsk.fusion.BRepFace
    :return: A Collection of the created sketches
    :rtype: adsk.core.ObjectCollection
    """
    import_manager = get_app_objects()['import_manager']
    dxf_options = import_manager.createDXF2DImportOptions(dxf_file, plane)
    import_manager.importToTarget(dxf_options, component)
    sketches = dxf_options.results
    return sketches


def sketch_by_name(sketches: adsk.fusion.Sketches, name: str) -> adsk.fusion.Sketch:
    """
    Finds a sketch by name in a list of sketches
    Useful for parsing a collection of  sketches such as DXF import results.
    :param sketches: A list of sketches.
    :type sketches: adsk.fusion.Sketches
    :param name: The name of the sketch to find.
    :return: The sketch matching the name if it is found.
    :rtype: adsk.fusion.Sketch
    """
    return_sketch = None
    for sketch in sketches:
        if sketch.name == name:
            return_sketch = sketch
    return return_sketch


def extrude_all_profiles(sketch, distance, component, operation) -> adsk.fusion.ExtrudeFeature:
    """
    Create extrude features of all profiles in a sketch
    The new feature will be created in the given target component and extruded by a distance
    :param sketch: The sketch from which to get profiles
    :type sketch: adsk.fusion.Sketch
    :param distance: The distance to extrude the profiles.
    :type distance: float
    :param component: The target component for the extrude feature
    :type component: adsk.fusion.Component
    :param operation: The feature operation type from enumerator.  
    :type operation: adsk.fusion.FeatureOperations
    :return: THe new extrude feature.
    :rtype: adsk.fusion.ExtrudeFeature
    """
    profile_collection = adsk.core.ObjectCollection.create()
    for profile in sketch.profiles:
        profile_collection.add(profile)

    extrudes = component.features.extrudeFeatures
    ext_input = extrudes.createInput(profile_collection, operation)
    distance_input = adsk.core.ValueInput.createByReal(distance)
    ext_input.setDistanceExtent(False, distance_input)
    extrude_feature = extrudes.add(ext_input)
    return extrude_feature


def create_component(target_component, name) -> adsk.fusion.Occurrence:
    """
    Creates a new empty component in the target component
    :param target_component: The target component for the new component
    :type target_component:
    :param name: The name of the new component
    :type name: str
    :return: The reference to the occurrence of the newly created component.
    :rtype: adsk.fusion.Occurrence
    """
    transform = adsk.core.Matrix3D.create()
    new_occurrence = target_component.occurrences.addNewComponent(transform)
    new_occurrence.component.name = name
    return new_occurrence


# Creates rectangle pattern of bodies based on vectors
def rect_body_pattern(target_component, bodies, x_axis, y_axis, x_qty, x_distance, y_qty,
                      y_distance) -> adsk.core.ObjectCollection:

    move_feats = target_component.features.moveFeatures

    x_bodies = adsk.core.ObjectCollection.create()
    all_bodies = adsk.core.ObjectCollection.create()

    for body in bodies:
        x_bodies.add(body)
        all_bodies.add(body)

    for i in range(1, x_qty):

        # Create a collection of entities for move
        x_source = adsk.core.ObjectCollection.create()

        for body in bodies:
            new_body = body.copyToComponent(target_component)
            x_source.add(new_body)
            x_bodies.add(new_body)
            all_bodies.add(new_body)

        x_transform = adsk.core.Matrix3D.create()
        x_axis.normalize()
        x_axis.scaleBy(x_distance * i)
        x_transform.translation = x_axis

        move_input_x = move_feats.createInput(x_source, x_transform)
        move_feats.add(move_input_x)

    for j in range(1, y_qty):
        # Create a collection of entities for move
        y_source = adsk.core.ObjectCollection.create()

        for body in x_bodies:
            new_body = body.copyToComponent(target_component)
            y_source.add(new_body)
            all_bodies.add(new_body)

        y_transform = adsk.core.Matrix3D.create()
        y_axis.normalize()
        y_axis.scaleBy(y_distance * j)
        y_transform.translation = y_axis

        move_input_y = move_feats.createInput(y_source, y_transform)
        move_feats.add(move_input_y)

    return all_bodies


# Creates Combine Feature in target with all tool bodies as source
# Specify operation as: adsk.fusion.FeatureOperations
# target_body -> single body
# tool_bodies -> list of bodies
def combine_feature(target_body: adsk.fusion.BRepBody, tool_bodies: List[adsk.fusion.BRepBody],
                    operation: adsk.fusion.FeatureOperations):

    # Get Combine Features
    combine_features = target_body.parentComponent.features.combineFeatures

    # Define a collection and add all tool bodies to it
    combine_tools = adsk.core.ObjectCollection.create()

    for tool in tool_bodies:
        # todo add error checking
        combine_tools.add(tool)

    # Create Combine Feature
    combine_input = combine_features.createInput(target_body, combine_tools)
    combine_input.operation = operation
    combine_features.add(combine_input)
