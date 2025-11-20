import bpy

class RELINKER_PT_Panel(bpy.types.Panel):
    bl_label = "LW ModelToGmodHelper"
    bl_idname = "RELINKER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'lw_pannel'

    def draw(self, context):
        layout = self.layout
        props = context.scene.relinker_props

        layout.prop(props, "folder_path")
        layout.operator("lw_pannel.relink_textures", icon='FILE_REFRESH')
        layout.separator()
        layout.operator("lw_pannel.create_lods", icon='MOD_DECIM')
        layout.separator()

        layout.label(text="Mirror Preview Axes :")
        row = layout.row(align=True)
        row.prop(props, "mirror_axis_x")
        row.prop(props, "mirror_axis_y")
        row.prop(props, "mirror_axis_z")
        row = layout.row(align=True)
        row.prop(props, "mirror_axis_neg_x")

        layout.separator()
        layout.label(text="Cleanup :")
        layout.operator("lw_pannel.merge_by_distance", icon='AUTOMERGE_ON')
        layout.operator("lw_pannel.clear_custom_normals", icon='NORMALS_VERTEX')

        layout.separator()
        layout.label(text="Séparation :")
        layout.operator("lw_pannel.separate_selected", icon='UV_ISLANDSEL')
        layout.operator("lw_pannel.separate_loose", icon='GROUP_VERTEX')

        layout.separator()
        layout.operator("lw_pannel.remove_unused_materials", icon='X')
        layout.operator("lw_pannel.select_objects_with_same_materials", icon='RESTRICT_SELECT_OFF')

        layout.label(text="Qualité du modèle (Subdivision)")
        layout.prop(props, "quality_level", slider=True)
        layout.operator("lw_pannel.increase_quality", icon='MOD_SUBSURF')
        layout.operator("lw_pannel.apply_quality", icon='FILE_TICK')
        layout.operator("lw_pannel.select_objects_with_same_materials", icon='RESTRICT_SELECT_OFF')

        layout.separator()
        layout.operator("lw_pannel.update_addon", icon='FILE_REFRESH')

        layout.separator()
        layout.label(text="Animation", icon='ARMATURE_DATA')
        layout.operator("lw_pannel.retarget_anim_auto", icon='ANIM_DATA')

        layout.separator()
        layout.label(text="PSK Tools", icon='OUTLINER_OB_ARMATURE')
        layout.operator("lw_pannel.fix_psk_bone_scale", icon='TOOL_SETTINGS')
        layout.operator("lw_pannel.rename_psk_bones", icon='FONT_DATA')
        layout.operator("lw_pannel.correct_valve_bone_roll", icon='ARMATURE_DATA')
        layout.operator("lw_pannel.scale_to_gmod", icon='MOD_SUBSURF')

        layout.separator()
        layout.label(text="USDZ Tools", icon="OUTLINER_OB_ARMATURE")
        layout.operator("lw_pannel.rename_usdz_bones", icon='FONT_DATA')
        
