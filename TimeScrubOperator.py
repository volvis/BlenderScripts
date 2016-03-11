import bpy
from mathutils import Vector
from bpy.props import FloatVectorProperty


class TimeScrubOperator(bpy.types.Operator):
    """Translate the view using mouse events"""
    bl_idname = "view3d.time_scrub_operator"
    bl_label = "Time Scrub Operator"

    

    def execute(self, context):
        context.scene.frame_set(self._initial_time - (self.offset*0.2))
        pass

    def modal(self, context, event):
        v3d = context.space_data
        rv3d = v3d.region_3d

        if event.value == 'RELEASE':
            context.area.header_text_set()
            return {'CANCELLED'}
        if event.type == 'MOUSEMOVE':
            self.offset = self._initial_mouse_x - event.mouse_x
            self.execute(context)

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.area.header_text_set()
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):

        if context.space_data.type == 'VIEW_3D':
            self._initial_mouse_x = event.mouse_x
            self._initial_time = context.scene.frame_current
            context.window_manager.modal_handler_add(self)
            print("invokin")
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(TimeScrubOperator)


def unregister():
    bpy.utils.unregister_class(TimeScrubOperator)


if __name__ == "__main__":
    register()
