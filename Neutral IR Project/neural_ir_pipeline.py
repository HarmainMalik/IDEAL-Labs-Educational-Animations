"""
Neural Information Retrieval Pipeline — educational Manim animation
Render (white background, 1080p, 30fps):
    manim -pqh neural_ir_pipeline.py NeuralIRPipeline
Render (fast preview):
    manim -pql neural_ir_pipeline.py NeuralIRPipeline

Target runtime: ~19 seconds.
"""

from manim import *

config.background_color = WHITE


class NeuralIRPipeline(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # ---------------------------------------------------------------
        # Persistent title + stage caption
        # ---------------------------------------------------------------
        title = Text(
            "Neural Information Retrieval Pipeline",
            font_size=30, color=BLACK, weight=BOLD
        ).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.9)

        def set_caption(text, first=False):
            cap = Text(text, font_size=22, color=GRAY_D)
            cap.next_to(title, DOWN, buff=0.25)
            if first:
                self.play(FadeIn(cap), run_time=0.35)
            else:
                self.play(FadeOut(self.current_caption), FadeIn(cap), run_time=0.4)
            self.current_caption = cap
            return cap

        # =================================================================
        # STAGE 1 — Search interface: user types a query
        # =================================================================
        cap = set_caption("1. User enters a query", first=True)

        search_box = RoundedRectangle(
            width=10.5, height=1.0, corner_radius=0.15,
            color=BLACK, stroke_width=2.5
        ).next_to(cap, DOWN, buff=0.6)

        mag_circle = Circle(radius=0.16, color=BLACK, stroke_width=3)
        mag_handle = Line(ORIGIN, [0.16, -0.16, 0], color=BLACK, stroke_width=3)
        mag_handle.next_to(mag_circle, DOWN, buff=-0.14).shift(RIGHT * 0.14)
        magnifier = VGroup(mag_circle, mag_handle)
        magnifier.next_to(search_box.get_left(), RIGHT, buff=0.4)

        query_text = Text(
            '"medicine reminder for elderly patients"',
            font_size=24, color=BLACK
        )
        query_text.next_to(magnifier, RIGHT, buff=0.35)

        self.play(Create(search_box), FadeIn(magnifier), run_time=0.7)
        self.play(Write(query_text), run_time=1.1)
        self.wait(0.35)

        # =================================================================
        # STAGE 2 — Query processing
        # =================================================================
        cap = set_caption("2. Query Processing")

        qp_box = RoundedRectangle(
            width=5.2, height=0.9, corner_radius=0.15,
            color=BLUE_E, stroke_width=2.5
        )
        qp_box.next_to(search_box, DOWN, buff=1.1)
        qp_label = Text("Query Processing", font_size=20, color=BLUE_E)
        qp_label.next_to(qp_box, UP, buff=0.18)
        qp_group = VGroup(qp_box, qp_label)

        arrow_to_qp = Arrow(
            search_box.get_bottom(), qp_label.get_top(),
            buff=0.15, color=BLACK, stroke_width=3, max_tip_length_to_length_ratio=0.15
        )

        self.play(Create(arrow_to_qp), FadeIn(qp_group), run_time=0.7)
        # scale the query text so it always fits comfortably inside the box,
        # regardless of query length, before animating the move
        safe_width = qp_box.width - 0.6
        fit_scale = min(0.4, safe_width / query_text.width)
        self.play(
            query_text.animate.scale(fit_scale).move_to(qp_box.get_center()),
            run_time=0.8
        )
        self.play(Indicate(qp_box, color=BLUE_E, scale_factor=1.05), run_time=0.5)
        self.play(
            FadeOut(search_box), FadeOut(magnifier), FadeOut(arrow_to_qp),
            FadeOut(query_text), FadeOut(qp_group),
            run_time=0.4
        )

        # =================================================================
        # STAGE 3 — Query becomes an embedding (vector)
        # =================================================================
        cap = set_caption("3. Query becomes a vector embedding")

        def make_embedding(color, n_rows=2, n_cols=3):
            dots = VGroup(*[Dot(radius=0.075, color=color) for _ in range(n_rows * n_cols)])
            dots.arrange_in_grid(rows=n_rows, cols=n_cols, buff=0.22)
            frame = SurroundingRectangle(dots, color=color, buff=0.18, stroke_width=1.8)
            return VGroup(dots, frame)

        query_emb = make_embedding(BLUE_E)
        query_emb.move_to(LEFT * 4.6 + UP * 0.6)
        query_emb_label = Text("Query Embedding", font_size=18, color=BLUE_E)
        query_emb_label.next_to(query_emb, DOWN, buff=0.2)

        ghost_dot = Dot(radius=0.01, color=BLUE_E).move_to(UP * 0.6)
        self.play(FadeIn(ghost_dot), run_time=0.1)
        self.play(
            ReplacementTransform(ghost_dot, query_emb),
            run_time=1.0
        )
        self.play(FadeIn(query_emb_label), run_time=0.4)
        self.wait(0.3)

        # =================================================================
        # STAGE 4 — Documents become embeddings too
        # =================================================================
        cap = set_caption("4. Documents become vector embeddings")

        doc_specs = [
            ("Doc A", "Grocery delivery service", GRAY_C, 0.38),
            ("Doc B", "Medication alarm for seniors", GREEN_E, 0.91),
            ("Doc C", "Weather forecast app", GRAY_C, 0.22),
        ]

        doc_cards = VGroup()
        for name, desc, color, score in doc_specs:
            rect = Rectangle(width=1.9, height=1.05, color=BLACK, stroke_width=2)
            lines = VGroup(*[
                Line(LEFT * 0.65, RIGHT * 0.65, color=GRAY_B, stroke_width=2)
                for _ in range(3)
            ]).arrange(DOWN, buff=0.14).move_to(rect.get_center())
            name_lbl = Text(name, font_size=16, color=BLACK, weight=BOLD)
            name_lbl.next_to(rect, UP, buff=0.12)
            card = VGroup(rect, lines, name_lbl)
            doc_cards.add(card)

        # arrange with a tighter buff and keep the whole row narrow enough
        # that every card (including Doc C on the far right) stays on screen
        doc_cards.arrange(RIGHT, buff=0.4)
        doc_cards.move_to(RIGHT * 1.3 + UP * 1.6)
        if doc_cards.get_right()[0] > 7.0 or doc_cards.get_left()[0] < -6.8:
            doc_cards.set(width=min(doc_cards.width, 8.5))
            doc_cards.move_to(RIGHT * 1.3 + UP * 1.6)

        self.play(LaggedStart(*[Create(c) for c in doc_cards], lag_ratio=0.2), run_time=1.0)
        self.wait(0.2)

        doc_embs = VGroup()
        colors = [GRAY_C, GREEN_E, GRAY_C]
        for card, color in zip(doc_cards, colors):
            emb = make_embedding(color, n_rows=2, n_cols=3).scale(0.75)
            emb.next_to(card, DOWN, buff=0.35)
            doc_embs.add(emb)

        self.play(
            *[ReplacementTransform(card.copy(), emb) for card, emb in zip(doc_cards, doc_embs)],
            FadeOut(doc_cards),
            run_time=1.1
        )
        doc_embs_label = Text("Document Embeddings", font_size=18, color=BLACK)
        doc_embs_label.next_to(doc_embs, DOWN, buff=0.25)
        self.play(FadeIn(doc_embs_label), run_time=0.4)
        self.wait(0.3)

        # =================================================================
        # STAGE 5 — Similarity comparison
        # =================================================================
        cap = set_caption("5. Comparing meaning, not just words")

        # Reposition query embedding + label to left-middle for clean comparison lines
        self.play(
            query_emb.animate.move_to(LEFT * 5 + DOWN * 0.3),
            query_emb_label.animate.next_to(LEFT * 5 + DOWN * 0.3, DOWN, buff=0.55),
            doc_embs.animate.arrange(DOWN, buff=0.55).move_to(RIGHT * 4 + DOWN * 0.3),
            FadeOut(doc_embs_label),
            run_time=0.9
        )

        sim_lines = VGroup()
        sim_labels = VGroup()
        for (name, desc, color, score), emb in zip(doc_specs, doc_embs):
            line = DashedLine(
                query_emb.get_right(), emb.get_left(),
                color=color, stroke_width=2 + 4 * score
            )
            score_lbl = Text(f"{score:.2f}", font_size=18, color=color, weight=BOLD)
            score_lbl.move_to(line.get_center()).shift(UP * 0.22)
            sim_lines.add(line)
            sim_labels.add(score_lbl)

        self.play(LaggedStart(*[Create(l) for l in sim_lines], lag_ratio=0.25), run_time=1.0)
        self.play(FadeIn(sim_labels), run_time=0.5)
        self.wait(0.4)

        # =================================================================
        # STAGE 6 — Ranking: most relevant rises to the top
        # =================================================================
        cap = set_caption("6. Ranking by semantic relevance")

        self.play(
            FadeOut(sim_lines), FadeOut(query_emb), FadeOut(query_emb_label),
            run_time=0.4
        )

        ranked = sorted(zip(doc_specs, doc_embs, sim_labels), key=lambda x: -x[0][3])

        rank_rows = VGroup()
        for i, ((name, desc, color, score), emb, score_lbl) in enumerate(ranked):
            rank_num = Text(f"#{i+1}", font_size=22, color=BLACK, weight=BOLD)
            doc_name = Text(f"{name} — {desc}", font_size=18, color=BLACK)
            score_txt = Text(f"score: {score:.2f}", font_size=16, color=color)
            row = VGroup(rank_num, doc_name, score_txt).arrange(RIGHT, buff=0.4)
            bg = SurroundingRectangle(row, color=color, buff=0.18, stroke_width=2.2)
            rank_rows.add(VGroup(bg, row))

        rank_rows.arrange(DOWN, buff=0.35)
        rank_rows.move_to(DOWN * 0.4)

        transforms = []
        for (spec, emb, score_lbl), row in zip(ranked, rank_rows):
            transforms.append(ReplacementTransform(emb, row))
            transforms.append(FadeOut(score_lbl))
        self.play(*transforms, run_time=1.3)

        self.play(
            Indicate(rank_rows[0], color=GREEN_E, scale_factor=1.06),
            run_time=0.8
        )
        top_note = Text(
            "Highest semantic match — ranked first",
            font_size=16, color=GREEN_E, slant=ITALIC
        ).next_to(rank_rows[0], RIGHT, buff=0.5)
        if top_note.get_right()[0] > 7.0:
            top_note.next_to(rank_rows, DOWN, buff=0.3)
        self.play(FadeIn(top_note), run_time=0.4)
        self.wait(0.5)

        # =================================================================
        # FINAL — Clean pipeline flow summary
        # =================================================================
        self.play(
            FadeOut(rank_rows), FadeOut(top_note), FadeOut(self.current_caption),
            run_time=0.5
        )

        flow_words = ["Query", "Embedding", "Similarity", "Ranking", "Results"]
        flow_boxes = VGroup()
        for w in flow_words:
            box = RoundedRectangle(width=2.2, height=0.9, corner_radius=0.12,
                                    color=BLUE_E, stroke_width=2.2)
            lbl = Text(w, font_size=18, color=BLUE_E)
            lbl.move_to(box.get_center())
            flow_boxes.add(VGroup(box, lbl))

        flow_boxes.arrange(RIGHT, buff=0.55)
        flow_boxes.move_to(ORIGIN)
        if flow_boxes.width > 13.5:
            flow_boxes.set(width=13.5)
            flow_boxes.move_to(ORIGIN)

        flow_arrows = VGroup(*[
            Arrow(flow_boxes[i].get_right(), flow_boxes[i + 1].get_left(),
                  buff=0.08, color=BLACK, stroke_width=3,
                  max_tip_length_to_length_ratio=0.25)
            for i in range(len(flow_boxes) - 1)
        ])

        self.play(
            LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in flow_boxes], lag_ratio=0.15),
            run_time=1.0
        )
        self.play(LaggedStart(*[Create(a) for a in flow_arrows], lag_ratio=0.2), run_time=0.8)
        self.wait(1.2)
