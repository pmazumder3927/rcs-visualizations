"""Creeping waves: extended physical-optics walkthrough.

The "basic" creeping-waves scene focuses on the four-stage story. This
enhanced version expands the EM background: the orthogonal E/B fields,
the three coexisting phenomena (reflection, diffraction, surface wave),
the surface-current picture, and the magnitude of the resulting return
relative to a physical-optics-only prediction.
"""

import numpy as np
from manim import (
    BLUE,
    BLUE_E,
    DEGREES,
    DOWN,
    GREEN,
    GREY_B,
    GREY_C,
    LEFT,
    ORANGE,
    PI,
    RED,
    RIGHT,
    TAU,
    UP,
    WHITE,
    YELLOW,
    AnimationGroup,
    Annulus,
    Arc,
    Arrow,
    Arrow3D,
    Create,
    CurvedArrow,
    DashedLine,
    Dot3D,
    FadeOut,
    Line,
    NumberPlane,
    ParametricFunction,
    Sphere,
    Text,
    VGroup,
    Write,
    interpolate_color,
    linear,
)

from scenes._common import RCSScene


class CreepingWavesEnhanced(RCSScene):
    camera_kwargs = {"phi": 65 * DEGREES, "theta": -45 * DEGREES, "distance": 10}

    def construct(self):
        self._title_sequence()
        self._em_wave_basics()
        self._wave_sphere_interaction()
        self._surface_wave_physics()
        self._creeping_wave_mechanism()
        self._radar_implications()

    # -- sections -----------------------------------------------------------

    def _title_sequence(self):
        self.play_title(
            "The Physics of Creeping Waves",
            "How electromagnetic waves sneak around curved surfaces",
        )

    def _em_wave_basics(self):
        self.clear_hud_text()
        section_title = Text("Understanding Electromagnetic Waves", font_size=28)
        section_title.to_edge(UP)
        self.add_hud_text(section_title)
        self.play(Write(section_title))

        wave_length = 8
        amplitude = 2
        e_wave = ParametricFunction(
            lambda t: np.array([t, 0.0, amplitude * np.sin(2 * PI * t / 2)]),
            t_range=[-wave_length / 2, wave_length / 2],
            color=BLUE,
        ).shift(UP * 1.5)
        b_wave = ParametricFunction(
            lambda t: np.array([t, amplitude * np.sin(2 * PI * t / 2), 0.0]),
            t_range=[-wave_length / 2, wave_length / 2],
            color=RED,
        ).shift(UP * 1.5)

        prop_arrow = Arrow(
            start=LEFT * 4 + UP * 1.5,
            end=RIGHT * 4 + UP * 1.5,
            color=GREEN,
            buff=0,
        )

        e_label = Text("E-field", font_size=20, color=BLUE).move_to(UP * 3 + LEFT * 3)
        b_label = Text("B-field", font_size=20, color=RED).move_to(UP * 0.5 + LEFT * 3)
        prop_label = Text("Propagation", font_size=20, color=GREEN).move_to(DOWN * 0.5 + RIGHT * 2)
        self.add_hud_text(e_label, b_label, prop_label)

        self.play(
            Create(e_wave),
            Create(b_wave),
            Create(prop_arrow),
            Write(e_label),
            Write(b_label),
            Write(prop_label),
            run_time=2,
        )
        self.play(
            e_wave.animate.shift(RIGHT * 2),
            b_wave.animate.shift(RIGHT * 2),
            run_time=2,
            rate_func=linear,
        )
        self.wait(1)
        self.play(FadeOut(VGroup(e_wave, b_wave, prop_arrow)), run_time=1)

    def _wave_sphere_interaction(self):
        self.clear_hud_text()
        section_title = Text("Wave Meets Sphere: Three Phenomena", font_size=28)
        section_title.to_edge(UP)
        self.add_hud_text(section_title)
        self.play(Write(section_title))

        self.sphere = Sphere(radius=2, resolution=(40, 40))
        self.sphere.set_color([GREY_B, GREY_C])
        self.sphere.set_opacity(0.95)

        grid = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
        )
        grid.rotate(90 * DEGREES, axis=RIGHT)
        grid.shift(LEFT * 3)

        self.play(Create(self.sphere), Create(grid), run_time=2)

        wave_lines = VGroup()
        for y in np.linspace(-3, 3, 7):
            wave_lines.add(
                Line(
                    start=np.array([-6, y, 0]),
                    end=np.array([-2.5, y, 0]),
                    color=BLUE,
                    stroke_width=2,
                )
            )
        self.play(Create(wave_lines))

        reflection_arrow = Arrow3D(
            start=np.array([-2, 0, 0]),
            end=np.array([-4, -2, 0]),
            color=RED,
            thickness=0.05,
        )
        reflection_label = Text("1. Reflection", font_size=20, color=RED).move_to(
            LEFT * 4 + DOWN * 3
        )

        diffraction_arcs = VGroup()
        for angle in np.linspace(-60, 60, 5) * DEGREES:
            arc = Arc(
                radius=0.5,
                start_angle=angle - 10 * DEGREES,
                angle=20 * DEGREES,
                color=YELLOW,
            )
            arc.move_to(
                np.array(
                    [
                        2 * np.cos(angle + 90 * DEGREES),
                        2 * np.sin(angle + 90 * DEGREES),
                        0,
                    ]
                )
            )
            diffraction_arcs.add(arc)
        diffraction_label = Text("2. Diffraction", font_size=20, color=YELLOW).move_to(
            RIGHT * 3 + UP * 3
        )

        surface_wave = ParametricFunction(
            lambda t: 2.05 * np.array([np.cos(t), np.sin(t), 0.0]),
            t_range=[PI, 2 * PI],
            color=ORANGE,
        ).set_stroke(width=4)
        surface_label = Text("3. Surface Wave", font_size=20, color=ORANGE).move_to(DOWN * 3)

        self.add_hud_text(reflection_label, diffraction_label, surface_label)
        self.play(
            Create(reflection_arrow),
            Write(reflection_label),
            Create(diffraction_arcs),
            Write(diffraction_label),
            Create(surface_wave),
            Write(surface_label),
            run_time=3,
        )
        self.wait(2)

        self.play(
            FadeOut(VGroup(wave_lines, grid, reflection_arrow, diffraction_arcs)),
            run_time=1,
        )

    def _surface_wave_physics(self):
        self.clear_hud_text()
        section_title = Text("The Birth of a Creeping Wave", font_size=28)
        section_title.to_edge(UP)
        self.add_hud_text(section_title)
        self.play(Write(section_title))

        self.move_camera(phi=45 * DEGREES, theta=-60 * DEGREES, distance=6, run_time=2)

        grazing_angle = 10 * DEGREES
        impact_point = np.array([2 * np.cos(grazing_angle), 2 * np.sin(grazing_angle), 0.0])

        incident_ray = Arrow3D(
            start=impact_point + np.array([-3.0, -0.5, 0.0]),
            end=impact_point,
            color=BLUE,
            thickness=0.04,
        )

        field_lines = VGroup()
        for i in range(5):
            offset = i * 0.2
            field_lines.add(
                CurvedArrow(
                    start_point=impact_point + np.array([-offset, 0.0, 0.0]),
                    end_point=impact_point + np.array([0.3, 0.3, 0.0]),
                    color=interpolate_color(BLUE, ORANGE, i / 4),
                    angle=-TAU / 8,
                )
            )

        self.play(Create(incident_ray), Create(field_lines), run_time=2)

        surface_current_region = Annulus(
            inner_radius=1.8,
            outer_radius=2.2,
            color=ORANGE,
            fill_opacity=0.3,
        )

        current_arrows = VGroup()
        for angle in np.linspace(0, PI / 3, 8):
            arrow_start = 2 * np.array([np.cos(angle), np.sin(angle), 0.0])
            tangent = np.array([-np.sin(angle), np.cos(angle), 0.0])
            current_arrows.add(
                Arrow(
                    start=arrow_start,
                    end=arrow_start + 0.5 * tangent,
                    color=ORANGE,
                    buff=0,
                    stroke_width=3,
                )
            )

        explanation = Text(
            "Grazing waves induce surface currents that propagate along the boundary",
            font_size=18,
        )
        explanation.to_edge(DOWN).shift(UP * 0.3)
        self.add_hud_text(explanation)

        self.play(
            Create(surface_current_region),
            Create(current_arrows),
            Write(explanation),
            run_time=2,
        )
        self.play(current_arrows.animate.shift(RIGHT * 0.5), rate_func=linear, run_time=1.5)
        self.wait(1)

        self.play(
            FadeOut(VGroup(incident_ray, field_lines, surface_current_region, current_arrows)),
            run_time=1,
        )

    def _creeping_wave_mechanism(self):
        self.clear_hud_text()
        section_title = Text("Creeping Wave Journey", font_size=28)
        section_title.to_edge(UP)
        self.add_hud_text(section_title)
        self.play(Write(section_title))

        self.move_camera(phi=70 * DEGREES, theta=30 * DEGREES, distance=12, run_time=2)

        num_packets = 6
        paths = VGroup()
        wave_packets = VGroup()

        for i in range(num_packets):
            z_offset = (i - num_packets / 2) * 0.3
            path = ParametricFunction(
                lambda t, z=z_offset: 2.1 * np.array([np.cos(PI - t), np.sin(PI - t), z]),
                t_range=[0, 1.5 * PI],
                color=ORANGE,
            ).set_stroke(width=2, opacity=0.5)
            paths.add(path)

            head = Dot3D(point=path.get_start(), radius=0.08, color=ORANGE)
            trail = VGroup()
            for j in range(3):
                trail_dot = Dot3D(
                    point=path.get_start(),
                    radius=0.06 - j * 0.02,
                    color=ORANGE,
                )
                trail_dot.set_opacity(0.7 - j * 0.2)
                trail.add(trail_dot)
            wave_packets.add(VGroup(head, trail))

        attenuation_text = Text("Wave amplitude decreases exponentially", font_size=18)
        attenuation_text.to_edge(RIGHT).shift(DOWN * 2)
        self.add_hud_text(attenuation_text)

        self.play(Create(paths), run_time=2)
        self.play(Write(attenuation_text))

        from manim import MoveAlongPath

        packet_animations = []
        for i, (packet, path) in enumerate(zip(wave_packets, paths)):
            packet_animations.append(
                AnimationGroup(
                    MoveAlongPath(packet, path),
                    packet.animate.set_opacity(0.1).scale(0.3),
                    lag_ratio=0.1 * i,
                    run_time=5,
                )
            )

        self.play(*packet_animations)
        self.wait(1)

        self.play(FadeOut(VGroup(paths, wave_packets)), run_time=1)

    def _radar_implications(self):
        self.clear_hud_text()
        section_title = Text("Why Creeping Waves Matter for Radar", font_size=28)
        section_title.to_edge(UP)
        self.add_hud_text(section_title)
        self.play(Write(section_title))

        divider = DashedLine(start=UP * 3, end=DOWN * 3, color=WHITE, stroke_width=2)
        self.add_fixed_in_frame_mobjects(divider)
        self.play(Create(divider))

        left_title = Text("Simplified Model\n(No Creeping Waves)", font_size=20)
        left_title.to_edge(LEFT).shift(UP * 2)

        left_sphere = Sphere(radius=1, resolution=(20, 20)).shift(LEFT * 3)
        left_sphere.set_color(GREY_C)
        left_sphere.set_opacity(0.8)

        left_incident = Arrow(start=LEFT * 5, end=LEFT * 4, color=BLUE)
        left_reflected = Arrow(start=LEFT * 4, end=LEFT * 5, color=RED)
        left_rcs_text = Text("Predicted RCS: 1.0", font_size=18, color=RED)
        left_rcs_text.move_to(LEFT * 3 + DOWN * 2.5)

        right_title = Text("Actual Physics\n(With Creeping Waves)", font_size=20)
        right_title.to_edge(RIGHT).shift(UP * 2)

        right_sphere = Sphere(radius=1, resolution=(20, 20)).shift(RIGHT * 3)
        right_sphere.set_color(GREY_C)
        right_sphere.set_opacity(0.8)

        right_incident = Arrow(start=RIGHT * 1, end=RIGHT * 2, color=BLUE)
        right_reflected = Arrow(start=RIGHT * 2, end=RIGHT * 1, color=RED)
        creeping_return = Arrow(
            start=RIGHT * 4,
            end=RIGHT * 2.5,
            color=ORANGE,
        ).set_stroke(width=4)

        right_rcs_text = Text("Actual RCS: 1.5", font_size=18, color=GREEN)
        right_rcs_text.move_to(RIGHT * 3 + DOWN * 2.5)

        self.add_fixed_in_frame_mobjects(left_title, right_title, left_rcs_text, right_rcs_text)

        self.play(
            Create(left_sphere),
            Create(right_sphere),
            Write(left_title),
            Write(right_title),
            run_time=2,
        )
        self.play(
            Create(left_incident),
            Create(left_reflected),
            Create(right_incident),
            Create(right_reflected),
            Write(left_rcs_text),
            run_time=2,
        )

        creeping_label = Text("Extra return from\ncreeping waves", font_size=16, color=ORANGE)
        creeping_label.move_to(RIGHT * 4 + UP * 0.5)
        self.add_fixed_in_frame_mobjects(creeping_label)

        self.play(
            Create(creeping_return),
            Write(creeping_label),
            Write(right_rcs_text),
            run_time=2,
        )

        conclusion = Text(
            "Creeping waves explain returns that simple PO models miss",
            font_size=22,
            color=YELLOW,
        )
        conclusion.to_edge(DOWN).shift(UP * 0.3)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait(3)

        self.move_camera(phi=80 * DEGREES, theta=-45 * DEGREES, distance=15, run_time=3)
        self.wait(2)
