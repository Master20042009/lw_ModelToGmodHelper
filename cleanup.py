import bpy

class RELINKER_OT_MergeByDistance(bpy.types.Operator):
    bl_idname = "relinker.merge_by_distance"
    bl_label = "Fusionner par distance"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.0001)
        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, "Fusion par distance effectuée.")
        return {'FINISHED'}


class RELINKER_OT_ClearCustomNormals(bpy.types.Operator):
    bl_idname = "relinker.clear_custom_normals"
    bl_label = "Clear Custom Split Normals"

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "Sélectionnez un mesh.")
            return {'CANCELLED'}

        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        try:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
        except:
            bpy.ops.object.mode_set(mode='OBJECT')
            self.report({'ERROR'}, "Impossible de nettoyer les normales.")
            return {'CANCELLED'}
        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Custom Split Normals nettoyés.")
        return {'FINISHED'}
