#!/usr/bin/env python3
"""
Script to render all RCS blog post visualizations
"""
import subprocess
import os

# List of visualization files and their scene names
visualizations = [
    {
        "file": "radar_facets_visualization.py",
        "scene": "RadarFacetsVisualization",
        "description": "Animation of radar hitting object with triangular facets"
    },
    {
        "file": "deformation_vectors_visualization.py", 
        "scene": "DeformationVectorsVisualization",
        "description": "Deformation vector demonstration"
    },
    {
        "file": "voxel_topology_visualization.py",
        "scene": "VoxelTopologyVisualization", 
        "description": "Voxel grid topology changes"
    },
    {
        "file": "optimizer_comparison_visualization.py",
        "scene": "OptimizerComparisonVisualization",
        "description": "Gradient descent vs Adam optimizer comparison"
    }
]

def render_visualization(viz_info, quality="high", preview=True):
    """Render a single visualization"""
    file_path = viz_info["file"]
    scene_name = viz_info["scene"]
    
    # Determine quality flag
    quality_flags = {
        "preview": "-pql",  # 480p, 15fps with preview
        "low": "-ql",       # 480p, 15fps
        "medium": "-qm",    # 720p, 30fps  
        "high": "-qh",      # 1080p, 60fps
        "4k": "-qk"         # 4K, 60fps
    }
    
    quality_flag = quality_flags.get(quality, "-qh")
    
    print(f"\n{'='*60}")
    print(f"Rendering: {viz_info['description']}")
    print(f"File: {file_path}")
    print(f"Scene: {scene_name}")
    print(f"Quality: {quality}")
    print(f"{'='*60}\n")
    
    # Construct manim command
    cmd = ["manim"]
    
    # Add quality flag
    if "-p" in quality_flag:
        cmd.append(quality_flag)
    else:
        cmd.append(quality_flag)
        if preview:
            cmd.append("-p")  # Add preview flag
    
    # Add file and scene
    cmd.extend([file_path, scene_name])
    
    try:
        # Run manim
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Successfully rendered {scene_name}")
            # Find output file
            output_dir = f"media/videos/{file_path[:-3]}/{quality}p60" if quality == "high" else f"media/videos/{file_path[:-3]}/480p15"
            output_file = f"{output_dir}/{scene_name}.mp4"
            if os.path.exists(output_file):
                print(f"  Output: {output_file}")
        else:
            print(f"✗ Error rendering {scene_name}")
            print(f"  Error: {result.stderr}")
            
    except Exception as e:
        print(f"✗ Exception while rendering {scene_name}: {e}")

def main():
    """Main function to render all visualizations"""
    print("RCS Blog Post Visualization Renderer")
    print("====================================\n")
    
    # Ask for quality preference
    print("Select rendering quality:")
    print("1. Preview (480p, 15fps) - Fastest, opens video after")
    print("2. Low (480p, 15fps) - Fast, no preview")
    print("3. Medium (720p, 30fps)")  
    print("4. High (1080p, 60fps) - Default")
    print("5. 4K (2160p, 60fps) - Slowest")
    
    quality_choice = input("\nEnter choice (1-5) [1]: ").strip() or "1"
    
    quality_map = {
        "1": "preview",
        "2": "low",
        "3": "medium",
        "4": "high",
        "5": "4k"
    }
    
    quality = quality_map.get(quality_choice, "preview")
    
    # Ask which to render
    print("\nWhich visualizations to render?")
    print("1. All visualizations")
    print("2. Select specific ones")
    
    render_choice = input("\nEnter choice (1-2) [1]: ").strip() or "1"
    
    if render_choice == "1":
        # Render all
        for viz in visualizations:
            render_visualization(viz, quality)
    else:
        # Select specific ones
        print("\nAvailable visualizations:")
        for i, viz in enumerate(visualizations):
            print(f"{i+1}. {viz['description']}")
        
        selections = input("\nEnter numbers separated by commas (e.g., 1,3): ").strip()
        
        try:
            indices = [int(x.strip()) - 1 for x in selections.split(",")]
            for idx in indices:
                if 0 <= idx < len(visualizations):
                    render_visualization(visualizations[idx], quality)
                else:
                    print(f"Invalid selection: {idx + 1}")
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
    
    print("\n" + "="*60)
    print("Rendering complete!")
    print("="*60)

if __name__ == "__main__":
    main()