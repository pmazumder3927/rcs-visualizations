from manim import *
import numpy as np

class CreepingWavesEnhanced(ThreeDScene):
    def construct(self):
        # Configure scene for better visibility
        self.renderer.background_color = "#0e1117"
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, distance=10)
        
        # Track text elements for cleanup
        self.current_text_elements = []
        
        # Create the main animation sequence
        self.create_title_sequence()
        self.demonstrate_em_wave_basics()
        self.show_wave_sphere_interaction()
        self.visualize_surface_wave_physics()
        self.show_creeping_wave_mechanism()
        self.demonstrate_radar_implications()
        
    def create_title_sequence(self):
        """Create an engaging title sequence"""
        # Main title
        title = Text("The Physics of Creeping Waves", font_size=40, weight=BOLD)
        subtitle = Text("How electromagnetic waves sneak around curved surfaces", font_size=24)
        subtitle.next_to(title, DOWN)
        
        title_group = VGroup(title, subtitle)
        title_group.to_edge(UP)
        
        self.add_fixed_in_frame_mobjects(title_group)
        self.play(
            Write(title),
            FadeIn(subtitle, shift=UP),
            run_time=2
        )
        
        self.wait(2)
        self.play(FadeOut(title_group))
        
    def demonstrate_em_wave_basics(self):
        """Show basic EM wave properties"""
        # Section title
        self.cleanup_text_elements()
        section_title = Text("Understanding Electromagnetic Waves", font_size=28)
        section_title.to_edge(UP)
        self.add_text_element(section_title)
        self.play(Write(section_title))
        
        # Create EM wave visualization
        wave_length = 8
        wave_height = 2
        
        # Electric field component (vertical)
        e_wave = ParametricFunction(
            lambda t: np.array([t, 0, wave_height * np.sin(2 * PI * t / 2)]),
            t_range=[-wave_length/2, wave_length/2],
            color=BLUE
        )
        e_wave.shift(UP * 1.5)
        
        # Magnetic field component (horizontal)
        b_wave = ParametricFunction(
            lambda t: np.array([t, wave_height * np.sin(2 * PI * t / 2), 0]),
            t_range=[-wave_length/2, wave_length/2],
            color=RED
        )
        b_wave.shift(UP * 1.5)
        
        # Propagation direction arrow
        prop_arrow = Arrow(
            start=LEFT * 4 + UP * 1.5,
            end=RIGHT * 4 + UP * 1.5,
            color=GREEN,
            buff=0
        )
        
        # Labels
        e_label = Text("E-field", font_size=20, color=BLUE)
        e_label.move_to(UP * 3 + LEFT * 3)
        b_label = Text("B-field", font_size=20, color=RED)
        b_label.move_to(UP * 0.5 + LEFT * 3)
        prop_label = Text("Propagation", font_size=20, color=GREEN)
        prop_label.move_to(DOWN * 0.5 + RIGHT * 2)
        
        self.add_text_element(e_label)
        self.add_text_element(b_label)
        self.add_text_element(prop_label)
        
        # Animate
        self.play(
            Create(e_wave),
            Create(b_wave),
            Create(prop_arrow),
            Write(e_label),
            Write(b_label),
            Write(prop_label),
            run_time=2
        )
        
        # Show wave motion
        self.play(
            e_wave.animate.shift(RIGHT * 2),
            b_wave.animate.shift(RIGHT * 2),
            run_time=2,
            rate_func=linear
        )
        
        self.wait(1)
        
        # Fade out
        self.play(
            FadeOut(VGroup(e_wave, b_wave, prop_arrow, e_label, b_label, prop_label, section_title)),
            run_time=1
        )
        
    def show_wave_sphere_interaction(self):
        """Show what happens when waves hit a sphere"""
        # New section title
        self.cleanup_text_elements()
        section_title = Text("Wave Meets Sphere: Three Phenomena", font_size=28)
        section_title.to_edge(UP)
        self.add_text_element(section_title)
        self.play(Write(section_title))
        
        # Create sphere with better materials
        sphere = Sphere(radius=2, resolution=(40, 40))
        sphere.set_color(color=[GREY_B, GREY_C])
        sphere.set_opacity(0.95)
        # Note: Sheen effects removed for compatibility
        
        # Create grid to show wave distortion
        grid = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        grid.rotate(90 * DEGREES, axis=RIGHT)
        grid.shift(LEFT * 3)
        
        self.play(
            Create(sphere),
            Create(grid),
            run_time=2
        )
        
        # Animate wave hitting sphere
        wave_lines = VGroup()
        for y in np.linspace(-3, 3, 7):
            line = Line(
                start=np.array([-6, y, 0]),
                end=np.array([-2.5, y, 0]),
                color=BLUE,
                stroke_width=2
            )
            wave_lines.add(line)
        
        self.play(Create(wave_lines))
        
        # Show three effects with labels
        # 1. Reflection
        reflection_arrow = Arrow3D(
            start=np.array([-2, 0, 0]),
            end=np.array([-4, -2, 0]),
            color=RED,
            thickness=0.05
        )
        reflection_label = Text("1. Reflection", font_size=20, color=RED)
        reflection_label.move_to(LEFT * 4 + DOWN * 3)
        
        # 2. Diffraction
        diffraction_arcs = VGroup()
        for angle in np.linspace(-60, 60, 5) * DEGREES:
            arc = Arc(
                radius=0.5,
                start_angle=angle - 10 * DEGREES,
                angle=20 * DEGREES,
                color=YELLOW
            )
            arc.move_to(np.array([2 * np.cos(angle + 90 * DEGREES), 2 * np.sin(angle + 90 * DEGREES), 0]))
            diffraction_arcs.add(arc)
        
        diffraction_label = Text("2. Diffraction", font_size=20, color=YELLOW)
        diffraction_label.move_to(RIGHT * 3 + UP * 3)
        
        # 3. Surface wave
        surface_wave = ParametricFunction(
            lambda t: 2.05 * np.array([np.cos(t), np.sin(t), 0]),
            t_range=[PI, 2 * PI],
            color=ORANGE
        )
        surface_wave.set_stroke(width=4)
        
        surface_label = Text("3. Surface Wave", font_size=20, color=ORANGE)
        surface_label.move_to(DOWN * 3)
        
        self.add_text_element(reflection_label)
        self.add_text_element(diffraction_label)
        self.add_text_element(surface_label)
        
        # Animate all three
        self.play(
            Create(reflection_arrow),
            Write(reflection_label),
            Create(diffraction_arcs),
            Write(diffraction_label),
            Create(surface_wave),
            Write(surface_label),
            run_time=3
        )
        
        self.wait(2)
        
        # Store sphere for later
        self.sphere = sphere
        
        # Clean up
        self.play(
            FadeOut(VGroup(
                wave_lines, grid, reflection_arrow, diffraction_arcs,
                reflection_label, diffraction_label, surface_label, section_title
            )),
            run_time=1
        )
        
    def visualize_surface_wave_physics(self):
        """Deep dive into surface wave physics"""
        # New title
        self.cleanup_text_elements()
        section_title = Text("The Birth of a Creeping Wave", font_size=28)
        section_title.to_edge(UP)
        self.add_text_element(section_title)
        self.play(Write(section_title))
        
        # Zoom in on surface
        self.move_camera(
            phi=45 * DEGREES,
            theta=-60 * DEGREES,
            distance=6,
            run_time=2
        )
        
        # Show grazing incidence
        grazing_angle = 10 * DEGREES
        impact_point = np.array([2 * np.cos(grazing_angle), 2 * np.sin(grazing_angle), 0])
        
        incident_ray = Arrow3D(
            start=impact_point + np.array([-3, -0.5, 0]),
            end=impact_point,
            color=BLUE,
            thickness=0.04
        )
        
        # Show field lines coupling to surface
        field_lines = VGroup()
        for i in range(5):
            offset = i * 0.2
            field_line = CurvedArrow(
                start_point=impact_point + np.array([-offset, 0, 0]),
                end_point=impact_point + np.array([0.3, 0.3, 0]),
                color=interpolate_color(BLUE, ORANGE, i/4),
                angle=-TAU/8
            )
            field_lines.add(field_line)
        
        self.play(
            Create(incident_ray),
            Create(field_lines),
            run_time=2
        )
        
        # Show surface current formation
        surface_current_region = Annulus(
            inner_radius=1.8,
            outer_radius=2.2,
            color=ORANGE,
            fill_opacity=0.3
        )
        surface_current_region.move_to(ORIGIN)
        
        current_arrows = VGroup()
        for angle in np.linspace(0, PI/3, 8):
            arrow_start = 2 * np.array([np.cos(angle), np.sin(angle), 0])
            tangent = np.array([-np.sin(angle), np.cos(angle), 0])
            arrow = Arrow(
                start=arrow_start,
                end=arrow_start + 0.5 * tangent,
                color=ORANGE,
                buff=0,
                stroke_width=3
            )
            current_arrows.add(arrow)
        
        explanation = Text(
            "Grazing waves induce surface currents that propagate along the boundary",
            font_size=18
        )
        explanation.to_edge(DOWN).shift(UP * 0.3)
        self.add_text_element(explanation)
        
        self.play(
            Create(surface_current_region),
            Create(current_arrows),
            Write(explanation),
            run_time=2
        )
        
        # Animate current flow
        self.play(
            current_arrows.animate.shift(RIGHT * 0.5),
            rate_func=linear,
            run_time=1.5
        )
        
        self.wait(1)
        
        # Clean up
        self.play(
            FadeOut(VGroup(
                incident_ray, field_lines, surface_current_region,
                current_arrows, explanation, section_title
            )),
            run_time=1
        )
        
    def show_creeping_wave_mechanism(self):
        """Show the full creeping wave propagation"""
        # New title
        self.cleanup_text_elements()
        section_title = Text("Creeping Wave Journey", font_size=28)
        section_title.to_edge(UP)
        self.add_text_element(section_title)
        self.play(Write(section_title))
        
        # Reset camera for full view
        self.move_camera(
            phi=70 * DEGREES,
            theta=30 * DEGREES,
            distance=12,
            run_time=2
        )
        
        # Create wave packet visualization
        num_packets = 6
        wave_packets = VGroup()
        paths = VGroup()
        
        for i in range(num_packets):
            # Create path
            z_offset = (i - num_packets/2) * 0.3
            path = ParametricFunction(
                lambda t: 2.1 * np.array([
                    np.cos(PI - t),
                    np.sin(PI - t),
                    z_offset
                ]),
                t_range=[0, 1.5 * PI],
                color=ORANGE
            )
            path.set_stroke(width=2, opacity=0.5)
            paths.add(path)
            
            # Create wave packet
            packet = VGroup()
            
            # Main dot
            dot = Dot3D(point=path.get_start(), radius=0.08, color=ORANGE)
            
            # Trailing wave visualization
            wave_trail = VGroup()
            for j in range(3):
                trail_dot = Dot3D(
                    point=path.get_start(),
                    radius=0.06 - j * 0.02,
                    color=ORANGE
                )
                trail_dot.set_opacity(0.7 - j * 0.2)
                wave_trail.add(trail_dot)
            
            packet.add(dot, wave_trail)
            wave_packets.add(packet)
        
        # Create attenuation zones
        attenuation_text = Text("Wave amplitude decreases exponentially", font_size=18)
        attenuation_text.to_edge(RIGHT).shift(DOWN * 2)
        self.add_text_element(attenuation_text)
        
        # Show paths first
        self.play(Create(paths), run_time=2)
        
        # Animate packets along paths with decay
        self.play(Write(attenuation_text))
        
        # Create individual animations for each packet
        packet_animations = []
        for i, (packet, path) in enumerate(zip(wave_packets, paths)):
            # Stagger the start times
            packet_animations.append(
                AnimationGroup(
                    MoveAlongPath(packet, path),
                    packet.animate.set_opacity(0.1).scale(0.3),
                    lag_ratio=0.1 * i,
                    run_time=5
                )
            )
        
        self.play(*packet_animations)
        
        self.wait(1)
        
        # Clean up
        self.play(
            FadeOut(VGroup(paths, wave_packets, attenuation_text, section_title)),
            run_time=1
        )
        
    def demonstrate_radar_implications(self):
        """Show the radar implications with clear comparison"""
        # Final title
        self.cleanup_text_elements()
        section_title = Text("Why Creeping Waves Matter for Radar", font_size=28)
        section_title.to_edge(UP)
        self.add_text_element(section_title)
        self.play(Write(section_title))
        
        # Create split screen comparison
        divider = DashedLine(
            start=UP * 3,
            end=DOWN * 3,
            color=WHITE,
            stroke_width=2
        )
        self.add_fixed_in_frame_mobjects(divider)
        self.play(Create(divider))
        
        # Left side - simplified model
        left_title = Text("Simplified Model\n(No Creeping Waves)", font_size=20)
        left_title.to_edge(LEFT).shift(UP * 2)
        
        # Create left sphere (smaller for display)
        left_sphere = Sphere(radius=1, resolution=(20, 20))
        left_sphere.shift(LEFT * 3)
        left_sphere.set_color(GREY_C)
        left_sphere.set_opacity(0.8)
        
        # Show only front reflection
        left_incident = Arrow(
            start=LEFT * 5,
            end=LEFT * 4,
            color=BLUE
        )
        left_reflected = Arrow(
            start=LEFT * 4,
            end=LEFT * 5,
            color=RED
        )
        
        left_rcs_text = Text("Predicted RCS: 1.0", font_size=18, color=RED)
        left_rcs_text.move_to(LEFT * 3 + DOWN * 2.5)
        
        # Right side - actual physics
        right_title = Text("Actual Physics\n(With Creeping Waves)", font_size=20)
        right_title.to_edge(RIGHT).shift(UP * 2)
        
        # Create right sphere
        right_sphere = Sphere(radius=1, resolution=(20, 20))
        right_sphere.shift(RIGHT * 3)
        right_sphere.set_color(GREY_C)
        right_sphere.set_opacity(0.8)
        
        # Show incident wave
        right_incident = Arrow(
            start=RIGHT * 1,
            end=RIGHT * 2,
            color=BLUE
        )
        
        # Show multiple returns
        right_reflected = Arrow(
            start=RIGHT * 2,
            end=RIGHT * 1,
            color=RED
        )
        
        # Creeping wave contribution
        creeping_return = Arrow(
            start=RIGHT * 4,
            end=RIGHT * 2.5,
            color=ORANGE
        )
        creeping_return.set_stroke(width=4)
        
        right_rcs_text = Text("Actual RCS: 1.5", font_size=18, color=GREEN)
        right_rcs_text.move_to(RIGHT * 3 + DOWN * 2.5)
        
        # Add all elements
        self.add_fixed_in_frame_mobjects(
            left_title, right_title,
            left_rcs_text, right_rcs_text
        )
        
        self.play(
            Create(left_sphere),
            Create(right_sphere),
            Write(left_title),
            Write(right_title),
            run_time=2
        )
        
        self.play(
            Create(left_incident),
            Create(left_reflected),
            Create(right_incident),
            Create(right_reflected),
            Write(left_rcs_text),
            run_time=2
        )
        
        # Emphasize the creeping wave contribution
        creeping_label = Text("Extra return from\ncreeping waves!", font_size=16, color=ORANGE)
        creeping_label.move_to(RIGHT * 4 + UP * 0.5)
        self.add_fixed_in_frame_mobjects(creeping_label)
        
        self.play(
            Create(creeping_return),
            Write(creeping_label),
            Write(right_rcs_text),
            run_time=2
        )
        
        # Final emphasis
        conclusion = Text(
            "Creeping waves explain why radar sees more than simple models predict",
            font_size=22,
            color=YELLOW
        )
        conclusion.to_edge(DOWN).shift(UP * 0.3)
        self.add_fixed_in_frame_mobjects(conclusion)
        
        self.play(Write(conclusion))
        self.wait(3)
        
        # Final camera rotation
        self.move_camera(
            phi=80 * DEGREES,
            theta=-45 * DEGREES,
            distance=15,
            run_time=3
        )
        self.wait(2)
        
    def cleanup_text_elements(self):
        """Remove all current text elements from the scene"""
        if self.current_text_elements:
            self.remove(*self.current_text_elements)
            self.current_text_elements = []
    
    def add_text_element(self, text_obj):
        """Add a text element and track it for cleanup"""
        self.current_text_elements.append(text_obj)
        self.add_fixed_in_frame_mobjects(text_obj)


if __name__ == "__main__":
    # Run with: manim -pqh creeping_waves_enhanced.py CreepingWavesEnhanced
    pass 