"""Density-based topology optimization on a voxel grid.

Unlike vertex deformation, density methods give the optimizer the freedom
to add or remove material anywhere in a fixed bounding volume. Each voxel
carries a density rho in [0, 1] (air to solid). The optimizer drives rho
toward 0 or 1, and the resulting topology can punch holes that pure
shape-deformation simply cannot reach.
"""

import numpy as np
from manim import (
    BLUE_C,
    DEGREES,
    DOWN,
    GREEN,
    GREEN_C,
    LEFT,
    RED,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Create,
    Cube,
    FadeOut,
    MathTex,
    Square,
    Text,
    VGroup,
    Write,
    interpolate_color,
)

from scenes._common import RCSScene

GRID_SIZE = 8
VOXEL_SIZE = 0.4
VOXEL_PITCH = VOXEL_SIZE * 1.2


def _make_voxel(position: np.ndarray, color=BLUE_C) -> Cube:
    voxel = Cube(side_length=VOXEL_SIZE).move_to(position)
    voxel.set_color(color)
    voxel.set_stroke(WHITE, width=1)
    return voxel


def _voxel_position(i: int, j: int, k: int) -> np.ndarray:
    """World position of integer voxel index (i, j, k)."""
    return np.array(
        [
            (i - GRID_SIZE / 2) * VOXEL_PITCH,
            (j - GRID_SIZE / 2) * VOXEL_PITCH,
            (k - GRID_SIZE / 2) * VOXEL_PITCH,
        ]
    )


def _initial_wing_voxels() -> list[tuple[int, int, int, Cube]]:
    """Build the wing-shaped seed geometry."""
    voxels: list[tuple[int, int, int, Cube]] = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            for k in range(GRID_SIZE):
                x_norm = (i - GRID_SIZE / 2) / (GRID_SIZE / 2)
                y_norm = (j - GRID_SIZE / 2) / (GRID_SIZE / 2)
                z_norm = (k - GRID_SIZE / 2) / (GRID_SIZE / 2)
                if (
                    abs(y_norm) < 0.8
                    and abs(z_norm) < 0.3 - 0.2 * abs(x_norm)
                    and abs(x_norm) < 0.9
                ):
                    voxels.append((i, j, k, _make_voxel(_voxel_position(i, j, k))))
    return voxels


