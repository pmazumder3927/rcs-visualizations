#!/usr/bin/env python3
"""
Render script for the Creeping Waves Animation
"""

import subprocess
import sys
import os

def render_animation(animation_file="creeping_waves_animation.py", 
                    scene_class="CreepingWavesVisualization",
                    quality="h"):
    """Render the creeping waves animation
    
    Args:
        animation_file: The animation file to render
        scene_class: The scene class name
        quality: Quality setting (l, m, h, k for low, medium, high, 4K)
    """
    
    # Check if manim is installed
    try:
        import manim
        print(f"Manim version: {manim.__version__}")
    except ImportError:
        print("Manim not found. Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Render the animation
    print(f"Rendering {scene_class} from {animation_file}...")
    print(f"Quality: {quality}")
    
    # Use Cairo renderer by default as it's more stable
    cmd = [
        "manim", 
        f"-pq{quality}",  # preview with specified quality
        animation_file, 
        scene_class
    ]
    
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    print("Animation rendered successfully!")
    print("Output file should be in the media/videos/ directory")

def main():
    """Main function with command line options"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Render Creeping Waves Animation")
    parser.add_argument(
        "--version",
        choices=["basic", "enhanced"],
        default="basic",
        help="Which version to render (basic or enhanced)"
    )
    parser.add_argument(
        "--quality",
        choices=["l", "m", "h", "k"],
        default="h",
        help="Render quality: l=low, m=medium, h=high, k=4K"
    )
    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Don't preview after rendering"
    )
    
    args = parser.parse_args()
    
    # Determine which file and class to render
    if args.version == "enhanced":
        animation_file = "creeping_waves_enhanced.py"
        scene_class = "CreepingWavesEnhanced"
    else:
        animation_file = "creeping_waves_animation.py"
        scene_class = "CreepingWavesVisualization"
    
    print(f"Rendering {args.version} version...")
    
    # Modify command if no preview
    if args.no_preview:
        # TODO: Implement no-preview option
        pass
    
    render_animation(animation_file, scene_class, args.quality)
    
    print("\nTips:")
    print("- Use --version=enhanced for the detailed physics explanation")
    print("- Use --quality=l for faster preview renders")
    print("- The output will be in media/videos/")

if __name__ == "__main__":
    main() 