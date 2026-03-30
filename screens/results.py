"""
Results Screen
Displays the AI prediction result with risk level, confidence bar,
and plain-language recommendations.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse, Line
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.clock import Clock

from utils.theme import Colors, Fonts, Spacing


# ---------------------------------------------------------------------------
# Risk gauge (simple arc-style widget)
# ---------------------------------------------------------------------------
class RiskGauge(Widget):
    """Semi-circular gauge showing risk level."""

    def __init__(self, risk="Low", confidence=0.85, **kwargs):
        kwargs.setdefault("size_hint", (None, None))
        kwargs.setdefault("size", (dp(180), dp(110)))
        super().__init__(**kwargs)
        self._risk       = risk
        self._confidence = confidence
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_):
        self.canvas.clear()
        cx = self.x + self.width  / 2
        cy = self.y + dp(10)
        r  = min(self.width, self.height * 2) / 2 - dp(8)

        risk_colors = {
            "Low":    Colors.RISK_LOW,
            "Medium": Colors.RISK_MEDIUM,
            "High":   Colors.RISK_HIGH,
        }
        col = risk_colors.get(self._risk, Colors.RISK_LOW)

        with self.canvas:
            # Background arc (gray)
            Color(*Colors.DIVIDER)
            Line(
                circle=(cx, cy, r, 0, 180),
                width=dp(12),
                cap="round",
            )
            # Foreground arc
            Color(*col)
            angle = {
                "Low":    60,
                "Medium": 110,
                "High":   170,
            }.get(self._risk, 60)
            Line(
                circle=(cx, cy, r, 0, angle),
                width=dp(12),
                cap="round",
            )

            # Center dot
            Color(*col)
            Ellipse(pos=(cx - dp(8), cy - dp(8)), size=(dp(16), dp(16)))


# ---------------------------------------------------------------------------
# Confidence bar
# ---------------------------------------------------------------------------
class ConfidenceBar(Widget):
    def __init__(self, confidence=0.85, risk="Low", **kwargs):
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(10))
        super().__init__(**kwargs)
        self._confidence = confidence
        self._risk = risk
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_):
        self.canvas.clear()
        risk_colors = {
            "Low":    Colors.RISK_LOW,
            "Medium": Colors.RISK_MEDIUM,
            "High":   Colors.RISK_HIGH,
        }
        col = risk_colors.get(self._risk, Colors.RISK_LOW)
        with self.canvas:
            Color(*Colors.DIVIDER)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
            Color(*col)
            fill_w = self.width * self._confidence
            RoundedRectangle(
                pos=self.pos,
                size=(fill_w, self.height),
                radius=[dp(5)],
            )


# ---------------------------------------------------------------------------
# Info card
# ---------------------------------------------------------------------------
class InfoCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            size_hint_y=None,
            padding=[dp(16), dp(14)],
            spacing=dp(8),
            **kwargs,
        )
        with self.canvas.before:
            Color(*Colors.CARD)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size,
                                          radius=[dp(Spacing.RADIUS_MD)])
        self.bind(pos=lambda w, v: setattr(self._rect, "pos", v),
                  size=lambda w, v: setattr(self._rect, "size", v))


# ---------------------------------------------------------------------------
# Results Screen
# ---------------------------------------------------------------------------
class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._disease = None
        self._result  = None

        with self.canvas.before:
            Color(*Colors.BACKGROUND)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd_bg, size=self._upd_bg)

    def _upd_bg(self, *_):
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def set_result(self, disease, result):
        self._disease = disease
        self._result  = result

    def on_enter(self):
        self.clear_widgets()
        self._build_ui()

    def _build_ui(self):
        result  = self._result or {}
        risk    = result.get("risk_label", "Low")
        conf    = result.get("confidence", 0.85)
        rec     = result.get("recommendation", "Please consult a healthcare professional.")
        disease = self._disease or "Assessment"

        risk_colors = {
            "Low":    Colors.RISK_LOW,
            "Medium": Colors.RISK_MEDIUM,
            "High":   Colors.RISK_HIGH,
        }
        risk_bgs = {
            "Low":    Colors.GREEN_LIGHT,
            "Medium": Colors.ORANGE_LIGHT,
            "High":   (1.0, 0.88, 0.88, 1),
        }
        risk_icons = {
            "Low":    "✅",
            "Medium": "⚠️",
            "High":   "🚨",
        }
        col    = risk_colors.get(risk, Colors.RISK_LOW)
        bg_col = risk_bgs.get(risk, Colors.GREEN_LIGHT)
        icon   = risk_icons.get(risk, "✅")

        root = BoxLayout(orientation="vertical")

        # ---- Header ----
        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(110),
            padding=[dp(Spacing.LG), dp(Spacing.MD)],
            spacing=dp(4),
        )
        with header.canvas.before:
            Color(*Colors.WHITE)
            hrect = RoundedRectangle(pos=header.pos, size=header.size,
                                     radius=[0, 0, dp(20), dp(20)])
        header.bind(pos=lambda w, v: setattr(hrect, "pos", v),
                    size=lambda w, v: setattr(hrect, "size", v))

        back_row = BoxLayout(size_hint_y=None, height=dp(36))
        back_btn = Button(
            text="←",
            font_size=sp(22),
            size_hint_x=None,
            width=dp(36),
            background_color=(0, 0, 0, 0),
            color=Colors.TEXT_DARK,
        )
        back_btn.bind(on_release=self._go_back)

        title_lbl = Label(
            text="Your Results",
            font_size=sp(Fonts.SIZE_LG),
            color=Colors.TEXT_DARK,
            bold=True,
            halign="left",
        )
        title_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

        back_row.add_widget(back_btn)
        back_row.add_widget(title_lbl)

        sub = Label(
            text=f"AI assessment for: {disease}",
            font_size=sp(Fonts.SIZE_XS),
            color=Colors.TEXT_GRAY,
            halign="left",
            size_hint_y=None,
            height=dp(18),
            padding=[dp(36), 0, 0, 0],
        )
        sub.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

        header.add_widget(back_row)
        header.add_widget(sub)
        root.add_widget(header)

        # ---- Scrollable content ----
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.gridlayout import GridLayout

        scroll = ScrollView(do_scroll_x=False)
        grid = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(12),
            padding=[dp(Spacing.LG), dp(Spacing.MD), dp(Spacing.LG), dp(Spacing.LG)],
        )
        grid.bind(minimum_height=grid.setter("height"))

        # ---- Risk badge card ----
        risk_card = InfoCard(height=dp(170))

        # Icon row
        icon_row = BoxLayout(size_hint_y=None, height=dp(60))
        icon_row.add_widget(Widget())

        circle = Widget(size_hint=(None, None), size=(dp(56), dp(56)))
        with circle.canvas:
            Color(*bg_col)
            Ellipse(pos=circle.pos, size=circle.size)
        def _upd_circle(w, _):
            w.canvas.clear()
            with w.canvas:
                Color(*bg_col)
                Ellipse(pos=w.pos, size=w.size)
            ci.pos  = w.pos
            ci.size = w.size
        ci = Label(text=icon, font_size=sp(26))
        circle.bind(pos=_upd_circle, size=_upd_circle)
        circle.add_widget(ci)

        icon_row.add_widget(circle)
        icon_row.add_widget(Widget())
        risk_card.add_widget(icon_row)

        risk_lbl = Label(
            text=f"{risk} Risk",
            font_size=sp(Fonts.SIZE_XL),
            color=col,
            bold=True,
            halign="center",
            size_hint_y=None,
            height=dp(36),
        )
        risk_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
        risk_card.add_widget(risk_lbl)

        pct_lbl = Label(
            text=f"Confidence: {int(conf * 100)}%",
            font_size=sp(Fonts.SIZE_SM),
            color=Colors.TEXT_GRAY,
            halign="center",
            size_hint_y=None,
            height=dp(22),
        )
        pct_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
        risk_card.add_widget(pct_lbl)

        grid.add_widget(risk_card)

        # ---- Confidence bar card ----
        conf_card = InfoCard(height=dp(90))
        conf_title = Label(
            text="Prediction Confidence",
            font_size=sp(Fonts.SIZE_SM),
            color=Colors.TEXT_DARK,
            bold=True,
            halign="left",
            size_hint_y=None,
            height=dp(24),
        )
        conf_title.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
        conf_card.add_widget(conf_title)

        bar = ConfidenceBar(confidence=conf, risk=risk)
        conf_card.add_widget(bar)

        bar_labels = BoxLayout(size_hint_y=None, height=dp(18))
        bar_labels.add_widget(Label(text="Low", font_size=sp(9),
                                    color=Colors.TEXT_LIGHT, halign="left"))
        bar_labels.add_widget(Widget())
        bar_labels.add_widget(Label(text="High", font_size=sp(9),
                                    color=Colors.TEXT_LIGHT, halign="right"))
        conf_card.add_widget(bar_labels)
        grid.add_widget(conf_card)

        # ---- Recommendation card ----
        rec_card = InfoCard()
        rec_title = Label(
            text="💡 Recommendation",
            font_size=sp(Fonts.SIZE_MD),
            color=Colors.TEXT_DARK,
            bold=True,
            halign="left",
            size_hint_y=None,
            height=dp(28),
        )
        rec_title.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
        rec_card.add_widget(rec_title)

        rec_lbl = Label(
            text=rec,
            font_size=sp(Fonts.SIZE_SM),
            color=Colors.TEXT_GRAY,
            halign="left",
            valign="top",
        )
        rec_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

        # Need dynamic height
        rec_lbl.bind(texture_size=lambda w, ts: setattr(w, "height", ts[1] + dp(8)))
        rec_lbl.size_hint_y = None
        rec_lbl.height = dp(80)
        rec_card.add_widget(rec_lbl)
        rec_card.bind(minimum_height=rec_card.setter("height"))
        rec_card.size_hint_y = None
        rec_card.height = dp(140)
        grid.add_widget(rec_card)

        # ---- Disclaimer card ----
        disc_card = InfoCard(height=dp(80))
        with disc_card.canvas.before:
            Color(*Colors.ORANGE_LIGHT)

        disc_lbl = Label(
            text=("⚠ This result is for informational purposes only and is NOT a "
                  "substitute for professional medical advice, diagnosis, or treatment."),
            font_size=sp(9),
            color=Colors.ORANGE,
            halign="left",
        )
        disc_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
        disc_card.add_widget(disc_lbl)
        grid.add_widget(disc_card)

        # ---- Action buttons ----
        new_btn = Button(
            text="Start New Assessment",
            font_size=sp(Fonts.SIZE_MD),
            bold=True,
            color=Colors.WHITE,
            background_color=(0, 0, 0, 0),
            size_hint_y=None,
            height=dp(52),
        )
        new_btn.bind(pos=self._draw_primary_btn, size=self._draw_primary_btn)
        self._new_btn = new_btn
        new_btn.bind(on_release=self._start_new)
        grid.add_widget(new_btn)

        home_btn = Button(
            text="Back to Categories",
            font_size=sp(Fonts.SIZE_MD),
            color=Colors.PRIMARY,
            background_color=(0, 0, 0, 0),
            size_hint_y=None,
            height=dp(44),
        )
        home_btn.bind(pos=self._draw_outline_btn, size=self._draw_outline_btn)
        self._home_btn = home_btn
        home_btn.bind(on_release=self._go_home)
        grid.add_widget(home_btn)

        scroll.add_widget(grid)
        root.add_widget(scroll)
        self.add_widget(root)

    def _draw_primary_btn(self, *_):
        w = self._new_btn
        w.canvas.before.clear()
        with w.canvas.before:
            Color(*Colors.PRIMARY)
            RoundedRectangle(pos=w.pos, size=w.size,
                             radius=[dp(Spacing.RADIUS_PILL)])

    def _draw_outline_btn(self, *_):
        w = self._home_btn
        w.canvas.before.clear()
        with w.canvas.before:
            Color(*Colors.BORDER)
            RoundedRectangle(pos=w.pos, size=w.size,
                             radius=[dp(Spacing.RADIUS_PILL)])

    def _go_back(self, *_):
        self.manager.transition.direction = "right"
        self.manager.current = "symptom_form"

    def _start_new(self, *_):
        self.manager.transition.direction = "right"
        self.manager.current = "home"

    def _go_home(self, *_):
        self.manager.transition.direction = "right"
        self.manager.current = "home"
