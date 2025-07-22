from manim import *
import numpy as np

class OptimizerComparisonVisualization(ThreeDScene):
    def construct(self):
        # Configure scene
        self.renderer.background_color = "#0e1117"
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES, distance=20)
        
        # Title
        title = Text("Optimization Algorithms: Gradient Descent vs Adam", font_size=32, weight=BOLD)
        subtitle = Text("Finding the minimum RCS configuration", font_size=20)
        subtitle.next_to(title, DOWN)
        
        title_group = VGroup(title, subtitle)
        title_group.to_edge(UP)
        
        self.add_fixed_in_frame_mobjects(title_group)
        self.play(Write(title), FadeIn(subtitle, shift=UP), run_time=2)
        self.wait(2)
        self.play(FadeOut(title_group))
        
        # Create loss landscape (hill/valley)
        def loss_surface(u, v):
            # Create a complex landscape with local minima
            x = 4 * (u - 0.5)
            y = 4 * (v - 0.5)
            
            # Main valley
            z = 0.5 * (x**2 + y**2)
            
            # Add some bumps and local minima
            z += 0.3 * np.sin(3 * x) * np.cos(3 * y)
            z += 0.2 * np.exp(-((x - 1)**2 + (y - 1)**2))
            z -= 0.4 * np.exp(-((x + 1)**2 + (y + 1)**2))  # Local minimum
            z -= 0.8 * np.exp(-((x - 0.5)**2 + (y + 0.5)**2))  # Global minimum
            
            return np.array([x, y, z * 0.5])
        
        surface = Surface(
            loss_surface,
            u_range=[0, 1],
            v_range=[0, 1],
            resolution=(40, 40),
            fill_opacity=0.8
        )
        
        # Color based on height
        surface.set_fill_by_value(axes=Axes(), colorscale=[(BLUE_E, -1), (BLUE_C, 0), (RED_C, 1), (RED_E, 2)])
        
        # Add coordinate system
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-1, 2, 1],
            x_length=8,
            y_length=8,
            z_length=4
        )
        axes.shift(DOWN * 1)
        
        # Labels
        x_label = Text("Deformation X", font_size=16)
        x_label.move_to(axes.x_axis.get_end() + DOWN * 0.5)
        y_label = Text("Deformation Y", font_size=16)
        y_label.move_to(axes.y_axis.get_end() + LEFT * 0.5)
        z_label = Text("RCS Value", font_size=16)
        z_label.move_to(axes.z_axis.get_end() + RIGHT * 0.5)
        
        self.add_fixed_in_frame_mobjects(x_label, y_label, z_label)
        
        self.play(
            Create(axes),
            Create(surface),
            Write(x_label),
            Write(y_label),
            Write(z_label),
            run_time=3
        )
        
        # Starting point for both optimizers
        start_point = np.array([1.5, -1.5, 0])
        start_z = loss_surface(0.875, 0.125)[2]
        start_point[2] = start_z
        
        # Create balls for each optimizer
        gd_ball = Sphere(radius=0.1, color=BLUE)
        gd_ball.move_to(start_point)
        
        adam_ball = Sphere(radius=0.1, color=GREEN)
        adam_ball.move_to(start_point)
        
        # Labels for optimizers
        gd_label = Text("Gradient Descent", font_size=18, color=BLUE)
        gd_label.to_edge(LEFT).shift(UP * 2)
        
        adam_label = Text("Adam Optimizer", font_size=18, color=GREEN)
        adam_label.to_edge(RIGHT).shift(UP * 2)
        
        self.add_fixed_in_frame_mobjects(gd_label, adam_label)
        
        self.play(
            Create(gd_ball),
            Create(adam_ball),
            Write(gd_label),
            Write(adam_label),
            run_time=2
        )
        
        # Show gradient arrows
        gradient_text = Text("Following the gradient downhill", font_size=20)
        gradient_text.to_edge(DOWN).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(gradient_text)
        self.play(Write(gradient_text))
        
        # Create paths for both optimizers
        gd_path = VMobject(color=BLUE, stroke_width=3)
        gd_path.set_points_as_corners([start_point])
        
        adam_path = VMobject(color=GREEN, stroke_width=3)
        adam_path.set_points_as_corners([start_point])
        
        self.add(gd_path, adam_path)
        
        # Simulate optimization steps
        gd_pos = start_point.copy()
        adam_pos = start_point.copy()
        
        gd_velocity = np.array([0.0, 0.0, 0.0])
        adam_m = np.array([0.0, 0.0, 0.0])  # First moment
        adam_v = np.array([0.0, 0.0, 0.0])  # Second moment
        
        # Learning rates
        gd_lr = 0.1
        adam_lr = 0.3
        
        # Adam parameters
        beta1 = 0.9
        beta2 = 0.999
        epsilon = 1e-8
        
        step_count = 0
        
        for i in range(15):
            step_count += 1
            
            # Calculate gradients (approximate)
            def calc_gradient(pos):
                x, y = pos[0], pos[1]
                # Gradient of our loss function
                dx = x + 0.9 * np.cos(3 * x) * np.cos(3 * y)
                dx += 0.4 * (x - 1) * np.exp(-((x - 1)**2 + (y - 1)**2))
                dx -= 0.8 * (x + 1) * np.exp(-((x + 1)**2 + (y + 1)**2))
                dx -= 1.6 * (x - 0.5) * np.exp(-((x - 0.5)**2 + (y + 0.5)**2))
                
                dy = y - 0.9 * np.sin(3 * x) * np.sin(3 * y)
                dy += 0.4 * (y - 1) * np.exp(-((x - 1)**2 + (y - 1)**2))
                dy -= 0.8 * (y + 1) * np.exp(-((x + 1)**2 + (y + 1)**2))
                dy -= 1.6 * (y + 0.5) * np.exp(-((x - 0.5)**2 + (y + 0.5)**2))
                
                return np.array([dx, dy, 0])
            
            # Gradient descent update
            gd_grad = calc_gradient(gd_pos)
            gd_pos_new = gd_pos - gd_lr * gd_grad
            
            # Adam update
            adam_grad = calc_gradient(adam_pos)
            adam_m = beta1 * adam_m + (1 - beta1) * adam_grad
            adam_v = beta2 * adam_v + (1 - beta2) * adam_grad**2
            
            # Bias correction
            m_hat = adam_m / (1 - beta1**step_count)
            v_hat = adam_v / (1 - beta2**step_count)
            
            adam_pos_new = adam_pos - adam_lr * m_hat / (np.sqrt(v_hat) + epsilon)
            
            # Update z coordinates
            u_gd = (gd_pos_new[0] + 2) / 4
            v_gd = (gd_pos_new[1] + 2) / 4
            gd_pos_new[2] = loss_surface(u_gd, v_gd)[2]
            
            u_adam = (adam_pos_new[0] + 2) / 4
            v_adam = (adam_pos_new[1] + 2) / 4
            adam_pos_new[2] = loss_surface(u_adam, v_adam)[2]
            
            # Add to paths
            gd_path.add_points_as_corners([gd_pos_new])
            adam_path.add_points_as_corners([adam_pos_new])
            
            # Animate movement
            self.play(
                gd_ball.animate.move_to(gd_pos_new),
                adam_ball.animate.move_to(adam_pos_new),
                run_time=0.5
            )
            
            gd_pos = gd_pos_new
            adam_pos = adam_pos_new
            
            # Show iteration number
            if i % 3 == 0:
                iter_text = Text(f"Step {i + 1}", font_size=16)
                iter_text.to_edge(DOWN).shift(LEFT * 3)
                self.add_fixed_in_frame_mobjects(iter_text)
                self.play(Write(iter_text, run_time=0.3))
                self.wait(0.2)
                self.play(FadeOut(iter_text, run_time=0.3))
        
        # Highlight differences
        self.play(FadeOut(gradient_text))
        
        comparison_text = Text("Key Differences:", font_size=22, weight=BOLD)
        comparison_text.to_edge(DOWN).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(comparison_text)
        self.play(Write(comparison_text))
        
        # Show gradient descent characteristics
        gd_chars = VGroup(
            Text("• Follows gradient directly", font_size=16),
            Text("• Can oscillate in valleys", font_size=16),
            Text("• Slower convergence", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT)
        gd_chars.next_to(comparison_text, DOWN).shift(LEFT * 3)
        gd_chars.set_color(BLUE)
        
        # Show Adam characteristics
        adam_chars = VGroup(
            Text("• Adaptive learning rates", font_size=16),
            Text("• Momentum helps escape", font_size=16),
            Text("• Faster convergence", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT)
        adam_chars.next_to(comparison_text, DOWN).shift(RIGHT * 3)
        adam_chars.set_color(GREEN)
        
        self.add_fixed_in_frame_mobjects(gd_chars, adam_chars)
        self.play(
            Write(gd_chars),
            Write(adam_chars),
            run_time=2
        )
        
        # Show final positions
        global_min = np.array([-0.5, 0.5, loss_surface(0.375, 0.625)[2]])
        
        global_min_marker = Sphere(radius=0.15, color=YELLOW)
        global_min_marker.move_to(global_min)
        
        min_label = Text("Global Minimum", font_size=18, color=YELLOW)
        min_label.move_to(global_min + UP * 1.5)
        self.add_fixed_in_frame_mobjects(min_label)
        
        self.play(
            Create(global_min_marker),
            Write(min_label),
            Flash(global_min_marker, color=YELLOW),
            run_time=2
        )
        
        # Calculate distances to minimum
        gd_dist = np.linalg.norm(gd_pos[:2] - global_min[:2])
        adam_dist = np.linalg.norm(adam_pos[:2] - global_min[:2])
        
        result_text = Text(
            f"Adam reached closer to optimum ({adam_dist:.2f} vs {gd_dist:.2f})",
            font_size=20,
            color=YELLOW
        )
        result_text.to_edge(DOWN).shift(DOWN * 0.5)
        self.add_fixed_in_frame_mobjects(result_text)
        self.play(Write(result_text))
        
        # Camera rotation for final view
        self.move_camera(
            phi=65 * DEGREES,
            theta=-60 * DEGREES,
            distance=18,
            run_time=3
        )
        
        # Show side view to emphasize the paths
        self.move_camera(
            phi=45 * DEGREES,
            theta=-90 * DEGREES,
            distance=15,
            run_time=2
        )
        
        self.wait(3)

if __name__ == "__main__":
    # Run with: manim -pqh optimizer_comparison_visualization.py OptimizerComparisonVisualization
    pass