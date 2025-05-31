import bpy

class RELINKER_OT_RemoveUnusedMaterials(bpy.types.Operator):
    bl_idname = "lw_pannel.remove_unused_materials"
    bl_label = "Retirer matériaux non utilisés"
    bl_description = "Supprime les matériaux non assignés à des faces sur l'objet sélectionné"

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "Sélectionnez un mesh.")
            return {'CANCELLED'}

        mesh = obj.data
        used_slots = set(poly.material_index for poly in mesh.polygons)
        removed = 0

        for i in reversed(range(len(obj.material_slots))):
            if i not in used_slots:
                obj.active_material_index = i
                bpy.ops.object.material_slot_remove()
                removed += 1

        self.report({'INFO'}, f"{removed} matériaux non utilisés retirés.")
        return {'FINISHED'}


# class RELINKER_OT_SelectObjectsWithSameMaterials(bpy.types.Operator):
#     bl_idname = "lw_pannel.select_objects_with_same_materials"
#     bl_label = "Sélectionner objets avec mêmes matériaux"
#     bl_description = "Sélectionne tous les objets qui partagent au moins un matériau avec l'objet actif"

#     def execute(self, context):
#         obj = context.active_object
#         if not obj or obj.type != 'MESH':
#             self.report({'WARNING'}, "Sélectionnez un mesh.")
#             return {'CANCELLED'}

#         mats = {slot.material for slot in obj.material_slots if slot.material}
#         if not mats:
#             self.report({'WARNING'}, "Aucun matériau trouvé sur l'objet actif.")
#             return {'CANCELLED'}

#         count = 0
#         # Utilise uniquement les objets visibles dans la View Layer courante
#         for o in context.view_layer.objects:
#             if o.type == 'MESH' and o != obj:
#                 if any((slot.material in mats) for slot in o.material_slots if slot.material):
#                     o.select_set(True)
#                     count += 1
#                 else:
#                     o.select_set(False)
#         obj.select_set(True)
#         context.view_layer.objects.active = obj
#         self.report({'INFO'}, f"{count} objets sélectionnés partageant au moins un matériau.")
#         return {'FINISHED'}