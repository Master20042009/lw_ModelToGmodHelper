import bpy
import urllib.request
import os
import zipfile

class RELINKER_OT_UpdateAddon(bpy.types.Operator):
    bl_idname = "lw_pannel.update_addon"
    bl_label = "Mettre à jour l'addon"
    bl_description = "Télécharge et installe la dernière version de l'addon depuis GitHub"

    def execute(self, context):
        # Remplace cette URL par celle de ton zip GitHub
        url = "https://github.com/Master20042009/lw_ModelToGmodHelper/archive/refs/heads/main.zip"
        addon_dir = os.path.dirname(os.path.abspath(__file__))
        zip_path = os.path.join(addon_dir, "update.zip")

        try:
            self.report({'INFO'}, "Téléchargement de la mise à jour...")
            urllib.request.urlretrieve(url, zip_path)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(addon_dir)

            os.remove(zip_path)
            self.report({'INFO'}, "Addon mis à jour ! Redémarre Blender ou recharge l'addon.")
        except Exception as e:
            self.report({'ERROR'}, f"Erreur lors de la mise à jour : {e}")
            return {'CANCELLED'}

        return {'FINISHED'}