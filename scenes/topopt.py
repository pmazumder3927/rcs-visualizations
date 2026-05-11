"""Topology optimization driving RCS down — toy demonstration.

NOT a real electromagnetic solver: the "RCS" is a stand-in proportional
to the projected cross-section of a sphere (RCS = pi r^2 in the optical
limit). The animation shows what every RCS-aware shape optimizer does in
principle: pick deformation directions that make the body smaller in the
high-sensitivity directions, then iterate.
"""

import numpy as np
from manim import (
    BLUE_D,
    BLUE_E,
    DEGREES,
    DOWN,
    GREEN,
    LEFT,
    RED,
    UL,
    UP,
    UR,
    YELLOW,
    Arrow3D,
    Create,
    DecimalNumber,
    FadeIn,
    FadeOut,
    Group,
    Surface,
    Tex,
    Text,
    ThreeDAxes,
    ValueTracker,
    Write,
    always_redraw,
)

from scenes._common import RCSScene


def fake_rcs(radius: float) -> float:
    """Toy model: RCS ∝ pi r^2 (sphere in the optical limit)."""
    return float(np.pi * radius**2)


def displacement_field(theta: float, strength: float = 0.15) -> float:
    """Per-vertex radial step. Negative on the rear hemisphere — that's
    where shrinking the silhouette pays off most for backscatter."""
    direction = 1 if np.cos(theta) > 0 else -2
    return strength * direction


class TopOptRCS(RCSScene):
    camera_kwargs = {"phi": 65 * DEGREES, "theta": -60 * DEGREES, "distance": 10}

    def construct(self):
        n_iterations = 5
        initial_radius = 2.0

        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        self.add(axes)

        radius_tracker = ValueTracker(initial_radius)
        rcs_tracker = (
            DecimalNumber(fake_rcs(initial_radius), num_decimal_places=2, include_sign=False)
            .to_corner(UR)
            .scale(0.8)
        )
        rcs_label = Text("RCS ≈ ", font="Ubuntu Mono").next_to(rcs_tracker, LEFT)
        self.add(rcs_label, rcs_tracker)

        sphere = always_redraw(
            lambda: Surface(
                lambda u, v: self._polar_to_xyz(u, v, radius_tracker.get_value()),
                u_range=[0, np.pi],
                v_range=[0, 2 * np.pi],
                resolution=(20, 40),
                fill_opacity=0.5,
                checkerboard_colors=[BLUE_E, BLUE_D],
            )
        )
        self.add(sphere)

        k_vec = Arrow3D(
            start=np.array([5.0, 0.0, 0.0]),
            end=np.array([2.8, 0.0, 0.0]),
            color=YELLOW,
        )
        k_label = Tex(r"$\vec{k}_\text{inc}$").next_to(k_vec, UP).set_color(YELLOW)
        self.add(k_vec, k_label)

        for itr in range(n_iterations):
            arrows = self._make_displacement_arrows(radius_tracker.get_value())
            self.play(
                *[Create(a, run_time=0.4) for a in arrows],
                lag_ratio=0.1,
            )

            new_radius = radius_tracker.get_value() * 0.9
            self.play(radius_tracker.animate.set_value(new_radius), run_time=0.8)
            self.play(FadeOut(Group(*arrows)), run_time=0.4)
            self.play(rcs_tracker.animate.set_value(fake_rcs(new_radius)), run_time=0.5)

            step_txt = Text(f"Iteration {itr + 1}", color="#ffffff", font="Ubuntu Mono").to_corner(
                UL
            )
            self.play(Write(step_txt), run_time=0.4)
            self.wait(0.6)
            self.play(FadeOut(step_txt))

        done = Text("Optimised shape → lower RCS", font="Ubuntu Mono", color=GREEN).to_edge(DOWN)
        self.play(FadeIn(done))
        self.wait(2)

    # ------------------------------------------------------------------ #
    # helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _polar_to_xyz(u: float, v: float, r: float) -> np.ndarray:
        """Convert (theta=u, phi=v) sphere coords to Cartesian."""
        return np.array(
            [
                r * np.sin(u) * np.cos(v),
                r * np.sin(u) * np.sin(v),
                r * np.cos(u),
            ]
        )

    def _make_displacement_arrows(self, r: float):
        arrows = []
        thetas = np.linspace(0, np.pi, 6)[1:-1]  # skip poles
        phis = np.linspace(0, 2 * np.pi, 10, endpoint=False)
        for theta in thetas:
            for phi in phis:
                pos = self._polar_to_xyz(theta, phi, r)
                delta = displacement_field(theta) * pos / np.linalg.norm(pos)
                arrows.append(
                    Arrow3D(
                        start=pos,
                        end=pos + delta,
                        stroke_width=1.2,
                        color=RED if displacement_field(theta) < 0 else GREEN,
                    )
                )
        return arrows
