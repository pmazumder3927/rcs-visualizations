# Rendering reference

Operational details for running the Manim scenes locally.

## Quality presets

| Preset    | Resolution    | Use case                              |
| --------- | ------------- | ------------------------------------- |
| `preview` | 480p, 15 fps  | Iterating on a scene; opens player    |
| `low`     | 480p, 15 fps  | Same render, no preview popup         |
| `medium`  | 720p, 30 fps  | Reasonable share-quality output       |
| `high`    | 1080p, 60 fps | Publication / embed quality           |
| `4k`      | 2160p, 60 fps | Print masters (slow)                  |

```bash
./render all -q high             # everything, one scene at a time
./render all --parallel -q high  # everything, N processes
./render "Radar Facets" -q low   # just one
./render --list                  # see registered names
```

## Speed knobs

* **Drop the resolution.** Most scenes use `resolution=(20, 40)` or
  `(40, 40)` on `Surface` and `Sphere`. Halving those values is the
  biggest single render-time win on a laptop.
* **Trim animation count.** Iterative scenes (deformation, voxel,
  optimizer) loop 3 - 15 times. Cut the loop count when iterating on
  visuals; the physics story works at 2 iterations.
* **Skip ahead.** Inside `construct`, call `self.next_section("name")`
  to mark a chapter, then render only that chapter with
  `manim ... --section name`.

## Cleaning up

Manim leaves a `media/` cache (partial-movie chunks, TeX cache, etc.)
that grows fast across iterative renders:

```bash
python scripts/clean.py
```

Rebuilds are cheap — manim re-renders only the animations whose
inputs changed.

## Output paths

Final MP4s land in:

```
media/videos/<filename_without_py>/<height>p<fps>/<SceneName>.mp4
```

e.g. `media/videos/radar_facets_visualization/1080p60/RadarFacetsVisualization.mp4`.

## Authoring a new scene

1. Drop a file under `scenes/` whose class inherits from
   `scenes._common.RCSScene`. You inherit the dark background, default
   camera, `play_title(...)`, and HUD-text helpers automatically.
2. Append an entry to `scenes/registry.py` with the module path, class
   name, display name, and description. `./render --list` and the
   interactive menu pick the new scene up automatically.
3. Render once at `preview` quality to confirm it renders; promote to
   `high` for committed previews.
