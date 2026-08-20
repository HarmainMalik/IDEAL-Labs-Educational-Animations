"""
Classical Information Retrieval (IR) Models — Educational Animations
======================================================================

Manim Community Edition project containing three standalone, professional
educational animations for a university PowerPoint presentation:

    1. BooleanModel        - Boolean Model with the AND operator
    2. CosineSimilarity     - Vector Space Model / Cosine Similarity
    3. Clustering           - Unsupervised Document Clustering

Render each scene individually, e.g.:

    manim -pqh main.py BooleanModel
    manim -pqh main.py CosineSimilarity
    manim -pqh main.py Clustering

All scenes share a common visual language (colors, fonts, spacing) defined
in the CONSTANTS section below so the three videos feel like parts of the
same lecture series.

Author: Generated for Harmain's Classical IR Models presentation.
"""

import numpy as np
from manim import *

# ----------------------------------------------------------------------
# GLOBAL CONFIGURATION
# ----------------------------------------------------------------------
# 1920x1080 @ 30 FPS is set both here (as a safe default) and in
# manim.cfg / CLI flags. Using -pqh (1080p60) or a custom -r flag also
# works; these defaults make `manim main.py <Scene>` alone behave well.
config.frame_width = 14.2222222
config.frame_height = 8.0
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30
config.background_color = "#FAFAFA"  # very light, near-white background


# ----------------------------------------------------------------------
# SHARED COLOR PALETTE  (modern, flat, "3Blue1Brown but simpler")
# ----------------------------------------------------------------------
COLOR_BG = "#FAFAFA"           # near-white background
COLOR_TEXT_DARK = "#1E293B"    # slate-800, primary text
COLOR_TEXT_MUTED = "#64748B"   # slate-500, secondary text
COLOR_PRIMARY = "#2563EB"      # blue-600, primary accent
COLOR_SECONDARY = "#7C3AED"    # violet-600, secondary accent
COLOR_SUCCESS = "#16A34A"      # green-600, positive / retrieved
COLOR_DANGER = "#DC2626"       # red-600, negative / missing
COLOR_WARNING = "#D97706"      # amber-600, highlight
COLOR_CARD_BG = "#FFFFFF"      # white card background
COLOR_CARD_BORDER = "#E2E8F0"  # slate-200 card border
COLOR_AXIS = "#94A3B8"         # slate-400 axis lines

# Cluster palette used in Animation 3 (five distinct, modern hues)
CLUSTER_COLORS = ["#2563EB", "#DC2626", "#16A34A", "#D97706", "#7C3AED"]

# Default font family for consistent professional typography.
FONT_MAIN = "Helvetica"


# ----------------------------------------------------------------------
# SHARED HELPER FUNCTIONS
# ----------------------------------------------------------------------
def make_title(text_str, color=COLOR_TEXT_DARK):
    """Create a consistent slide title, top-anchored."""
    title = Text(text_str, font=FONT_MAIN, weight=BOLD, color=color, font_size=52)
    title.to_edge(UP, buff=0.6)
    return title


def make_underline(title_mobject, color=COLOR_PRIMARY, width_scale=1.0):
    """Create a thin accent underline beneath a title."""
    line = Line(LEFT, RIGHT, color=color, stroke_width=5)
    line.set_width(title_mobject.width * width_scale)
    line.next_to(title_mobject, DOWN, buff=0.25)
    return line


def make_card(width=3.6, height=2.4, fill=COLOR_CARD_BG, border=COLOR_CARD_BORDER):
    """Create a flat, modern rounded rectangle card (used as a base panel)."""
    card = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        fill_color=fill,
        fill_opacity=1.0,
        stroke_color=border,
        stroke_width=2,
    )
    return card


