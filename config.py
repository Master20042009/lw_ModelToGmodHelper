from bpy.props import StringProperty, BoolProperty, IntProperty, PointerProperty
import bpy

# Import des opérateurs et panels depuis leurs modules respectifs
from .relink_textures import RELINKER_OT_RelinkTextures
from .lod_generator import RELINKER_OT_CreateLODs
from .mirror import RELINKER_OT_MirrorObject
from .separators import RELINKER_OT_SeparateSelected, RELINKER_OT_SeparateLoose
from .cleanup import RELINKER_OT_MergeByDistance, RELINKER_OT_ClearCustomNormals
from .quality import RELINKER_OT_IncreaseQuality, RELINKER_OT_ApplyQuality
from .texturecleaner import RELINKER_OT_RemoveUnusedMaterials
from .updater import RELINKER_OT_UpdateAddon
from .retargetanim import LW_OT_retarget_anim_auto
from .psk_category import LW_OT_RenamePSKBones, LW_OT_CorrectValveBoneRoll, LW_OT_ScaleToGmod
from .usdz import LW_OT_RenameUSDZBones
from .collision_convex import RELINKER_OT_CreateCollision

# Import des modules de compilation (CORRIGÉ - ancien fichier mal orthographié supprimé)
from .compilation import (
    CompilationProperties,
    BodyPropGroup,
    SequencePropGroup,
    COMPILATION_UL_BodyList,
    COMPILATION_UL_SequenceList,
    COMPILATION_OT_AddBody,
    COMPILATION_OT_RemoveBody,
    COMPILATION_OT_AddSequence,
    COMPILATION_OT_RemoveSequence,
    COMPILATION_OT_CompileModel,
)

from .panel import (
    RELINKER_PT_Panel,
    COMPILATION_PT_MainPanel,
    COMPILATION_PT_CollisionPanel,
    COMPILATION_PT_GeneralOptionsPanel,
    COMPILATION_PT_SequencesPanel,
)


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
    # Propriétés
    RelinkerProperties,
    CompilationProperties,
    BodyPropGroup,
    SequencePropGroup,
    
    # UI Lists
    COMPILATION_UL_BodyList,
    COMPILATION_UL_SequenceList,
    
    # Panels
    RELINKER_PT_Panel,
    COMPILATION_PT_MainPanel,
    COMPILATION_PT_CollisionPanel,
    COMPILATION_PT_GeneralOptionsPanel,
    COMPILATION_PT_SequencesPanel,
    
    # Opérateurs originaux
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
    LW_OT_retarget_anim_auto,
    LW_OT_RenamePSKBones,
    LW_OT_CorrectValveBoneRoll,
    LW_OT_ScaleToGmod,
    LW_OT_RenameUSDZBones,
    RELINKER_OT_CreateCollision,
    
    # Nouveaux opérateurs de compilation
    COMPILATION_OT_AddBody,
    COMPILATION_OT_RemoveBody,
    COMPILATION_OT_AddSequence,
    COMPILATION_OT_RemoveSequence,
    COMPILATION_OT_CompileModel,
)