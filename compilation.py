import bpy
import os
import subprocess
import shutil
from pathlib import Path
from io import StringIO


def validate_compilation_config(context):
    """Valide que tous les chemins nécessaires sont définis"""
    scene = context.scene.compilation_props
    
    return (
        os.path.exists(scene.studiomdl_path) and
        os.path.exists(scene.gameinfo_path) and
        scene.studiomdl_path.endswith("studiomdl.exe") and
        scene.gameinfo_path.endswith("gameinfo.txt")
    )


def on_compilation_path_changed(self, context):
    """Callback quand un chemin de compilation change"""
    validate_compilation_config(context)


class CompilationProperties(bpy.types.PropertyGroup):
    """Propriétés pour la compilation Source Engine"""
    
    studiomdl_path: bpy.props.StringProperty(
        name="studiomdl.exe",
        description="Path to studiomdl.exe",
        subtype='FILE_PATH',
        update=on_compilation_path_changed
    )
    
    gameinfo_path: bpy.props.StringProperty(
        name="gameinfo.txt",
        description="Path to gameinfo.txt",
        subtype='FILE_PATH',
        update=on_compilation_path_changed
    )
    
    modelname: bpy.props.StringProperty(
        name="$modelname",
        description="Model path (e.g., props/mymodel.mdl)",
        default="props/mymodel.mdl"
    )
    
    cdmaterials: bpy.props.StringProperty(
        name="$cdmaterials",
        description="Material paths (one per line)",
        default="models/props/"
    )
    
    collision_mesh: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Collision Mesh",
        description="Mesh object used for collision",
        poll=lambda self, obj: obj.type == 'MESH'
    )
    
    collision_mass: bpy.props.FloatProperty(
        name="$mass",
        description="Mass in kilograms",
        default=250.0,
        min=0.1
    )
    
    staticprop: bpy.props.BoolProperty(
        name="$staticprop",
        description="Make this a static prop",
        default=False
    )
    
    surfaceprop: bpy.props.StringProperty(
        name="$surfaceprop",
        description="Surface property type",
        default="default"
    )
    
    smd_output_path: bpy.props.StringProperty(
        name="SMD Output Path",
        description="Custom path for SMD file export (leave empty for temp directory)",
        subtype='DIR_PATH',
        default=""
    )
    
    model_output_path: bpy.props.StringProperty(
        name="Model Output Path",
        description="Custom path where compiled model files will be saved",
        subtype='DIR_PATH',
        default=""
    )
    
    # Options supplémentaires pour le QC
    illumposition_x: bpy.props.FloatProperty(name="Illum X", default=0.0)
    illumposition_y: bpy.props.FloatProperty(name="Illum Y", default=0.0)
    illumposition_z: bpy.props.FloatProperty(name="Illum Z", default=0.0)
    
    constantdirectionallight: bpy.props.FloatProperty(
        name="Constant Directional Light",
        default=0.15,
        min=0.0,
        max=1.0
    )
    
    ambientboost: bpy.props.BoolProperty(
        name="Ambient Boost",
        description="Enable ambient boost",
        default=False
    )
    
    casttextureshadows: bpy.props.BoolProperty(
        name="Cast Texture Shadows",
        description="Enable texture shadow casting",
        default=False
    )
    
    origin_x: bpy.props.FloatProperty(name="Origin X", default=0.0)
    origin_y: bpy.props.FloatProperty(name="Origin Y", default=0.0)
    origin_z: bpy.props.FloatProperty(name="Origin Z", default=0.0)
    
    skipboneinbbox: bpy.props.BoolProperty(
        name="Skip Bone In Bbox",
        description="Skip bone in bounding box calculation",
        default=False
    )
    
    # Options de collision
    collision_type: bpy.props.EnumProperty(
        name="Collision Type",
        description="Type of collision model",
        items=[
            ('MODEL', "Collision Model (phy)", "Use collision model with convex hulls"),
            ('JOINTS', "Collision Joints", "Use collision joints for ragdoll")
        ],
        default='MODEL'
    )
    
    # Collision Model options
    collision_mass: bpy.props.IntProperty(
        name="Mass",
        description="Mass in kg (0-255)",
        default=0,
        min=0,
        max=255
    )
    
    collision_enable_mass: bpy.props.BoolProperty(
        name="Enable Mass",
        description="Enable mass parameter",
        default=False
    )
    
    collision_maxconvexpieces: bpy.props.IntProperty(
        name="Max Convex Pieces",
        description="Maximum convex pieces (0-65536)",
        default=0,
        min=0,
        max=65536
    )
    
    collision_enable_maxconvex: bpy.props.BoolProperty(
        name="Enable Max Convex Pieces",
        description="Enable max convex pieces parameter",
        default=False
    )
    
    collision_concave: bpy.props.BoolProperty(
        name="Concave",
        description="Use concave collision",
        default=False
    )
    
    # Collision Joints options
    collision_joints_mass: bpy.props.IntProperty(
        name="Joints Mass",
        description="Mass for joints (0-255)",
        default=0,
        min=0,
        max=255
    )
    
    collision_enable_joints_mass: bpy.props.BoolProperty(
        name="Enable Joints Mass",
        description="Enable mass for joints",
        default=False
    )
    
    collision_joints_rootbone: bpy.props.StringProperty(
        name="Root Bone",
        description="Name of the root bone for joints",
        default=""
    )
    
    collision_enable_joints_rootbone: bpy.props.BoolProperty(
        name="Enable Root Bone",
        description="Enable root bone parameter",
        default=False
    )
    
    collision_joints_inertia: bpy.props.FloatProperty(
        name="Inertia",
        description="Inertia value",
        default=2.0,
        min=0.0
    )
    
    collision_enable_joints_inertia: bpy.props.BoolProperty(
        name="Enable Inertia",
        description="Enable inertia parameter",
        default=False
    )
    
    collision_joints_damping: bpy.props.FloatProperty(
        name="Damping",
        description="Damping value",
        default=0.01,
        min=0.0
    )
    
    collision_enable_joints_damping: bpy.props.BoolProperty(
        name="Enable Damping",
        description="Enable damping parameter",
        default=False
    )
    
    collision_joints_rotdamping: bpy.props.FloatProperty(
        name="Rotation Damping",
        description="Rotation damping value",
        default=0.40,
        min=0.0
    )
    
    collision_enable_joints_rotdamping: bpy.props.BoolProperty(
        name="Enable Rotation Damping",
        description="Enable rotation damping parameter",
        default=False
    )
    
    # Shadow LOD options
    enable_shadowlod: bpy.props.BoolProperty(
        name="Enable Shadow LOD",
        description="Enable shadow LOD replacement",
        default=False
    )
    
    shadowlod_replace_from_obj: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Shadow LOD From",
        description="Original mesh object for shadow LOD",
        poll=lambda self, obj: obj.type == 'MESH'
    )
    
    shadowlod_replace_to_obj: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Shadow LOD To",
        description="Replacement mesh object for shadow LOD",
        poll=lambda self, obj: obj.type == 'MESH'
    )


