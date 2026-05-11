"""Gradient descent vs Adam on a 3D RCS loss landscape.

RCS objectives are non-convex: lots of shallow local minima from
interference effects, plus narrow valleys near the global optimum. Plain
gradient descent stalls on plateaus and skitters across valleys. Adam's
momentum + adaptive step size lets it slide further down before settling.
This scene rolls both optimizers from the same start and shows where
they end up.
"""

import numpy as np
from manim import (
    BLUE,
    BLUE_C,
    BLUE_E,
    DEGREES,
    DOWN,
    GREEN,
    LEFT,
    RED_C,
    RED_E,
    RIGHT,
    UP,
    YELLOW,
    Axes,
    Create,
    FadeOut,
    Flash,
    Sphere,
    Surface,
    Text,
    ThreeDAxes,
    VGroup,
    VMobject,
    Write,
)

from scenes._common import RCSScene

# Adam defaults.
BETA1 = 0.9
BETA2 = 0.999
EPSILON = 1e-8


def _loss_value(x: float, y: float) -> float:
    """Bumpy bowl-shaped loss with one local minimum and one global minimum."""
    z = 0.5 * (x**2 + y**2)
    z += 0.3 * np.sin(3 * x) * np.cos(3 * y)
    z += 0.2 * np.exp(-((x - 1) ** 2 + (y - 1) ** 2))
    z -= 0.4 * np.exp(-((x + 1) ** 2 + (y + 1) ** 2))  # local minimum
    z -= 0.8 * np.exp(-((x - 0.5) ** 2 + (y + 0.5) ** 2))  # global minimum
    return 0.5 * z


def _loss_point(u: float, v: float) -> np.ndarray:
    """Parametric ``(u, v) in [0, 1]`` -> world space point on the surface."""
    x = 4 * (u - 0.5)
    y = 4 * (v - 0.5)
    return np.array([x, y, _loss_value(x, y)])


def _gradient(pos: np.ndarray) -> np.ndarray:
    """Analytic gradient of ``_loss_value``."""
    x, y = pos[0], pos[1]
    dx = x + 0.9 * np.cos(3 * x) * np.cos(3 * y)
    dx += 0.4 * (x - 1) * np.exp(-((x - 1) ** 2 + (y - 1) ** 2))
    dx -= 0.8 * (x + 1) * np.exp(-((x + 1) ** 2 + (y + 1) ** 2))
    dx -= 1.6 * (x - 0.5) * np.exp(-((x - 0.5) ** 2 + (y + 0.5) ** 2))

    dy = y - 0.9 * np.sin(3 * x) * np.sin(3 * y)
    dy += 0.4 * (y - 1) * np.exp(-((x - 1) ** 2 + (y - 1) ** 2))
    dy -= 0.8 * (y + 1) * np.exp(-((x + 1) ** 2 + (y + 1) ** 2))
    dy -= 1.6 * (y + 0.5) * np.exp(-((x - 0.5) ** 2 + (y + 0.5) ** 2))
    return np.array([dx, dy, 0.0])


def _project_to_surface(pos: np.ndarray) -> np.ndarray:
    """Snap z back onto the loss surface after an optimizer step."""
    u = (pos[0] + 2) / 4
    v = (pos[1] + 2) / 4
    pos = pos.copy()
    pos[2] = _loss_point(u, v)[2]
    return pos


