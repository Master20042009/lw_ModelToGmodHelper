import bpy

class RELINKER_OT_CreateLODs(bpy.types.Operator):
    bl_idname = "lw_pannel.create_lods"
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

        # Récupérer la collection d'origine de l'objet
        original_collection = None
        for col in bpy.data.collections:
            if obj.name in col.objects:
                original_collection = col
                break
        collection_name = original_collection.name if original_collection else "Scene"

        # Dictionnaire pour stocker les collections LOD
        lod_collections = {}

        for lod_name, ratio in lods.items():
            # Créer ou récupérer la collection pour ce LOD
            lod_collection_name = f"{collection_name}_{lod_name}"
            if lod_collection_name not in lod_collections:
                if lod_collection_name not in bpy.data.collections:
                    lod_collection = bpy.data.collections.new(lod_collection_name)
                    bpy.context.scene.collection.children.link(lod_collection)
                else:
                    lod_collection = bpy.data.collections[lod_collection_name]
                lod_collections[lod_collection_name] = lod_collection
            else:
                lod_collection = lod_collections[lod_collection_name]

            # Créer le LOD
            copy = obj.copy()
            copy.data = obj.data.copy()
            copy.name = f"{obj.name}_{lod_name}"
            bpy.context.view_layer.objects.active = copy

            mod = copy.modifiers.new(name="Decimate", type='DECIMATE')
            mod.ratio = ratio
            bpy.ops.object.modifier_apply(modifier=mod.name)

            # Retirer le LOD de toutes les collections existantes
            for col in copy.users_collection:
                col.objects.unlink(copy)

            # Ajouter le LOD à la collection correspondante
            lod_collection.objects.link(copy)

        self.report({'INFO'}, "LODs créés dans des collections séparées.")
        return {'FINISHED'}
