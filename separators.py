import bpy

class RELINKER_OT_SeparateSelected(bpy.types.Operator):
    bl_idname = "lw_pannel.separate_selected"
    bl_label = "Séparer sélection"

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "Sélectionnez un mesh.")
            return {'CANCELLED'}
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, "Séparation par sélection effectuée.")
        return {'FINISHED'}


class RELINKER_OT_SeparateLoose(bpy.types.Operator):
    bl_idname = "lw_pannel.separate_loose"
    bl_label = "Séparer loose parts"

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "Sélectionnez un mesh.")
            return {'CANCELLED'}
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, "Séparation par loose parts effectuée.")
        return {'FINISHED'}