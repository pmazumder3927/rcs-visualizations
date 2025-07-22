from manim import *
import numpy as np

class RadarFacetsVisualization(ThreeDScene):
    def construct(self):
        # Configure scene for better visibility
        self.renderer.background_color = "#0e1117"
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, distance=10)
        
        # Create title
        title = Text("Radar Wave Interaction with Triangular Facets", font_size=32, weight=BOLD)
        subtitle = Text("Phase Computation and Interference", font_size=20)
        subtitle.next_to(title, DOWN)
        
        title_group = VGroup(title, subtitle)
        title_group.to_edge(UP)
        
        self.add_fixed_in_frame_mobjects(title_group)
        self.play(Write(title), FadeIn(subtitle, shift=UP), run_time=2)
        self.wait(2)
        self.play(FadeOut(title_group))
        
        # Create faceted object (simple icosahedron)
        vertices = []
        phi = (1.0 + np.sqrt(5.0)) / 2.0  # Golden ratio
        
        # Create vertices
        for i in [-1, 1]:
            for j in [-1, 1]:
                vertices.append([0, i, j * phi])
                vertices.append([i, j * phi, 0])
                vertices.append([j * phi, 0, i])
        
        vertices = np.array(vertices) * 0.7  # Scale down
        
        # Create faces (triangular facets)
        faces = VGroup()
        face_normals = []
        face_centers = []
        
        # Create some example triangular faces
        face_indices = [
            [0, 2, 8], [0, 8, 4], [0, 4, 6], [0, 6, 10], [0, 10, 2],
            [1, 3, 11], [1, 11, 7], [1, 7, 5], [1, 5, 9], [1, 9, 3]
        ]
        
        for indices in face_indices:
            v1, v2, v3 = vertices[indices[0]], vertices[indices[1]], vertices[indices[2]]
            
            # Create triangle
            triangle = Polygon(v1, v2, v3, 
                             color=GREY_B, 
                             fill_color=GREY_C, 
                             fill_opacity=0.7,
                             stroke_color=WHITE,
                             stroke_width=2)
            faces.add(triangle)
            
            # Calculate face normal and center
            center = (v1 + v2 + v3) / 3
            edge1 = v2 - v1
            edge2 = v3 - v1
            normal = np.cross(edge1, edge2)
            normal = normal / np.linalg.norm(normal)
            
            face_normals.append(normal)
            face_centers.append(center)
        
        # Show the object
        self.play(Create(faces), run_time=2)
        self.move_camera(phi=70 * DEGREES, theta=-30 * DEGREES, distance=8, run_time=2)
        
        # Create incident radar wave
        wave_origin = np.array([-5, 0, 2])
        wave_direction = np.array([1, 0, -0.3])
        wave_direction = wave_direction / np.linalg.norm(wave_direction)
        
        # Wave visualization
        wave_lines = VGroup()
        for i in range(5):
            offset = i * 0.5
            line = Line(
                start=wave_origin - wave_direction * offset,
                end=wave_origin - wave_direction * offset + wave_direction * 4,
                color=BLUE,
                stroke_width=3 - i * 0.5
            )
            wave_lines.add(line)
        
        wave_label = Text("Incident Radar Wave", font_size=20, color=BLUE)
        wave_label.move_to(wave_origin + UP * 1.5)
        self.add_fixed_in_frame_mobjects(wave_label)
        
        self.play(
            Create(wave_lines),
            Write(wave_label),
            run_time=2
        )
        
        # Animate wave propagation
        self.play(
            wave_lines.animate.shift(wave_direction * 2),
            rate_func=linear,
            run_time=1.5
        )
        
        # Show illuminated facets
        illuminated_faces = VGroup()
        non_illuminated_faces = VGroup()
        
        for i, (face, normal, center) in enumerate(zip(faces, face_normals, face_centers)):
            cos_theta = np.dot(-wave_direction, normal)
            if cos_theta > 0:  # Face is illuminated
                illuminated_faces.add(face)
                
                # Add normal arrow
                normal_arrow = Arrow3D(
                    start=center,
                    end=center + normal * 0.5,
                    color=YELLOW,
                    thickness=0.02
                )
                self.play(
                    face.animate.set_fill(YELLOW, opacity=0.8),
                    Create(normal_arrow),
                    run_time=0.2
                )
            else:
                non_illuminated_faces.add(face)
                self.play(
                    face.animate.set_fill(DARK_GREY, opacity=0.3),
                    run_time=0.2
                )
        
        illumination_text = Text("Illuminated facets contribute to scattered field", font_size=18)
        illumination_text.to_edge(DOWN).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(illumination_text)
        self.play(Write(illumination_text))
        self.wait(2)
        
        # Phase computation visualization
        self.play(FadeOut(illumination_text))
        
        phase_title = Text("Phase Computation for Each Facet", font_size=24)
        phase_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(phase_title)
        self.play(Write(phase_title))
        
        # Focus on one illuminated facet
        example_face_idx = 2  # Pick an illuminated face
        example_face = faces[example_face_idx]
        example_center = face_centers[example_face_idx]
        
        # Move camera to focus on this facet
        self.move_camera(
            frame_center=example_center,
            distance=5,
            run_time=2
        )
        
        # Show phase calculation components
        ki_arrow = Arrow3D(
            start=example_center - wave_direction * 1.5,
            end=example_center,
            color=BLUE,
            thickness=0.03
        )
        ki_label = MathTex(r"\hat{k}_i", color=BLUE)
        ki_label.move_to(example_center - wave_direction * 2 + RIGHT * 0.5)
        
        ks_direction = np.array([0.5, 0.5, 0.7])
        ks_direction = ks_direction / np.linalg.norm(ks_direction)
        
        ks_arrow = Arrow3D(
            start=example_center,
            end=example_center + ks_direction * 1.5,
            color=GREEN,
            thickness=0.03
        )
        ks_label = MathTex(r"\hat{k}_s", color=GREEN)
        ks_label.move_to(example_center + ks_direction * 2 + LEFT * 0.5)
        
        self.add_fixed_in_frame_mobjects(ki_label, ks_label)
        
        self.play(
            Create(ki_arrow),
            Create(ks_arrow),
            Write(ki_label),
            Write(ks_label),
            run_time=2
        )
        
        # Show phase equation
        phase_eq = MathTex(
            r"\phi = k \cdot (\hat{k}_i - \hat{k}_s) \cdot \vec{r}",
            font_size=28
        )
        phase_eq.to_edge(RIGHT).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(phase_eq)
        self.play(Write(phase_eq))
        
        # Visualize path difference
        path_diff_line = DashedLine(
            start=example_center - wave_direction * 1,
            end=example_center + ks_direction * 1,
            color=ORANGE,
            stroke_width=3
        )
        
        path_label = Text("Path difference determines phase", font_size=16, color=ORANGE)
        path_label.next_to(phase_eq, DOWN)
        self.add_fixed_in_frame_mobjects(path_label)
        
        self.play(
            Create(path_diff_line),
            Write(path_label),
            run_time=2
        )
        
        self.wait(2)
        
        # Show interference pattern
        self.play(
            FadeOut(VGroup(ki_arrow, ks_arrow, path_diff_line)),
            FadeOut(VGroup(ki_label, ks_label, path_label, phase_eq)),
            run_time=1
        )
        
        # Reset camera view
        self.move_camera(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            distance=10,
            frame_center=ORIGIN,
            run_time=2
        )
        
        interference_title = Text("Constructive and Destructive Interference", font_size=24)
        interference_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(interference_title)
        self.play(
            FadeOut(phase_title),
            Write(interference_title)
        )
        
        # Show scattered waves from multiple facets
        scattered_waves = VGroup()
        phase_indicators = VGroup()
        
        for i, (face, center, normal) in enumerate(zip(faces[:5], face_centers[:5], face_normals[:5])):
            if np.dot(-wave_direction, normal) > 0:  # Only illuminated faces
                # Create expanding wave
                wave_circle = Circle(radius=0.1, color=ORANGE)
                wave_circle.move_to(center)
                
                # Random phase for demonstration
                phase = np.random.uniform(0, 2 * PI)
                color = interpolate_color(RED, GREEN, (np.cos(phase) + 1) / 2)
                wave_circle.set_color(color)
                
                scattered_waves.add(wave_circle)
                
                # Phase indicator
                phase_arrow = Arrow(
                    start=center,
                    end=center + 0.3 * np.array([np.cos(phase), np.sin(phase), 0]),
                    color=color,
                    buff=0,
                    stroke_width=4
                )
                phase_indicators.add(phase_arrow)
        
        self.play(
            *[Create(wave) for wave in scattered_waves],
            *[Create(arrow) for arrow in phase_indicators],
            run_time=2
        )
        
        # Animate wave expansion and interference
        self.play(
            *[wave.animate.scale(5).set_stroke(opacity=0.2) for wave in scattered_waves],
            run_time=3
        )
        
        # Final summary
        summary_text = Text(
            "Total scattered field = Sum of contributions from all illuminated facets",
            font_size=20,
            color=YELLOW
        )
        summary_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(summary_text)
        
        equation = MathTex(
            r"E_s = \sum_{\text{illuminated}} E_{\text{facet}} \cdot e^{i\phi_{\text{facet}}}",
            font_size=24
        )
        equation.next_to(summary_text, UP)
        self.add_fixed_in_frame_mobjects(equation)
        
        self.play(
            Write(summary_text),
            Write(equation),
            run_time=2
        )
        
        # Final camera rotation
        self.move_camera(
            phi=80 * DEGREES,
            theta=-60 * DEGREES,
            distance=12,
            run_time=3
        )
        
        self.wait(3)

if __name__ == "__main__":
    # Run with: manim -pqh radar_facets_visualization.py RadarFacetsVisualization
    pass