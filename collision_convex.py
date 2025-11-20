import bpy
from mathutils import Vector

def create_simple_box_from_object(obj):
    """Crée une boîte simple à partir d'un objet entier"""
    # Créer un cube à l'origine
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    cube = bpy.context.active_object

    # Copier la transformation de l'objet original
    cube.location = obj.location.copy()
    cube.rotation_euler = obj.rotation_euler.copy()
    cube.scale = obj.scale.copy()

    # Calculer la bounding box en espace local
    local_bbox = obj.bound_box
    min_x = min(corner[0] for corner in local_bbox)
    max_x = max(corner[0] for corner in local_bbox)
    min_y = min(corner[1] for corner in local_bbox)
    max_y = max(corner[1] for corner in local_bbox)
    min_z = min(corner[2] for corner in local_bbox)
    max_z = max(corner[2] for corner in local_bbox)

    # Centre local
    local_center = Vector((
        (min_x + max_x) / 2,
        (min_y + max_y) / 2,
        (min_z + max_z) / 2
    ))

    # Dimensions locales
    dimensions = Vector((
        max_x - min_x,
        max_y - min_y,
        max_z - min_z
    ))

    # Appliquer le décalage local au cube
    cube.location += cube.matrix_world.to_3x3() @ local_center

    # Définir les dimensions (en tenant compte du scale)
    cube.dimensions = Vector((
        dimensions.x * obj.scale.x,
        dimensions.y * obj.scale.y,
        dimensions.z * obj.scale.z
    ))

    return cube

def create_simple_collision():
    """Crée une boîte de collision pour chaque objet sélectionné"""
    selected_objects = bpy.context.selected_objects
    if not selected_objects:
        print("Erreur : Aucun objet sélectionné")
        return

    phy_collections = {}

    for obj in selected_objects:
        if obj.type != 'MESH':
            print(f"Erreur : L'objet '{obj.name}' doit être un mesh")
            continue

        # Récupérer la collection d'origine
        original_collection = None
        for col in bpy.data.collections:
            if obj.name in col.objects:
                original_collection = col
                break
        collection_name = original_collection.name if original_collection else "Scene"

        # Créer ou récupérer la collection _phy
        phy_collection_name = collection_name + "_phy"
        if phy_collection_name not in phy_collections:
            if phy_collection_name not in bpy.data.collections:
                phy_collection = bpy.data.collections.new(phy_collection_name)
                bpy.context.scene.collection.children.link(phy_collection)
            else:
                phy_collection = bpy.data.collections[phy_collection_name]
            phy_collections[phy_collection_name] = phy_collection
        else:
            phy_collection = phy_collections[phy_collection_name]

        # Créer la boîte de collision
        collision_box = create_simple_box_from_object(obj)
        collision_box.name = f"{obj.name}_collision"

        # Retirer de toutes les collections actuelles
        for col in collision_box.users_collection:
            col.objects.unlink(collision_box)

        # Ajouter à la collection _phy
        phy_collection.objects.link(collision_box)

    # Reselectionner les objets originaux
    bpy.ops.object.select_all(action='DESELECT')
    for obj in selected_objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = selected_objects[0]

    print("Boîtes de collision créées pour tous les objets sélectionnés.")

# ----------------------------------------
# Opérateur Blender pour le panel
# ----------------------------------------
class RELINKER_OT_CreateCollision(bpy.types.Operator):
    bl_idname = "lw_pannel.create_collision"
    bl_label = "Créer Collision (Convex Hull)"
    bl_description = "Crée une boîte de collision simple pour les objets sélectionnés"

    def execute(self, context):
        try:
            create_simple_collision()
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        return {'FINISHED'}
