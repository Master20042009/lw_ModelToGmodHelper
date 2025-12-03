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


class BodyPropGroup(bpy.types.PropertyGroup):
    """Groupe de propriétés pour un $body"""
    name: bpy.props.StringProperty(
        name="Body Name",
        default="Body"
    )
    
    mesh_object: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Mesh",
        description="Mesh object for this body",
        poll=lambda self, obj: obj.type == 'MESH'
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
                f.write(f'$cdmaterials "{props.cdmaterials}"\n\n')
            
            # Options
            if props.staticprop:
                f.write('$staticprop\n\n')
            
            f.write(f'$surfaceprop "{props.surfaceprop}"\n')
            f.write('$contents "solid"\n\n')
            
            # Séquence par défaut
            f.write('$sequence "idle"\n{\n')
            f.write(f'\t"{scene.body_list[0].name}_ref.smd"\n')
            f.write('\tfps 30\n')
            f.write('}\n\n')
            
            # Collision
            if props.collision_mesh and props.collision_mesh.type == 'MESH':
                f.write('$collisionmodel "collision.smd"\n{\n')
                f.write(f'\t$mass {props.collision_mass}\n')
                f.write('\t$rootbone " "\n')
                f.write('}\n')
    
    def export_meshes(self, context, temp_path):
        """Exporte tous les meshes en SMD"""
        scene = context.scene
        os.makedirs(temp_path, exist_ok=True)
        
        for body in scene.body_list:
            smd_path = os.path.join(temp_path, f"{body.name}_ref.smd")
            self.export_mesh_to_smd(body.mesh_object, smd_path, False)
        
        if scene.compilation_props.collision_mesh:
            smd_path = os.path.join(temp_path, "collision.smd")
            self.export_mesh_to_smd(scene.compilation_props.collision_mesh, smd_path, True)
    
    def copy_files_to_game_dir(self, context, temp_path, game_dir):
        """Copie les fichiers SMD et QC vers le répertoire du jeu"""
        scene = context.scene
        
        for body in scene.body_list:
            src = os.path.join(temp_path, f"{body.name}_ref.smd")
            dst = os.path.join(game_dir, f"{body.name}_ref.smd")
            if os.path.exists(src):
                shutil.copy2(src, dst)
        
        if scene.compilation_props.collision_mesh:
            src = os.path.join(temp_path, "collision.smd")
            dst = os.path.join(game_dir, "collision.smd")
            if os.path.exists(src):
                shutil.copy2(src, dst)
        
        src = os.path.join(temp_path, "model_compile.qc")
        dst = os.path.join(game_dir, "model_compile.qc")
        if os.path.exists(src):
            shutil.copy2(src, dst)
    
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
