from manim import *
import numpy as np

class CreepingWavesVisualization(ThreeDScene):
    def construct(self):
        # Configure scene
        self.renderer.background_color = "#0e1117"
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES, distance=12)
        
        # Track text elements for cleanup
        self.current_text_elements = []
        
        # Part 1: Introduction - What happens when radar hits a sphere?
        self.introduce_concept()
        
        # Part 2: Show direct reflection (specular)
        self.show_direct_reflection()
        
        # Part 3: Introduce surface waves
        self.show_surface_wave_formation()
        
        # Part 4: Show creeping wave propagation
        self.demonstrate_creeping_waves()
        
        # Part 5: Show backscatter contribution
        self.show_backscatter_contribution()
        
        # Part 6: Compare with and without creeping waves
        self.show_comparison()
    
    def cleanup_text_elements(self):
        """Remove all current text elements from the scene"""
        if self.current_text_elements:
            self.remove(*self.current_text_elements)
            self.current_text_elements = []
    
    def add_text_element(self, text_obj):
        """Add a text element and track it for cleanup"""
        self.current_text_elements.append(text_obj)
        self.add_fixed_in_frame_mobjects(text_obj)
        
    def introduce_concept(self):
        """Introduce the basic setup with clear, educational graphics"""
        # Title with fade in
        title = Text("How Creeping Waves Form on Curved Surfaces", font_size=32)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.add_text_element(title)
        self.play(Write(title))
        
        # Create a high-quality metallic sphere
        sphere = Sphere(radius=2, resolution=(30, 30))
        sphere.set_color(GREY_B)
        sphere.set_opacity(0.9)
        
        # Add shading to make it look 3D
        # Note: Sheen effects removed for compatibility
        
        # Add coordinate axes for reference
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={"include_tip": False},
            x_length=6,
            y_length=6,
            z_length=6
        )
        axes.set_opacity(0.3)
        
        self.play(
            Create(axes),
            Create(sphere),
            run_time=2
        )
        
        # Add sphere label
        sphere_label = Text("Metallic Sphere", font_size=20)
        sphere_label.next_to(sphere, DOWN * 3)
        self.add_text_element(sphere_label)
        self.play(Write(sphere_label))
        
        self.wait(1)
        
        # Store for later use
        self.sphere = sphere
        self.axes = axes
        self.title = title
        
    def show_direct_reflection(self):
        """Show how most energy reflects directly (specular reflection)"""
        # Clean up old text and update title
        self.cleanup_text_elements()
        new_title = Text("Step 1: Direct (Specular) Reflection", font_size=28)
        new_title.to_edge(UP).shift(DOWN * 0.3)
        self.add_text_element(new_title)
        self.play(Write(new_title))
        
        # Create incident wave representation
        incident_direction = normalize(np.array([1, 0, 0]))
        wave_start = np.array([-5, 0, 0])
        
        # Show incident ray
        incident_ray = Arrow3D(
            start=wave_start,
            end=wave_start + 3 * incident_direction,
            color=BLUE,
            thickness=0.05
        )
        
        incident_label = Text("Incident Wave", font_size=18, color=BLUE)
        incident_label.move_to(wave_start + LEFT)
        self.add_text_element(incident_label)
        
        self.play(
            Create(incident_ray),
            Write(incident_label),
            run_time=1.5
        )
        
        # Show impact point
        impact_point = np.array([-2, 0, 0])
        impact_dot = Sphere(radius=0.1, resolution=(10, 10))
        impact_dot.move_to(impact_point)
        impact_dot.set_color(YELLOW)
        
        self.play(Create(impact_dot))
        
        # Show reflected ray (specular)
        reflected_direction = normalize(np.array([-1, 0, 0]))
        reflected_ray = Arrow3D(
            start=impact_point,
            end=impact_point + 3 * reflected_direction,
            color=RED,
            thickness=0.05
        )
        
        reflected_label = Text("Reflected Wave", font_size=18, color=RED)
        reflected_label.move_to(impact_point + LEFT * 3 + UP)
        self.add_text_element(reflected_label)
        
        self.play(
            Create(reflected_ray),
            Write(reflected_label),
            run_time=1.5
        )
        
        # Add explanation
        explanation = Text(
            "Most energy reflects like a mirror",
            font_size=20,
            color=WHITE
        )
        explanation.to_edge(DOWN).shift(UP * 0.5)
        self.add_text_element(explanation)
        self.play(Write(explanation))
        
        self.wait(2)
        
        # Fade out for next section
        self.play(
            FadeOut(incident_ray),
            FadeOut(incident_label),
            FadeOut(reflected_ray),
            FadeOut(reflected_label),
            FadeOut(impact_dot),
            FadeOut(explanation),
            run_time=1
        )
        
    def show_surface_wave_formation(self):
        """Show how some energy converts to surface waves"""
        # Clean up old text and update title
        self.cleanup_text_elements()
        new_title = Text("Step 2: Surface Wave Formation", font_size=28)
        new_title.to_edge(UP).shift(DOWN * 0.3)
        self.add_text_element(new_title)
        self.play(Write(new_title))
        
        # Show incident wave hitting at grazing angle
        incident_direction = normalize(np.array([1, 0.3, 0]))
        wave_start = np.array([-5, -1.5, 0])
        impact_point = np.array([-1.8, -0.87, 0])  # Point on sphere surface
        
        # Incident wave
        incident_wave = Arrow3D(
            start=wave_start,
            end=impact_point,
            color=BLUE,
            thickness=0.05
        )
        
        self.play(Create(incident_wave))
        
        # Show energy coupling into surface
        coupling_circle = Circle(radius=0.3, color=ORANGE)
        coupling_circle.move_to(impact_point)
        coupling_circle.set_stroke(width=3)
        
        self.play(
            Create(coupling_circle),
            coupling_circle.animate.scale(1.5).set_opacity(0.5),
            run_time=1
        )
        
        # Create surface wave visualization
        # Show wave "hugging" the surface
        surface_wave_path = ParametricFunction(
            lambda t: 2 * np.array([
                np.cos(PI - t),
                np.sin(PI - t),
                0
            ]),
            t_range=[0, PI/2],
            color=ORANGE
        )
        surface_wave_path.set_stroke(width=4)
        
        # Animate wave packet moving along surface
        wave_packet = Dot(radius=0.15, color=ORANGE)
        wave_packet.move_to(impact_point)
        
        explanation = Text(
            "Some energy couples into the surface and travels along it",
            font_size=20,
            color=WHITE
        )
        explanation.to_edge(DOWN).shift(UP * 0.5)
        self.add_text_element(explanation)
        
        self.play(
            Create(surface_wave_path),
            Write(explanation),
            run_time=1
        )
        
        self.play(
            MoveAlongPath(wave_packet, surface_wave_path),
            run_time=3,
            rate_func=linear
        )
        
        self.wait(1)
        
        # Store elements
        self.surface_wave_path = surface_wave_path
        self.incident_wave = incident_wave
        
    def demonstrate_creeping_waves(self):
        """Show the full creeping wave effect with clear visualization"""
        # Clean up old text and update title
        self.cleanup_text_elements()
        new_title = Text("Step 3: Creeping Wave Propagation", font_size=28)
        new_title.to_edge(UP).shift(DOWN * 0.3)
        self.add_text_element(new_title)
        self.play(Write(new_title))
        
        # Rotate camera for better view
        self.move_camera(phi=60 * DEGREES, theta=-30 * DEGREES, run_time=2)
        
        # Create multiple creeping wave paths
        creeping_paths = VGroup()
        
        # Generate paths at different heights on the sphere
        for z in np.linspace(-0.5, 0.5, 3):
            # Path that wraps around the sphere
            path = ParametricFunction(
                lambda t: 2.05 * np.array([  # Slightly larger than sphere radius
                    np.cos(PI - t),
                    np.sin(PI - t),
                    z
                ]),
                t_range=[0, 1.2 * PI],
                color=ORANGE
            )
            path.set_stroke(width=3, opacity=0.7)
            creeping_paths.add(path)
        
        # Show wave propagation
        self.play(Create(creeping_paths), run_time=2)
        
        # Animate multiple wave packets
        wave_packets = VGroup()
        for i, path in enumerate(creeping_paths):
            packet = Dot(radius=0.1, color=ORANGE)
            packet.move_to(path.get_start())
            wave_packets.add(packet)
        
        # Add wave decay visualization
        explanation = Text(
            "Waves 'creep' around the curved surface, losing energy as they travel",
            font_size=20,
            color=WHITE
        )
        explanation.to_edge(DOWN).shift(UP * 0.5)
        self.add_text_element(explanation)
        self.play(Write(explanation))
        
        # Animate packets with decay
        animations = []
        for packet, path in zip(wave_packets, creeping_paths):
            animations.append(
                MoveAlongPath(packet, path)
            )
            animations.append(
                packet.animate.set_opacity(0.2).scale(0.5)
            )
        
        self.play(*animations, run_time=4, rate_func=linear)
        
        self.wait(1)
        
        # Store for later
        self.creeping_paths = creeping_paths
        
    def show_backscatter_contribution(self):
        """Show how creeping waves contribute to backscatter"""
        # Clean up old text and update title
        self.cleanup_text_elements()
        new_title = Text("Step 4: Backscatter from Creeping Waves", font_size=28)
        new_title.to_edge(UP).shift(DOWN * 0.3)
        self.add_text_element(new_title)
        self.play(Write(new_title))
        
        # Rotate camera to show back of sphere
        self.move_camera(phi=70 * DEGREES, theta=150 * DEGREES, run_time=2)
        
        # Show radiation from the back
        back_radiation_points = [
            np.array([1.5, 0, 0.5]),
            np.array([1.5, 0, 0]),
            np.array([1.5, 0, -0.5])
        ]
        
        radiation_waves = VGroup()
        for point in back_radiation_points:
            # Create expanding circles to show radiation
            for r in np.linspace(0.2, 1, 3):
                circle = Circle(radius=r, color=PURPLE)
                circle.move_to(point)
                circle.set_stroke(width=2, opacity=0.5)
                radiation_waves.add(circle)
        
        # Show backscatter arrows
        backscatter_arrows = VGroup()
        for point in back_radiation_points:
            arrow = Arrow3D(
                start=point,
                end=point + np.array([-2, 0, 0]),
                color=PURPLE,
                thickness=0.03
            )
            backscatter_arrows.add(arrow)
        
        explanation = Text(
            "Creeping waves radiate from the shadow region, creating additional backscatter",
            font_size=20,
            color=WHITE
        )
        explanation.to_edge(DOWN).shift(UP * 0.5)
        self.add_text_element(explanation)
        
        self.play(
            Create(radiation_waves),
            Create(backscatter_arrows),
            Write(explanation),
            run_time=2
        )
        
        # Animate radiation
        self.play(
            radiation_waves.animate.scale(1.5).set_opacity(0.1),
            run_time=2
        )
        
        self.wait(1)
        
    def show_comparison(self):
        """Show comparison between with and without creeping waves"""
        # Clean up previous elements
        self.play(
            FadeOut(self.creeping_paths),
            FadeOut(self.incident_wave),
            FadeOut(self.surface_wave_path),
            run_time=1
        )
        
        # Clean up old text and update title
        self.cleanup_text_elements()
        new_title = Text("Comparison: Effect of Creeping Waves", font_size=28)
        new_title.to_edge(UP).shift(DOWN * 0.3)
        self.add_text_element(new_title)
        self.play(Write(new_title))
        
        # Reset camera
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=2)
        
        # Create comparison visualization
        comparison_group = VGroup()
        
        # Left side - Without creeping waves
        left_label = Text("Without Creeping Waves\n(Physical Optics Only)", font_size=18)
        left_label.to_edge(LEFT).shift(UP * 2)
        
        left_backscatter = Arrow(
            start=LEFT * 3,
            end=LEFT * 3 + LEFT * 1,
            color=RED,
            stroke_width=6
        )
        left_backscatter.shift(DOWN)
        
        # Right side - With creeping waves
        right_label = Text("With Creeping Waves\n(Actual Physics)", font_size=18)
        right_label.to_edge(RIGHT).shift(UP * 2)
        
        right_backscatter = Arrow(
            start=RIGHT * 3,
            end=RIGHT * 3 + LEFT * 1.5,
            color=GREEN,
            stroke_width=8
        )
        right_backscatter.shift(DOWN)
        
        # Add percentage labels
        left_percentage = Text("100%", font_size=24, color=RED)
        left_percentage.next_to(left_backscatter, DOWN)
        
        right_percentage = Text("150%", font_size=24, color=GREEN)
        right_percentage.next_to(right_backscatter, DOWN)
        
        # Add text elements with tracking
        self.add_text_element(left_label)
        self.add_text_element(right_label)
        self.add_text_element(left_percentage)
        self.add_text_element(right_percentage)
        
        # Add non-text elements normally
        self.add_fixed_in_frame_mobjects(left_backscatter, right_backscatter)
        
        self.play(
            Write(left_label),
            Write(right_label),
            Create(left_backscatter),
            Create(right_backscatter),
            Write(left_percentage),
            Write(right_percentage),
            run_time=2
        )
        
        # Final message
        final_message = Text(
            "Creeping waves can increase radar returns by 50% or more!",
            font_size=22,
            color=YELLOW
        )
        final_message.to_edge(DOWN).shift(UP * 0.5)
        self.add_text_element(final_message)
        self.play(Write(final_message))
        
        # Final rotation
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        

if __name__ == "__main__":
    # This file is meant to be run with manim
    pass 