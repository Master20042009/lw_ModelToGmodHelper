import bpy

class RELINKER_OT_IncreaseQuality(bpy.types.Operator):
    bl_idname = "lw_pannel.increase_quality"
    bl_label = "Améliorer la qualité"
    bl_description = "Ajuste le niveau de subdivision selon le slider"

    def execute(self, context):
        obj = context.active_object
        quality = context.scene.relinker_props.quality_level

        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "Sélectionnez un mesh.")
            return {'CANCELLED'}

        sub = None
        for mod in obj.modifiers:
            if mod.type == 'SUBSURF':
                sub = mod
                break

        if quality == 0:
            if sub:
                obj.modifiers.remove(sub)
                self.report({'INFO'}, "Modificateur Subdivision supprimé (qualité 0).")
            else:
                self.report({'INFO'}, "Qualité = 0 : aucun modificateur à supprimer.")
            return {'FINISHED'}

        if not sub:
            sub = obj.modifiers.new(name="Subsurf", type='SUBSURF')

        sub.levels = quality
        sub.render_levels = quality

        self.report({'INFO'}, f"Subdivision mise à jour au niveau {quality}.")
        return {'FINISHED'}


class RELINKER_OT_ApplyQuality(bpy.types.Operator):
    bl_idname = "lw_pannel.apply_quality"
    bl_label = "Appliquer la qualité"
    bl_description = "Applique le modificateur subdivision pour rendre la qualité permanente"

    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "Sélectionnez un mesh.")
            return {'CANCELLED'}

        sub = None
        for mod in obj.modifiers:
            if mod.type == 'SUBSURF':
                sub = mod
                break

        if not sub:
            self.report({'WARNING'}, "Pas de modificateur subdivision à appliquer.")
            return {'CANCELLED'}

        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=sub.name)
        self.report({'INFO'}, "Modificateur subdivision appliqué, qualité permanente.")
        return {'FINISHED'}
