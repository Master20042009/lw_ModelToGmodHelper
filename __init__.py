bl_info = {
    "name": "LW ModelToGmodHelper",
    "author": "LowWard",
    "version": (0, 1),
    "blender": (4, 4, 3),
    "location": "View3D > Sidebar > LW / ModelToGmodHelper",
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