class VoxelTopologyVisualization(RCSScene):
    camera_kwargs = {"phi": 65 * DEGREES, "theta": -45 * DEGREES, "distance": 12}

    def construct(self):
        self.play_title(
            "Density-Based Topology Optimization",
            "Creating and removing material for optimal RCS",
        )

        voxels = _initial_wing_voxels()
        voxel_objects = VGroup(*(v[3] for v in voxels))

        self.play(Create(voxel_objects), run_time=2)

        initial_label = Text("Initial Design", font_size=20, color="#5dade2")
        initial_label.to_edge(LEFT).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(initial_label)
        self.play(Write(initial_label))

        explanation = Text("Each voxel has density ρ ∈ [0, 1]", font_size=22)
        explanation.to_edge(DOWN).shift(UP * 0.5)
        density_eq = MathTex(
            r"\rho = 0 \text{ (air)}, \quad \rho = 1 \text{ (material)}",
            font_size=24,
        )
        density_eq.next_to(explanation, UP)
        self.add_fixed_in_frame_mobjects(explanation, density_eq)
        self.play(Write(explanation), Write(density_eq))
        self.wait(2)

        self.play(FadeOut(explanation), FadeOut(density_eq), FadeOut(initial_label))

        opt_title = Text("Optimization in Progress...", font_size=24, color=YELLOW)
        opt_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(opt_title)
        self.play(Write(opt_title))

        density_scale = self._make_density_scale()
        self.add_fixed_in_frame_mobjects(density_scale)
        self.play(Create(density_scale))

        rng = np.random.default_rng(seed=7)

        for iteration in range(3):
            iter_text = Text(f"Iteration {iteration + 1}", font_size=20)
            iter_text.to_edge(RIGHT).shift(UP * 2)
            self.add_fixed_in_frame_mobjects(iter_text)
            self.play(Write(iter_text))

            current = {(i, j, k) for i, j, k, _ in voxels}
            voxels_to_remove = []
            for i, j, k, voxel in voxels:
                neighbours = sum(
                    1
                    for di in (-1, 0, 1)
                    for dj in (-1, 0, 1)
                    for dk in (-1, 0, 1)
                    if (i + di, j + dj, k + dk) in current
                )
                if neighbours > 20 and rng.random() < 0.3:
                    voxels_to_remove.append(voxel)

            voxels_to_add: list[tuple[int, int, int, Cube]] = []
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    for k in range(GRID_SIZE):
                        if (i, j, k) in current:
                            continue
                        adjacent = any(
                            (i + di, j + dj, k + dk) in current
                            for di in (-1, 0, 1)
                            for dj in (-1, 0, 1)
                            for dk in (-1, 0, 1)
                            if abs(di) + abs(dj) + abs(dk) == 1
                        )
                        if adjacent and rng.random() < 0.1:
                            new_voxel = _make_voxel(_voxel_position(i, j, k), color=GREEN_C)
                            new_voxel.set_opacity(0)
                            voxels_to_add.append((i, j, k, new_voxel))

            if voxels_to_remove:
                self.play(
                    *[v.animate.set_opacity(0.2).set_color(RED) for v in voxels_to_remove],
                    run_time=1,
                )
                self.play(*[FadeOut(v) for v in voxels_to_remove], run_time=1)

            if voxels_to_add:
                for i, j, k, voxel in voxels_to_add:
                    self.add(voxel)
                self.play(
                    *[v.animate.set_opacity(1) for _, _, _, v in voxels_to_add],
                    run_time=1,
                )
                self.play(
                    *[v.animate.set_color(BLUE_C) for _, _, _, v in voxels_to_add],
                    run_time=0.5,
                )
                voxels.extend(voxels_to_add)

            voxels = [v for v in voxels if v[3] not in voxels_to_remove]

            self.play(FadeOut(iter_text))
            self.wait(0.5)

        self.play(FadeOut(opt_title))

        final_title = Text("Optimized Topology", font_size=24, color=GREEN)
        final_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(final_title)
        self.play(Write(final_title))

        change_text = Text(
            "Material removed from low-sensitivity regions\nadded where it matters most",
            font_size=18,
            color=YELLOW,
        )
        change_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(change_text)
        self.play(Write(change_text))

        self.move_camera(phi=45 * DEGREES, theta=-60 * DEGREES, distance=10, run_time=3)
        self.wait(1)

        # Punching a hole - the topology change deformation cannot reach.
        self.play(FadeOut(change_text), FadeOut(density_scale))

        hole_title = Text("Key Advantage: Topology Changes", font_size=24)
        hole_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(hole_title)
        self.play(FadeOut(final_title), Write(hole_title))

        hole_demo = VGroup()
        for i in range(5):
            for j in range(5):
                for k in range(2):
                    pos = np.array([i * 0.5 - 1, j * 0.5 - 1, k * 0.5]) + RIGHT * 5
                    hole_demo.add(_make_voxel(pos))
        self.play(Create(hole_demo))

        center_voxels = []
        for i in range(1, 4):
            for j in range(1, 4):
                idx = i * 5 + j
                for k in range(2):
                    center_voxels.append(hole_demo[idx * 2 + k])

        hole_text = Text(
            "Creating internal voids — impossible with pure shape deformation",
            font_size=18,
        )
        hole_text.next_to(hole_demo, DOWN)
        self.add_fixed_in_frame_mobjects(hole_text)
        self.play(
            *[v.animate.set_color(RED).set_opacity(0.3) for v in center_voxels],
            Write(hole_text),
            run_time=1,
        )
        self.play(*[FadeOut(v) for v in center_voxels], run_time=1)

        summary = Text(
            "Density-based methods enable true topology changes\nat the cost of manufacturing constraints",
            font_size=20,
            color=YELLOW,
        )
        summary.to_edge(DOWN).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(summary)
        self.play(FadeOut(hole_text), Write(summary))

        self.move_camera(phi=70 * DEGREES, theta=45 * DEGREES, distance=12, run_time=3)
        self.wait(3)

    @staticmethod
    def _make_density_scale() -> VGroup:
        """Bottom-of-frame legend showing the air-to-solid density gradient."""
        items = VGroup()
        for i in range(11):
            density = i / 10
            color = interpolate_color(WHITE, BLUE_C, density)
            box = Square(side_length=0.3)
            box.set_fill(color, opacity=density if density > 0 else 0.1)
            box.set_stroke(WHITE, width=1)
            box.shift(RIGHT * (i - 5) * 0.35 + DOWN * 3)
            if i % 5 == 0:
                label = Text(f"{density:.1f}", font_size=12)
                label.next_to(box, DOWN, buff=0.1)
                items.add(label)
            items.add(box)

        title = Text("Density Scale", font_size=16)
        title.next_to(items, UP)
        items.add(title)
        return items
