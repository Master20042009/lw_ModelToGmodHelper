bl_info = {
    "name": "LW ModelToGmodHelper",
    "author": "LowWard",
    "version": (0, 1, 0),
    "blender": (4, 4, 3),
    "location": "View3D > Sidebar > LW / ModelToGmodHelper",
    "description": "Relink textures, génère des LODs, outils de nettoyage géométrique + Source Engine Compilation",
    "category": "Material",
}

import bpy
from . import config


def register():
    # Enregistrer toutes les classes
    for cls in config.classes:
        bpy.utils.register_class(cls)
    
    # Enregistrer les propriétés dans la scène
    bpy.types.Scene.relinker_props = bpy.props.PointerProperty(type=config.RelinkerProperties)
    bpy.types.Scene.compilation_props = bpy.props.PointerProperty(type=config.CompilationProperties)
    
    # Enregistrer les listes pour la compilation
    bpy.types.Scene.body_list = bpy.props.CollectionProperty(type=config.BodyPropGroup)
    bpy.types.Scene.body_list_index = bpy.props.IntProperty()
    bpy.types.Scene.sequence_list = bpy.props.CollectionProperty(type=config.SequencePropGroup)
    bpy.types.Scene.sequence_list_index = bpy.props.IntProperty()


def unregister():
    # Supprimer les propriétés de la scène
    del bpy.types.Scene.relinker_props
    del bpy.types.Scene.compilation_props
    del bpy.types.Scene.body_list
    del bpy.types.Scene.body_list_index
    del bpy.types.Scene.sequence_list
    del bpy.types.Scene.sequence_list_index
    
    # Désenregistrer toutes les classes
    for cls in reversed(config.classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()