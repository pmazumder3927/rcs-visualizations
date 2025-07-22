from manim import *
import numpy as np

class VoxelTopologyVisualization(ThreeDScene):
    def construct(self):
        # Configure scene
        self.renderer.background_color = "#0e1117"
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, distance=12)
        
        # Title
        title = Text("Density-Based Topology Optimization", font_size=32, weight=BOLD)
        subtitle = Text("Creating and removing material for optimal RCS", font_size=20)
        subtitle.next_to(title, DOWN)
        
        title_group = VGroup(title, subtitle)
        title_group.to_edge(UP)
        
        self.add_fixed_in_frame_mobjects(title_group)
        self.play(Write(title), FadeIn(subtitle, shift=UP), run_time=2)
        self.wait(2)
        self.play(FadeOut(title_group))
        
        # Create voxel grid
        grid_size = 8
        voxel_size = 0.4
        
        # Initial shape - a solid block with some structure
        initial_voxels = []
        voxel_objects = VGroup()
        
        # Create initial shape (wing-like structure)
        for i in range(grid_size):
            for j in range(grid_size):
                for k in range(grid_size):
                    # Create a wing-like initial shape
                    x_norm = (i - grid_size/2) / (grid_size/2)
                    y_norm = (j - grid_size/2) / (grid_size/2)
                    z_norm = (k - grid_size/2) / (grid_size/2)
                    
                    # Wing profile condition
                    if (abs(y_norm) < 0.8 and 
                        abs(z_norm) < 0.3 - 0.2 * abs(x_norm) and
                        abs(x_norm) < 0.9):
                        
                        pos = np.array([
                            (i - grid_size/2) * voxel_size * 1.2,
                            (j - grid_size/2) * voxel_size * 1.2,
                            (k - grid_size/2) * voxel_size * 1.2
                        ])
                        
                        voxel = Cube(side_length=voxel_size)
                        voxel.move_to(pos)
                        voxel.set_color(BLUE_C)
                        voxel.set_stroke(WHITE, width=1)
                        
                        initial_voxels.append((i, j, k, voxel))
                        voxel_objects.add(voxel)
        
        # Show initial structure
        self.play(Create(voxel_objects), run_time=2)
        
        initial_label = Text("Initial Design", font_size=20, color=BLUE)
        initial_label.to_edge(LEFT).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(initial_label)
        self.play(Write(initial_label))
        
        # Explain density approach
        explanation = Text(
            "Each voxel has density ρ ∈ [0, 1]",
            font_size=22
        )
        explanation.to_edge(DOWN).shift(UP * 0.5)
        
        density_eq = MathTex(
            r"\rho = 0 \text{ (air)}, \quad \rho = 1 \text{ (material)}",
            font_size=24
        )
        density_eq.next_to(explanation, UP)
        
        self.add_fixed_in_frame_mobjects(explanation, density_eq)
        self.play(Write(explanation), Write(density_eq))
        self.wait(2)
        
        # Show optimization process
        self.play(FadeOut(explanation), FadeOut(density_eq), FadeOut(initial_label))
        
        opt_title = Text("Optimization in Progress...", font_size=24, color=YELLOW)
        opt_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(opt_title)
        self.play(Write(opt_title))
        
        # Create density visualization
        density_scale = VGroup()
        for i in range(11):
            density = i / 10
            color = interpolate_color(WHITE, BLUE_C, density)
            
            box = Square(side_length=0.3)
            box.set_fill(color, opacity=density if density > 0 else 0.1)
            box.set_stroke(WHITE, width=1)
            box.shift(RIGHT * (i - 5) * 0.35 + DOWN * 3)
            
            if i % 5 == 0:
                label = Text(f"{density:.1f}", font_size=12)
                label.next_to(box, DOWN, buff=0.1)
                density_scale.add(label)
            
            density_scale.add(box)
        
        density_label = Text("Density Scale", font_size=16)
        density_label.next_to(density_scale, UP)
        density_scale.add(density_label)
        
        self.add_fixed_in_frame_mobjects(density_scale)
        self.play(Create(density_scale))
        
        # Optimization iterations
        for iteration in range(3):
            iter_text = Text(f"Iteration {iteration + 1}", font_size=20)
            iter_text.to_edge(RIGHT).shift(UP * 2)
            self.add_fixed_in_frame_mobjects(iter_text)
            self.play(Write(iter_text))
            
            # Voxels to remove (low sensitivity regions)
            voxels_to_remove = []
            # Voxels to add (high sensitivity regions)
            voxels_to_add = []
            
            current_voxels = [(i, j, k) for i, j, k, _ in initial_voxels]
            
            # Simulate sensitivity analysis
            for i, j, k, voxel in initial_voxels:
                # Remove voxels from thick regions
                neighbors = sum(1 for di in [-1, 0, 1] for dj in [-1, 0, 1] for dk in [-1, 0, 1]
                              if (i+di, j+dj, k+dk) in current_voxels)
                
                if neighbors > 20 and np.random.random() < 0.3:
                    voxels_to_remove.append(voxel)
            
            # Add voxels at edges (for demonstration)
            for i in range(grid_size):
                for j in range(grid_size):
                    for k in range(grid_size):
                        if (i, j, k) not in current_voxels:
                            # Check if adjacent to existing voxel
                            adjacent = any((i+di, j+dj, k+dk) in current_voxels 
                                         for di in [-1, 0, 1] for dj in [-1, 0, 1] for dk in [-1, 0, 1]
                                         if abs(di) + abs(dj) + abs(dk) == 1)
                            
                            if adjacent and np.random.random() < 0.1:
                                pos = np.array([
                                    (i - grid_size/2) * voxel_size * 1.2,
                                    (j - grid_size/2) * voxel_size * 1.2,
                                    (k - grid_size/2) * voxel_size * 1.2
                                ])
                                
                                new_voxel = Cube(side_length=voxel_size)
                                new_voxel.move_to(pos)
                                new_voxel.set_color(GREEN_C)
                                new_voxel.set_stroke(WHITE, width=1)
                                new_voxel.set_opacity(0)
                                
                                voxels_to_add.append((i, j, k, new_voxel))
            
            # Animate removal (fade to transparent)
            if voxels_to_remove:
                self.play(
                    *[voxel.animate.set_opacity(0.2).set_color(RED) for voxel in voxels_to_remove],
                    run_time=1
                )
                self.play(
                    *[FadeOut(voxel) for voxel in voxels_to_remove],
                    run_time=1
                )
            
            # Animate addition
            if voxels_to_add:
                for i, j, k, voxel in voxels_to_add:
                    self.add(voxel)
                
                self.play(
                    *[voxel.animate.set_opacity(1) for _, _, _, voxel in voxels_to_add],
                    run_time=1
                )
                
                # Change color to match
                self.play(
                    *[voxel.animate.set_color(BLUE_C) for _, _, _, voxel in voxels_to_add],
                    run_time=0.5
                )
                
                # Update initial_voxels
                initial_voxels.extend(voxels_to_add)
            
            # Update current voxels list
            initial_voxels = [v for v in initial_voxels if v[3] not in voxels_to_remove]
            
            self.play(FadeOut(iter_text))
            self.wait(0.5)
        
        # Show final optimized structure
        self.play(FadeOut(opt_title))
        
        final_title = Text("Optimized Topology", font_size=24, color=GREEN)
        final_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(final_title)
        self.play(Write(final_title))
        
        # Highlight topology changes
        change_text = Text(
            "Material removed from low-sensitivity regions\nMaterial added to high-impact areas",
            font_size=18,
            color=YELLOW
        )
        change_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(change_text)
        self.play(Write(change_text))
        
        # Rotate camera to show structure
        self.move_camera(
            phi=45 * DEGREES,
            theta=-60 * DEGREES,
            distance=10,
            run_time=3
        )
        
        self.wait(1)
        
        # Show advantage: hole creation
        self.play(FadeOut(change_text), FadeOut(density_scale))
        
        hole_title = Text("Key Advantage: Topology Changes", font_size=24)
        hole_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(hole_title)
        self.play(
            FadeOut(final_title),
            Write(hole_title)
        )
        
        # Create example with hole
        hole_demo = VGroup()
        
        # Initial solid block
        for i in range(5):
            for j in range(5):
                for k in range(2):
                    pos = np.array([i * 0.5 - 1, j * 0.5 - 1, k * 0.5]) + RIGHT * 5
                    voxel = Cube(side_length=0.4)
                    voxel.move_to(pos)
                    voxel.set_color(BLUE_C)
                    voxel.set_stroke(WHITE, width=1)
                    hole_demo.add(voxel)
        
        self.play(Create(hole_demo))
        
        # Remove center voxels to create hole
        center_voxels = []
        for i in range(1, 4):
            for j in range(1, 4):
                idx = i * 5 + j
                for k in range(2):
                    center_voxels.append(hole_demo[idx * 2 + k])
        
        hole_text = Text("Creating internal voids\nimpossible with deformation", font_size=18)
        hole_text.next_to(hole_demo, DOWN)
        self.add_fixed_in_frame_mobjects(hole_text)
        
        self.play(
            *[voxel.animate.set_color(RED).set_opacity(0.3) for voxel in center_voxels],
            Write(hole_text),
            run_time=1
        )
        
        self.play(
            *[FadeOut(voxel) for voxel in center_voxels],
            run_time=1
        )
        
        # Final summary
        summary = Text(
            "Density-based methods enable true topology optimization\nbut require manufacturing constraints",
            font_size=20,
            color=YELLOW
        )
        summary.to_edge(DOWN).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(summary)
        self.play(
            FadeOut(hole_text),
            Write(summary)
        )
        
        # Final camera movement
        self.move_camera(
            phi=70 * DEGREES,
            theta=45 * DEGREES,
            distance=12,
            run_time=3
        )
        
        self.wait(3)

if __name__ == "__main__":
    # Run with: manim -pqh voxel_topology_visualization.py VoxelTopologyVisualization
    pass