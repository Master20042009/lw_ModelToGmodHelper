import bpy
import os

class RELINKER_OT_RelinkTextures(bpy.types.Operator):
    bl_idname = "relinker.relink_textures"
    bl_label = "Relinker les textures"

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'WARNING'}, "Aucun objet sélectionné.")
            return {'CANCELLED'}

        directory = context.scene.relinker_props.folder_path
        if not directory or not os.path.exists(directory):
            self.report({'WARNING'}, "Dossier invalide.")
            return {'CANCELLED'}

        count = 0
        for slot in obj.material_slots:
            material = slot.material
            if material and material.use_nodes:
                for node in material.node_tree.nodes:
                    if node.type == 'TEX_IMAGE' and node.image:
                        img_name = node.image.name
                        if not node.image.filepath or not os.path.exists(bpy.path.abspath(node.image.filepath)):
                            for root, _, files in os.walk(directory):
                                for file in files:
                                    if file.lower() == img_name.lower():
                                        node.image.filepath = os.path.join(root, file)
                                        try:
                                            node.image.reload()
                                            count += 1
                                        except:
                                            pass
        self.report({'INFO'}, f"{count} textures relinkées.")
        return {'FINISHED'}