class BodyPropGroup(bpy.types.PropertyGroup):
    """Groupe de propriétés pour un $body"""
    name: bpy.props.StringProperty(
        name="Body Name",
        default="Body"
    )
    
    mesh_object: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Mesh Category",
        description="Mesh collection for this body",
        poll=lambda self, obj: obj.type == 'EMPTY' and obj.instance_type == 'COLLECTION'
    )


class SequencePropGroup(bpy.types.PropertyGroup):
    """Groupe de propriétés pour une séquence d'animation"""
    name: bpy.props.StringProperty(
        name="Sequence Name",
        default="idle"
    )
    
    enabled: bpy.props.BoolProperty(
        name="Enabled",
        default=True
    )
    
    animation_mode: bpy.props.EnumProperty(
        name="Animation Source",
        description="Where to get the animation from",
        items=[
            ('MESH', "Animated Mesh", "Use animated mesh (baked animation or shape keys)"),
            ('ARMATURE', "Armature", "Use armature deformer with animations")
        ],
        default='MESH'
    )
    
    # Mesh animé pour mode MESH
    animation_mesh: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Animated Mesh",
        description="Mesh object with animation (baked or shape keys)",
        poll=lambda self, obj: obj.type == 'MESH'
    )
    
    # Armature pour mode ARMATURE
    animation_armature: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Animation Armature",
        description="Armature with animations",
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    
    # Sequence options
    enable_activity: bpy.props.BoolProperty(
        name="Enable Activity",
        description="Enable activity parameter",
        default=False
    )
    
    activity: bpy.props.StringProperty(
        name="Activity",
        description="Activity type",
        default=""
    )
    
    activity_weight: bpy.props.IntProperty(
        name="Activity Weight",
        description="Activity weight (0 or 1)",
        default=0,
        min=0,
        max=1
    )
    
    enable_fadein: bpy.props.BoolProperty(
        name="Enable Fade In",
        description="Enable fade in parameter",
        default=False
    )
    
    fadein: bpy.props.IntProperty(
        name="Fade In",
        description="Fade in duration (0-10)",
        default=0,
        min=0,
        max=10
    )
    
    enable_fadeout: bpy.props.BoolProperty(
        name="Enable Fade Out",
        description="Enable fade out parameter",
        default=False
    )
    
    fadeout: bpy.props.IntProperty(
        name="Fade Out",
        description="Fade out duration (0-10)",
        default=0,
        min=0,
        max=10
    )
    
    enable_fps: bpy.props.BoolProperty(
        name="Enable FPS",
        description="Enable fps parameter",
        default=True
    )
    
    fps: bpy.props.IntProperty(
        name="FPS",
        description="Frames per second (0-180)",
        default=30,
        min=0,
        max=180
    )


