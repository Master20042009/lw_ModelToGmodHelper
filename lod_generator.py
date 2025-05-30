import bpy

class RELINKER_OT_CreateLODs(bpy.types.Operator):
    bl_idname = "relinker.create_lods"
    bl_label = "Générer les LODs"

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "Sélectionnez un mesh.")
            return {'CANCELLED'}

        lods = {
            "lod1": 0.5, "lod2": 0.25, "lod3": 0.12,
            "lod4": 0.06, "lod5": 0.03, "lod6": 0.015,
        }

        for name, ratio in lods.items():
            copy = obj.copy()
            copy.data = obj.data.copy()
            copy.name = f"{obj.name}_{name}"
            context.collection.objects.link(copy)

            mod = copy.modifiers.new(name="Decimate", type='DECIMATE')
            mod.ratio = ratio
            bpy.context.view_layer.objects.active = copy
            bpy.ops.object.modifier_apply(modifier=mod.name)

        self.report({'INFO'}, "LODs créés.")
        return {'FINISHED'}