class OptimizerComparisonVisualization(RCSScene):
    camera_kwargs = {"phi": 75 * DEGREES, "theta": -45 * DEGREES, "distance": 20}

    def construct(self):
        self.play_title(
            "Optimization Algorithms: Gradient Descent vs Adam",
            "Finding the minimum RCS configuration",
        )

        surface = Surface(
            _loss_point,
            u_range=[0, 1],
            v_range=[0, 1],
            resolution=(40, 40),
            fill_opacity=0.8,
        )
        surface.set_fill_by_value(
            axes=Axes(),
            colorscale=[(BLUE_E, -1), (BLUE_C, 0), (RED_C, 1), (RED_E, 2)],
        )

        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-1, 2, 1],
            x_length=8,
            y_length=8,
            z_length=4,
        )
        axes.shift(DOWN)

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
            run_time=3,
        )

        start_point = _loss_point(0.875, 0.125)
        start_point[0], start_point[1] = 1.5, -1.5

        gd_ball = Sphere(radius=0.1, color=BLUE).move_to(start_point)
        adam_ball = Sphere(radius=0.1, color=GREEN).move_to(start_point)

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
            run_time=2,
        )

        gradient_text = Text("Following the gradient downhill", font_size=20)
        gradient_text.to_edge(DOWN).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(gradient_text)
        self.play(Write(gradient_text))

        gd_path = VMobject(color=BLUE, stroke_width=3).set_points_as_corners([start_point])
        adam_path = VMobject(color=GREEN, stroke_width=3).set_points_as_corners([start_point])
        self.add(gd_path, adam_path)

        gd_pos = start_point.copy()
        adam_pos = start_point.copy()
        adam_m = np.zeros(3)
        adam_v = np.zeros(3)
        gd_lr, adam_lr = 0.1, 0.3

        for step in range(1, 16):
            gd_pos_new = _project_to_surface(gd_pos - gd_lr * _gradient(gd_pos))

            adam_grad = _gradient(adam_pos)
            adam_m = BETA1 * adam_m + (1 - BETA1) * adam_grad
            adam_v = BETA2 * adam_v + (1 - BETA2) * adam_grad**2
            m_hat = adam_m / (1 - BETA1**step)
            v_hat = adam_v / (1 - BETA2**step)
            adam_pos_new = _project_to_surface(
                adam_pos - adam_lr * m_hat / (np.sqrt(v_hat) + EPSILON)
            )

            gd_path.add_points_as_corners([gd_pos_new])
            adam_path.add_points_as_corners([adam_pos_new])

            self.play(
                gd_ball.animate.move_to(gd_pos_new),
                adam_ball.animate.move_to(adam_pos_new),
                run_time=0.5,
            )
            gd_pos, adam_pos = gd_pos_new, adam_pos_new

            if step % 3 == 1:
                iter_text = Text(f"Step {step}", font_size=16)
                iter_text.to_edge(DOWN).shift(LEFT * 3)
                self.add_fixed_in_frame_mobjects(iter_text)
                self.play(Write(iter_text, run_time=0.3))
                self.wait(0.2)
                self.play(FadeOut(iter_text, run_time=0.3))

        self.play(FadeOut(gradient_text))

        comparison_text = Text("Key Differences:", font_size=22, weight="BOLD")
        comparison_text.to_edge(DOWN).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(comparison_text)
        self.play(Write(comparison_text))

        gd_chars = VGroup(
            Text("• Follows gradient directly", font_size=16),
            Text("• Can oscillate in valleys", font_size=16),
            Text("• Slower convergence", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT)
        gd_chars.next_to(comparison_text, DOWN).shift(LEFT * 3)
        gd_chars.set_color(BLUE)

        adam_chars = VGroup(
            Text("• Adaptive learning rates", font_size=16),
            Text("• Momentum escapes plateaus", font_size=16),
            Text("• Faster convergence", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT)
        adam_chars.next_to(comparison_text, DOWN).shift(RIGHT * 3)
        adam_chars.set_color(GREEN)

        self.add_fixed_in_frame_mobjects(gd_chars, adam_chars)
        self.play(Write(gd_chars), Write(adam_chars), run_time=2)

        global_min = _loss_point(0.375, 0.625)
        global_min[0], global_min[1] = -0.5, 0.5
        global_min_marker = Sphere(radius=0.15, color=YELLOW).move_to(global_min)

        min_label = Text("Global Minimum", font_size=18, color=YELLOW)
        min_label.move_to(global_min + UP * 1.5)
        self.add_fixed_in_frame_mobjects(min_label)

        self.play(
            Create(global_min_marker),
            Write(min_label),
            Flash(global_min_marker, color=YELLOW),
            run_time=2,
        )

        gd_dist = float(np.linalg.norm(gd_pos[:2] - global_min[:2]))
        adam_dist = float(np.linalg.norm(adam_pos[:2] - global_min[:2]))
        result_text = Text(
            f"Adam reached closer to the optimum ({adam_dist:.2f} vs {gd_dist:.2f})",
            font_size=20,
            color=YELLOW,
        )
        result_text.to_edge(DOWN).shift(DOWN * 0.5)
        self.add_fixed_in_frame_mobjects(result_text)
        self.play(Write(result_text))

        self.move_camera(phi=65 * DEGREES, theta=-60 * DEGREES, distance=18, run_time=3)
        self.move_camera(phi=45 * DEGREES, theta=-90 * DEGREES, distance=15, run_time=2)
        self.wait(3)
