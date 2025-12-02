import bpy
import os
import subprocess
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
    
    # Configuration de base
    game_name: bpy.props.StringProperty(
        name="Game",
        description="Name of the Source game",
        default="Garry's Mod"
    )
    
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
    
    # Model info
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
    
    # Collision
    collision_mesh: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Collision Mesh",
        description="Mesh object used for collision"
    )
    
    collision_concave: bpy.props.BoolProperty(
        name="$concave",
        description="Enable concave collision",
        default=False
    )
    
    collision_mass: bpy.props.FloatProperty(
        name="$mass",
        description="Mass in kilograms",
        default=250.0,
        min=0.1
    )
    
    collision_maxconvex: bpy.props.IntProperty(
        name="$maxconvexpieces",
        description="Maximum number of convex pieces",
        default=5,
        min=1
    )
    
    # General options
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
    
    illumposition_enable: bpy.props.BoolProperty(
        name="Enable $illumposition",
        default=False
    )
    
    illumposition: bpy.props.FloatVectorProperty(
        name="$illumposition",
        description="Illumination position",
        default=(0.0, 0.0, 50.0),
        size=3
    )
    
    constantdirectionallight: bpy.props.BoolProperty(
        name="$constantdirectionallight",
        description="Use constant directional lighting",
        default=False
    )
    
    ambientboost: bpy.props.BoolProperty(
        name="$ambientboost",
        description="Boost ambient lighting",
        default=False
    )
    
    casttextureshadows: bpy.props.BoolProperty(
        name="$casttextureshadows",
        description="Cast texture shadows",
        default=False
    )
    
    origin_enable: bpy.props.BoolProperty(
        name="Enable $origin",
        default=False
    )
    
    origin: bpy.props.FloatVectorProperty(
        name="$origin",
        description="Model origin offset",
        default=(0.0, 0.0, 0.0),
        size=3
    )
    
    skipboneinbbox: bpy.props.BoolProperty(
        name="$skipboneinbbox",
        description="Skip bone in bounding box calculation",
        default=False
    )


class BodyPropGroup(bpy.types.PropertyGroup):
    """Groupe de propriétés pour un $body"""
    name: bpy.props.StringProperty(
        name="Body Name",
        default="Body"
    )
    
    mesh_object: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Mesh",
        description="Mesh object for this body"
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
    
    activity: bpy.props.StringProperty(
        name="Activity",
        default="ACT_IDLE",
        description="Activity name for the sequence"
    )
    
    activity_weight: bpy.props.IntProperty(
        name="Activity Weight",
        default=1,
        min=1
    )
    
    fadein: bpy.props.FloatProperty(
        name="Fade In",
        default=0.2,
        min=0.0
    )
    
    fadeout: bpy.props.FloatProperty(
        name="Fade Out",
        default=0.2,
        min=0.0
    )
    
    fps: bpy.props.IntProperty(
        name="FPS",
        default=1,
        min=1
    )
    
    loop: bpy.props.BoolProperty(
        name="Loop",
        default=True
    )
    
    autoplay: bpy.props.BoolProperty(
        name="Autoplay",
        default=False
    )


# ==================== UI LISTS ====================

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
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='ANIM')


# ==================== OPERATORS ====================

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


