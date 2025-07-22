# RCS Blog Post Visualizations

This directory contains Manim visualizations for the RCS (Radar Cross Section) calculations blog post. Each visualization corresponds to a `[VISUALIZATION REQUESTED]` tag in the blog.

## Visualizations

### 1. Radar Facets Visualization (`radar_facets_visualization.py`)
- **Scene**: `RadarFacetsVisualization`
- **Description**: Shows how radar waves interact with triangular facets on an object, demonstrating illumination detection and phase computation
- **Blog Section**: "From math to code" - demonstrates the discrete approximation process

### 2. Deformation Vectors Visualization (`deformation_vectors_visualization.py`)
- **Scene**: `DeformationVectorsVisualization`
- **Description**: Demonstrates how deformation vectors modify mesh geometry for shape optimization
- **Blog Section**: "Deformation Vectors" - shows the x_new = x_original + d concept

### 3. Voxel Topology Visualization (`voxel_topology_visualization.py`)
- **Scene**: `VoxelTopologyVisualization`
- **Description**: Shows density-based topology optimization with voxels being added/removed
- **Blog Section**: "Density-Based Methods" - demonstrates topology changes and hole creation

### 4. Optimizer Comparison Visualization (`optimizer_comparison_visualization.py`)
- **Scene**: `OptimizerComparisonVisualization`
- **Description**: Compares gradient descent vs Adam optimizer using a 3D loss landscape
- **Blog Section**: "Adam!" - shows the ball rolling on a hill analogy

## Rendering Instructions

### Quick Start
```bash
# Render all visualizations in high quality
python render_all_visualizations.py

# Or render individual scenes
manim -pqh radar_facets_visualization.py RadarFacetsVisualization
manim -pqh deformation_vectors_visualization.py DeformationVectorsVisualization
manim -pqh voxel_topology_visualization.py VoxelTopologyVisualization
manim -pqh optimizer_comparison_visualization.py OptimizerComparisonVisualization
```

### Quality Options
- `-ql`: Low quality (480p, 15fps) - Fast preview
- `-qm`: Medium quality (720p, 30fps)
- `-qh`: High quality (1080p, 60fps) - Recommended
- `-qk`: 4K quality (2160p, 60fps) - Best quality

### Output Location
Rendered videos will be saved in:
```
media/videos/<filename_without_py>/<quality>/SceneName.mp4
```

For example:
```
media/videos/radar_facets_visualization/1080p60/RadarFacetsVisualization.mp4
```

## Dependencies
- manim==0.18.0
- numpy>=1.21.0
- See requirements.txt for full list

## Customization

Each visualization can be customized by modifying:
- Colors and styles (look for color constants like `BLUE`, `GREEN`, etc.)
- Animation timing (look for `run_time` parameters)
- Camera angles (look for `set_camera_orientation` calls)
- Text and labels (look for `Text` and `MathTex` objects)

## Integration with Blog

When embedding in your blog post:
1. Export the videos from the media folder
2. Upload to your preferred video hosting service
3. Replace the `[VISUALIZATION REQUESTED]` tags with the video embeds

Each visualization is designed to be self-contained and explains the concept visually without requiring additional context.