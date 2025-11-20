from bpy.props import StringProperty, BoolProperty, IntProperty, PointerProperty
import bpy

# Import des opérateurs et panels depuis leurs modules respectifs
from .relink_textures import RELINKER_OT_RelinkTextures
from .lod_generator import RELINKER_OT_CreateLODs
from .mirror import RELINKER_OT_MirrorObject
from .separators import RELINKER_OT_SeparateSelected, RELINKER_OT_SeparateLoose
from .cleanup import RELINKER_OT_MergeByDistance, RELINKER_OT_ClearCustomNormals
from .quality import RELINKER_OT_IncreaseQuality, RELINKER_OT_ApplyQuality
from .panel import RELINKER_PT_Panel
from .texturecleaner import RELINKER_OT_RemoveUnusedMaterials #, RELINKER_OT_SelectObjectsWithSameMaterials
from .updater import RELINKER_OT_UpdateAddon
from .retargetanim import LW_OT_retarget_anim_auto
from .psk_category import LW_OT_RenamePSKBones, LW_OT_CorrectValveBoneRoll, LW_OT_ScaleToGmod
from .usdz import LW_OT_RenameUSDZBones


class RelinkerProperties(bpy.types.PropertyGroup):
    folder_path: StringProperty(
        name="Dossier de Textures",
        subtype='DIR_PATH'
    )
    mirror_axis_x: BoolProperty(name="X", default=True)
    mirror_axis_y: BoolProperty(name="Y", default=False)
    mirror_axis_z: BoolProperty(name="Z", default=False)
    mirror_axis_neg_x: BoolProperty(name="-X", default=False)
    mirror_axis_neg_y: BoolProperty(name="-Y", default=False)
    mirror_axis_neg_z: BoolProperty(name="-Z", default=False)
    quality_level: IntProperty(
        name="Niveau de qualité",
        description="Niveau de subdivision (0 = aucun, 10 = très haute qualité)",
        default=2,
        min=0,
        max=10
    )

# Liste de toutes les classes à enregistrer
classes = (
    RelinkerProperties,
    RELINKER_PT_Panel,
    RELINKER_OT_RelinkTextures,
    RELINKER_OT_CreateLODs,
    RELINKER_OT_MirrorObject,
    RELINKER_OT_SeparateSelected,
    RELINKER_OT_SeparateLoose,
    RELINKER_OT_MergeByDistance,
    RELINKER_OT_ClearCustomNormals,
    RELINKER_OT_IncreaseQuality,
    RELINKER_OT_ApplyQuality,
    RELINKER_OT_RemoveUnusedMaterials,
    RELINKER_OT_UpdateAddon,
    # RELINKER_OT_SelectObjectsWithSameMaterials,
    LW_OT_retarget_anim_auto,
    LW_OT_RenamePSKBones,
    LW_OT_CorrectValveBoneRoll,
    LW_OT_ScaleToGmod,
    LW_OT_RenameUSDZBones,
)
