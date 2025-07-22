# Performance Tips for Faster Rendering

## Quick Solutions

### 1. Use Preview Quality (Fastest)
```bash
# Single scene - 480p, 15fps with preview
manim -pql radar_facets_visualization.py RadarFacetsVisualization

# All scenes in parallel (very fast)
./render_fast.sh
```

### 2. Disable Caching (Sometimes Helps)
```bash
manim -ql --disable_caching your_scene.py YourScene
```

### 3. Use Specific Sections
If you only need to check part of an animation, use sections:
```python
# In your scene's construct method:
self.next_section("Part 1")
# ... some animations ...
self.next_section("Part 2")
# ... more animations ...
```

Then render only that section:
```bash
manim -ql your_scene.py YourScene --section "Part 1"
```

## Optimization Tips for the Code

### 1. Reduce Resolution
In the visualizations, look for resolution parameters:
```python
# Change from:
surface = Surface(..., resolution=(40, 40))
# To:
surface = Surface(..., resolution=(20, 20))
```

### 2. Simplify 3D Objects
```python
# Change from:
sphere = Sphere(radius=2, resolution=(40, 40))
# To:
sphere = Sphere(radius=2, resolution=(20, 20))
```

### 3. Reduce Animation Steps
```python
# Change from:
for i in range(15):  # Many steps
# To:
for i in range(5):   # Fewer steps
```

### 4. Disable Smooth Animations
```python
# Add to construct method:
self.renderer.skip_animations = True  # Just show final frame
```

## Hardware Acceleration

### Enable GPU Rendering (if available)
```bash
# Check if GPU is available
manim --help | grep gpu

# Use GPU if available
manim -ql --use_opengl_renderer your_scene.py YourScene
```

## Parallel Rendering

The `render_fast.sh` script runs all 4 visualizations in parallel, which can be 4x faster on multi-core systems.

## Quick Preview Workflow

1. **Initial Development**: Use `-pql` (preview low quality)
2. **Review**: Use `-qm` (medium quality) 
3. **Final Export**: Use `-qh` (high quality)

## Estimated Render Times

On a typical system:
- Preview (480p, 15fps): ~30 seconds per scene
- Low (480p, 15fps): ~30 seconds per scene
- Medium (720p, 30fps): ~1-2 minutes per scene
- High (1080p, 60fps): ~3-5 minutes per scene
- 4K (2160p, 60fps): ~10-15 minutes per scene

Using `render_fast.sh` with parallel rendering:
- All 4 scenes in preview: ~30-45 seconds total