"""Shared helpers for RCS visualization scenes.

Keeps a consistent visual identity (background colour, title sequence,
camera defaults) and removes duplication across the seven scene files.
"""

from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np
from manim import (
    BOLD,
    DEGREES,
    DOWN,
    UP,
    FadeIn,
    FadeOut,
    Text,
    ThreeDScene,
    VGroup,
    Write,
)

# --- Visual identity -------------------------------------------------------

BACKGROUND_COLOR: str = "#0e1117"
"""Dark grey background used across every scene."""

DEFAULT_CAMERA = {"phi": 65 * DEGREES, "theta": -45 * DEGREES, "distance": 10}
"""Default 3D camera orientation. Override per-scene when needed."""

TITLE_FONT_SIZE: int = 32
SUBTITLE_FONT_SIZE: int = 20
CAPTION_FONT_SIZE: int = 20


# --- Reusable mixin --------------------------------------------------------


class RCSScene(ThreeDScene):
    """ThreeDScene with the project's shared visual identity baked in.

    Subclasses get:
      * dark background applied automatically
      * camera positioned to a sane default
      * a tracked-text helper so headings can be swapped cleanly between
        sections without leftover overlap (a problem in the original
        ``creeping_waves_*`` scenes).
    """

    camera_kwargs: dict = DEFAULT_CAMERA

    def setup(self) -> None:  # noqa: D401 — Manim hook
        super().setup()
        self.renderer.background_color = BACKGROUND_COLOR
        self.set_camera_orientation(**self.camera_kwargs)
        self._tracked_text: list = []

    # -- text tracking ------------------------------------------------------

    def add_hud_text(self, *mobjects) -> None:
        """Pin text to the camera frame and remember it for later cleanup."""
        self._tracked_text.extend(mobjects)
        self.add_fixed_in_frame_mobjects(*mobjects)

    def clear_hud_text(self) -> None:
        """Remove every tracked HUD text element from the scene."""
        if self._tracked_text:
            self.remove(*self._tracked_text)
            self._tracked_text = []

    # -- title sequence -----------------------------------------------------

    def play_title(self, title: str, subtitle: str | None = None, hold: float = 2.0) -> None:
        """Play the standard fade-in title card and clear it afterwards."""
        title_mob = Text(title, font_size=TITLE_FONT_SIZE, weight=BOLD)
        group = VGroup(title_mob)
        if subtitle:
            sub_mob = Text(subtitle, font_size=SUBTITLE_FONT_SIZE)
            sub_mob.next_to(title_mob, DOWN)
            group = VGroup(title_mob, sub_mob)
        group.to_edge(UP)

        self.add_fixed_in_frame_mobjects(group)
        animations = [Write(title_mob)]
        if subtitle:
            animations.append(FadeIn(group[1], shift=UP))
        self.play(*animations, run_time=2)
        self.wait(hold)
        self.play(FadeOut(group))


# --- Geometry utilities ----------------------------------------------------


def icosahedron_vertices(scale: float = 1.0) -> np.ndarray:
    """Return the 12 vertices of a regular icosahedron, optionally scaled.

    Used by the radar-facets demo as a simple convex faceted body.
    """
    phi = (1.0 + np.sqrt(5.0)) / 2.0
    raw = []
    for i in (-1, 1):
        for j in (-1, 1):
            raw.append([0, i, j * phi])
            raw.append([i, j * phi, 0])
            raw.append([j * phi, 0, i])
    return np.array(raw) * scale


def sphere_point(phi: float, theta: float, r: float = 1.0) -> np.ndarray:
    """Spherical -> Cartesian (physics convention: phi from +z axis)."""
    return np.array(
        [
            r * np.sin(phi) * np.cos(theta),
            r * np.sin(phi) * np.sin(theta),
            r * np.cos(phi),
        ]
    )


def face_normal_and_centroid(
    vertices: Sequence[np.ndarray],
) -> tuple[np.ndarray, np.ndarray]:
    """Outward face normal (unit) and centroid for a triangular facet."""
    v1, v2, v3 = vertices
    centroid = (v1 + v2 + v3) / 3.0
    normal = np.cross(v2 - v1, v3 - v1)
    normal = normal / np.linalg.norm(normal)
    return normal, centroid


def is_illuminated(face_normal: np.ndarray, wave_direction: np.ndarray) -> bool:
    """A facet is illuminated when its outward normal opposes the wave."""
    return float(np.dot(-wave_direction, face_normal)) > 0.0


def unit(vector: Iterable[float]) -> np.ndarray:
    """Return ``vector`` normalised to unit length."""
    arr = np.asarray(vector, dtype=float)
    norm = np.linalg.norm(arr)
    if norm == 0:
        raise ValueError("cannot normalize the zero vector")
    return arr / norm