class LODPropGroup(bpy.types.PropertyGroup):
    """Groupe de propriétés pour un LOD"""
    lod_level: bpy.props.IntProperty(
        name="LOD Level",
        description="LOD level (0-65535)",
        default=1,
        min=0,
        max=65535
    )
    
    # Model replacements using mesh objects
    replace_model_from_obj: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="From Model",
        description="Original mesh object to replace",
        poll=lambda self, obj: obj.type == 'MESH'
    )
    
    replace_model_to_obj: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="To Model",
        description="Replacement mesh object",
        poll=lambda self, obj: obj.type == 'MESH'
    )
    
    enable_replace_material: bpy.props.BoolProperty(
        name="Enable Replace Material",
        description="Enable material replacement",
        default=False
    )
    
    replace_material_from: bpy.props.StringProperty(
        name="From Material",
        description="Original material name to replace",
        default=""
    )
    
    replace_material_to: bpy.props.StringProperty(
        name="To Material",
        description="Replacement material name",
        default=""
    )


class COMPILATION_UL_BodyList(bpy.types.UIList):
    """Liste UI pour les bodies"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, "name", text="", emboss=False, icon='MESH_DATA')
            row.prop(item, "mesh_object", text="", icon='OBJECT_DATA')
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='MESH_DATA')


class COMPILATION_UL_SequenceList(bpy.types.UIList):
    """Liste UI pour les séquences d'animation"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, "enabled", text="")
            row.prop(item, "name", text="", emboss=False, icon='ANIM')
            
            # Afficher le mode d'animation
            anim_icon = 'ARMATURE_DATA' if item.animation_mode == 'ARMATURE' else 'MESH_DATA'
            row.label(text=item.animation_mode, icon=anim_icon)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='ANIM')


