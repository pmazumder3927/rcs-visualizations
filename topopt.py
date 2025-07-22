# topopt_rcs.py
#
# Concept demo – NOT a real EM solver!
# Requires: manim ≥ 0.18.0  (pip install manim)
from manim import *
import numpy as np

###############################################################################
# Helper: fake “RCS” model and displacement field
###############################################################################
def fake_rcs(radius: float) -> float:
    """
    Toy model: RCS ∝ radius² (spherical target, optical limit)
    We pretend optimisation wants to shrink *effective* radius.
    """
    return np.pi * radius ** 2

def displacement_field(theta: float, strength: float = 0.15) -> np.ndarray:
    """
    Simple radial displacement that flattens the back half of the sphere.
    Given polar angle θ (0 front, π back), return outward Δr direction.
    """
    # Push front points *out* a bit, pull back points *in* more
    direction = 1 if np.cos(theta) > 0 else -2   # emphasise back side
    return strength * direction

###############################################################################
# Main Scene
###############################################################################
class TopOptRCS(ThreeDScene):
    def construct(self):
        # Configurables -------------------------------------------------------
        n_iterations   = 5
        initial_radius = 2.0

        # 3‑D camera set‑up ---------------------------------------------------
        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        self.add(axes)

        # ValueTrackers for live parameters -----------------------------------
        radius_tracker = ValueTracker(initial_radius)
        rcs_tracker    = DecimalNumber(
            fake_rcs(initial_radius),
            num_decimal_places=2,
            include_sign=False
        ).to_corner(UR).scale(0.8)
        rcs_label = Text("RCS ≈ ", font="Ubuntu Mono").next_to(rcs_tracker, LEFT)
        self.add(rcs_label, rcs_tracker)

        # Sphere surface (updated each frame) ---------------------------------
        sphere = always_redraw(
            lambda: Surface(
                lambda u, v: self.polar_to_xyz(u, v, radius_tracker.get_value()),
                u_range=[0, np.pi],
                v_range=[0, 2 * np.pi],
                resolution=(20, 40),
                fill_opacity=0.5,
                checkerboard_colors=[BLUE_E, BLUE_D],
            )
        )
        self.add(sphere)
        # Incident plane‑wave arrow -------------------------------------------
        k_vec = Arrow3D(
            start=np.array([5, 0, 0]),
            end=np.array([2.8, 0, 0]),
            color=YELLOW,
        )
        k_label = Tex(r"$\vec{k}_\text{inc}$").next_to(k_vec, UP).set_color(YELLOW)
        self.add(k_vec, k_label)

        # Iterate -------------------------------------------------------------
        for itr in range(n_iterations):
            # -----------------------------------------------
            # 1) Draw “displacement” arrows on sphere shell
            # -----------------------------------------------
            disp_arrows = self.make_displacement_arrows(radius_tracker.get_value())
            self.play(
                AnimationGroup(*[Create(a, run_time=0.4) for a in disp_arrows]),
                lag_ratio=0.1
            )

            # -----------------------------------------------
            # 2) Update radius (mock optimisation step)
            #    shrink back hemisphere more than front
            # -----------------------------------------------
            new_radius = radius_tracker.get_value() * 0.9  # simple radial shrink
            self.play(radius_tracker.animate.set_value(new_radius), run_time=0.8)

            # -----------------------------------------------
            # 3) Fade displacement arrows
            # -----------------------------------------------
            self.play(FadeOut(Group(*disp_arrows)), run_time=0.4)

            # -----------------------------------------------
            # 4) Update displayed RCS
            # -----------------------------------------------
            new_rcs = fake_rcs(new_radius)
            self.play(rcs_tracker.animate.set_value(new_rcs), run_time=0.5)

            # Comment heading each iteration
            step_txt = Text(
                f"Iteration {itr+1}", color=WHITE, font="Ubuntu Mono"
            ).to_corner(UL)
            self.play(Write(step_txt), run_time=0.4)
            self.wait(0.6)
            self.play(FadeOut(step_txt))

        # Outro label ---------------------------------------------------------
        done = Text(
            "Optimised shape → lower RCS!", font="Ubuntu Mono", color=GREEN
        ).to_edge(DOWN)
        self.play(FadeIn(done))
        self.wait(2)

    # --------------------------------------------------------------------- #
    # Utilities
    # --------------------------------------------------------------------- #
    def polar_to_xyz(self, u: float, v: float, r: float) -> np.ndarray:
        """Convert (θ=u, φ=v) sphere coords to Cartesian."""
        return np.array([
            r * np.sin(u) * np.cos(v),
            r * np.sin(u) * np.sin(v),
            r * np.cos(u),
        ])

    def make_displacement_arrows(self, r: float):
        arrows = []
        # Sample a handful of surface points
        thetas = np.linspace(0, np.pi, 6)[1:-1]  # skip poles
        phis   = np.linspace(0, 2 * np.pi, 10, endpoint=False)
        for θ in thetas:
            for φ in phis:
                # Position on the sphere
                pos = self.polar_to_xyz(θ, φ, r)
                # Direction = ± radial normal scaled
                delta = displacement_field(θ) * pos / np.linalg.norm(pos)
                arrow = Arrow3D(
                    start=pos,
                    end=pos + delta,
                    stroke_width=1.2,
                    color=RED if displacement_field(θ) < 0 else GREEN,
                )
                arrows.append(arrow)
        return arrows