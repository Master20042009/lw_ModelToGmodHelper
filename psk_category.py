import bpy

class LW_OT_RenamePSKBones(bpy.types.Operator):
    bl_idname = "lw_pannel.rename_psk_bones"
    bl_label = "Renommer les os PSK"
    bl_description = "Renomme automatiquement les os d’un squelette PSK en noms ValveBiped"
    bl_options = {'REGISTER', 'UNDO'}

    bone_name_map = {

    "Pelvis": "ValveBiped.Bip01_Pelvis",

    "Spine": "ValveBiped.Bip01_Spine",
    "Spine0": "ValveBiped.Bip01_Spine1",
    "Spine1": "ValveBiped.Bip01_Spine2",
    "Spine3": "ValveBiped.Bip01_Spine4",

    # Côté gauche
    "LeftShoulder": "ValveBiped.Bip01_L_Clavicle",
    "LeftArm": "ValveBiped.Bip01_L_UpperArm",
    "LeftForeArm": "ValveBiped.Bip01_L_Forearm",
    "LeftHand": "ValveBiped.Bip01_L_Hand",
    "LeftHandThumb1": "ValveBiped.Bip01_L_Finger0",
    "LeftHandThumb2": "ValveBiped.Bip01_L_Finger01",
    "LeftHandThumb3": "ValveBiped.Bip01_L_Finger02",
    "LeftHandIndex1": "ValveBiped.Bip01_L_Finger1",
    "LeftHandIndex2": "ValveBiped.Bip01_L_Finger11",
    "LeftHandIndex3": "ValveBiped.Bip01_L_Finger12",
    "LeftHandMiddle1": "ValveBiped.Bip01_L_Finger2",
    "LeftHandMiddle2": "ValveBiped.Bip01_L_Finger21",
    "LeftHandMiddle3": "ValveBiped.Bip01_L_Finger22",
    "LeftHandRing1": "ValveBiped.Bip01_L_Finger3",
    "LeftHandRing2": "ValveBiped.Bip01_L_Finger31",
    "LeftHandRing3": "ValveBiped.Bip01_L_Finger32",
    "LeftHandPinky1": "ValveBiped.Bip01_L_Finger4",
    "LeftHandPinky2": "ValveBiped.Bip01_L_Finger41",
    "LeftHandPinky3": "ValveBiped.Bip01_L_Finger42",

    "LeftUpLeg": "ValveBiped.Bip01_L_Thigh",
    "LeftLeg": "ValveBiped.Bip01_L_Calf",
    "LeftFoot": "ValveBiped.Bip01_L_Foot",
    "LeftToeBase": "ValveBiped.Bip01_L_Toe0",

    # Côté droit
    "RightShoulder": "ValveBiped.Bip01_R_Clavicle",
    "RightArm": "ValveBiped.Bip01_R_UpperArm",
    "RightForeArm": "ValveBiped.Bip01_R_Forearm",
    "RightHand": "ValveBiped.Bip01_R_Hand",
    "RightHandThumb1": "ValveBiped.Bip01_R_Finger0",
    "RightHandThumb2": "ValveBiped.Bip01_R_Finger01",
    "RightHandThumb3": "ValveBiped.Bip01_R_Finger02",
    "RightHandIndex1": "ValveBiped.Bip01_R_Finger1",
    "RightHandIndex2": "ValveBiped.Bip01_R_Finger11",
    "RightHandIndex3": "ValveBiped.Bip01_R_Finger12",
    "RightHandMiddle1": "ValveBiped.Bip01_R_Finger2",
    "RightHandMiddle2": "ValveBiped.Bip01_R_Finger21",
    "RightHandMiddle3": "ValveBiped.Bip01_R_Finger22",
    "RightHandRing1": "ValveBiped.Bip01_R_Finger3",
    "RightHandRing2": "ValveBiped.Bip01_R_Finger31",
    "RightHandRing3": "ValveBiped.Bip01_R_Finger32",
    "RightHandPinky1": "ValveBiped.Bip01_R_Finger4",
    "RightHandPinky2": "ValveBiped.Bip01_R_Finger41",
    "RightHandPinky3": "ValveBiped.Bip01_R_Finger42",

    "RightUpLeg": "ValveBiped.Bip01_R_Thigh",
    "RightLeg": "ValveBiped.Bip01_R_Calf",
    "RightFoot": "ValveBiped.Bip01_R_Foot",
    "RightToeBase": "ValveBiped.Bip01_R_Toe0",

    # Tête
    "Neck": "ValveBiped.Bip01_Neck1",
    "Head": "ValveBiped.Bip01_Head",

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
    
class LW_OT_CorrectValveBoneRoll(bpy.types.Operator):
    bl_idname = "lw_pannel.correct_valve_bone_roll"
    bl_label = "Corriger le roll des os ValveBiped"
    bl_description = "Aligne automatiquement le roll des os selon ValveBiped (axe vers enfant, sinon 0)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "Sélectionne une armature.")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        arm = obj.data

        for bone in arm.edit_bones:
            if bone.children:
                vec = bone.children[0].head - bone.head
                bone.align_roll(vec)
            else:
                bone.roll = 0.0

        bpy.ops.object.mode_set(mode='POSE')
        self.report({'INFO'}, "Roll des os corrigé.")
        return {'FINISHED'}
    
class LW_OT_ScaleToGmod(bpy.types.Operator):
    bl_idname = "lw_pannel.scale_to_gmod"
    bl_label = "Mettre à l’échelle GMod"
    bl_description = "Met le modèle à la taille standard ValveBiped pour GMod"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "Sélectionne une armature.")
            return {'CANCELLED'}

        arm = obj.data
        pelvis = arm.bones.get("ValveBiped.Bip01_Pelvis")
        head = arm.bones.get("ValveBiped.Bip01_Head")

        if not pelvis or not head:
            self.report({'WARNING'}, "Os pelvis ou tête ValveBiped non trouvés.")
            return {'CANCELLED'}

        pelvis_head_pos = pelvis.head_local
        head_head_pos = head.head_local

        current_height = (head_head_pos - pelvis_head_pos).length
        if current_height == 0:
            self.report({'WARNING'}, "Hauteur actuelle nulle.")
            return {'CANCELLED'}

        target_height = 1.7  # 1.7 mètres (170 cm) standard GMod
        scale_factor = target_height / current_height

        # Appliquer la scale uniformément sur l’objet
        obj.scale = (scale_factor, scale_factor, scale_factor)

        # Appliquer la transformation pour remettre la scale à (1,1,1)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(scale=True)

        self.report({'INFO'}, f"Modèle mis à l’échelle avec un facteur {scale_factor:.2f}.")
        return {'FINISHED'}