# RCS Visualizations

Educational animations explaining Radar Cross Section (RCS) calculations and stealth physics using Manim.

Companion to [nighthawk_rcs](https://github.com/pmazumder3927/nighthawk_rcs) (Physical Optics RCS simulator + topology optimizer).

## Quick Start

```bash
# Render all visualizations with interactive menu
./render

# Quick parallel render (all scenes, preview quality)
./render all --parallel

# Render specific scene
./render "Radar Facets" -q high

# List available scenes
./render --list

# Clean media cache
python scripts/clean.py
```

## Project Structure

```
rcs-visualizations/
├── scenes/                # All visualization scenes
│   ├── registry.py       # Central registry of all scenes
│   ├── radar_facets_visualization.py
│   ├── deformation_vectors_visualization.py
│   ├── voxel_topology_visualization.py
│   ├── optimizer_comparison_visualization.py
│   ├── creeping_waves_enhanced.py
│   ├── creeping_waves_animation.py
│   └── topopt.py
├── scripts/              # Utility scripts
│   ├── render.py        # Universal render script
│   └── clean.py         # Clean media cache
├── docs/                # Documentation
│   ├── VISUALIZATIONS_README.md
│   ├── PERFORMANCE_TIPS.md
│   └── TESTING_SUMMARY.md
├── render               # Main render command
└── requirements.txt

```

## Available Scenes

All scenes are automatically discovered from `scenes/registry.py`. Current scenes include:

1. **Radar Facets** - Shows radar waves interacting with triangular facets
2. **Deformation Vectors** - Demonstrates mesh deformation for optimization
3. **Voxel Topology** - Density-based topology optimization
4. **Optimizer Comparison** - Gradient descent vs Adam optimizer
5. **Creeping Waves** - Electromagnetic wave propagation on curved surfaces
6. **Topology Optimization** - RCS reduction through shape optimization

## Adding New Scenes

1. Create your scene file in `scenes/`:
```python
# scenes/my_new_scene.py
from manim import *

class MyNewScene(Scene):
    def construct(self):
        # Your animation code
        pass
```

2. Register it in `scenes/registry.py`:
```python
SCENES = [
    # ... existing scenes ...
    {
        "module": "scenes.my_new_scene",
        "class": "MyNewScene",
        "name": "My New Scene",
        "description": "Description of what it shows",
        "blog_section": "Section name"
    }
]
```

3. Render it:
```bash
./render "My New Scene"
```

## Rendering Options

### Interactive Menu
```bash
./render
```
Provides an interactive menu to select quality and scenes.

### Command Line
```bash
# Render all scenes in parallel
./render all --parallel

# Render specific scenes
./render "Radar Facets" "Voxel Topology" -q medium

# Render with specific quality
./render all -q high  # Options: preview, low, medium, high, 4k

# Control parallel workers
./render all --parallel --workers 2
```

### Quality Presets

- **preview** (480p, 15fps) - Fastest, opens video after rendering
- **low** (480p, 15fps) - Fast, no preview
- **medium** (720p, 30fps) - Balanced quality/speed
- **high** (1080p, 60fps) - Publication quality
- **4k** (2160p, 60fps) - Maximum quality, very slow

## Performance Tips

For faster rendering:

1. Use preview quality during development:
   ```bash
   ./render "Scene Name" -q preview
   ```

2. Use parallel rendering for multiple scenes:
   ```bash
   ./render all --parallel
   ```

3. Clean media cache regularly:
   ```bash
   python scripts/clean.py
   ```

See `docs/PERFORMANCE_TIPS.md` for more optimization strategies.

## Physics Concepts Covered

### Radar Cross Section (RCS)
- How electromagnetic waves interact with objects
- Phase computation and interference
- Discrete approximation with triangular facets

### Shape Optimization
- Deformation vectors for smooth shape changes
- Density-based topology optimization
- Gradient descent vs advanced optimizers

### Wave Propagation
- Creeping waves on curved surfaces
- Surface currents and electromagnetic coupling
- Backscatter contributions

## Requirements

- Python 3.8+
- Manim 0.18.0
- NumPy, SciPy

Install dependencies:
```bash
pip install -r requirements.txt
```

## Output

Rendered videos are saved in:
```
media/videos/<scene_name>/<quality>/<SceneName>.mp4
```

## Documentation

- `docs/VISUALIZATIONS_README.md` - Detailed scene descriptions
- `docs/PERFORMANCE_TIPS.md` - Rendering optimization guide
- `docs/TESTING_SUMMARY.md` - Testing documentation

## Troubleshooting

1. **Slow rendering**: Use preview quality or parallel rendering
2. **Out of memory**: Clean media cache with `python scripts/clean.py`
3. **Import errors**: Ensure you're in the project root when running scripts

## Credits

Created as educational companion to radar cross-section physics explanations for blog posts on stealth technology and electromagnetic wave behavior.