class COMPILATION_UL_LODList(bpy.types.UIList):
    """Liste UI pour les LODs"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.label(text=f"LOD {item.lod_level}", icon='MOD_DECIM')
            
            from_name = item.replace_model_from_obj.name if item.replace_model_from_obj else "None"
            to_name = item.replace_model_to_obj.name if item.replace_model_to_obj else "None"
            row.label(text=f"From: {from_name}")
            row.label(text=f"To: {to_name}")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='MOD_DECIM')


class COMPILATION_OT_AddBody(bpy.types.Operator):
    """Ajouter un nouveau body"""
    bl_idname = "lw_pannel.add_body"
    bl_label = "Add Body"
    bl_description = "Add a new body to the list"
    
    def execute(self, context):
        body = context.scene.body_list.add()
        body.name = f"Body_{len(context.scene.body_list)}"
        context.scene.body_list_index = len(context.scene.body_list) - 1
        return {'FINISHED'}


class COMPILATION_OT_RemoveBody(bpy.types.Operator):
    """Supprimer un body"""
    bl_idname = "lw_pannel.remove_body"
    bl_label = "Remove Body"
    bl_description = "Remove selected body from the list"
    
    def execute(self, context):
        scene = context.scene
        if len(scene.body_list) > 0:
            scene.body_list.remove(scene.body_list_index)
            scene.body_list_index = min(max(0, scene.body_list_index - 1), len(scene.body_list) - 1)
        return {'FINISHED'}


class COMPILATION_OT_AddSequence(bpy.types.Operator):
    """Ajouter une nouvelle séquence"""
    bl_idname = "lw_pannel.add_sequence"
    bl_label = "Add Sequence"
    bl_description = "Add a new animation sequence"
    
    def execute(self, context):
        seq = context.scene.sequence_list.add()
        seq.name = f"sequence_{len(context.scene.sequence_list)}"
        context.scene.sequence_list_index = len(context.scene.sequence_list) - 1
        return {'FINISHED'}


class COMPILATION_OT_RemoveSequence(bpy.types.Operator):
    """Supprimer une séquence"""
    bl_idname = "lw_pannel.remove_sequence"
    bl_label = "Remove Sequence"
    bl_description = "Remove selected sequence from the list"
    
    def execute(self, context):
        scene = context.scene
        if len(scene.sequence_list) > 0:
            scene.sequence_list.remove(scene.sequence_list_index)
            scene.sequence_list_index = min(max(0, scene.sequence_list_index - 1), len(scene.sequence_list) - 1)
        return {'FINISHED'}


class COMPILATION_OT_AddLOD(bpy.types.Operator):
    """Ajouter un nouveau LOD"""
    bl_idname = "lw_pannel.add_lod"
    bl_label = "Add LOD"
    bl_description = "Add a new LOD level"
    
    def execute(self, context):
        lod = context.scene.lod_list.add()
        lod.lod_level = len(context.scene.lod_list)
        context.scene.lod_list_index = len(context.scene.lod_list) - 1
        return {'FINISHED'}


class COMPILATION_OT_RemoveLOD(bpy.types.Operator):
    """Supprimer un LOD"""
    bl_idname = "lw_pannel.remove_lod"
    bl_label = "Remove LOD"
    bl_description = "Remove selected LOD"
    
    def execute(self, context):
        scene = context.scene
        if len(scene.lod_list) > 0:
            scene.lod_list.remove(scene.lod_list_index)
            scene.lod_list_index = min(max(0, scene.lod_list_index - 1), len(scene.lod_list) - 1)
        return {'FINISHED'}


class COMPILATION_OT_CompileModel(bpy.types.Operator):
    """Compiler le modèle"""
    bl_idname = "lw_pannel.compile_model"
    bl_label = "Compile Model"
    bl_description = "Compile model to Source Engine MDL format"
    
    def execute(self, context):
        scene = context.scene
        props = scene.compilation_props
        
        # Validation
        if not validate_compilation_config(context):
            self.report({'ERROR'}, "Please configure studiomdl.exe and gameinfo.txt paths")
            return {'CANCELLED'}
        
        if not props.modelname:
            self.report({'ERROR'}, "Please define a $modelname")
            return {'CANCELLED'}
        
        if len(scene.body_list) == 0:
            self.report({'ERROR'}, "Please add at least one body")
            return {'CANCELLED'}
        
        # Vérifier que tous les bodies ont un mesh valide
        for body in scene.body_list:
            if not body.mesh_object or body.mesh_object.type != 'MESH':
                self.report({'ERROR'}, f"Body '{body.name}' has no valid mesh")
                return {'CANCELLED'}
        
        # Récupérer les chemins
        game_dir = os.path.dirname(props.gameinfo_path)
        
        # Utiliser le chemin personnalisé pour SMD ou le répertoire temp
        if props.smd_output_path and os.path.exists(props.smd_output_path):
            temp_path = props.smd_output_path
        else:
            temp_path = bpy.app.tempdir
        
        qc_path = os.path.join(temp_path, "model_compile.qc")
        
        try:
            print(f"[COMPILATION] Starting compilation...")
            
            self.generate_qc(context, qc_path)
            self.export_meshes(context, temp_path)
            self.copy_files_to_game_dir(context, temp_path, game_dir)
            self.run_studiomdl(context, game_dir)
            
            self.report({'INFO'}, "Compilation successful!")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Compilation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}
    
    def generate_qc(self, context, qc_path):
        """Génère le fichier QC"""
        scene = context.scene
        props = scene.compilation_props
        
        with open(qc_path, "w") as f:
            # Ordre correct : modelname, cdmaterials, body, lod, shadowlod, options, sequences, collision
            f.write(f'$modelname "{props.modelname}"\n')
            
            # $cdmaterials
            if props.cdmaterials:
                f.write(f'$cdmaterials "{props.cdmaterials}"\n')
            
            f.write('\n')
            
            # $body ou $bodygroup
            if len(scene.body_list) == 1:
                body = scene.body_list[0]
                if body.mesh_object:
                    if isinstance(body.mesh_object, bpy.types.Collection):
                        body_filename = f"{body.mesh_object.name}.smd"
                    else:
                        body_filename = f"{body.mesh_object.name}.smd"
                    f.write(f'$body "{body.name}" "{body_filename}"\n\n')
            else:
                f.write('$bodygroup "Body"\n{\n')
                for body in scene.body_list:
                    if body.mesh_object:
                        if isinstance(body.mesh_object, bpy.types.Collection):
                            body_filename = f"{body.mesh_object.name}.smd"
                        else:
                            body_filename = f"{body.mesh_object.name}.smd"
                        f.write(f'\tstudio "{body_filename}"\n')
                f.write('}\n\n')
            
            # LOD Levels (seulement si valides : from ET to définis)
            lods_written = False
            if len(scene.lod_list) > 0:
                for lod in scene.lod_list:
                    if lod.replace_model_from_obj and lod.replace_model_to_obj:
                        f.write(f'$lod {lod.lod_level}\n')
                        f.write('{\n')
                        f.write(f'\treplacemodel "{lod.replace_model_from_obj.name}" "{lod.replace_model_to_obj.name}"\n')
                        
                        if lod.enable_replace_material and lod.replace_material_from and lod.replace_material_to:
                            f.write(f'\treplacematerial "{lod.replace_material_from}" "{lod.replace_material_to}"\n')
                        
                        f.write('}\n\n')
                        lods_written = True
            
            # Shadow LOD (seulement si valide : from ET to définis)
            if props.enable_shadowlod and props.shadowlod_replace_from_obj and props.shadowlod_replace_to_obj:
                f.write('$shadowlod\n')
                f.write('{\n')
                f.write(f'\treplacemodel "{props.shadowlod_replace_from_obj.name}" "{props.shadowlod_replace_to_obj.name}"\n')
                f.write('}\n\n')
            
            # Options
            if props.staticprop:
                f.write('$staticprop\n')
            
            f.write(f'$surfaceprop "{props.surfaceprop}"\n')
            f.write('$contents "solid"\n')
            
            # Illum position
            f.write(f'$illumposition {props.illumposition_x} {props.illumposition_y} {props.illumposition_z}\n')
            
            # Constant directional light
            f.write(f'$constantdirectionallight {props.constantdirectionallight}\n')
            
            # Ambient boost
            if props.ambientboost:
                f.write('$ambientboost\n')
            
            # Cast texture shadows
            if props.casttextureshadows:
                f.write('$casttextureshadows\n')
            
            # Origin
            f.write(f'$origin {props.origin_x} {props.origin_y} {props.origin_z}\n')
            
            # Skip bone in bbox
            if props.skipboneinbbox:
                f.write('$skipboneinbbox\n')
            
            f.write('\n')
            
            # Générer les séquences
            if len(scene.sequence_list) > 0:
                first_body = scene.body_list[0]
                if first_body.mesh_object:
                    if isinstance(first_body.mesh_object, bpy.types.Collection):
                        first_body_filename = f"{first_body.mesh_object.name}.smd"
                    else:
                        first_body_filename = f"{first_body.mesh_object.name}.smd"
                else:
                    first_body_filename = f"{first_body.name}_ref.smd"
                
                for seq in scene.sequence_list:
                    if seq.enabled:
                        f.write(f'$sequence "{seq.name}" {{\n')
                        f.write(f'\t"{first_body_filename}"\n')
                        
                        # Activity
                        if seq.enable_activity and seq.activity:
                            f.write(f'\tactivity "{seq.activity}" {seq.activity_weight}\n')
                        
                        # Fade in
                        if seq.enable_fadein:
                            f.write(f'\tfadein {seq.fadein}\n')
                        
                        # Fade out
                        if seq.enable_fadeout:
                            f.write(f'\tfadeout {seq.fadeout}\n')
                        
                        # FPS
                        if seq.enable_fps:
                            f.write(f'\tfps {seq.fps}\n')
                        
                        f.write('}\n\n')
            else:
                # Séquence par défaut si aucune séquence n'est définie
                first_body = scene.body_list[0]
                if first_body.mesh_object:
                    if isinstance(first_body.mesh_object, bpy.types.Collection):
                        first_body_filename = f"{first_body.mesh_object.name}.smd"
                    else:
                        first_body_filename = f"{first_body.mesh_object.name}.smd"
                else:
                    first_body_filename = f"{first_body.name}_ref.smd"
                
                f.write('$sequence "idle" {\n')
                f.write(f'\t"{first_body_filename}"\n')
                f.write('\tfps 30\n')
                f.write('}\n\n')
            
            # Collision
            if props.collision_mesh and props.collision_mesh.type == 'MESH':
                if props.collision_type == 'MODEL':
                    # Collision Model
                    f.write('$collisionmodel    "phy"\n')
                    f.write('{\n')
                    if props.collision_enable_mass:
                        f.write(f'\t$mass {props.collision_mass}\n')
                    if props.collision_enable_maxconvex:
                        f.write(f'\t$maxconvexpieces {props.collision_maxconvexpieces}\n')
                    if props.collision_concave:
                        f.write('\t$concave\n')
                    f.write('}\n')
                else:
                    # Collision Joints
                    f.write('$collisionjoints\n')
                    f.write('{\n')
                    if props.collision_enable_joints_mass:
                        f.write(f'\t$mass {props.collision_joints_mass}\n')
                    if props.collision_enable_joints_rootbone and props.collision_joints_rootbone:
                        f.write(f'\t$rootbone "{props.collision_joints_rootbone}"\n')
                    if props.collision_enable_joints_inertia:
                        f.write(f'\t$inertia {props.collision_joints_inertia:.2f}\n')
                    if props.collision_enable_joints_damping:
                        f.write(f'\t$damping {props.collision_joints_damping:.2f}\n')
                    if props.collision_enable_joints_rotdamping:
                        f.write(f'\t$rotdamping {props.collision_joints_rotdamping:.2f}\n')
                    f.write('}\n')
    
    def export_meshes(self, context, temp_path):
        """Exporte tous les meshes en SMD"""
        scene = context.scene
        os.makedirs(temp_path, exist_ok=True)
        
        # Exporter les bodies
        for body in scene.body_list:
            # Déterminer le nom du fichier SMD à partir du nom exact de l'objet Blender
            if body.mesh_object:
                if isinstance(body.mesh_object, bpy.types.Collection):
                    # Si c'est une Collection, utiliser son nom
                    smd_filename = f"{body.mesh_object.name}.smd"
                    smd_path = os.path.join(temp_path, smd_filename)
                    self.export_collection_to_smd(body.mesh_object, smd_path, False)
                elif body.mesh_object.type == 'MESH':
                    # Si c'est un objet mesh, utiliser son nom
                    smd_filename = f"{body.mesh_object.name}.smd"
                    smd_path = os.path.join(temp_path, smd_filename)
                    self.export_mesh_to_smd(body.mesh_object, smd_path, False)
        
        # Exporter les modèles LOD
        for lod in scene.lod_list:
            if lod.replace_model_from_obj:
                smd_path = os.path.join(temp_path, f"{lod.replace_model_from_obj.name}.smd")
                self.export_mesh_to_smd(lod.replace_model_from_obj, smd_path, False)
            
            if lod.replace_model_to_obj:
                smd_path = os.path.join(temp_path, f"{lod.replace_model_to_obj.name}.smd")
                self.export_mesh_to_smd(lod.replace_model_to_obj, smd_path, False)
        
        # Exporter les modèles shadowlod
        if scene.compilation_props.shadowlod_replace_from_obj:
            smd_path = os.path.join(temp_path, f"{scene.compilation_props.shadowlod_replace_from_obj.name}.smd")
            self.export_mesh_to_smd(scene.compilation_props.shadowlod_replace_from_obj, smd_path, False)
        
        if scene.compilation_props.shadowlod_replace_to_obj:
            smd_path = os.path.join(temp_path, f"{scene.compilation_props.shadowlod_replace_to_obj.name}.smd")
            self.export_mesh_to_smd(scene.compilation_props.shadowlod_replace_to_obj, smd_path, False)
        
        # Exporter la collision mesh
        if scene.compilation_props.collision_mesh:
            smd_path = os.path.join(temp_path, f"{scene.compilation_props.collision_mesh.name}.smd")
            self.export_mesh_to_smd(scene.compilation_props.collision_mesh, smd_path, True)
    
    def copy_files_to_game_dir(self, context, temp_path, game_dir):
        """Copie les fichiers SMD et QC vers le répertoire du jeu"""
        scene = context.scene
        
        # Copier les bodies
        for body in scene.body_list:
            if body.mesh_object:
                if isinstance(body.mesh_object, bpy.types.Collection):
                    body_filename = f"{body.mesh_object.name}.smd"
                else:
                    body_filename = f"{body.mesh_object.name}.smd"
                src = os.path.join(temp_path, body_filename)
                dst = os.path.join(game_dir, body_filename)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
        
        # Copier les modèles LOD
        for lod in scene.lod_list:
            if lod.replace_model_from_obj:
                src = os.path.join(temp_path, f"{lod.replace_model_from_obj.name}.smd")
                dst = os.path.join(game_dir, f"{lod.replace_model_from_obj.name}.smd")
                if os.path.exists(src):
                    shutil.copy2(src, dst)
            
            if lod.replace_model_to_obj:
                src = os.path.join(temp_path, f"{lod.replace_model_to_obj.name}.smd")
                dst = os.path.join(game_dir, f"{lod.replace_model_to_obj.name}.smd")
                if os.path.exists(src):
                    shutil.copy2(src, dst)
        
        # Copier les modèles shadowlod
        if scene.compilation_props.shadowlod_replace_from_obj:
            src = os.path.join(temp_path, f"{scene.compilation_props.shadowlod_replace_from_obj.name}.smd")
            dst = os.path.join(game_dir, f"{scene.compilation_props.shadowlod_replace_from_obj.name}.smd")
            if os.path.exists(src):
                shutil.copy2(src, dst)
        
        if scene.compilation_props.shadowlod_replace_to_obj:
            src = os.path.join(temp_path, f"{scene.compilation_props.shadowlod_replace_to_obj.name}.smd")
            dst = os.path.join(game_dir, f"{scene.compilation_props.shadowlod_replace_to_obj.name}.smd")
            if os.path.exists(src):
                shutil.copy2(src, dst)
        
        # Copier la collision
        if scene.compilation_props.collision_mesh:
            src = os.path.join(temp_path, f"{scene.compilation_props.collision_mesh.name}.smd")
            dst = os.path.join(game_dir, f"{scene.compilation_props.collision_mesh.name}.smd")
            if os.path.exists(src):
                shutil.copy2(src, dst)
        
        # Copier le QC
        src = os.path.join(temp_path, "model_compile.qc")
        dst = os.path.join(game_dir, "model_compile.qc")
        if os.path.exists(src):
            shutil.copy2(src, dst)
    
    def export_collection_to_smd(self, collection, path, is_collision_smd):
        """Exporte tous les meshes d'une collection en SMD"""
        # Récupérer tous les objets mesh de la collection
        mesh_objects = [obj for obj in collection.all_objects if obj.type == 'MESH']
        
        if not mesh_objects:
            raise Exception(f"No mesh objects found in collection '{collection.name}'")
        
        current_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        # Écrire l'en-tête du SMD
        with open(path, "w") as f:
            f.write("version 1\nnodes\n0 \"root\" -1\nend\nskeleton\ntime 0\n0 0 0 0 0 0 0\nend\ntriangles\n")
            
            sb = StringIO()
            
            # Exporter chaque mesh
            for obj in mesh_objects:
                depsgraph = bpy.context.evaluated_depsgraph_get()
                object_eval = obj.evaluated_get(depsgraph)
                mesh = object_eval.to_mesh()
                mesh.calc_loop_triangles()
                mesh.transform(obj.matrix_world)
                
                has_materials = len(obj.material_slots) > 0
                
                if is_collision_smd:
                    self.export_mesh_smd_collision(sb, mesh)
                else:
                    if has_materials:
                        self.export_mesh_smd_with_materials(sb, obj, mesh)
                    else:
                        self.export_mesh_smd_no_materials(sb, mesh)
            
            f.write(sb.getvalue())
            f.write("end\n")
        
        if current_mode != 'OBJECT' and bpy.context.object:
            bpy.ops.object.mode_set(mode=current_mode)
    
    def export_mesh_to_smd(self, obj, path, is_collision_smd):
        """Exporte un mesh en SMD - adapté de SanjiMDL"""
        current_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        depsgraph = bpy.context.evaluated_depsgraph_get()
        object_eval = obj.evaluated_get(depsgraph)
        mesh = object_eval.to_mesh()
        mesh.calc_loop_triangles()
        mesh.transform(obj.matrix_world)
        
        with open(path, "w") as f:
            f.write("version 1\nnodes\n0 \"root\" -1\nend\nskeleton\ntime 0\n0 0 0 0 0 0 0\nend\ntriangles\n")
            
            sb = StringIO()
            has_materials = len(obj.material_slots) > 0
            
            if is_collision_smd:
                self.export_mesh_smd_collision(sb, mesh)
            else:
                if has_materials:
                    self.export_mesh_smd_with_materials(sb, obj, mesh)
                else:
                    self.export_mesh_smd_no_materials(sb, mesh)
            
            f.write(sb.getvalue())
            f.write("end\n")
        
        if current_mode != 'OBJECT' and bpy.context.object:
            bpy.ops.object.mode_set(mode=current_mode)
    
    def export_mesh_smd_collision(self, sb, mesh):
        """Export collision mesh"""
        for tri in mesh.loop_triangles:
            material_name = "Phy"
            
            vert_a = mesh.vertices[tri.vertices[0]]
            vert_b = mesh.vertices[tri.vertices[1]]
            vert_c = mesh.vertices[tri.vertices[2]]
            
            pos_a = vert_a.co
            pos_b = vert_b.co
            pos_c = vert_c.co
            
            normal_a = vert_a.normal
            normal_b = vert_b.normal
            normal_c = vert_c.normal
            
            uv_a = mesh.uv_layers.active.data[tri.loops[0]].uv if mesh.uv_layers.active else (0.0, 0.0)
            uv_b = mesh.uv_layers.active.data[tri.loops[1]].uv if mesh.uv_layers.active else (0.0, 0.0)
            uv_c = mesh.uv_layers.active.data[tri.loops[2]].uv if mesh.uv_layers.active else (0.0, 0.0)
            
            sb.write(f"{material_name}\n0  {pos_a.x:.6f} {pos_a.y:.6f} {pos_a.z:.6f}  {normal_a.x:.6f} {normal_a.y:.6f} {normal_a.z:.6f}  {uv_a[0]:.6f} {uv_a[1]:.6f} 0\n0  {pos_b.x:.6f} {pos_b.y:.6f} {pos_b.z:.6f}  {normal_b.x:.6f} {normal_b.y:.6f} {normal_b.z:.6f}  {uv_b[0]:.6f} {uv_b[1]:.6f} 0\n0  {pos_c.x:.6f} {pos_c.y:.6f} {pos_c.z:.6f}  {normal_c.x:.6f} {normal_c.y:.6f} {normal_c.z:.6f}  {uv_c[0]:.6f} {uv_c[1]:.6f} 0\n")
    
    def export_mesh_smd_with_materials(self, sb, obj, mesh):
        """Export mesh with materials"""
        for tri in mesh.loop_triangles:
            material_name = obj.material_slots[tri.material_index].name if tri.material_index < len(obj.material_slots) else "default"
            
            vert_a = mesh.vertices[tri.vertices[0]]
            vert_b = mesh.vertices[tri.vertices[1]]
            vert_c = mesh.vertices[tri.vertices[2]]
            
            pos_a = vert_a.co
            pos_b = vert_b.co
            pos_c = vert_c.co
            
            normal_a = vert_a.normal
            normal_b = vert_b.normal
            normal_c = vert_c.normal
            
            if not tri.use_smooth:
                normal = (pos_b - pos_a).cross(pos_c - pos_a).normalized()
                normal_a = normal
                normal_b = normal
                normal_c = normal
            
            uv_a = mesh.uv_layers.active.data[tri.loops[0]].uv if mesh.uv_layers.active else (0.0, 0.0)
            uv_b = mesh.uv_layers.active.data[tri.loops[1]].uv if mesh.uv_layers.active else (0.0, 0.0)
            uv_c = mesh.uv_layers.active.data[tri.loops[2]].uv if mesh.uv_layers.active else (0.0, 0.0)
            
            sb.write(f"{material_name}\n0  {pos_a.x:.6f} {pos_a.y:.6f} {pos_a.z:.6f}  {normal_a.x:.6f} {normal_a.y:.6f} {normal_a.z:.6f}  {uv_a[0]:.6f} {uv_a[1]:.6f} 0\n0  {pos_b.x:.6f} {pos_b.y:.6f} {pos_b.z:.6f}  {normal_b.x:.6f} {normal_b.y:.6f} {normal_b.z:.6f}  {uv_b[0]:.6f} {uv_b[1]:.6f} 0\n0  {pos_c.x:.6f} {pos_c.y:.6f} {pos_c.z:.6f}  {normal_c.x:.6f} {normal_c.y:.6f} {normal_c.z:.6f}  {uv_c[0]:.6f} {uv_c[1]:.6f} 0\n")
    
    def export_mesh_smd_no_materials(self, sb, mesh):
        """Export mesh without materials"""
        for tri in mesh.loop_triangles:
            material_name = "None"
            
            vert_a = mesh.vertices[tri.vertices[0]]
            vert_b = mesh.vertices[tri.vertices[1]]
            vert_c = mesh.vertices[tri.vertices[2]]
            
            pos_a = vert_a.co
            pos_b = vert_b.co
            pos_c = vert_c.co
            
            normal_a = vert_a.normal
            normal_b = vert_b.normal
            normal_c = vert_c.normal
            
            if not tri.use_smooth:
                normal = (pos_b - pos_a).cross(pos_c - pos_a).normalized()
                normal_a = normal
                normal_b = normal
                normal_c = normal
            
            uv_a = mesh.uv_layers.active.data[tri.loops[0]].uv if mesh.uv_layers.active else (0.0, 0.0)
            uv_b = mesh.uv_layers.active.data[tri.loops[1]].uv if mesh.uv_layers.active else (0.0, 0.0)
            uv_c = mesh.uv_layers.active.data[tri.loops[2]].uv if mesh.uv_layers.active else (0.0, 0.0)
            
            sb.write(f"{material_name}\n0  {pos_a.x:.6f} {pos_a.y:.6f} {pos_a.z:.6f}  {normal_a.x:.6f} {normal_a.y:.6f} {normal_a.z:.6f}  {uv_a[0]:.6f} {uv_a[1]:.6f} 0\n0  {pos_b.x:.6f} {pos_b.y:.6f} {pos_b.z:.6f}  {normal_b.x:.6f} {normal_b.y:.6f} {normal_b.z:.6f}  {uv_b[0]:.6f} {uv_b[1]:.6f} 0\n0  {pos_c.x:.6f} {pos_c.y:.6f} {pos_c.z:.6f}  {normal_c.x:.6f} {normal_c.y:.6f} {normal_c.z:.6f}  {uv_c[0]:.6f} {uv_c[1]:.6f} 0\n")
    
    def run_studiomdl(self, context, game_dir):
        """Exécute studiomdl.exe"""
        props = context.scene.compilation_props
        
        if not os.path.exists(game_dir):
            raise Exception(f"Game directory not found: {game_dir}")
        
        if not os.path.exists(props.studiomdl_path):
            raise Exception(f"studiomdl.exe not found: {props.studiomdl_path}")
        
        qc_full_path = os.path.join(game_dir, "model_compile.qc")
        
        if not os.path.exists(qc_full_path):
            raise Exception(f"QC file not found: {qc_full_path}")
        
        print(f"[DEBUG] studiomdl path: {props.studiomdl_path}")
        print(f"[DEBUG] game directory: {game_dir}")
        print(f"[DEBUG] QC file: {qc_full_path}")
        print(f"[DEBUG] Working directory: {game_dir}")
        
        # Vérifier que studiomdl.exe est bien exécutable
        if not os.access(props.studiomdl_path, os.X_OK):
            print(f"[WARNING] studiomdl.exe may not be executable")
        
        studiomdl_args = [
            props.studiomdl_path,
            "-game", game_dir,
            "-nop4",
            qc_full_path
        ]
        
        print(f"[DEBUG] Command: {' '.join(studiomdl_args)}")
        
        try:
            result = subprocess.run(
                studiomdl_args, 
                cwd=game_dir,
                capture_output=True,
                text=True,
                timeout=120,
                shell=False
            )
            
            # Afficher la sortie pour debug
            print(f"[STUDIOMDL] Return code: {result.returncode}")
            if result.stdout:
                print(f"[STUDIOMDL STDOUT]\n{result.stdout}")
            if result.stderr:
                print(f"[STUDIOMDL STDERR]\n{result.stderr}")
            
            if result.returncode != 0:
                error_msg = f"studiomdl.exe failed with exit code {result.returncode}"
                if result.stderr:
                    error_msg += f"\nSTDERR: {result.stderr}"
                if result.stdout:
                    error_msg += f"\nSTDOUT: {result.stdout}"
                raise Exception(error_msg)
        except FileNotFoundError as e:
            raise Exception(f"Cannot find studiomdl.exe: {e}")
        except subprocess.TimeoutExpired:
            raise Exception("studiomdl.exe timeout (exceeded 120 seconds)")
