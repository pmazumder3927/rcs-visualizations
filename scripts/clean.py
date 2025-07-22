#!/usr/bin/env python3
"""
Clean up media cache and temporary files
"""
import os
import shutil
from pathlib import Path

def clean_media_cache():
    """Remove partial movie files and cache"""
    media_dir = Path("media")
    
    if not media_dir.exists():
        print("No media directory found")
        return
    
    # Count files before cleaning
    total_before = sum(1 for _ in media_dir.rglob("*") if _.is_file())
    total_size_before = sum(f.stat().st_size for f in media_dir.rglob("*") if f.is_file()) / (1024 * 1024)
    
    # Remove partial movie files
    partial_files = list(media_dir.rglob("partial_movie_files"))
    for partial_dir in partial_files:
        if partial_dir.is_dir():
            print(f"Removing {partial_dir}")
            shutil.rmtree(partial_dir)
    
    # Remove Tex cache (can be regenerated)
    tex_dir = media_dir / "Tex"
    if tex_dir.exists():
        print(f"Removing {tex_dir}")
        shutil.rmtree(tex_dir)
    
    # Remove texts cache
    texts_dir = media_dir / "texts"
    if texts_dir.exists():
        print(f"Removing {texts_dir}")
        shutil.rmtree(texts_dir)
    
    # Count after cleaning
    total_after = sum(1 for _ in media_dir.rglob("*") if _.is_file()) if media_dir.exists() else 0
    total_size_after = sum(f.stat().st_size for f in media_dir.rglob("*") if f.is_file()) / (1024 * 1024) if media_dir.exists() else 0
    
    print(f"\nCleaning complete:")
    print(f"Files: {total_before} → {total_after} (-{total_before - total_after})")
    print(f"Size: {total_size_before:.1f}MB → {total_size_after:.1f}MB (-{total_size_before - total_size_after:.1f}MB)")

def clean_checkpoints():
    """Remove empty checkpoints directory"""
    checkpoints_dir = Path("checkpoints")
    if checkpoints_dir.exists() and not any(checkpoints_dir.iterdir()):
        print(f"Removing empty {checkpoints_dir}")
        checkpoints_dir.rmdir()

def main():
    """Main cleaning function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clean media cache and temporary files")
    parser.add_argument("--all", action="store_true", help="Clean everything")
    parser.add_argument("--media", action="store_true", help="Clean media cache only")
    parser.add_argument("--checkpoints", action="store_true", help="Clean checkpoints only")
    
    args = parser.parse_args()
    
    if not any([args.all, args.media, args.checkpoints]):
        args.all = True  # Default to all if nothing specified
    
    print("RCS Visualization Cleaner")
    print("=" * 50)
    
    if args.all or args.media:
        clean_media_cache()
    
    if args.all or args.checkpoints:
        clean_checkpoints()

if __name__ == "__main__":
    main()