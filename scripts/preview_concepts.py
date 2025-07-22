#!/usr/bin/env python3
"""
Generate static preview images showing key concepts from the animations
"""

from manim import *
import numpy as np

class CreepingWavesConcepts(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = "#0e1117"
        
        # Create a grid of concepts
        concepts = VGroup()
        
        # Concept 1: Direct Reflection
        concept1 = self.create_direct_reflection_concept()
        concept1.scale(0.4).to_corner(UL)
        concepts.add(concept1)
        
        # Concept 2: Surface Wave Formation
        concept2 = self.create_surface_wave_concept()
        concept2.scale(0.4).to_corner(UR)
        concepts.add(concept2)
        
        # Concept 3: Creeping Wave Path
        concept3 = self.create_creeping_path_concept()
        concept3.scale(0.4).to_corner(DL)
        concepts.add(concept3)
        
        # Concept 4: Backscatter Comparison
        concept4 = self.create_comparison_concept()
        concept4.scale(0.4).to_corner(DR)
        concepts.add(concept4)
        
        # Add all concepts
        self.add(concepts)
        
        # Add title
        title = Text("Creeping Waves: Key Concepts", font_size=36, weight=BOLD)
        title.to_edge(UP)
        self.add(title)
        
        # Add central explanation
        explanation = Text(
            "How electromagnetic waves create unexpected radar returns",
            font_size=20
        )
        explanation.next_to(title, DOWN)
        self.add(explanation)
        
    def create_direct_reflection_concept(self):
        """Create visual for direct reflection"""
        group = VGroup()
        
        # Sphere
        sphere = Circle(radius=1, color=GREY_B, fill_opacity=0.8)
        sphere.set_stroke(WHITE, 2)
        
        # Incident ray
        incident = Arrow(
            start=LEFT * 2.5,
            end=LEFT * 1,
            color=BLUE,
            buff=0
        )
        
        # Reflected ray
        reflected = Arrow(
            start=LEFT * 1,
            end=LEFT * 2.5 + UP * 1,
            color=RED,
            buff=0
        )
        
        # Label
        label = Text("Direct Reflection", font_size=16)
        label.next_to(sphere, DOWN, buff=0.5)
        
        group.add(sphere, incident, reflected, label)
        return group
        
    def create_surface_wave_concept(self):
        """Create visual for surface wave formation"""
        group = VGroup()
        
        # Sphere
        sphere = Circle(radius=1, color=GREY_B, fill_opacity=0.8)
        sphere.set_stroke(WHITE, 2)
        
        # Grazing incident ray
        incident = Arrow(
            start=LEFT * 2.5 + DOWN * 0.3,
            end=LEFT * 0.9 + DOWN * 0.9,
            color=BLUE,
            buff=0
        )
        
        # Surface wave indication
        surface_arc = Arc(
            radius=1.1,
            start_angle=225 * DEGREES,
            angle=-90 * DEGREES,
            color=ORANGE,
            stroke_width=4
        )
        
        # Energy coupling visualization
        coupling_dots = VGroup()
        for i in range(5):
            dot = Dot(
                point=sphere.point_at_angle(225 * DEGREES - i * 15 * DEGREES),
                radius=0.08,
                color=ORANGE
            )
            dot.set_opacity(1 - i * 0.15)
            coupling_dots.add(dot)
        
        # Label
        label = Text("Surface Wave Formation", font_size=16)
        label.next_to(sphere, DOWN, buff=0.5)
        
        group.add(sphere, incident, surface_arc, coupling_dots, label)
        return group
        
    def create_creeping_path_concept(self):
        """Create visual for creeping wave path"""
        group = VGroup()
        
        # Sphere
        sphere = Circle(radius=1, color=GREY_B, fill_opacity=0.8)
        sphere.set_stroke(WHITE, 2)
        
        # Multiple creeping paths
        paths = VGroup()
        for offset in [-0.3, 0, 0.3]:
            path = Arc(
                radius=1.05,
                start_angle=180 * DEGREES,
                angle=-270 * DEGREES,
                color=ORANGE
            )
            path.shift(UP * offset * 0.5)
            path.set_stroke(width=3, opacity=0.7)
            paths.add(path)
        
        # Decay indication
        for i, path in enumerate(paths):
            # Add fading effect
            path.set_stroke(opacity=0.8 - i * 0.1)
        
        # Shadow region indicator
        shadow_arc = Arc(
            radius=1,
            start_angle=0,
            angle=180 * DEGREES,
            color=DARK_GREY,
            fill_opacity=0.3,
            stroke_width=0
        )
        
        # Label
        label = Text("Creeping Wave Path", font_size=16)
        label.next_to(sphere, DOWN, buff=0.5)
        
        group.add(shadow_arc, sphere, paths, label)
        return group
        
    def create_comparison_concept(self):
        """Create visual for RCS comparison"""
        group = VGroup()
        
        # Create bar chart
        axes = Axes(
            x_range=[0, 2, 1],
            y_range=[0, 1.5, 0.5],
            x_length=3,
            y_length=2,
            axis_config={"include_tip": False}
        )
        
        # PO bar
        po_bar = Rectangle(
            width=0.6,
            height=1,
            color=RED,
            fill_opacity=0.8
        )
        po_bar.move_to(axes.c2p(0.5, 0.5))
        
        # Actual bar
        actual_bar = Rectangle(
            width=0.6,
            height=1.5,
            color=GREEN,
            fill_opacity=0.8
        )
        actual_bar.move_to(axes.c2p(1.5, 0.75))
        
        # Labels
        po_label = Text("PO", font_size=14)
        po_label.next_to(po_bar, DOWN)
        
        actual_label = Text("Actual", font_size=14)
        actual_label.next_to(actual_bar, DOWN)
        
        # Title
        chart_title = Text("RCS Comparison", font_size=16)
        chart_title.next_to(axes, UP)
        
        # Percentage labels
        po_percent = Text("100%", font_size=12, color=RED)
        po_percent.next_to(po_bar, UP)
        
        actual_percent = Text("150%", font_size=12, color=GREEN)
        actual_percent.next_to(actual_bar, UP)
        
        group.add(axes, po_bar, actual_bar, po_label, actual_label, 
                  chart_title, po_percent, actual_percent)
        return group


class PhysicsExplanation(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = "#0e1117"
        
        # Title
        title = Text("The Physics Behind Creeping Waves", font_size=32, weight=BOLD)
        title.to_edge(UP)
        self.add(title)
        
        # Create three panels showing the progression
        panels = VGroup()
        
        # Panel 1: Wave hits sphere
        panel1 = self.create_wave_impact_panel()
        panel1.scale(0.8).shift(LEFT * 4)
        panels.add(panel1)
        
        # Panel 2: Surface propagation
        panel2 = self.create_propagation_panel()
        panel2.scale(0.8)
        panels.add(panel2)
        
        # Panel 3: Backscatter
        panel3 = self.create_backscatter_panel()
        panel3.scale(0.8).shift(RIGHT * 4)
        panels.add(panel3)
        
        self.add(panels)
        
        # Add flow arrows between panels
        arrow1 = Arrow(
            start=panel1.get_right(),
            end=panel2.get_left(),
            color=YELLOW,
            buff=0.1
        )
        arrow2 = Arrow(
            start=panel2.get_right(),
            end=panel3.get_left(),
            color=YELLOW,
            buff=0.1
        )
        
        self.add(arrow1, arrow2)
        
        # Add explanatory text
        explanations = VGroup()
        
        exp1 = Text("Grazing incidence\ncouples to surface", font_size=14)
        exp1.next_to(panel1, DOWN)
        
        exp2 = Text("Wave travels along\ncurved boundary", font_size=14)
        exp2.next_to(panel2, DOWN)
        
        exp3 = Text("Radiation from\nshadow region", font_size=14)
        exp3.next_to(panel3, DOWN)
        
        explanations.add(exp1, exp2, exp3)
        self.add(explanations)
        
    def create_wave_impact_panel(self):
        """Panel showing wave impact"""
        group = VGroup()
        
        # Sphere
        sphere = Circle(radius=0.8, color=GREY_B, fill_opacity=0.8)
        
        # Multiple incident rays at grazing angle
        rays = VGroup()
        for i in range(3):
            ray = Arrow(
                start=LEFT * 1.5 + UP * (0.2 - i * 0.1),
                end=sphere.get_left() + UP * (0.2 - i * 0.1),
                color=BLUE,
                buff=0,
                stroke_width=2
            )
            rays.add(ray)
        
        # Impact region highlight
        impact = Dot(sphere.get_left(), radius=0.15, color=YELLOW)
        
        group.add(sphere, rays, impact)
        return group
        
    def create_propagation_panel(self):
        """Panel showing surface propagation"""
        group = VGroup()
        
        # Sphere
        sphere = Circle(radius=0.8, color=GREY_B, fill_opacity=0.8)
        
        # Surface wave visualization
        wave_path = Arc(
            radius=0.85,
            start_angle=180 * DEGREES,
            angle=-180 * DEGREES,
            color=ORANGE,
            stroke_width=4
        )
        
        # Wave packets along path
        packets = VGroup()
        for angle in [150, 90, 30, -30]:
            packet = Dot(
                sphere.point_at_angle(angle * DEGREES),
                radius=0.08,
                color=ORANGE
            )
            packet.set_opacity(1 - abs(angle) / 180)
            packets.add(packet)
        
        # Decay indication
        decay_text = Text("e^(-αs)", font_size=12, color=ORANGE)
        decay_text.next_to(sphere, RIGHT)
        
        group.add(sphere, wave_path, packets, decay_text)
        return group
        
    def create_backscatter_panel(self):
        """Panel showing backscatter"""
        group = VGroup()
        
        # Sphere
        sphere = Circle(radius=0.8, color=GREY_B, fill_opacity=0.8)
        
        # Shadow region
        shadow = Arc(
            radius=0.8,
            start_angle=0,
            angle=180 * DEGREES,
            color=DARK_GREY,
            fill_opacity=0.4,
            stroke_width=0
        )
        
        # Radiating waves from back
        radiation = VGroup()
        for r in [0.3, 0.5, 0.7]:
            arc = Arc(
                radius=r,
                start_angle=-60 * DEGREES,
                angle=120 * DEGREES,
                color=PURPLE,
                stroke_width=2,
                stroke_opacity=0.7 - r
            )
            arc.shift(RIGHT * 0.8)
            radiation.add(arc)
        
        # Backscatter arrow
        back_arrow = Arrow(
            start=RIGHT * 0.8,
            end=RIGHT * 2,
            color=PURPLE,
            buff=0
        )
        
        group.add(shadow, sphere, radiation, back_arrow)
        return group


if __name__ == "__main__":
    # Generate preview images
    import subprocess
    
    print("Generating concept preview...")
    subprocess.run([
        "manim", "-qh", "-s", 
        "preview_concepts.py", 
        "CreepingWavesConcepts"
    ])
    
    print("Generating physics explanation preview...")
    subprocess.run([
        "manim", "-qh", "-s",
        "preview_concepts.py",
        "PhysicsExplanation"
    ])
    
    print("\nPreview images saved to media/images/")
    print("These show the key concepts that will be animated in the full versions") 