import bpy

class LW_OT_RenameUSDZBones(bpy.types.Operator):
    bl_idname = "lw_pannel.rename_usdz_bones"
    bl_label = "Renommer les os USDZ"
    bl_description = "Renomme automatiquement les os d’un squelette PSK en noms ValveBiped"
    bl_options = {'REGISTER', 'UNDO'}

    bone_name_map = {

    "n187": "ValveBiped.Bip01_Pelvis",

    "n6": "ValveBiped.Bip01_Spine",
    "n7": "ValveBiped.Bip01_Spine1",
    "": "ValveBiped.Bip01_Spine2",
    "": "ValveBiped.Bip01_Spine4",

    # Côté gauche
    "n158": "ValveBiped.Bip01_L_Clavicle",
    "n159": "ValveBiped.Bip01_L_UpperArm",
    "n160": "ValveBiped.Bip01_L_Forearm",
    "n163": "ValveBiped.Bip01_L_Hand",
    "n164": "ValveBiped.Bip01_L_Finger0",
    "n165": "ValveBiped.Bip01_L_Finger01",
    "n166": "ValveBiped.Bip01_L_Finger02",
    "n168": "ValveBiped.Bip01_L_Finger1",
    "n169": "ValveBiped.Bip01_L_Finger11",
    "n170": "ValveBiped.Bip01_L_Finger12",
    "n172": "ValveBiped.Bip01_L_Finger2",
    "n173": "ValveBiped.Bip01_L_Finger21",
    "n174": "ValveBiped.Bip01_L_Finger22",
    "n177": "ValveBiped.Bip01_L_Finger3",
    "n178": "ValveBiped.Bip01_L_Finger31",
    "n179": "ValveBiped.Bip01_L_Finger32",
    "n181": "ValveBiped.Bip01_L_Finger4",
    "n182": "ValveBiped.Bip01_L_Finger41",
    "n183": "ValveBiped.Bip01_L_Finger42",

    "n198": "ValveBiped.Bip01_L_Thigh",
    "n199": "ValveBiped.Bip01_L_Calf",
    "n201": "ValveBiped.Bip01_L_Foot",
    "n202": "ValveBiped.Bip01_L_Toe0",

    # Côté droit
    "n129": "ValveBiped.Bip01_R_Clavicle",
    "n130": "ValveBiped.Bip01_R_UpperArm",
    "n131": "ValveBiped.Bip01_R_Forearm",

    "134": "ValveBiped.Bip01_R_Hand",
    "n135": "ValveBiped.Bip01_R_Finger0",
    "n136": "ValveBiped.Bip01_R_Finger01",

    "n137": "ValveBiped.Bip01_R_Finger02",
    "n139": "ValveBiped.Bip01_R_Finger1",
    "n140": "ValveBiped.Bip01_R_Finger11",

    "n141": "ValveBiped.Bip01_R_Finger12",
    "n143": "ValveBiped.Bip01_R_Finger2",
    "n144": "ValveBiped.Bip01_R_Finger21",
    "n145": "ValveBiped.Bip01_R_Finger22",

    "n148": "ValveBiped.Bip01_R_Finger3",
    "n149": "ValveBiped.Bip01_R_Finger31",
    "n150": "ValveBiped.Bip01_R_Finger32",

    "n152": "ValveBiped.Bip01_R_Finger4",
    "n153": "ValveBiped.Bip01_R_Finger41",
    "n154": "ValveBiped.Bip01_R_Finger42",

    "n188": "ValveBiped.Bip01_R_Thigh",
    "n189": "ValveBiped.Bip01_R_Calf",
    "n190": "ValveBiped.Bip01_R_Foot",
    "n191": "ValveBiped.Bip01_R_Toe0",

    # Tête
    "n8": "ValveBiped.Bip01_Neck1",
    "n9": "ValveBiped.Bip01_Head",

    # Yeux / mâchoire
    "LeftEye": "ValveBiped.Bip01_L_Eye",
    "RightEye": "ValveBiped.Bip01_R_Eye",
    "Jaw": "ValveBiped.Bip01_Jaw",

    }

    def execute(self, context):
        obj = context.object

        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "Sélectionne une armature.")
            return {'CANCELLED'}

        renamed_count = 0
        for bone in obj.data.bones:
            if bone.name in self.bone_name_map:
                old = bone.name
                bone.name = self.bone_name_map[old]
                renamed_count += 1

        if renamed_count > 0:
            self.report({'INFO'}, f"{renamed_count} os renommés avec succès.")
        else:
            self.report({'WARNING'}, "Aucun os à renommer trouvé.")
        return {'FINISHED'}
    