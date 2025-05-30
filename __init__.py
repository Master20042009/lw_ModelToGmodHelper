bl_info = {
    "name": "LW ModelToGmodHelper",
    "author": "Fratelo + ChatGPT",
    "version": (1, 3),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Relinker",
    "description": "Relink textures, génère des LODs, outils de nettoyage géométrique",
    "category": "Material",
}

import bpy
from . import config

def register():
    for cls in config.classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.relinker_props = bpy.props.PointerProperty(type=config.RelinkerProperties)

def unregister():
    for cls in reversed(config.classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.relinker_props

if __name__ == "__main__":
    register()