# ========================================================================
# ANIMATION 1 — BOOLEAN MODEL (AND OPERATOR)
# ========================================================================
class BooleanModel(Scene):
    """
    Demonstrates the Boolean Retrieval Model using the AND operator.

    Three document cards are evaluated against the query
    "indexing AND ranking". Only the document containing BOTH terms
    is retrieved. Total runtime target: ~18 seconds.
    """

    def construct(self):
        self.camera.background_color = COLOR_BG

        # ----------------------------------------------------------
        # BLOCK 1: Title
        # ----------------------------------------------------------
        title = make_title("Boolean Model — AND Operator")
        underline = make_underline(title)
        self.play(Write(title), run_time=0.8)
        self.play(Create(underline), run_time=0.4)

        # ----------------------------------------------------------
        # BLOCK 2: Build the three document cards
        # ----------------------------------------------------------
        doc_texts = [
            ("D1", "Information Retrieval uses indexing"),
            ("D2", "Search engines use ranking"),
            ("D3", "Indexing and ranking improve retrieval"),
        ]

        doc_cards = VGroup()
        doc_labels = VGroup()   # word-level Text mobjects, kept for highlighting
        for label, sentence in doc_texts:
            card = make_card(width=3.9, height=2.1)
            tag = Text(label, font=FONT_MAIN, weight=BOLD,
                       color=COLOR_PRIMARY, font_size=30)
            body = Text(sentence, font=FONT_MAIN, color=COLOR_TEXT_DARK,
                        font_size=22, line_spacing=1.2, t2c={
                            "indexing": COLOR_TEXT_DARK,
                            "ranking": COLOR_TEXT_DARK,
                        })
            body.set(width=3.3)
            tag.move_to(card.get_top() + DOWN * 0.45)
            body.move_to(card.get_center() + DOWN * 0.15)
            group = VGroup(card, tag, body)
            doc_cards.add(group)
            doc_labels.add(body)

        doc_cards.arrange(RIGHT, buff=0.7)
        doc_cards.move_to(ORIGIN + UP * 0.6)

        self.play(
            LaggedStart(*[Create(g[0]) for g in doc_cards], lag_ratio=0.2),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[FadeIn(VGroup(g[1], g[2]), shift=UP * 0.1) for g in doc_cards],
                        lag_ratio=0.2),
            run_time=1.0,
        )

        # ----------------------------------------------------------
        # BLOCK 3: Search bar with animated typing
        # ----------------------------------------------------------
        search_box = RoundedRectangle(
            width=6.5, height=0.85, corner_radius=0.42,
            fill_color=COLOR_CARD_BG, fill_opacity=1.0,
            stroke_color=COLOR_PRIMARY, stroke_width=3,
        )
        search_box.move_to(DOWN * 1.6)
        search_icon = Circle(radius=0.1, color=COLOR_TEXT_MUTED, stroke_width=3)
        search_icon.move_to(search_box.get_left() + RIGHT * 0.5)
        search_handle = Line(
            search_icon.get_center() + np.array([0.07, -0.07, 0]),
            search_icon.get_center() + np.array([0.22, -0.22, 0]),
            color=COLOR_TEXT_MUTED, stroke_width=3,
        )

        self.play(Create(search_box), Create(search_icon), Create(search_handle),
                  run_time=0.6)

        # Animate typing the query letter by letter
        query_str = "indexing AND ranking"
        query_text = Text(query_str, font=FONT_MAIN, font_size=28, color=COLOR_TEXT_DARK)
        query_text.move_to(search_box.get_center() + RIGHT * 0.35)
        query_text.align_to(search_icon, LEFT).shift(RIGHT * 0.55)

        self.play(AddTextLetterByLetter(query_text, time_per_char=0.045), run_time=1.2)
        self.wait(0.2)

        # Highlight "indexing" and "ranking" within the typed query
        idx_start = query_str.index("indexing")
        idx_word = query_text[idx_start: idx_start + len("indexing")]
        rank_start = query_str.index("ranking")
        rank_word = query_text[rank_start: rank_start + len("ranking")]

        self.play(
            idx_word.animate.set_color(COLOR_WARNING),
            rank_word.animate.set_color(COLOR_SECONDARY),
            run_time=0.6,
        )
        self.play(Indicate(idx_word, color=COLOR_WARNING, scale_factor=1.15),
                   Indicate(rank_word, color=COLOR_SECONDARY, scale_factor=1.15),
                   run_time=0.8)
        self.wait(0.2)

        # ----------------------------------------------------------
        # BLOCK 4: Evaluate each document against the AND condition
        # ----------------------------------------------------------
        # Helper to spawn a verdict label under a given card
        def verdict_label(card_group, text_str, color):
            label = Text(text_str, font=FONT_MAIN, weight=BOLD,
                         font_size=24, color=color)
            label.next_to(card_group, DOWN, buff=0.25)
            return label

        # --- D1: has "indexing", missing "ranking" -> Not Retrieved
        d1_group = doc_cards[0]
        d1_body = doc_labels[0]
        indexing_in_d1 = self._find_word(d1_body, "indexing")
        self.play(Circumscribe(indexing_in_d1, color=COLOR_SUCCESS, fade_out=True),
                   indexing_in_d1.animate.set_color(COLOR_SUCCESS), run_time=0.7)
        missing_ranking_1 = Text("ranking: missing", font=FONT_MAIN,
                                  font_size=18, color=COLOR_DANGER, slant=ITALIC)
        missing_ranking_1.next_to(d1_group, UP, buff=0.15)
        self.play(FadeIn(missing_ranking_1, shift=UP * 0.1), run_time=0.4)
        v1 = verdict_label(d1_group, "✗ Not Retrieved", COLOR_DANGER)
        self.play(d1_group.animate.set_opacity(0.4), Write(v1), run_time=0.7)

        # --- D2: has "ranking", missing "indexing" -> Not Retrieved
        d2_group = doc_cards[1]
        d2_body = doc_labels[1]
        ranking_in_d2 = self._find_word(d2_body, "ranking")
        self.play(Circumscribe(ranking_in_d2, color=COLOR_SUCCESS, fade_out=True),
                   ranking_in_d2.animate.set_color(COLOR_SUCCESS), run_time=0.7)
        missing_indexing_2 = Text("indexing: missing", font=FONT_MAIN,
                                   font_size=18, color=COLOR_DANGER, slant=ITALIC)
        missing_indexing_2.next_to(d2_group, UP, buff=0.15)
        self.play(FadeIn(missing_indexing_2, shift=UP * 0.1), run_time=0.4)
        v2 = verdict_label(d2_group, "✗ Not Retrieved", COLOR_DANGER)
        self.play(d2_group.animate.set_opacity(0.4), Write(v2), run_time=0.7)

        # --- D3: has BOTH -> Retrieved
        d3_group = doc_cards[2]
        d3_body = doc_labels[2]
        indexing_in_d3 = self._find_word(d3_body, "Indexing")
        ranking_in_d3 = self._find_word(d3_body, "ranking")
        self.play(
            indexing_in_d3.animate.set_color(COLOR_SUCCESS),
            ranking_in_d3.animate.set_color(COLOR_SUCCESS),
            run_time=0.6,
        )
        glow = d3_group[0].copy()
        glow.set_stroke(color=COLOR_SUCCESS, width=10, opacity=0.6)
        glow.set_fill(opacity=0)
        self.play(
            FadeIn(glow),
            d3_group.animate.scale(1.08),
            run_time=0.7,
        )
        v3 = verdict_label(d3_group, "✓ Retrieved", COLOR_SUCCESS)
        self.play(Write(v3), Indicate(d3_group, color=COLOR_SUCCESS, scale_factor=1.03),
                   run_time=0.7)

        # ----------------------------------------------------------
        # BLOCK 5: Final summary statement
        # ----------------------------------------------------------
        summary = Text("Only D3 satisfies the AND condition.",
                        font=FONT_MAIN, weight=BOLD, font_size=30,
                        color=COLOR_TEXT_DARK)
        summary.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(summary, shift=UP * 0.2), run_time=0.8)
        self.wait(3.0)

        # Fade everything out for a clean end
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.8,
        )

    @staticmethod
    def _find_word(text_mobject, word):
        """
        Return the sub-mobject slice of `text_mobject` corresponding to
        the first occurrence of `word` (case-sensitive) in its string.
        Falls back to a case-insensitive search if an exact match fails.
        """
        full_str = text_mobject.text
        start = full_str.find(word)
        if start == -1:
            start = full_str.lower().find(word.lower())
        end = start + len(word)
        return text_mobject[start:end]


