import bpy

class RELINKER_OT_MirrorObject(bpy.types.Operator):
    bl_idname = "relinker.mirror_object"
    bl_label = "Mirror + Preview"

    def execute(self, context):
        props = context.scene.relinker_props
        obj = context.active_object

        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "Sélectionnez un mesh.")
            return {'CANCELLED'}

        mod = obj.modifiers.new(name="Mirror", type='MIRROR')
        mod.use_axis[0] = props.mirror_axis_x
        mod.use_axis[1] = props.mirror_axis_y
        mod.use_axis[2] = props.mirror_axis_z
        mod.use_bisect_axis[0] = props.mirror_axis_neg_x
        mod.use_bisect_axis[1] = props.mirror_axis_neg_y
        mod.use_bisect_axis[2] = props.mirror_axis_neg_z

        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
        self.report({'INFO'}, "Mirror appliqué.")
        return {'FINISHED'}
