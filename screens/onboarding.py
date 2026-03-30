"""
Onboarding Screens
3-step onboarding carousel matching the Figma design:
  Step 1 – Welcome to HealthAI     (blue heart)
  Step 2 – Fast & Accurate Analysis (teal lightning)
  Step 3 – Your Privacy Matters     (green shield)
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, RoundedRectangle, Rectangle
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.clock import Clock
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.theme import Colors, Fonts, Spacing

# ---------------------------------------------------------------------------
# Slide definitions
# ---------------------------------------------------------------------------
SLIDES = [
    {
        "icon":       "♥",
        "icon_color": Colors.PRIMARY,
        "bg_color":   Colors.PRIMARY_LIGHT,
        "title":      "Welcome to HealthAI",
        "subtitle":   ("Your trusted AI-powered symptom checker\n"
                       "that helps you understand your\nhealth concerns."),
        "btn_text":   "Continue  →",
        "dot_colors": [Colors.PRIMARY, Colors.INACTIVE_DOT, Colors.INACTIVE_DOT],
    },
    {
        "icon":       "⚡",
        "icon_color": Colors.TEAL,
        "bg_color":   Colors.TEAL_LIGHT,
        "title":      "Fast & Accurate Analysis",
        "subtitle":   ("Get instant insights about your symptoms\n"
                       "using advanced AI technology\ntrained on medical data."),
        "btn_text":   "Continue  →",
        "dot_colors": [Colors.PRIMARY, Colors.PRIMARY, Colors.INACTIVE_DOT],
    },
    {
        "icon":       "🛡",
        "icon_color": Colors.GREEN,
        "bg_color":   Colors.GREEN_LIGHT,
        "title":      "Your Privacy Matters",
        "subtitle":   ("Your health data is encrypted and secure.\n"
                       "We never share your information\nwith third parties."),
        "btn_text":   "Get Started  →",
        "dot_colors": [Colors.PRIMARY, Colors.PRIMARY, Colors.PRIMARY],
        "bullets": [
            "HIPAA compliant encryption",
            "No data sharing",
            "Anonymous usage option",
        ],
        "footer": ("By continuing, you agree to our Terms of Service and Privacy\n"
                   "Policy. This app is not a substitute for professional medical advice."),
    },
]

# ---------------------------------------------------------------------------
# Helper: draw colored rounded background
# ---------------------------------------------------------------------------
class RoundedCard(Widget):
    def __init__(self, bg_color=None, radius=Spacing.RADIUS_MD, **kwargs):
        super().__init__(**kwargs)
        self._bg_color = bg_color or Colors.CARD
        self._radius   = radius
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self._bg_color)
            RoundedRectangle(pos=self.pos, size=self.size,
                             radius=[dp(self._radius)])


# ---------------------------------------------------------------------------
# Icon circle widget
# ---------------------------------------------------------------------------
class IconCircle(Widget):
    def __init__(self, icon="♥", icon_color=Colors.PRIMARY,
                 bg_color=Colors.PRIMARY_LIGHT, size_dp=100, **kwargs):
        kwargs.setdefault("size_hint", (None, None))
        kwargs.setdefault("size", (dp(size_dp), dp(size_dp)))
        super().__init__(**kwargs)
        self._bg_color   = bg_color
        self._icon_color = icon_color
        self._icon       = icon
        self._size_dp    = size_dp

        self._lbl = Label(
            text=icon,
            font_size=sp(40),
            color=icon_color,
            halign="center",
            valign="middle",
        )
        self.add_widget(self._lbl)
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self._bg_color)
            d = min(self.width, self.height)
            Ellipse(pos=self.pos, size=(d, d))
        self._lbl.pos  = self.pos
        self._lbl.size = self.size


# ---------------------------------------------------------------------------
# Progress dots
# ---------------------------------------------------------------------------
class ProgressDots(Widget):
    def __init__(self, dot_colors=None, **kwargs):
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(10))
        super().__init__(**kwargs)
        self._dot_colors = dot_colors or [Colors.PRIMARY,
                                          Colors.INACTIVE_DOT,
                                          Colors.INACTIVE_DOT]
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *_):
        self.canvas.clear()
        n      = len(self._dot_colors)
        dot_w  = dp(28)
        dot_h  = dp(4)
        gap    = dp(6)
        total  = n * dot_w + (n - 1) * gap
        start_x = self.x + (self.width - total) / 2
        y = self.y + (self.height - dot_h) / 2

        with self.canvas:
            for i, col in enumerate(self._dot_colors):
                Color(*col)
                RoundedRectangle(
                    pos=(start_x + i * (dot_w + gap), y),
                    size=(dot_w, dot_h),
                    radius=[dp(3)],
                )


# ---------------------------------------------------------------------------
# CTA Button
# ---------------------------------------------------------------------------
class PrimaryButton(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault("background_color", (0, 0, 0, 0))
        kwargs.setdefault("color",            Colors.WHITE)
        kwargs.setdefault("font_size",        sp(Fonts.SIZE_MD))
        kwargs.setdefault("bold",             True)
        kwargs.setdefault("size_hint_y",      None)
        kwargs.setdefault("height",           dp(52))
        super().__init__(**kwargs)
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*Colors.PRIMARY)
            RoundedRectangle(pos=self.pos, size=self.size,
                             radius=[dp(Spacing.RADIUS_PILL)])

    def on_press(self):
        anim = Animation(opacity=0.7, duration=0.1)
        anim.start(self)

    def on_release(self):
        anim = Animation(opacity=1.0, duration=0.1)
        anim.start(self)


# ---------------------------------------------------------------------------
# Single Onboarding slide content (reused across the 3 screens)
# ---------------------------------------------------------------------------
class OnboardingContent(BoxLayout):
    def __init__(self, slide_idx=0, on_continue=None, on_skip=None, **kwargs):
        super().__init__(orientation="vertical",
                         padding=[dp(Spacing.LG), dp(Spacing.MD)],
                         spacing=0,
                         **kwargs)
        data = SLIDES[slide_idx]
        self._on_continue = on_continue
        self._on_skip     = on_skip

        # --- Top bar (dots + skip) ---
        top_bar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40),
        )
        dots = ProgressDots(dot_colors=data["dot_colors"], size_hint_x=0.7)
        skip_btn = Button(
            text="Skip",
            size_hint=(None, None),
            size=(dp(60), dp(36)),
            color=Colors.TEXT_GRAY,
            background_color=(0, 0, 0, 0),
            font_size=sp(Fonts.SIZE_MD),
        )
        skip_btn.bind(on_release=lambda *_: on_skip and on_skip())
        top_bar.add_widget(dots)
        top_bar.add_widget(skip_btn)
        self.add_widget(top_bar)

        # --- Spacer ---
        self.add_widget(Widget(size_hint_y=None, height=dp(40)))

        # --- Icon circle (centered) ---
        icon_box = BoxLayout(size_hint_y=None, height=dp(110))
        icon_box.add_widget(Widget())
        circle = IconCircle(
            icon       =data["icon"],
            icon_color =data["icon_color"],
            bg_color   =data["bg_color"],
            size_dp    =100,
        )
        icon_box.add_widget(circle)
        icon_box.add_widget(Widget())
        self.add_widget(icon_box)

        # --- Spacer ---
        self.add_widget(Widget(size_hint_y=None, height=dp(28)))

        # --- Title ---
        title = Label(
            text=data["title"],
            font_size=sp(Fonts.SIZE_XXL),
            color=Colors.TEXT_DARK,
            bold=True,
            halign="center",
            valign="top",
            size_hint_y=None,
            height=dp(48),
        )
        title.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
        self.add_widget(title)

        self.add_widget(Widget(size_hint_y=None, height=dp(12)))

        # --- Subtitle ---
        subtitle = Label(
            text=data["subtitle"],
            font_size=sp(Fonts.SIZE_SM),
            color=Colors.TEXT_GRAY,
            halign="center",
            valign="top",
            size_hint_y=None,
            height=dp(60),
        )
        subtitle.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
        self.add_widget(subtitle)

        # --- Bullets (slide 3 only) ---
        if "bullets" in data:
            self.add_widget(Widget(size_hint_y=None, height=dp(16)))
            for bullet in data["bullets"]:
                row = BoxLayout(size_hint_y=None, height=dp(32),
                                spacing=dp(10),
                                padding=[dp(Spacing.LG), 0])
                check = Label(
                    text="✓",
                    font_size=sp(Fonts.SIZE_MD),
                    color=Colors.GREEN,
                    size_hint_x=None,
                    width=dp(24),
                )
                lbl = Label(
                    text=bullet,
                    font_size=sp(Fonts.SIZE_SM),
                    color=Colors.TEXT_DARK,
                    halign="left",
                    valign="middle",
                )
                lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
                row.add_widget(check)
                row.add_widget(lbl)
                self.add_widget(row)

        # --- Flexible spacer ---
        self.add_widget(Widget())

        # --- Continue button ---
        btn = PrimaryButton(
            text=data["btn_text"],
            size_hint_x=1,
        )
        btn.bind(on_release=lambda *_: on_continue and on_continue())
        self.add_widget(btn)

        self.add_widget(Widget(size_hint_y=None, height=dp(8)))

        # --- Footer (slide 3 only) ---
        if "footer" in data:
            footer = Label(
                text=data["footer"],
                font_size=sp(9),
                color=Colors.TEXT_LIGHT,
                halign="center",
                size_hint_y=None,
                height=dp(36),
            )
            footer.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
            self.add_widget(footer)

        self.add_widget(Widget(size_hint_y=None, height=dp(Spacing.SM)))


# ---------------------------------------------------------------------------
# Onboarding Screen wrapper
# ---------------------------------------------------------------------------
class OnboardingScreen(Screen):
    def __init__(self, slide_idx=0, **kwargs):
        super().__init__(**kwargs)
        self._slide_idx = slide_idx

        with self.canvas.before:
            Color(*Colors.WHITE)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd_bg, size=self._upd_bg)

    def _upd_bg(self, *_):
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def on_enter(self):
        self.clear_widgets()
        content = OnboardingContent(
            slide_idx=self._slide_idx,
            on_continue=self._on_continue,
            on_skip=self._on_skip,
        )
        self.add_widget(content)

    def _on_continue(self):
        sm = self.manager
        if self._slide_idx < 2:
            sm.transition.direction = "left"
            sm.current = f"onboarding_{self._slide_idx + 1}"
        else:
            sm.transition.direction = "left"
            sm.current = "home"

    def _on_skip(self):
        self.manager.transition.direction = "left"
        self.manager.current = "home"