# ========================================================================
# ANIMATION 2 — COSINE SIMILARITY (VECTOR SPACE MODEL)
# ========================================================================
class CosineSimilarity(Scene):
    """
    Demonstrates the Vector Space Model's cosine similarity measure.

    A document vector rotates from ~60 degrees away from the query
    vector down to ~10 degrees, while the similarity score animates
    upward from 20% to 95%. Total runtime target: ~20 seconds.
    """

    def construct(self):
        self.camera.background_color = COLOR_BG

        # ----------------------------------------------------------
        # BLOCK 1: Title
        # ----------------------------------------------------------
        title = make_title("Cosine Similarity")
        underline = make_underline(title)
        self.play(Write(title), run_time=0.8)
        self.play(Create(underline), run_time=0.4)

        # ----------------------------------------------------------
        # BLOCK 2: Axes
        # ----------------------------------------------------------
        axes = Axes(
            x_range=[-0.5, 4.5, 1],
            y_range=[-0.5, 4.5, 1],
            x_length=6.5,
            y_length=6.5,
            axis_config={"color": COLOR_AXIS, "stroke_width": 3,
                         "include_tip": True, "tip_length": 0.2},
        )
        axes.move_to(DOWN * 0.3 + LEFT * 2.3)
        origin = axes.c2p(0, 0)

        self.play(Create(axes), run_time=1.0)

        # ----------------------------------------------------------
        # BLOCK 3: Query vector (fixed) and Document vector (animated)
        # ----------------------------------------------------------
        query_angle = 65 * DEGREES     # fixed query direction
        start_angle = 5 * DEGREES      # document starts 60 deg away from query
        end_angle = 55 * DEGREES       # document ends 10 deg away from query
        vec_length = 3.0

        angle_tracker = ValueTracker(start_angle)

        def polar_point(angle, length=vec_length):
            return origin + length * np.array([np.cos(angle), np.sin(angle), 0])

        query_vec = Arrow(
            start=origin, end=polar_point(query_angle),
            buff=0, color=COLOR_PRIMARY, stroke_width=7, max_tip_length_to_length_ratio=0.08,
        )
        query_label = Text("Query Vector", font=FONT_MAIN, font_size=24,
                            color=COLOR_PRIMARY, weight=BOLD)
        query_label.next_to(query_vec.get_end(), UP + RIGHT, buff=0.1)

        doc_vec = always_redraw(
            lambda: Arrow(
                start=origin, end=polar_point(angle_tracker.get_value()),
                buff=0, color=COLOR_SECONDARY, stroke_width=7,
                max_tip_length_to_length_ratio=0.08,
            )
        )
        doc_label = always_redraw(
            lambda: Text("Document Vector", font=FONT_MAIN, font_size=24,
                         color=COLOR_SECONDARY, weight=BOLD).next_to(
                polar_point(angle_tracker.get_value()), DOWN + RIGHT, buff=0.1)
        )

        # Angle arc between the two vectors, always redrawn as they change
        angle_arc = always_redraw(
            lambda: Angle(
                Line(origin, polar_point(angle_tracker.get_value())),
                Line(origin, polar_point(query_angle)),
                radius=0.8, color=COLOR_WARNING, stroke_width=5,
            )
        )

        self.play(GrowArrow(query_vec), Write(query_label), run_time=0.8)
        self.play(GrowArrow(doc_vec), Write(doc_label), run_time=0.8)
        self.play(Create(angle_arc), run_time=0.6)

        # ----------------------------------------------------------
        # BLOCK 4: Side panel — similarity readout & status text
        # ----------------------------------------------------------
        panel_x = 3.6
        status_text = Text("Low Similarity", font=FONT_MAIN, weight=BOLD,
                            font_size=34, color=COLOR_DANGER)
        status_text.move_to(np.array([panel_x, 2.0, 0]))
        self.play(FadeIn(status_text, shift=UP * 0.2), run_time=0.6)

        # "Angle" readout (degrees), live-updating.
        # NOTE: DecimalNumber's `unit` kwarg always renders via LaTeX
        # internally regardless of `mob_class`, so instead we build the
        # numeric readout and its unit suffix ("°" / "%") as two separate
        # plain-Text-based mobjects grouped together — this keeps the
        # whole project LaTeX-free and portable.
        angle_caption = Text("Angle", font=FONT_MAIN, font_size=24,
                              color=COLOR_TEXT_MUTED)
        angle_caption.move_to(np.array([panel_x, 1.1, 0]))
        angle_number = DecimalNumber(
            (query_angle - start_angle) / DEGREES, num_decimal_places=0,
            color=COLOR_TEXT_DARK, font_size=40,
            mob_class=Text,  # avoid LaTeX dependency; render with plain Text
        )
        angle_suffix = Text("°", font=FONT_MAIN, font_size=40, color=COLOR_TEXT_DARK)
        angle_value = VGroup(angle_number, angle_suffix)
        angle_suffix.next_to(angle_number, RIGHT, buff=0.04, aligned_edge=UP)
        angle_value.move_to(np.array([panel_x, 0.6, 0]))

        def update_angle_readout(mob):
            num, suffix = mob
            num.set_value((query_angle - angle_tracker.get_value()) / DEGREES)
            suffix.next_to(num, RIGHT, buff=0.04, aligned_edge=UP)
        # NOTE: the live-updater is attached AFTER the fade-in animation
        # below completes. Attaching it beforehand would let the
        # DecimalNumber regenerate its glyph submobjects mid-FadeIn,
        # desynchronising the animation's cached mobject family.

        # "Similarity" readout (percentage), live-updating via cosine formula
        sim_caption = Text("Similarity", font=FONT_MAIN, font_size=24,
                            color=COLOR_TEXT_MUTED)
        sim_caption.move_to(np.array([panel_x, -0.3, 0]))
        sim_number = DecimalNumber(
            0, num_decimal_places=0, color=COLOR_PRIMARY, font_size=48,
            mob_class=Text,  # avoid LaTeX dependency; render with plain Text
        )
        sim_suffix = Text("%", font=FONT_MAIN, font_size=48, color=COLOR_PRIMARY)
        sim_value = VGroup(sim_number, sim_suffix)
        sim_suffix.next_to(sim_number, RIGHT, buff=0.04, aligned_edge=UP)
        sim_value.move_to(np.array([panel_x, -0.9, 0]))

        def compute_similarity():
            diff = query_angle - angle_tracker.get_value()
            return float(np.cos(diff)) * 100

        def update_sim_readout(mob):
            num, suffix = mob
            num.set_value(compute_similarity())
            suffix.next_to(num, RIGHT, buff=0.04, aligned_edge=UP)
        # NOTE: same reasoning as update_angle_readout — updater is
        # attached only after the initial fade-in below has finished.

        self.play(
            FadeIn(angle_caption), FadeIn(angle_value),
            FadeIn(sim_caption), FadeIn(sim_value),
            run_time=0.6,
        )
        # Attach the live updaters now that both readouts have finished
        # fading in, so subsequent glyph-count changes only affect
        # animations that are aware of them (ValueTracker-driven moves).
        angle_value.add_updater(update_angle_readout)
        sim_value.add_updater(update_sim_readout)
        self.wait(0.3)

        # ----------------------------------------------------------
        # BLOCK 5: Rotate the document vector toward the query vector
        # ----------------------------------------------------------
        # As the angle shrinks, similarity should rise; we drive the
        # status text through intermediate captions to match the
        # requested progression (20% -> 45% -> 70% -> 95%).
        milestones = [0.20, 0.45, 0.70, 0.95]  # similarity fractions
        # Corresponding angles for each milestone via arccos, staying
        # within [start_angle, end_angle] rotation path.
        total_rotation = end_angle - start_angle

        self.play(
            angle_tracker.animate.set_value(start_angle + total_rotation * 0.33),
            run_time=2.0,
            rate_func=smooth,
        )
        self.play(Transform(
            status_text,
            Text("Angle ↓", font=FONT_MAIN, weight=BOLD, font_size=34,
                 color=COLOR_WARNING).move_to(status_text.get_center())
        ), run_time=0.5)

        self.play(
            angle_tracker.animate.set_value(start_angle + total_rotation * 0.66),
            run_time=2.0,
            rate_func=smooth,
        )
        self.play(Transform(
            status_text,
            Text("Similarity ↑", font=FONT_MAIN, weight=BOLD, font_size=34,
                 color=COLOR_WARNING).move_to(status_text.get_center())
        ), run_time=0.5)

        self.play(
            angle_tracker.animate.set_value(end_angle),
            run_time=2.5,
            rate_func=smooth,
        )
        self.play(Transform(
            status_text,
            Text("High Similarity", font=FONT_MAIN, weight=BOLD, font_size=34,
                 color=COLOR_SUCCESS).move_to(status_text.get_center())
        ), run_time=0.6)

        self.wait(0.5)

        # ----------------------------------------------------------
        # BLOCK 6: Closing statement
        # ----------------------------------------------------------
        # Freeze the updaters so we can clear the vectors safely.
        angle_value.clear_updaters()
        sim_value.clear_updaters()

        closing = Text("Smaller Angle = Higher Similarity", font=FONT_MAIN,
                        weight=BOLD, font_size=36, color=COLOR_TEXT_DARK)
        closing.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(closing, shift=UP * 0.2), run_time=0.8)
        self.wait(3.0)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


