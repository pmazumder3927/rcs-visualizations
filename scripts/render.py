#!/usr/bin/env python3
"""
Universal render script for all RCS visualizations
Automatically discovers scenes from the registry
"""

import concurrent.futures
import os
import subprocess
import sys
import time
from pathlib import Path

# Add parent directory to path to import scenes
sys.path.insert(0, str(Path(__file__).parent.parent))

from scenes.registry import SCENES

# Quality presets
QUALITY_PRESETS = {
    "preview": {
        "flag": "-pql",
        "name": "Preview (480p, 15fps)",
        "description": "Fastest - opens video after rendering",
    },
    "low": {
        "flag": "-ql",
        "name": "Low (480p, 15fps)",
        "description": "Fast - no preview",
    },
    "medium": {
        "flag": "-qm",
        "name": "Medium (720p, 30fps)",
        "description": "Balanced quality and speed",
    },
    "high": {
        "flag": "-qh",
        "name": "High (1080p, 60fps)",
        "description": "Publication quality",
    },
    "4k": {
        "flag": "-qk",
        "name": "4K (2160p, 60fps)",
        "description": "Maximum quality - very slow",
    },
}


PROJECT_ROOT = Path(__file__).parent.parent


def render_scene(scene_info, quality="preview", show_output=True):
    """Render a single scene"""
    module_path = scene_info["module"].replace(".", "/") + ".py"

    cmd = ["manim", QUALITY_PRESETS[quality]["flag"], module_path, scene_info["class"]]

    # Scenes import from ``scenes._common``, so manim must run with the project
    # root on PYTHONPATH and from the project root as the working directory.
    env = {**os.environ}
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{PROJECT_ROOT}{os.pathsep}{existing}" if existing else str(PROJECT_ROOT)

    if show_output:
        print(f"\n{'=' * 60}")
        print(f"Rendering: {scene_info['name']}")
        print(f"Description: {scene_info['description']}")
        print(f"Quality: {QUALITY_PRESETS[quality]['name']}")
        print(f"Command: {' '.join(cmd)}")
        print(f"{'=' * 60}\n")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT, env=env)

        if result.returncode == 0:
            if show_output:
                print(f"✓ Successfully rendered {scene_info['name']}")
            return True, scene_info["name"], None
        else:
            error_msg = result.stderr.split("\n")[-10:]  # Last 10 lines of error
            if show_output:
                print(f"✗ Error rendering {scene_info['name']}")
                print(f"  Error: {chr(10).join(error_msg)}")
            return False, scene_info["name"], chr(10).join(error_msg)

    except Exception as e:
        if show_output:
            print(f"✗ Exception while rendering {scene_info['name']}: {e}")
        return False, scene_info["name"], str(e)


def render_parallel(scenes, quality="preview", max_workers=4):
    """Render multiple scenes in parallel"""
    print(f"\nRendering {len(scenes)} scenes in parallel (max {max_workers} workers)...")
    print(f"Quality: {QUALITY_PRESETS[quality]['name']}\n")

    start_time = time.time()
    results = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_scene = {
            executor.submit(render_scene, scene, quality, show_output=False): scene
            for scene in scenes
        }

        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_scene):
            success, name, error = future.result()
            results.append((success, name, error))

            if success:
                print(f"✓ {name}")
            else:
                print(f"✗ {name}: {error if error else 'Failed'}")

    elapsed = time.time() - start_time
    successful = sum(1 for s, _, _ in results if s)

    print(f"\n{'=' * 60}")
    print(f"Completed in {elapsed:.1f} seconds")
    print(f"Successful: {successful}/{len(scenes)}")
    print(f"{'=' * 60}\n")

    return results


