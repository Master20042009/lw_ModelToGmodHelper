import bpy

class LW_OT_retarget_anim_auto(bpy.types.Operator):
    bl_idname = "lw_pannel.retarget_anim_auto"
    bl_label = "Retarget auto Animation A → B"
    bl_description = "Retarget l'animation de Armature_A vers Armature_B en détectant automatiquement les os communs"

    def execute(self, context):
        source_name = "Armature_A"  # Tu peux changer ces noms ou les rendre dynamiques plus tard
        target_name = "Armature_B"

        source = bpy.data.objects.get(source_name)
        target = bpy.data.objects.get(target_name)

        if not source or not target:
            self.report({'ERROR'}, f"Armature '{source_name}' ou '{target_name}' introuvable.")
            return {'CANCELLED'}

        common_bones = set(source.pose.bones.keys()) & set(target.pose.bones.keys())
        if not common_bones:
            self.report({'WARNING'}, "Aucun os commun trouvé entre les deux armatures.")
            return {'CANCELLED'}

        start = context.scene.frame_start
        end = context.scene.frame_end

        bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='POSE')

        for frame in range(start, end + 1):
            context.scene.frame_set(frame)
            for bone_name in common_bones:
                sb = source.pose.bones[bone_name]
                tb = target.pose.bones[bone_name]
                tb.rotation_mode = sb.rotation_mode

                if sb.rotation_mode == 'QUATERNION':
                    tb.rotation_quaternion = sb.rotation_quaternion.copy()
                    tb.keyframe_insert(data_path="rotation_quaternion", frame=frame)
                else:
                    tb.rotation_euler = sb.rotation_euler.copy()
                    tb.keyframe_insert(data_path="rotation_euler", frame=frame)

        self.report({'INFO'}, f"✅ Animation retargetée sur {len(common_bones)} os.")
        return {'FINISHED'}
