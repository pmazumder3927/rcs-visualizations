from manim import *
import numpy as np

class DeformationVectorsVisualization(ThreeDScene):
    def construct(self):
        # Configure scene
        self.renderer.background_color = "#0e1117"
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, distance=8)
        
        # Title
        title = Text("Deformation Vectors: Shaping for Stealth", font_size=32, weight=BOLD)
        subtitle = Text("How optimization algorithms modify geometry", font_size=20)
        subtitle.next_to(title, DOWN)
        
        title_group = VGroup(title, subtitle)
        title_group.to_edge(UP)
        
        self.add_fixed_in_frame_mobjects(title_group)
        self.play(Write(title), FadeIn(subtitle, shift=UP), run_time=2)
        self.wait(2)
        self.play(FadeOut(title_group))
        
        # Create initial mesh (sphere)
        num_points = 20
        phi_vals = np.linspace(0, PI, num_points//2)
        theta_vals = np.linspace(0, 2*PI, num_points)
        
        mesh_points = []
        for phi in phi_vals:
            for theta in theta_vals:
                x = 2 * np.sin(phi) * np.cos(theta)
                y = 2 * np.sin(phi) * np.sin(theta)
                z = 2 * np.cos(phi)
                mesh_points.append([x, y, z])
        
        mesh_points = np.array(mesh_points)
        
        # Create dots for mesh points
        mesh_dots = VGroup()
        for point in mesh_points[:100]:  # Limit for performance
            dot = Dot3D(point=point, radius=0.03, color=BLUE)
            mesh_dots.add(dot)
        
        # Create initial surface representation
        surface = Surface(
            lambda u, v: np.array([
                2 * np.sin(u) * np.cos(v),
                2 * np.sin(u) * np.sin(v),
                2 * np.cos(u)
            ]),
            u_range=[0, PI],
            v_range=[0, 2*PI],
            resolution=(20, 40),
            fill_color=BLUE_C,
            fill_opacity=0.3,
            stroke_color=BLUE_E,
            stroke_width=1
        )
        
        # Show initial shape
        shape_label = Text("Original Shape", font_size=20, color=BLUE)
        shape_label.to_edge(LEFT).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(shape_label)
        
        self.play(
            Create(surface),
            Create(mesh_dots),
            Write(shape_label),
            run_time=2
        )
        
        # Explain deformation vectors
        explanation = Text(
            "Each point gets a deformation vector d",
            font_size=22
        )
        explanation.to_edge(DOWN).shift(UP * 0.5)
        
        formula = MathTex(
            r"\vec{x}_{\text{new}} = \vec{x}_{\text{original}} + \vec{d}",
            font_size=28
        )
        formula.next_to(explanation, UP)
        
        self.add_fixed_in_frame_mobjects(explanation, formula)
        self.play(Write(explanation), Write(formula))
        
        # Create deformation vectors
        deformation_vectors = VGroup()
        deformed_points = []
        
        # Generate smooth deformation field (elongate and add some waviness)
        for i, point in enumerate(mesh_points[:100]):
            # Create deformation that elongates in x direction and adds waviness
            theta = np.arctan2(point[1], point[0])
            phi = np.arccos(point[2] / np.linalg.norm(point))
            
            # Deformation components
            dx = 0.3 * np.sin(3 * theta) * np.sin(phi)
            dy = 0.2 * np.cos(2 * theta) * np.sin(phi)
            dz = -0.1 * np.sin(phi)
            
            deformation = np.array([dx, dy, dz])
            deformed_point = point + deformation
            deformed_points.append(deformed_point)
            
            # Create arrow
            if i % 5 == 0:  # Show every 5th vector for clarity
                arrow = Arrow3D(
                    start=point,
                    end=deformed_point,
                    color=ORANGE,
                    thickness=0.02
                )
                deformation_vectors.add(arrow)
        
        # Show deformation vectors
        vector_label = Text("Deformation Vectors", font_size=20, color=ORANGE)
        vector_label.to_edge(RIGHT).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(vector_label)
        
        self.play(
            Create(deformation_vectors),
            Write(vector_label),
            run_time=2
        )
        
        self.wait(2)
        
        # Animate the deformation
        self.play(FadeOut(explanation), FadeOut(formula))
        
        deform_text = Text("Applying deformation...", font_size=22, color=YELLOW)
        deform_text.to_edge(DOWN).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(deform_text)
        self.play(Write(deform_text))
        
        # Create deformed mesh dots
        deformed_dots = VGroup()
        for point in deformed_points:
            dot = Dot3D(point=point, radius=0.03, color=GREEN)
            deformed_dots.add(dot)
        
        # Create deformed surface
        def deformed_func(u, v):
            x = 2 * np.sin(u) * np.cos(v)
            y = 2 * np.sin(u) * np.sin(v)
            z = 2 * np.cos(u)
            
            # Apply deformation
            dx = 0.3 * np.sin(3 * v) * np.sin(u)
            dy = 0.2 * np.cos(2 * v) * np.sin(u)
            dz = -0.1 * np.sin(u)
            
            return np.array([x + dx, y + dy, z + dz])
        
        deformed_surface = Surface(
            deformed_func,
            u_range=[0, PI],
            v_range=[0, 2*PI],
            resolution=(20, 40),
            fill_color=GREEN_C,
            fill_opacity=0.3,
            stroke_color=GREEN_E,
            stroke_width=1
        )
        
        # Animate transformation
        self.play(
            Transform(mesh_dots, deformed_dots),
            Transform(surface, deformed_surface),
            run_time=3
        )
        
        deformed_label = Text("Deformed Shape", font_size=20, color=GREEN)
        deformed_label.to_edge(LEFT).shift(DOWN * 2)
        self.add_fixed_in_frame_mobjects(deformed_label)
        self.play(
            FadeOut(shape_label),
            Write(deformed_label),
            FadeOut(deform_text)
        )
        
        # Show RCS comparison
        rcs_comparison = Text("RCS Comparison", font_size=24, weight=BOLD)
        rcs_comparison.to_edge(UP)
        self.add_fixed_in_frame_mobjects(rcs_comparison)
        self.play(Write(rcs_comparison))
        
        # Create RCS indicator bars
        original_rcs = Rectangle(
            width=0.5,
            height=2,
            fill_color=BLUE,
            fill_opacity=0.8,
            stroke_color=WHITE
        )
        original_rcs.shift(LEFT * 2 + DOWN * 0.5)
        
        deformed_rcs = Rectangle(
            width=0.5,
            height=1.2,
            fill_color=GREEN,
            fill_opacity=0.8,
            stroke_color=WHITE
        )
        deformed_rcs.shift(RIGHT * 2 + DOWN * 0.5)
        deformed_rcs.align_to(original_rcs, DOWN)
        
        original_label = Text("Original\nRCS: 1.0", font_size=16)
        original_label.next_to(original_rcs, DOWN)
        
        deformed_label_rcs = Text("Optimized\nRCS: 0.6", font_size=16)
        deformed_label_rcs.next_to(deformed_rcs, DOWN)
        
        improvement = Text("40% Reduction!", font_size=20, color=YELLOW)
        improvement.next_to(deformed_rcs, RIGHT).shift(UP)
        
        self.add_fixed_in_frame_mobjects(
            original_rcs, deformed_rcs,
            original_label, deformed_label_rcs,
            improvement
        )
        
        self.play(
            Create(original_rcs),
            Create(deformed_rcs),
            Write(original_label),
            Write(deformed_label_rcs),
            run_time=2
        )
        
        self.play(
            Write(improvement),
            Flash(improvement, color=YELLOW),
            run_time=1.5
        )
        
        # Show iterative optimization process
        self.play(
            FadeOut(VGroup(original_rcs, deformed_rcs, original_label, deformed_label_rcs, improvement)),
            FadeOut(rcs_comparison)
        )
        
        iteration_title = Text("Iterative Optimization Process", font_size=24)
        iteration_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(iteration_title)
        self.play(Write(iteration_title))
        
        # Show multiple iterations
        iteration_text = Text("Iteration: 1", font_size=20)
        iteration_text.to_edge(RIGHT).shift(DOWN * 2)
        self.add_fixed_in_frame_mobjects(iteration_text)
        self.play(Write(iteration_text))
        
        # Animate through iterations
        for i in range(3):
            # Update iteration counter
            new_text = Text(f"Iteration: {i + 2}", font_size=20)
            new_text.move_to(iteration_text)
            self.add_fixed_in_frame_mobjects(new_text)
            
            # Create new deformation vectors (smaller each time)
            scale = 0.5 ** (i + 1)
            new_vectors = VGroup()
            
            for j in range(0, len(mesh_points[:100]), 5):
                point = mesh_dots[j].get_center()
                theta = np.arctan2(point[1], point[0])
                
                # Smaller, more refined deformations
                deformation = scale * np.array([
                    0.2 * np.sin(5 * theta),
                    0.1 * np.cos(4 * theta),
                    0.05 * np.sin(3 * theta)
                ])
                
                arrow = Arrow3D(
                    start=point,
                    end=point + deformation,
                    color=interpolate_color(ORANGE, RED, i/2),
                    thickness=0.015
                )
                new_vectors.add(arrow)
            
            self.play(
                Transform(iteration_text, new_text),
                FadeOut(deformation_vectors),
                Create(new_vectors),
                run_time=1
            )
            
            deformation_vectors = new_vectors
            
            # Apply deformation
            self.play(
                mesh_dots.animate.shift(RIGHT * 0.1 * scale),
                surface.animate.shift(RIGHT * 0.1 * scale),
                run_time=1
            )
            
            self.wait(0.5)
        
        # Final message
        self.play(FadeOut(deformation_vectors))
        
        final_text = Text(
            "Deformation vectors allow smooth shape optimization\nwhile preserving mesh topology",
            font_size=22,
            color=YELLOW
        )
        final_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(final_text)
        self.play(Write(final_text))
        
        # Camera rotation for final view
        self.move_camera(
            phi=45 * DEGREES,
            theta=-60 * DEGREES,
            distance=10,
            run_time=3
        )
        
        self.wait(3)

if __name__ == "__main__":
    # Run with: manim -pqh deformation_vectors_visualization.py DeformationVectorsVisualization
    pass