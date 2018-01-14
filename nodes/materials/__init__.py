import bpy
from bpy.types import NodeTree
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem, NodeItemCustom
from ...ui import ICON_MATERIAL

# Import all material nodes just so they get registered
from .emission import LuxCoreNodeMatEmission
from .cloth import LuxCoreNodeMatCloth
from .glass import LuxCoreNodeMatGlass
from .glossytranslucent import LuxCoreNodeMatGlossyTranslucent
from .glossy2 import LuxCoreNodeMatGlossy2
from .glossycoating import LuxCoreNodeMatGlossyCoating
from .carpaint import LuxCoreNodeMatCarpaint
from .matte import LuxCoreNodeMatMatte
from .mattetranslucent import LuxCoreNodeMatMatteTranslucent
from .metal import LuxCoreNodeMatMetal
from .mirror import LuxCoreNodeMatMirror
from .mix import LuxCoreNodeMatMix
from .velvet import LuxCoreNodeMatVelvet
from .null import LuxCoreNodeMatNull
from .output import LuxCoreNodeMatOutput


class LuxCoreMaterialNodeTree(NodeTree):
    bl_idname = "luxcore_material_nodes"
    bl_label = "LuxCore Material Nodes"
    bl_icon = ICON_MATERIAL

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == "LUXCORE"

    @classmethod
    def get_from_context(cls, context):
        """
        Switches the displayed node tree when user selects object/material
        """
        obj = context.active_object

        if obj and obj.type not in {"LAMP", "CAMERA"}:
            mat = obj.active_material

            if mat:
                # ID pointer
                node_tree = mat.luxcore.node_tree

                if node_tree:
                    return node_tree, mat, mat

        return None, None, None

    # This block updates the preview, when socket links change
    def update(self):
        self.refresh = True

    def acknowledge_connection(self, context):
        while self.refresh:
            self.refresh = False
            break

    refresh = bpy.props.BoolProperty(name="Links Changed",
                                     default=False,
                                     update=acknowledge_connection)


class LuxCoreNodeCategoryMaterial(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "luxcore_material_nodes"


# Here we define the menu structure the user sees when he
# presses Shift+A in the node editor to add a new node.
# In general it is a good idea to put often used nodes near the top.
luxcore_node_categories_material = [
    LuxCoreNodeCategoryMaterial("LUXCORE_MATERIAL_MATERIAL", "Material", items=[
        NodeItem("LuxCoreNodeMatMix", label="Mix"),
        NodeItem("LuxCoreNodeMatMatte", label="Matte"),
        NodeItem("LuxCoreNodeMatMatteTranslucent", label="Matte Translucent"),
        NodeItem("LuxCoreNodeMatMetal", label="Metal"),
        NodeItem("LuxCoreNodeMatMirror", label="Mirror"),
        NodeItem("LuxCoreNodeMatGlossy2", label="Glossy"),
        NodeItem("LuxCoreNodeMatGlossyTranslucent", label="Glossy Translucent"),
        NodeItem("LuxCoreNodeMatGlossyCoating", label="Glossy Coating"),
        NodeItem("LuxCoreNodeMatGlass", label="Glass"),
        NodeItem("LuxCoreNodeMatNull", label="Null (Transparent)"),
        NodeItem("LuxCoreNodeMatCarpaint", label="Carpaint"),
        NodeItem("LuxCoreNodeMatCloth", label="Cloth"),
        NodeItem("LuxCoreNodeMatVelvet", label="Velvet"),        
    ]),

    LuxCoreNodeCategoryMaterial("LUXCORE_MATERIAL_TEXTURE", "Texture", items=[
        NodeItem("LuxCoreNodeTexColorMix", label="ColorMix"),
        NodeItem("LuxCoreNodeTexImagemap", label="Imagemap"),
        NodeItem("LuxCoreNodeTexFresnel", label="Fresnel"),
        NodeItem("LuxCoreNodeTexCheckerboard3D", label="3D Checkerboard"),
        NodeItem("LuxCoreNodeTexWrinkled", label="Wrinkled"),        
    ]),
    
    LuxCoreNodeCategoryMaterial("LUXCORE_MATERIAL_BLENDERTEXTURE", "Texture (Blender)", items=[
        NodeItem("LuxCoreNodeTexBlenderBlend", label="Blend"),
        NodeItem("LuxCoreNodeTexBlenderClouds", label="Clouds"),
        NodeItem("LuxCoreNodeTexBlenderDistortedNoise", label="Distorted Noise"),
        NodeItem("LuxCoreNodeTexBlenderMagic", label="Magic"),
        NodeItem("LuxCoreNodeTexBlenderMarble", label="Marble"),
        NodeItem("LuxCoreNodeTexBlenderMusgrave", label="Musgrave"),
        NodeItem("LuxCoreNodeTexBlenderStucci", label="Stucci"),
        NodeItem("LuxCoreNodeTexBlenderWood", label="Wood"),
        NodeItem("LuxCoreNodeTexBlenderVoronoi", label="Voronoi"),
    ]),
    
    LuxCoreNodeCategoryMaterial("LUXCORE_MATERIAL_UTILS", "Utils", items=[
        NodeItem("LuxCoreNodeTexColorAtDepth", label="Color at depth"),        
    ]),
   
    LuxCoreNodeCategoryMaterial("LUXCORE_MATERIAL_MAPPING", "Mapping", items=[
        NodeItem("LuxCoreNodeTexMapping2D", label="2D Mapping"),
        NodeItem("LuxCoreNodeTexMapping3D", label="3D Mapping"),
    ]),

    LuxCoreNodeCategoryMaterial("LUXCORE_MATERIAL_LIGHT", "Light", items=[
        NodeItem("LuxCoreNodeMatEmission", label="Light Emission"),
        NodeItem("LuxCoreNodeTexLampSpectrum", label="Lamp Spectrum"),
        NodeItem("LuxCoreNodeTexBlackbody", label="Lamp Blackbody Temperature"),
    ]),

    LuxCoreNodeCategoryMaterial("LUXCORE_MATERIAL_POINTER", "Pointer", items=[
        NodeItem("LuxCoreNodeTreePointer", label="Pointer"),
    ]),

    LuxCoreNodeCategoryMaterial("LUXCORE_MATERIAL_OUTPUT", "Output", items=[
        NodeItem("LuxCoreNodeMatOutput", label="Output"),
    ]),
]


def register():
    nodeitems_utils.register_node_categories("LUXCORE_MATERIAL_TREE", luxcore_node_categories_material)


def unregister():
    nodeitems_utils.unregister_node_categories("LUXCORE_MATERIAL_TREE")
