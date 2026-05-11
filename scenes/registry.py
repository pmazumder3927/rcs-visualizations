"""
Scene Registry - Central location for all visualization scenes
Add new scenes here to automatically include them in render scripts
"""

SCENES = [
    {
        "module": "scenes.radar_facets_visualization",
        "class": "RadarFacetsVisualization",
        "name": "Radar Facets",
        "description": "Animation of radar hitting object with triangular facets and phase computation",
        "blog_section": "From math to code",
    },
    {
        "module": "scenes.deformation_vectors_visualization",
        "class": "DeformationVectorsVisualization",
        "name": "Deformation Vectors",
        "description": "Demonstrates how deformation vectors modify mesh geometry",
        "blog_section": "Deformation Vectors",
    },
    {
        "module": "scenes.voxel_topology_visualization",
        "class": "VoxelTopologyVisualization",
        "name": "Voxel Topology",
        "description": "Shows density-based topology optimization with voxels",
        "blog_section": "Density-Based Methods",
    },
    {
        "module": "scenes.optimizer_comparison_visualization",
        "class": "OptimizerComparisonVisualization",
        "name": "Optimizer Comparison",
        "description": "Compares gradient descent vs Adam optimizer on 3D loss landscape",
        "blog_section": "Adam!",
    },
    {
        "module": "scenes.creeping_waves_enhanced",
        "class": "CreepingWavesEnhanced",
        "name": "Creeping Waves Enhanced",
        "description": "Enhanced visualization of electromagnetic creeping waves",
        "blog_section": "Creepy Waves",
    },
    {
        "module": "scenes.creeping_waves_animation",
        "class": "CreepingWavesVisualization",
        "name": "Creeping Waves Basic",
        "description": "Basic creeping waves animation",
        "blog_section": "Creepy Waves",
    },
    {
        "module": "scenes.topopt",
        "class": "TopOptRCS",
        "name": "Topology Optimization",
        "description": "Topology optimization for RCS reduction",
        "blog_section": "Designing a shape",
    },
]


def get_scene_by_name(name):
    """Get scene info by name (case insensitive)"""
    for scene in SCENES:
        if scene["name"].lower() == name.lower():
            return scene
    return None


def get_scene_by_class(class_name):
    """Get scene info by class name"""
    for scene in SCENES:
        if scene["class"] == class_name:
            return scene
    return None
