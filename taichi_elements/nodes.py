import bpy


class BaseNode(bpy.types.Node):
    @classmethod
    def poll(cls, node_tree):
        return node_tree.bl_idname == 'elements_node_tree'


class ElementsMpmSolverNode(BaseNode):
    bl_idname = 'elements_mpm_solver_node'
    bl_label = 'MPM Solver'

    def init(self, context):
        self.width = 175.0
        self.outputs.new(
            'elements_solver_socket',
            'MPM Solver'
        )
        resolution = self.inputs.new(
            'elements_integer_socket',
            'Resolution'
        )
        resolution.text = 'Resolution'
        resolution.value = 128


class ElementsMaterialNode(BaseNode):
    bl_idname = 'elements_material_node'
    bl_label = 'Material'

    def init(self, context):
        self.outputs.new(
            'elements_material_socket',
            'Value'
        )


class ElementsIntegerNode(BaseNode):
    bl_idname = 'elements_integer_node'
    bl_label = 'Integer'

    def init(self, context):
        integer_socket = self.outputs.new(
            'elements_integer_socket',
            'Integer'
        )
        integer_socket.text = ''


class ElementsFloatNode(BaseNode):
    bl_idname = 'elements_float_node'
    bl_label = 'Float'

    def init(self, context):
        float_socket = self.outputs.new(
            'elements_float_socket',
            'Float'
        )
        float_socket.text = ''


class ElementsEmitterNode(BaseNode):
    bl_idname = 'elements_emitter_node'
    bl_label = 'Emitter'

    def init(self, context):
        emitter_output_socket = self.outputs.new(
            'elements_struct_socket',
            'Emitter'
        )
        emitter_output_socket.text = 'Emitter'

        emit_time_socket = self.inputs.new(
            'elements_integer_socket',
            'Emit Time'
        )
        emit_time_socket.text = 'Emit Time'

        source_geometry_socket = self.inputs.new(
            'elements_struct_socket',
            'Source Geometry'
        )
        source_geometry_socket.text = 'Source Geometry'

        material_socket = self.inputs.new(
            'elements_struct_socket',
            'Material'
        )
        material_socket.text = 'Material'


class ElementsSimulationHubNode(BaseNode):
    bl_idname = 'elements_simulation_hub_node'
    bl_label = 'Simulation Hub'

    def init(self, context):
        solver_socket = self.inputs.new(
            'elements_solver_socket',
            'Solver'
        )
        solver_socket.text = 'Solver'

        forces_socket = self.inputs.new(
            'elements_struct_socket',
            'Forces'
        )
        forces_socket.text = 'Forces'

        emitters_socket = self.inputs.new(
            'elements_struct_socket',
            'Emitters'
        )
        emitters_socket.text = 'Emitters'

    def draw_buttons(self, context, layout):
        layout.operator('elements.simulate_particles')


class ElementsSourceObjectNode(BaseNode):
    bl_idname = 'elements_source_object_node'
    bl_label = 'Source Object'

    object_name: bpy.props.StringProperty()

    def init(self, context):
        object_output_socket = self.outputs.new(
            'elements_struct_socket',
            'Object'
        )
        object_output_socket.text = 'Source Geometry'

    def draw_buttons(self, context, layout):
        layout.prop_search(self, 'object_name', bpy.data, 'objects', text='')


class ElementsGravityNode(BaseNode):
    bl_idname = 'elements_gravity_node'
    bl_label = 'Gravity'

    def init(self, context):
        self.width = 175.0

        gravity_output = self.outputs.new(
            'elements_struct_socket',
            'Gravity'
        )
        gravity_output.text = 'Gravity Force'
        speed_socket = self.inputs.new(
            'elements_float_socket',
            'Speed'
        )
        speed_socket.text = 'Speed'
        speed_socket.value = 9.8

        direction_socket = self.inputs.new(
            'elements_3d_vector_float_socket',
            'Direction'
        )
        direction_socket.text = 'Direction'
        direction_socket.value = (0.0, 0.0, -1.0)


class ElementsSetNode(BaseNode):
    bl_idname = 'elements_set_node'
    bl_label = 'Set'

    def add_linked_socket(self, links):
        empty_input_socket = self.inputs.new(
            'elements_struct_socket',
            'Element'
        )
        empty_input_socket.text = 'Element'
        node_tree = bpy.context.space_data.node_tree
        if len(links):
            node_tree.links.new(links[0].from_socket, empty_input_socket)

    def add_empty_socket(self):
        empty_input_socket = self.inputs.new(
            'elements_add_socket',
            'Add'
        )

    def init(self, context):
        self.add_empty_socket()
        output_socket = self.outputs.new(
            'elements_struct_socket',
            'Set Elements'
        )
        output_socket.text = 'Elements'

    def update(self):
        for input_socket in self.inputs:
            if input_socket.bl_idname == 'elements_struct_socket':
                if not input_socket.is_linked:
                    self.inputs.remove(input_socket)
        for input_socket in self.inputs:
            if input_socket.bl_idname == 'elements_add_socket':
                if input_socket.is_linked:
                    self.add_linked_socket(input_socket.links)
                    self.inputs.remove(input_socket)
                    self.add_empty_socket()


node_classes = [
    ElementsMpmSolverNode,
    ElementsMaterialNode,
    ElementsEmitterNode,
    ElementsSimulationHubNode,
    ElementsSourceObjectNode,
    ElementsIntegerNode,
    ElementsFloatNode,
    ElementsGravityNode,
    ElementsSetNode
]


def register():
    for node_class in node_classes:
        bpy.utils.register_class(node_class)


def unregister():
    for node_class in reversed(node_classes):
        bpy.utils.unregister_class(node_class)