# ========================================================================
# ANIMATION 3 — DOCUMENT CLUSTERING
# ========================================================================
class Clustering(Scene):
    """
    Demonstrates unsupervised document clustering: ~40 scattered points
    smoothly converge into five labeled thematic clusters.
    Total runtime target: ~22 seconds.
    """

    def construct(self):
        self.camera.background_color = COLOR_BG
        np.random.seed(42)  # deterministic layout for reproducible renders

        # ----------------------------------------------------------
        # BLOCK 1: Title
        # ----------------------------------------------------------
        title = make_title("Document Clustering")
        underline = make_underline(title)
        self.play(Write(title), run_time=0.8)
        self.play(Create(underline), run_time=0.4)

        # ----------------------------------------------------------
        # BLOCK 2: Cluster definitions (labels + target centers)
        # ----------------------------------------------------------
        cluster_names = [
            "Healthcare", "Cybersecurity", "Education",
            "E-Commerce", "Information Retrieval",
        ]
        # Five target centers arranged in a balanced pentagon-like layout
        # within the plotting area (below the title, above the caption).
        centers = [
            np.array([-4.6, 0.7, 0]),
            np.array([-2.2, -1.8, 0]),
            np.array([0.6, 1.3, 0]),
            np.array([3.2, -1.6, 0]),
            np.array([5.0, 1.0, 0]),
        ]

        n_dots = 40
        n_clusters = len(centers)

        # Assign each dot a target cluster (roughly even distribution)
        assignments = [i % n_clusters for i in range(n_dots)]
        np.random.shuffle(assignments)

        # ----------------------------------------------------------
        # BLOCK 3: Create dots at random scattered starting positions
        # ----------------------------------------------------------
        dots = VGroup()
        scatter_area_x = (-6.0, 6.0)
        scatter_area_y = (-2.6, 2.2)

        for i in range(n_dots):
            cluster_idx = assignments[i]
            color = CLUSTER_COLORS[cluster_idx]
            start_pos = np.array([
                np.random.uniform(*scatter_area_x),
                np.random.uniform(*scatter_area_y),
                0,
            ])
            dot = Dot(point=start_pos, radius=0.11, color=color, fill_opacity=0.85)
            # Store its final target on the mobject for later use
            jitter = np.array([
                np.random.uniform(-0.55, 0.55),
                np.random.uniform(-0.55, 0.55),
                0,
            ])
            dot.target_pos = centers[cluster_idx] + jitter
            dots.add(dot)

        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.03),
            run_time=1.5,
        )
        self.wait(0.3)

        # ----------------------------------------------------------
        # BLOCK 4: Animate dots settling into their five clusters
        # ----------------------------------------------------------
        for d in dots:
            d.generate_target()
            d.target.move_to(d.target_pos)

        self.play(
            AnimationGroup(*[MoveToTarget(d, path_arc=30 * DEGREES) for d in dots]),
            run_time=3.5,
            rate_func=smooth,
        )
        self.wait(0.3)

        # A gentle secondary settle so the motion doesn't feel like a
        # sudden jump — dots ease into slightly tighter final spots.
        for d in dots:
            d.generate_target()
            tight_jitter = (d.target_pos - centers[assignments[dots.submobjects.index(d)]]) * 0.6
            d.target.move_to(centers[assignments[dots.submobjects.index(d)]] + tight_jitter)

        self.play(
            LaggedStart(*[MoveToTarget(d) for d in dots], lag_ratio=0.01),
            run_time=1.5,
            rate_func=there_and_back_with_pause,
        )

        # ----------------------------------------------------------
        # BLOCK 5: Draw soft cluster boundary circles and labels
        # ----------------------------------------------------------
        cluster_circles = VGroup()
        cluster_labels = VGroup()
        for idx, center in enumerate(centers):
            circle = Circle(radius=1.15, color=CLUSTER_COLORS[idx], stroke_width=3,
                             fill_color=CLUSTER_COLORS[idx], fill_opacity=0.06)
            circle.move_to(center)
            label = Text(cluster_names[idx], font=FONT_MAIN, weight=BOLD,
                         font_size=22, color=CLUSTER_COLORS[idx])
            label.next_to(circle, DOWN, buff=0.18)
            cluster_circles.add(circle)
            cluster_labels.add(label)

        self.play(
            LaggedStart(*[Create(c) for c in cluster_circles], lag_ratio=0.15),
            run_time=1.2,
        )

        # ----------------------------------------------------------
        # BLOCK 6: Explanatory captions
        # ----------------------------------------------------------
        caption1 = Text("No labels were provided.", font=FONT_MAIN,
                        font_size=26, color=COLOR_TEXT_MUTED)
        caption2 = Text("The algorithm discovered these groups automatically.",
                        font=FONT_MAIN, weight=BOLD, font_size=28,
                        color=COLOR_TEXT_DARK)
        captions = VGroup(caption1, caption2).arrange(DOWN, buff=0.15)
        captions.to_edge(DOWN, buff=0.4)

        self.play(FadeIn(caption1, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(caption2, shift=UP * 0.15), run_time=0.8)
        self.wait(1.2)

        # ----------------------------------------------------------
        # BLOCK 7: Fade in cluster labels over the settled clusters
        # ----------------------------------------------------------
        self.play(
            LaggedStart(*[FadeIn(lbl, shift=UP * 0.1) for lbl in cluster_labels],
                        lag_ratio=0.2),
            run_time=1.5,
        )

        self.wait(5.5)

        # Clean fade-out for a professional end
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
