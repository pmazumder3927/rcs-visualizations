"""Radar wave interaction with triangular facets.

Most CAD geometry meets the radar solver as a triangular mesh. This scene
walks through what physical-optics codes actually compute: which facets
the incident wave illuminates, the per-facet phase from the path-length
to the observer, and the coherent sum that becomes the scattered field.
"""

import numpy as np
from manim import (
    BLUE,
    DARK_GREY,
    DEGREES,
    DOWN,
    GREEN,
    GREY_B,
    GREY_C,
    LEFT,
    ORANGE,
    ORIGIN,
    PI,
    RED,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Arrow,
    Arrow3D,
    Circle,
    Create,
    DashedLine,
    FadeOut,
    Line,
    MathTex,
    Polygon,
    Text,
    VGroup,
    Write,
    interpolate_color,
    linear,
)

from scenes._common import (
    RCSScene,
    face_normal_and_centroid,
    icosahedron_vertices,
    is_illuminated,
    unit,
)


class RadarFacetsVisualization(RCSScene):
    camera_kwargs = {"phi": 65 * DEGREES, "theta": -45 * DEGREES, "distance": 10}

    def construct(self):
        self.play_title(
            "Radar Wave Interaction with Triangular Facets",
            "Phase Computation and Interference",
        )

        # Build a faceted body from an icosahedron.
        vertices = icosahedron_vertices(scale=0.7)
        face_indices = [
            [0, 2, 8],
            [0, 8, 4],
            [0, 4, 6],
            [0, 6, 10],
            [0, 10, 2],
            [1, 3, 11],
            [1, 11, 7],
            [1, 7, 5],
            [1, 5, 9],
            [1, 9, 3],
        ]

        faces = VGroup()
        face_normals = []
        face_centers = []
        for indices in face_indices:
            tri = [vertices[i] for i in indices]
            facet = Polygon(
                *tri,
                color=GREY_B,
                fill_color=GREY_C,
                fill_opacity=0.7,
                stroke_color=WHITE,
                stroke_width=2,
            )
            faces.add(facet)
            normal, centroid = face_normal_and_centroid(tri)
            face_normals.append(normal)
            face_centers.append(centroid)

        self.play(Create(faces), run_time=2)
        self.move_camera(phi=70 * DEGREES, theta=-30 * DEGREES, distance=8, run_time=2)

        # Incident plane wave.
        wave_origin = np.array([-5.0, 0.0, 2.0])
        wave_direction = unit([1.0, 0.0, -0.3])

        wave_lines = VGroup()
        for i in range(5):
            offset = i * 0.5
            wave_lines.add(
                Line(
                    start=wave_origin - wave_direction * offset,
                    end=wave_origin - wave_direction * offset + wave_direction * 4,
                    color=BLUE,
                    stroke_width=3 - i * 0.5,
                )
            )

        wave_label = Text("Incident Radar Wave", font_size=20, color=BLUE)
        wave_label.move_to(wave_origin + UP * 1.5)
        self.add_fixed_in_frame_mobjects(wave_label)

        self.play(Create(wave_lines), Write(wave_label), run_time=2)
        self.play(wave_lines.animate.shift(wave_direction * 2), rate_func=linear, run_time=1.5)

        # Highlight illuminated vs shadowed facets.
        for face, normal, center in zip(faces, face_normals, face_centers):
            if is_illuminated(normal, wave_direction):
                normal_arrow = Arrow3D(
                    start=center,
                    end=center + normal * 0.5,
                    color=YELLOW,
                    thickness=0.02,
                )
                self.play(
                    face.animate.set_fill(YELLOW, opacity=0.8),
                    Create(normal_arrow),
                    run_time=0.2,
                )
            else:
                self.play(face.animate.set_fill(DARK_GREY, opacity=0.3), run_time=0.2)

        illumination_text = Text(
            "Illuminated facets contribute to the scattered field",
            font_size=18,
        )
        illumination_text.to_edge(DOWN).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(illumination_text)
        self.play(Write(illumination_text))
        self.wait(2)
        self.play(FadeOut(illumination_text))

        # Phase-computation close-up on a single facet.
        phase_title = Text("Phase Computation for Each Facet", font_size=24)
        phase_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(phase_title)
        self.play(Write(phase_title))

        example_idx = 2
        example_center = face_centers[example_idx]
        self.move_camera(frame_center=example_center, distance=5, run_time=2)

        ki_arrow = Arrow3D(
            start=example_center - wave_direction * 1.5,
            end=example_center,
            color=BLUE,
            thickness=0.03,
        )
        ki_label = MathTex(r"\hat{k}_i", color=BLUE)
        ki_label.move_to(example_center - wave_direction * 2 + RIGHT * 0.5)

        ks_direction = unit([0.5, 0.5, 0.7])
        ks_arrow = Arrow3D(
            start=example_center,
            end=example_center + ks_direction * 1.5,
            color=GREEN,
            thickness=0.03,
        )
        ks_label = MathTex(r"\hat{k}_s", color=GREEN)
        ks_label.move_to(example_center + ks_direction * 2 + LEFT * 0.5)

        self.add_fixed_in_frame_mobjects(ki_label, ks_label)
        self.play(
            Create(ki_arrow),
            Create(ks_arrow),
            Write(ki_label),
            Write(ks_label),
            run_time=2,
        )

        phase_eq = MathTex(r"\phi = k \cdot (\hat{k}_i - \hat{k}_s) \cdot \vec{r}", font_size=28)
        phase_eq.to_edge(RIGHT).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(phase_eq)
        self.play(Write(phase_eq))

        path_diff_line = DashedLine(
            start=example_center - wave_direction,
            end=example_center + ks_direction,
            color=ORANGE,
            stroke_width=3,
        )
        path_label = Text("Path difference determines phase", font_size=16, color=ORANGE)
        path_label.next_to(phase_eq, DOWN)
        self.add_fixed_in_frame_mobjects(path_label)
        self.play(Create(path_diff_line), Write(path_label), run_time=2)
        self.wait(2)

        self.play(
            FadeOut(VGroup(ki_arrow, ks_arrow, path_diff_line)),
            FadeOut(VGroup(ki_label, ks_label, path_label, phase_eq)),
            run_time=1,
        )
        self.move_camera(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            distance=10,
            frame_center=ORIGIN,
            run_time=2,
        )

        interference_title = Text("Constructive and Destructive Interference", font_size=24)
        interference_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(interference_title)
        self.play(FadeOut(phase_title), Write(interference_title))

        # Coherent sum: scattered wavelets from each illuminated facet.
        scattered_waves = VGroup()
        phase_indicators = VGroup()
        rng = np.random.default_rng(seed=42)
        for face, center, normal in zip(faces[:5], face_centers[:5], face_normals[:5]):
            if not is_illuminated(normal, wave_direction):
                continue
            phase = rng.uniform(0.0, 2.0 * PI)
            color = interpolate_color(RED, GREEN, (np.cos(phase) + 1) / 2)
            wave_circle = Circle(radius=0.1, color=color).move_to(center)
            scattered_waves.add(wave_circle)
            arrow = Arrow(
                start=center,
                end=center + 0.3 * np.array([np.cos(phase), np.sin(phase), 0.0]),
                color=color,
                buff=0,
                stroke_width=4,
            )
            phase_indicators.add(arrow)

        self.play(
            *[Create(w) for w in scattered_waves],
            *[Create(a) for a in phase_indicators],
            run_time=2,
        )
        self.play(
            *[w.animate.scale(5).set_stroke(opacity=0.2) for w in scattered_waves],
            run_time=3,
        )

        summary_text = Text(
            "Scattered field = sum of contributions from all illuminated facets",
            font_size=20,
            color=YELLOW,
        )
        summary_text.to_edge(DOWN)
        equation = MathTex(
            r"E_s = \sum_{\text{illuminated}} E_{\text{facet}} \cdot e^{i\phi_{\text{facet}}}",
            font_size=24,
        )
        equation.next_to(summary_text, UP)
        self.add_fixed_in_frame_mobjects(summary_text, equation)
        self.play(Write(summary_text), Write(equation), run_time=2)

        self.move_camera(phi=80 * DEGREES, theta=-60 * DEGREES, distance=12, run_time=3)
        self.wait(3)
