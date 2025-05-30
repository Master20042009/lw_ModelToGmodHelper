import bpy

class RELINKER_PT_Panel(bpy.types.Panel):
    bl_label = "Auto Texture Relinker"
    bl_idname = "RELINKER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Relinker'

    def draw(self, context):
        layout = self.layout
        props = context.scene.relinker_props

        layout.prop(props, "folder_path")
        layout.operator("relinker.relink_textures", icon='FILE_REFRESH')
        layout.separator()
        layout.operator("relinker.create_lods", icon='MOD_DECIM')
        layout.separator()

        layout.label(text="Mirror Preview Axes :")
        row = layout.row(align=True)
        row.prop(props, "mirror_axis_x")
        row.prop(props, "mirror_axis_y")
        row.prop(props, "mirror_axis_z")
        row = layout.row(align=True)
        row.prop(props, "mirror_axis_neg_x")
        row.prop(props, "mirror_axis_neg_y")
        row.prop(props, "mirror_axis_neg_z")
        layout.operator("relinker.mirror_object", icon='MOD_MIRROR')

        layout.separator()
        layout.operator("relinker.separate_selected", icon='UV_SYNC_SELECT')
        layout.operator("relinker.separate_loose", icon='GROUP_VERTEX')
        layout.operator("relinker.merge_by_distance", icon='AUTOMERGE_ON')
        layout.operator("relinker.clear_custom_normals", icon='NORMALS_VERTEX')

        layout.separator()
        layout.label(text="Qualité du modèle (Subdivision)")
        layout.prop(props, "quality_level", slider=True)
        layout.operator("relinker.increase_quality", icon='MOD_SUBSURF')
        layout.operator("relinker.apply_quality", icon='FILE_TICK')
