import bpy
from .compilation import validate_compilation_config


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
        row.prop(props, "mirror_axis_neg_y")
        row.prop(props, "mirror_axis_neg_z")

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

        layout.label(text="Qualité du modèle (Subdivision)")
        layout.prop(props, "quality_level", slider=True)
        layout.operator("lw_pannel.increase_quality", icon='MOD_SUBSURF')
        layout.operator("lw_pannel.apply_quality", icon='FILE_TICK')

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
        
        layout.separator()
        layout.label(text="Collision Model (Convex Hull)")
        layout.operator("lw_pannel.create_collision", icon='MESH_CUBE')


class COMPILATION_PT_MainPanel(bpy.types.Panel):
    """Panel principal pour la compilation Source Engine"""
    bl_label = "Source Compilation"
    bl_idname = "COMPILATION_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'lw_pannel'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.compilation_props
        
        # Configuration de base
        box = layout.box()
        box.label(text="Configuration", icon='SETTINGS')
        box.prop(props, "game_name")
        box.prop(props, "studiomdl_path", text="studiomdl.exe")
        box.prop(props, "gameinfo_path", text="gameinfo.txt")
        
        if not validate_compilation_config(context):
            box.label(text="⚠ Configuration incomplete", icon='ERROR')
            return
        
        box.label(text="✓ Configuration valide", icon='CHECKMARK')
        
        # Model info
        layout.separator()
        box = layout.box()
        box.label(text="Model Info", icon='OBJECT_DATA')
        layout.prop(props, "modelname", text="$modelname")
        layout.prop(props, "cdmaterials", text="$cdmaterials")
        
        # Bodies
        layout.separator()
        box = layout.box()
        box.label(text="Bodies", icon='MESH_DATA')
        
        row = box.row()
        row.template_list(
            "COMPILATION_UL_BodyList", "",
            context.scene, "body_list",
            context.scene, "body_list_index",
            rows=3
        )
        
        col = row.column(align=True)
        col.operator("lw_pannel.add_body", icon='ADD', text="")
        col.operator("lw_pannel.remove_body", icon='REMOVE', text="")
        
        # Détails du body sélectionné
        if len(context.scene.body_list) > 0 and context.scene.body_list_index < len(context.scene.body_list):
            body = context.scene.body_list[context.scene.body_list_index]
            
            layout.separator()
            box = layout.box()
            box.label(text=f"Body: {body.name}", icon='MESH_DATA')
            
            box.prop(body, "name", text="Name")
            # Utiliser prop avec type filter pour afficher seulement les Mesh
            box.prop(body, "mesh_object", text="Mesh", icon='MESH_DATA')
        
        # Bouton de compilation principal
        layout.separator()
        row = layout.row()
        row.scale_y = 2.0
        row.operator("lw_pannel.compile_model", icon='PLAY')


class COMPILATION_PT_CollisionPanel(bpy.types.Panel):
    """Panel pour les options de collision"""
    bl_label = "Collision Options"
    bl_idname = "COMPILATION_PT_collision"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'lw_pannel'
    bl_parent_id = "COMPILATION_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return validate_compilation_config(context)
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.compilation_props
        
        layout.prop(props, "collision_mesh", text="Collision Mesh", icon='MESH_DATA')
        
        if props.collision_mesh:
            layout.separator()
            layout.prop(props, "collision_concave")
            layout.prop(props, "collision_mass")
            layout.prop(props, "collision_maxconvex")


class COMPILATION_PT_GeneralOptionsPanel(bpy.types.Panel):
    """Panel pour les options générales"""
    bl_label = "General Options"
    bl_idname = "COMPILATION_PT_general"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'lw_pannel'
    bl_parent_id = "COMPILATION_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return validate_compilation_config(context)
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.compilation_props
        
        layout.prop(props, "staticprop")
        layout.prop(props, "surfaceprop")


class COMPILATION_PT_SequencesPanel(bpy.types.Panel):
    """Panel pour les séquences d'animation"""
    bl_label = "Sequences"
    bl_idname = "COMPILATION_PT_sequences"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'lw_pannel'
    bl_parent_id = "COMPILATION_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return validate_compilation_config(context)
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        row = layout.row()
        row.template_list(
            "COMPILATION_UL_SequenceList", "",
            scene, "sequence_list",
            scene, "sequence_list_index",
            rows=3
        )
        
        col = row.column(align=True)
        col.operator("lw_pannel.add_sequence", icon='ADD', text="")
        col.operator("lw_pannel.remove_sequence", icon='REMOVE', text="")
        
        # Détails de la séquence sélectionnée
        if len(scene.sequence_list) > 0 and scene.sequence_list_index < len(scene.sequence_list):
            seq = scene.sequence_list[scene.sequence_list_index]
            
            layout.separator()
            box = layout.box()
            box.label(text=f"Sequence: {seq.name}", icon='ANIM')
            
            box.prop(seq, "activity")
            box.prop(seq, "activity_weight")
            
            row = box.row(align=True)
            row.prop(seq, "fadein")
            row.prop(seq, "fadeout")
            
            box.prop(seq, "fps")
            
            row = box.row(align=True)
            row.prop(seq, "loop")
            row.prop(seq, "autoplay")


class COMPILATION_PT_PathsPanel(bpy.types.Panel):
    """Panel pour les chemins personnalisés"""
    bl_label = "Custom Paths"
    bl_idname = "COMPILATION_PT_paths"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'lw_pannel'
    bl_parent_id = "COMPILATION_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return validate_compilation_config(context)
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.compilation_props
        
        layout.label(text="SMD Files", icon='EXPORT')
        layout.prop(props, "smd_output_path", text="SMD Output Path")
        layout.label(text="Leave empty to use temp directory", icon='INFO')
        
        layout.separator()
        layout.label(text="Compiled Model", icon='OUTPUT')
        layout.prop(props, "model_output_path", text="Model Output Path")
        layout.label(text="Leave empty to use game directory", icon='INFO')


# Classes du panel à exporter
panel_classes = (
    RELINKER_PT_Panel,
    COMPILATION_PT_MainPanel,
    COMPILATION_PT_CollisionPanel,
    COMPILATION_PT_GeneralOptionsPanel,
    COMPILATION_PT_SequencesPanel,
    COMPILATION_PT_PathsPanel,
)