class COMPILATION_OT_CompileModel(bpy.types.Operator):
    """Compiler le modèle avec les options avancées"""
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
        
        # Générer le QC
        temp_path = bpy.app.tempdir
        qc_path = os.path.join(temp_path, "model_compile.qc")
        
        try:
            self.generate_qc(context, qc_path)
            self.export_meshes(context)
            self.run_studiomdl(context, qc_path)
            self.report({'INFO'}, "Compilation successful!")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Compilation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}
    
    def generate_qc(self, context, qc_path):
        """Génère le fichier QC avec toutes les options"""
        scene = context.scene
        props = scene.compilation_props
        
        with open(qc_path, "w") as f:
            # $modelname
            f.write(f'$modelname "{props.modelname}"\n\n')
            
            # $body ou $bodygroup
            if len(scene.body_list) == 1:
                body = scene.body_list[0]
                f.write(f'$body "{body.name}" "{body.name}_ref.smd"\n\n')
            else:
                f.write('$bodygroup "Body"\n{\n')
                for body in scene.body_list:
                    f.write(f'\tstudio "{body.name}_ref.smd"\n')
                f.write('}\n\n')
            
            # $cdmaterials
            if props.cdmaterials:
                for cdmat in props.cdmaterials.split('\n'):
                    cdmat = cdmat.strip()
                    if cdmat:
                        f.write(f'$cdmaterials "{cdmat}"\n')
                f.write('\n')
            
            # Options générales
            if props.staticprop:
                f.write('$staticprop\n')
            
            f.write(f'$surfaceprop "{props.surfaceprop}"\n')
            
            if props.illumposition_enable:
                pos = props.illumposition
                f.write(f'$illumposition {pos[0]:.2f} {pos[1]:.2f} {pos[2]:.2f}\n')
            
            if props.constantdirectionallight:
                f.write('$constantdirectionallight 1\n')
            
            if props.ambientboost:
                f.write('$ambientboost 1\n')
            
            if props.casttextureshadows:
                f.write('$casttextureshadows\n')
            
            if props.origin_enable:
                org = props.origin
                f.write(f'$origin {org[0]:.2f} {org[1]:.2f} {org[2]:.2f}\n')
            
            if props.skipboneinbbox:
                f.write('$skipboneinbbox\n')
            
            f.write('\n')
            
            # Séquences
            if len(scene.sequence_list) > 0:
                for seq in scene.sequence_list:
                    if seq.enabled:
                        f.write(f'$sequence "{seq.name}"\n{{\n')
                        f.write(f'\t"{seq.name}.smd"\n')
                        f.write(f'\tactivity "{seq.activity}" {seq.activity_weight}\n')
                        f.write(f'\tfadein {seq.fadein}\n')
                        f.write(f'\tfadeout {seq.fadeout}\n')
                        f.write(f'\tfps {seq.fps}\n')
                        if seq.loop:
                            f.write('\tloop\n')
                        if seq.autoplay:
                            f.write('\tautoplay\n')
                        f.write('}\n\n')
            else:
                # Séquence par défaut
                f.write('$sequence "idle"\n{\n')
                f.write(f'\t"{scene.body_list[0].name}_ref.smd"\n')
                f.write('\tfps 1\n')
                f.write('}\n\n')
            
            # Collision
            if props.collision_mesh and props.collision_mesh.type == 'MESH':
                f.write('$collisionmodel "collision.smd"\n{\n')
                
                if props.collision_concave:
                    f.write('\t$concave\n')
                
                f.write(f'\t$mass {props.collision_mass}\n')
                f.write(f'\t$maxconvexpieces {props.collision_maxconvex}\n')
                f.write('\t$rootbone " "\n')
                f.write('}\n')
    
    def export_meshes(self, context):
        """Exporte tous les meshes en SMD"""
        scene = context.scene
        temp_path = bpy.app.tempdir
        
        # Exporter les bodies
        for body in scene.body_list:
            smd_path = os.path.join(temp_path, f"{body.name}_ref.smd")
            self.export_mesh_to_smd(body.mesh_object, smd_path)
        
        # Exporter la collision
        if scene.compilation_props.collision_mesh:
            smd_path = os.path.join(temp_path, "collision.smd")
            self.export_mesh_to_smd(scene.compilation_props.collision_mesh, smd_path)
    
    def export_mesh_to_smd(self, obj, path):
        """Exporte un mesh en SMD"""
        # Sauvegarder le mode actuel
        current_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        # Obtenir le mesh évalué
        depsgraph = bpy.context.evaluated_depsgraph_get()
        object_eval = obj.evaluated_get(depsgraph)
        mesh = object_eval.to_mesh()
        mesh.calc_loop_triangles()
        mesh.transform(obj.matrix_world)
        
        with open(path, "w") as f:
            # Header SMD
            f.write("version 1\n")
            f.write("nodes\n")
            f.write('0 "root" -1\n')
            f.write("end\n")
            f.write("skeleton\n")
            f.write("time 0\n")
            f.write("0 0.0 0.0 0.0 0.0 0.0 0.0\n")
            f.write("end\n")
            f.write("triangles\n")
            
            # Triangles
            for tri in mesh.loop_triangles:
                # Nom du matériau
                mat_name = "default"
                if len(obj.material_slots) > 0 and tri.material_index < len(obj.material_slots):
                    mat_name = obj.material_slots[tri.material_index].name
                
                f.write(f"{mat_name}\n")
                
                # Pour chaque vertex du triangle
                for i in range(3):
                    vert = mesh.vertices[tri.vertices[i]]
                    pos = vert.co
                    normal = vert.normal
                    
                    # UV (si disponible)
                    if mesh.uv_layers.active:
                        uv = mesh.uv_layers.active.data[tri.loops[i]].uv
                    else:
                        uv = (0.0, 0.0)
                    
                    f.write(f"0  {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}  ")
                    f.write(f"{normal.x:.6f} {normal.y:.6f} {normal.z:.6f}  ")
                    f.write(f"{uv[0]:.6f} {uv[1]:.6f} 0\n")
            
            f.write("end\n")
        
        # Restaurer le mode
        if current_mode != 'OBJECT' and bpy.context.object:
            bpy.ops.object.mode_set(mode=current_mode)
    
    def run_studiomdl(self, context, qc_path):
        """Exécute studiomdl.exe"""
        props = context.scene.compilation_props
        game_dir = os.path.dirname(props.gameinfo_path)
        
        # Vérifier que le chemin du jeu existe
        if not os.path.exists(game_dir):
            raise Exception(f"Game directory not found: {game_dir}")
        
        # Vérifier que le fichier QC existe
        if not os.path.exists(qc_path):
            raise Exception(f"QC file not found: {qc_path}")
        
        args = [
            props.studiomdl_path,
            "-game", game_dir,
            "-nop4",
            qc_path
        ]
        
        result = subprocess.run(args, capture_output=True, text=True, cwd=game_dir)
        
        # Afficher la sortie complète pour le débogage
        print(f"studiomdl output: {result.stdout}")
        print(f"studiomdl errors: {result.stderr}")
        
        if result.returncode != 0:
            error_msg = result.stderr if result.stderr else result.stdout
            raise Exception(f"studiomdl.exe failed with code {result.returncode}: {error_msg}")