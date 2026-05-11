"""Deformation vectors: smooth shape optimization for low RCS.

Surface optimizers expose each mesh vertex as a tunable handle. Letting
the solver push every vertex by its own little offset vector keeps the
topology intact while the silhouette migrates toward a stealthier shape.
This scene shows the deformation field, the resulting surface, and a
toy RCS bar-chart payoff.
"""

import numpy as np
from manim import (
    BLUE,
    BLUE_C,
    BLUE_E,
    DEGREES,
    DOWN,
    GREEN,
    GREEN_C,
    GREEN_E,
    LEFT,
    ORANGE,
    PI,
    RED,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Arrow3D,
    Create,
    Dot3D,
    FadeOut,
    Flash,
    MathTex,
    Rectangle,
    Surface,
    Text,
    Transform,
    VGroup,
    Write,
    interpolate_color,
)

from scenes._common import RCSScene, sphere_point

SPHERE_RADIUS = 2.0


def _sphere_mesh_points(num_points: int = 20, radius: float = SPHERE_RADIUS) -> np.ndarray:
    """Sample a sphere on a phi-theta grid for dot scatter."""
    phis = np.linspace(0, PI, num_points // 2)
    thetas = np.linspace(0, 2 * PI, num_points)
    points = [sphere_point(phi, theta, radius) for phi in phis for theta in thetas]
    return np.asarray(points)


def _deformation_at(point: np.ndarray) -> np.ndarray:
    """Smooth direction field used to perturb the base sphere."""
    norm = np.linalg.norm(point)
    theta = np.arctan2(point[1], point[0])
    phi = np.arccos(point[2] / norm)
    return np.array(
        [
            0.3 * np.sin(3 * theta) * np.sin(phi),
            0.2 * np.cos(2 * theta) * np.sin(phi),
            -0.1 * np.sin(phi),
        ]
    )


class DeformationVectorsVisualization(RCSScene):
    camera_kwargs = {"phi": 65 * DEGREES, "theta": -45 * DEGREES, "distance": 8}

    def construct(self):
        self.play_title(
            "Deformation Vectors: Shaping for Stealth",
            "How optimization algorithms modify geometry",
        )

        mesh_points = _sphere_mesh_points()[:100]
        mesh_dots = VGroup(*[Dot3D(point=p, radius=0.03, color=BLUE) for p in mesh_points])

        surface = Surface(
            lambda u, v: sphere_point(u, v, SPHERE_RADIUS),
            u_range=[0, PI],
            v_range=[0, 2 * PI],
            resolution=(20, 40),
            fill_color=BLUE_C,
            fill_opacity=0.3,
            stroke_color=BLUE_E,
            stroke_width=1,
        )

        shape_label = Text("Original Shape", font_size=20, color=BLUE)
        shape_label.to_edge(LEFT).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(shape_label)
        self.play(Create(surface), Create(mesh_dots), Write(shape_label), run_time=2)

        explanation = Text("Each point gets a deformation vector d", font_size=22)
        explanation.to_edge(DOWN).shift(UP * 0.5)
        formula = MathTex(
            r"\vec{x}_{\text{new}} = \vec{x}_{\text{original}} + \vec{d}",
            font_size=28,
        )
        formula.next_to(explanation, UP)
        self.add_fixed_in_frame_mobjects(explanation, formula)
        self.play(Write(explanation), Write(formula))

        # Visualize a subset of deformation arrows on the mesh.
        deformed_points = [p + _deformation_at(p) for p in mesh_points]
        deformation_vectors = VGroup(
            *[
                Arrow3D(start=p, end=q, color=ORANGE, thickness=0.02)
                for i, (p, q) in enumerate(zip(mesh_points, deformed_points))
                if i % 5 == 0
            ]
        )

        vector_label = Text("Deformation Vectors", font_size=20, color=ORANGE)
        vector_label.to_edge(RIGHT).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(vector_label)
        self.play(Create(deformation_vectors), Write(vector_label), run_time=2)
        self.wait(2)

        self.play(FadeOut(explanation), FadeOut(formula))

        deform_text = Text("Applying deformation...", font_size=22, color=YELLOW)
        deform_text.to_edge(DOWN).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(deform_text)
        self.play(Write(deform_text))

        deformed_dots = VGroup(*[Dot3D(point=p, radius=0.03, color=GREEN) for p in deformed_points])

        def deformed_surface_func(u, v):
            base = sphere_point(u, v, SPHERE_RADIUS)
            return base + _deformation_at(base)

        deformed_surface = Surface(
            deformed_surface_func,
            u_range=[0, PI],
            v_range=[0, 2 * PI],
            resolution=(20, 40),
            fill_color=GREEN_C,
            fill_opacity=0.3,
            stroke_color=GREEN_E,
            stroke_width=1,
        )

        self.play(
            Transform(mesh_dots, deformed_dots),
            Transform(surface, deformed_surface),
            run_time=3,
        )

        deformed_label = Text("Deformed Shape", font_size=20, color=GREEN)
        deformed_label.to_edge(LEFT).shift(DOWN * 2)
        self.add_fixed_in_frame_mobjects(deformed_label)
        self.play(FadeOut(shape_label), Write(deformed_label), FadeOut(deform_text))

        rcs_comparison = Text("RCS Comparison", font_size=24, weight="BOLD")
        rcs_comparison.to_edge(UP)
        self.add_fixed_in_frame_mobjects(rcs_comparison)
        self.play(Write(rcs_comparison))

        original_rcs = Rectangle(
            width=0.5, height=2.0, fill_color=BLUE, fill_opacity=0.8, stroke_color=WHITE
        )
        original_rcs.shift(LEFT * 2 + DOWN * 0.5)

        deformed_rcs = Rectangle(
            width=0.5,
            height=1.2,
            fill_color=GREEN,
            fill_opacity=0.8,
            stroke_color=WHITE,
        )
        deformed_rcs.shift(RIGHT * 2 + DOWN * 0.5)
        deformed_rcs.align_to(original_rcs, DOWN)

        original_label = Text("Original\nRCS: 1.0", font_size=16)
        original_label.next_to(original_rcs, DOWN)
        optimized_label = Text("Optimized\nRCS: 0.6", font_size=16)
        optimized_label.next_to(deformed_rcs, DOWN)

        improvement = Text("40% Reduction", font_size=20, color=YELLOW)
        improvement.next_to(deformed_rcs, RIGHT).shift(UP)

        self.add_fixed_in_frame_mobjects(
            original_rcs, deformed_rcs, original_label, optimized_label, improvement
        )
        self.play(
            Create(original_rcs),
            Create(deformed_rcs),
            Write(original_label),
            Write(optimized_label),
            run_time=2,
        )
        self.play(Write(improvement), Flash(improvement, color=YELLOW), run_time=1.5)

        self.play(
            FadeOut(
                VGroup(
                    original_rcs,
                    deformed_rcs,
                    original_label,
                    optimized_label,
                    improvement,
                )
            ),
            FadeOut(rcs_comparison),
        )

        iteration_title = Text("Iterative Optimization Process", font_size=24)
        iteration_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(iteration_title)
        self.play(Write(iteration_title))

        iteration_text = Text("Iteration: 1", font_size=20)
        iteration_text.to_edge(RIGHT).shift(DOWN * 2)
        self.add_fixed_in_frame_mobjects(iteration_text)
        self.play(Write(iteration_text))

        for i in range(3):
            new_text = Text(f"Iteration: {i + 2}", font_size=20)
            new_text.move_to(iteration_text)
            self.add_fixed_in_frame_mobjects(new_text)

            scale = 0.5 ** (i + 1)
            new_vectors = VGroup()
            for j in range(0, len(mesh_points), 5):
                point = mesh_dots[j].get_center()
                theta = np.arctan2(point[1], point[0])
                deformation = scale * np.array(
                    [
                        0.2 * np.sin(5 * theta),
                        0.1 * np.cos(4 * theta),
                        0.05 * np.sin(3 * theta),
                    ]
                )
                new_vectors.add(
                    Arrow3D(
                        start=point,
                        end=point + deformation,
                        color=interpolate_color(ORANGE, RED, i / 2),
                        thickness=0.015,
                    )
                )

            self.play(
                Transform(iteration_text, new_text),
                FadeOut(deformation_vectors),
                Create(new_vectors),
                run_time=1,
            )
            deformation_vectors = new_vectors
            self.play(
                mesh_dots.animate.shift(RIGHT * 0.1 * scale),
                surface.animate.shift(RIGHT * 0.1 * scale),
                run_time=1,
            )
            self.wait(0.5)

        self.play(FadeOut(deformation_vectors))

        final_text = Text(
            "Deformation vectors enable smooth shape changes\nwhile preserving mesh topology",
            font_size=22,
            color=YELLOW,
        )
        final_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(final_text)
        self.play(Write(final_text))

        self.move_camera(phi=45 * DEGREES, theta=-60 * DEGREES, distance=10, run_time=3)
        self.wait(3)