def interactive_menu():
    """Interactive menu for rendering"""
    print("RCS Visualization Renderer")
    print("=" * 50)
    print(f"\nFound {len(SCENES)} scenes in registry\n")

    # Quality selection
    print("Select quality:")
    for i, (key, preset) in enumerate(QUALITY_PRESETS.items(), 1):
        print(f"{i}. {preset['name']} - {preset['description']}")

    quality_choice = input("\nQuality [1-5] (default: 1): ").strip() or "1"
    quality_keys = list(QUALITY_PRESETS.keys())

    try:
        quality = quality_keys[int(quality_choice) - 1]
    except (ValueError, IndexError):
        quality = "preview"

    # Scene selection
    print("\n" + "=" * 50)
    print("Select scenes to render:")
    print("1. All scenes")
    print("2. Select by number")
    print("3. Select by blog section")
    print("4. Quick parallel render (all scenes)")

    render_choice = input("\nChoice [1-4] (default: 4): ").strip() or "4"

    if render_choice == "1":
        # Render all sequentially
        for scene in SCENES:
            render_scene(scene, quality)

    elif render_choice == "2":
        # Select specific scenes
        print("\nAvailable scenes:")
        for i, scene in enumerate(SCENES, 1):
            print(f"{i}. {scene['name']} - {scene['description']}")

        selections = input("\nEnter numbers separated by commas: ").strip()

        try:
            indices = [int(x.strip()) - 1 for x in selections.split(",")]
            for idx in indices:
                if 0 <= idx < len(SCENES):
                    render_scene(SCENES[idx], quality)
                else:
                    print(f"Invalid selection: {idx + 1}")
        except ValueError:
            print("Invalid input")

    elif render_choice == "3":
        # Select by blog section
        sections = {}
        for scene in SCENES:
            section = scene.get("blog_section", "Other")
            if section not in sections:
                sections[section] = []
            sections[section].append(scene)

        print("\nBlog sections:")
        section_list = list(sections.keys())
        for i, section in enumerate(section_list, 1):
            print(f"{i}. {section} ({len(sections[section])} scenes)")

        section_choice = input("\nSelect section: ").strip()

        try:
            section_idx = int(section_choice) - 1
            if 0 <= section_idx < len(section_list):
                selected_section = section_list[section_idx]
                for scene in sections[selected_section]:
                    render_scene(scene, quality)
        except ValueError:
            print("Invalid input")

    elif render_choice == "4":
        # Parallel render
        render_parallel(SCENES, quality)

    else:
        print("Invalid choice")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Render RCS visualizations")
    parser.add_argument("scenes", nargs="*", help="Scene names or 'all'")
    parser.add_argument(
        "-q",
        "--quality",
        choices=QUALITY_PRESETS.keys(),
        default="preview",
        help="Render quality",
    )
    parser.add_argument("-p", "--parallel", action="store_true", help="Render in parallel")
    parser.add_argument(
        "-w", "--workers", type=int, default=4, help="Max parallel workers (default: 4)"
    )
    parser.add_argument("-l", "--list", action="store_true", help="List available scenes")

    args = parser.parse_args()

    if args.list:
        print("\nAvailable scenes:")
        print("=" * 70)
        for i, scene in enumerate(SCENES, 1):
            print(f"{i}. {scene['name']:<25} {scene['description']}")
        print()
        return

    if not args.scenes:
        # Interactive mode
        interactive_menu()
    else:
        # Command line mode
        if "all" in args.scenes:
            scenes_to_render = SCENES
        else:
            scenes_to_render = []
            for name in args.scenes:
                # Try to match by name or class
                scene = None
                for s in SCENES:
                    if s["name"].lower() == name.lower() or s["class"].lower() == name.lower():
                        scene = s
                        break

                if scene:
                    scenes_to_render.append(scene)
                else:
                    print(f"Warning: Scene '{name}' not found")

        if scenes_to_render:
            if args.parallel:
                render_parallel(scenes_to_render, args.quality, args.workers)
            else:
                for scene in scenes_to_render:
                    render_scene(scene, args.quality)


if __name__ == "__main__":
    main()
