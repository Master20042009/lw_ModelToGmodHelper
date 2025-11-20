import bpy
import urllib.request
import os
import zipfile
import shutil

class RELINKER_OT_UpdateAddon(bpy.types.Operator):
    bl_idname = "lw_pannel.update_addon"
    bl_label = "Mettre à jour l'addon"
    bl_description = "Télécharge et installe la dernière version de l'addon depuis GitHub"

    def execute(self, context):
        url = "https://github.com/Master20042009/lw_ModelToGmodHelper/archive/refs/heads/main.zip"
        addon_dir = os.path.dirname(os.path.abspath(__file__))
        zip_path = os.path.join(addon_dir, "update.zip")
        temp_dir = os.path.join(addon_dir, "temp_update")

        try:
            self.report({'INFO'}, "Téléchargement de la mise à jour...")
            urllib.request.urlretrieve(url, zip_path)

            # Créer un dossier temporaire
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)

            # Extraire le zip dans le dossier temporaire
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Le zip contient un sous-dossier lw_ModelToGmodHelper-main
            extracted_dir = os.path.join(temp_dir, "lw_ModelToGmodHelper-main")

            # Copier tous les fichiers et dossiers vers le dossier actuel
            for item in os.listdir(extracted_dir):
                s = os.path.join(extracted_dir, item)
                d = os.path.join(addon_dir, item)
                if os.path.isdir(s):
                    if os.path.exists(d):
                        shutil.rmtree(d)
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)

            # Nettoyer
            shutil.rmtree(temp_dir)
            os.remove(zip_path)

            self.report({'INFO'}, "Addon mis à jour ! Redémarre Blender ou recharge l'addon.")

        except Exception as e:
            self.report({'ERROR'}, f"Erreur lors de la mise à jour : {e}")
            return {'CANCELLED'}

        return {'FINISHED'}
