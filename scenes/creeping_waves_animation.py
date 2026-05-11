"""Creeping waves: the basic story.

Specular reflection accounts for the bright forward returns from a
metallic body, but it does not explain why a smooth sphere keeps
returning energy when illuminated near-edge-on. The answer is creeping
waves — surface currents that propagate around the shadowed side and
re-radiate. This scene walks through the four stages: incidence,
coupling, propagation, and back-side radiation.
"""

import numpy as np
from manim import (
    BLUE,
    DEGREES,
    DOWN,
    GREEN,
    GREY_B,
    LEFT,
    ORANGE,
    PI,
    PURPLE,
    RED,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Arrow,
    Arrow3D,
    Circle,
    Create,
    Dot,
    FadeOut,
    MoveAlongPath,
    ParametricFunction,
    Sphere,
    Text,
    ThreeDAxes,
    VGroup,
    Write,
    linear,
    normalize,
)

from scenes._common import RCSScene


class CreepingWavesVisualization(RCSScene):
    camera_kwargs = {"phi": 70 * DEGREES, "theta": -45 * DEGREES, "distance": 12}

    def construct(self):
        self._introduce_concept()
        self._show_direct_reflection()
        self._show_surface_wave_formation()
        self._demonstrate_creeping_waves()
        self._show_backscatter_contribution()
        self._show_comparison()

    # -- sections -----------------------------------------------------------

    def _introduce_concept(self):
        title = Text("How Creeping Waves Form on Curved Surfaces", font_size=32)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.add_hud_text(title)
        self.play(Write(title))

        self.sphere = Sphere(radius=2, resolution=(30, 30))
        self.sphere.set_color(GREY_B)
        self.sphere.set_opacity(0.9)

        self.axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={"include_tip": False},
            x_length=6,
            y_length=6,
            z_length=6,
        )
        self.axes.set_opacity(0.3)

        self.play(Create(self.axes), Create(self.sphere), run_time=2)

        sphere_label = Text("Metallic Sphere", font_size=20)
        sphere_label.next_to(self.sphere, DOWN * 3)
        self.add_hud_text(sphere_label)
        self.play(Write(sphere_label))
        self.wait(1)

    def _show_direct_reflection(self):
        self.clear_hud_text()
        title = Text("Step 1: Direct (Specular) Reflection", font_size=28)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.add_hud_text(title)
        self.play(Write(title))

        incident_dir = normalize(np.array([1.0, 0.0, 0.0]))
        wave_start = np.array([-5.0, 0.0, 0.0])
        incident_ray = Arrow3D(
            start=wave_start,
            end=wave_start + 3 * incident_dir,
            color=BLUE,
            thickness=0.05,
        )
        incident_label = Text("Incident Wave", font_size=18, color=BLUE)
        incident_label.move_to(wave_start + LEFT)
        self.add_hud_text(incident_label)
        self.play(Create(incident_ray), Write(incident_label), run_time=1.5)

        impact_point = np.array([-2.0, 0.0, 0.0])
        impact_dot = Sphere(radius=0.1, resolution=(10, 10)).move_to(impact_point)
        impact_dot.set_color(YELLOW)
        self.play(Create(impact_dot))

        reflected_dir = normalize(np.array([-1.0, 0.0, 0.0]))
        reflected_ray = Arrow3D(
            start=impact_point,
            end=impact_point + 3 * reflected_dir,
            color=RED,
            thickness=0.05,
        )
        reflected_label = Text("Reflected Wave", font_size=18, color=RED)
        reflected_label.move_to(impact_point + LEFT * 3 + UP)
        self.add_hud_text(reflected_label)
        self.play(Create(reflected_ray), Write(reflected_label), run_time=1.5)

        explanation = Text("Most energy reflects like a mirror", font_size=20, color=WHITE)
        explanation.to_edge(DOWN).shift(UP * 0.5)
        self.add_hud_text(explanation)
        self.play(Write(explanation))
        self.wait(2)

        self.play(
            FadeOut(incident_ray),
            FadeOut(reflected_ray),
            FadeOut(impact_dot),
            run_time=1,
        )

    def _show_surface_wave_formation(self):
        self.clear_hud_text()
        title = Text("Step 2: Surface Wave Formation", font_size=28)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.add_hud_text(title)
        self.play(Write(title))

        wave_start = np.array([-5.0, -1.5, 0.0])
        impact_point = np.array([-1.8, -0.87, 0.0])
        incident_wave = Arrow3D(start=wave_start, end=impact_point, color=BLUE, thickness=0.05)
        self.play(Create(incident_wave))

        coupling_circle = Circle(radius=0.3, color=ORANGE).move_to(impact_point)
        coupling_circle.set_stroke(width=3)
        self.play(
            Create(coupling_circle),
            coupling_circle.animate.scale(1.5).set_opacity(0.5),
            run_time=1,
        )

        # Wave "hugs" the surface around the front quarter.
        surface_wave_path = ParametricFunction(
            lambda t: 2 * np.array([np.cos(PI - t), np.sin(PI - t), 0.0]),
            t_range=[0, PI / 2],
            color=ORANGE,
        ).set_stroke(width=4)

        wave_packet = Dot(radius=0.15, color=ORANGE).move_to(impact_point)

        explanation = Text(
            "Some energy couples into the surface and travels along it",
            font_size=20,
            color=WHITE,
        )
        explanation.to_edge(DOWN).shift(UP * 0.5)
        self.add_hud_text(explanation)

        self.play(Create(surface_wave_path), Write(explanation), run_time=1)
        self.play(MoveAlongPath(wave_packet, surface_wave_path), run_time=3, rate_func=linear)
        self.wait(1)

        self.surface_wave_path = surface_wave_path
        self.incident_wave = incident_wave

    def _demonstrate_creeping_waves(self):
        self.clear_hud_text()
        title = Text("Step 3: Creeping Wave Propagation", font_size=28)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.add_hud_text(title)
        self.play(Write(title))

        self.move_camera(phi=60 * DEGREES, theta=-30 * DEGREES, run_time=2)

        creeping_paths = VGroup()
        for z in np.linspace(-0.5, 0.5, 3):
            path = ParametricFunction(
                lambda t, z=z: 2.05 * np.array([np.cos(PI - t), np.sin(PI - t), z]),
                t_range=[0, 1.2 * PI],
                color=ORANGE,
            ).set_stroke(width=3, opacity=0.7)
            creeping_paths.add(path)

        self.play(Create(creeping_paths), run_time=2)

        wave_packets = VGroup()
        for path in creeping_paths:
            packet = Dot(radius=0.1, color=ORANGE).move_to(path.get_start())
            wave_packets.add(packet)

        explanation = Text(
            "Waves 'creep' around the curved surface, losing energy as they travel",
            font_size=20,
            color=WHITE,
        )
        explanation.to_edge(DOWN).shift(UP * 0.5)
        self.add_hud_text(explanation)
        self.play(Write(explanation))

        animations = []
        for packet, path in zip(wave_packets, creeping_paths):
            animations.append(MoveAlongPath(packet, path))
            animations.append(packet.animate.set_opacity(0.2).scale(0.5))
        self.play(*animations, run_time=4, rate_func=linear)
        self.wait(1)

        self.creeping_paths = creeping_paths

    def _show_backscatter_contribution(self):
        self.clear_hud_text()
        title = Text("Step 4: Backscatter from Creeping Waves", font_size=28)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.add_hud_text(title)
        self.play(Write(title))

        self.move_camera(phi=70 * DEGREES, theta=150 * DEGREES, run_time=2)

        back_points = [
            np.array([1.5, 0.0, 0.5]),
            np.array([1.5, 0.0, 0.0]),
            np.array([1.5, 0.0, -0.5]),
        ]

        radiation_waves = VGroup()
        for point in back_points:
            for r in np.linspace(0.2, 1.0, 3):
                circle = Circle(radius=r, color=PURPLE).move_to(point)
                circle.set_stroke(width=2, opacity=0.5)
                radiation_waves.add(circle)

        backscatter_arrows = VGroup(
            *[
                Arrow3D(
                    start=point,
                    end=point + np.array([-2.0, 0.0, 0.0]),
                    color=PURPLE,
                    thickness=0.03,
                )
                for point in back_points
            ]
        )

        explanation = Text(
            "Creeping waves radiate from the shadow region, adding extra backscatter",
            font_size=20,
            color=WHITE,
        )
        explanation.to_edge(DOWN).shift(UP * 0.5)
        self.add_hud_text(explanation)

        self.play(
            Create(radiation_waves),
            Create(backscatter_arrows),
            Write(explanation),
            run_time=2,
        )
        self.play(radiation_waves.animate.scale(1.5).set_opacity(0.1), run_time=2)
        self.wait(1)

    def _show_comparison(self):
        self.play(
            FadeOut(self.creeping_paths),
            FadeOut(self.incident_wave),
            FadeOut(self.surface_wave_path),
            run_time=1,
        )
        self.clear_hud_text()

        title = Text("Comparison: Effect of Creeping Waves", font_size=28)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.add_hud_text(title)
        self.play(Write(title))

        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=2)

        left_label = Text("Without Creeping Waves\n(Physical Optics Only)", font_size=18)
        left_label.to_edge(LEFT).shift(UP * 2)

        left_backscatter = Arrow(
            start=LEFT * 3,
            end=LEFT * 4,
            color=RED,
            stroke_width=6,
        ).shift(DOWN)

        right_label = Text("With Creeping Waves\n(Actual Physics)", font_size=18)
        right_label.to_edge(RIGHT).shift(UP * 2)

        right_backscatter = Arrow(
            start=RIGHT * 3,
            end=RIGHT * 3 + LEFT * 1.5,
            color=GREEN,
            stroke_width=8,
        ).shift(DOWN)

        left_percentage = Text("100%", font_size=24, color=RED)
        left_percentage.next_to(left_backscatter, DOWN)
        right_percentage = Text("150%", font_size=24, color=GREEN)
        right_percentage.next_to(right_backscatter, DOWN)

        self.add_hud_text(left_label, right_label, left_percentage, right_percentage)
        self.add_fixed_in_frame_mobjects(left_backscatter, right_backscatter)
        self.play(
            Write(left_label),
            Write(right_label),
            Create(left_backscatter),
            Create(right_backscatter),
            Write(left_percentage),
            Write(right_percentage),
            run_time=2,
        )

        final_message = Text(
            "Creeping waves can increase radar returns by 50% or more",
            font_size=22,
            color=YELLOW,
        )
        final_message.to_edge(DOWN).shift(UP * 0.5)
        self.add_hud_text(final_message)
        self.play(Write(final_message))

        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()
