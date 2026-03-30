"""
Disease List Screen
Shows diseases for the selected category.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp, sp
from kivy.animation import Animation

from utils.theme import Colors, Fonts, Spacing
from data.form_schemas import CATEGORY_DISEASES, DISEASE_FORMS


# ---------------------------------------------------------------------------
# Disease row button
# ---------------------------------------------------------------------------
class DiseaseRow(Button):
    def __init__(self, disease_name, category, on_tap=None, **kwargs):
        super().__init__(
            background_color=(0, 0, 0, 0),
            size_hint_y=None,
            height=dp(68),
            **kwargs,
        )
        self._disease  = disease_name
        self._on_tap   = on_tap
        meta = DISEASE_FORMS.get(disease_name, {})

        self.bind(pos=self._draw, size=self._draw)

        layout = BoxLayout(
            orientation="horizontal",
            padding=[dp(14), dp(10)],
            spacing=dp(12),
        )
        layout.bind(pos=lambda w, _: setattr(w, "pos", self.pos),
                    size=lambda w, _: setattr(w, "size", self.size))

        # Icon
        cat = meta.get("category", "common")
        from utils.theme import CATEGORIES
        cat_info = next((c for c in CATEGORIES if c["id"] == cat), CATEGORIES[0])

        icon_box = Widget(size_hint=(None, None), size=(dp(44), dp(44)))

        def _draw_icon(w, _):
            w.canvas.clear()
            with w.canvas:
                Color(*cat_info.get("icon_bg", Colors.PRIMARY_LIGHT))
                RoundedRectangle(pos=w.pos, size=w.size, radius=[dp(10)])
            ilbl.pos  = w.pos
            ilbl.size = w.size

        ilbl = Label(
            text=cat_info.get("icon_text", "?"),
            font_size=sp(20),
            color=cat_info.get("icon_color", Colors.PRIMARY),
        )
        icon_box.bind(pos=_draw_icon, size=_draw_icon)
        icon_box.add_widget(ilbl)
        layout.add_widget(icon_box)

        # Text
        text_col = BoxLayout(orientation="vertical", spacing=dp(2))
        name_lbl = Label(
            text=disease_name,
            font_size=sp(Fonts.SIZE_MD),
            color=Colors.TEXT_DARK,
            bold=True,
            halign="left",
        )
        name_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

        desc = meta.get("description", "Tap to start assessment")
        desc_lbl = Label(
            text=desc,
            font_size=sp(Fonts.SIZE_XS),
            color=Colors.TEXT_GRAY,
            halign="left",
        )
        desc_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

        text_col.add_widget(name_lbl)
        text_col.add_widget(desc_lbl)
        layout.add_widget(text_col)

        # Chevron
        layout.add_widget(Label(
            text="›",
            font_size=sp(24),
            color=Colors.TEXT_LIGHT,
            size_hint_x=None,
            width=dp(24),
        ))

        self.add_widget(layout)
        self.bind(on_release=self._tap)

    def _draw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*Colors.CARD)
            RoundedRectangle(pos=self.pos, size=self.size,
                             radius=[dp(Spacing.RADIUS_MD)])

    def _tap(self, *_):
        anim = Animation(opacity=0.7, duration=0.08) + Animation(opacity=1, duration=0.08)
        anim.start(self)
        if self._on_tap:
            self._on_tap(self._disease)


# ---------------------------------------------------------------------------
# Disease List Screen
# ---------------------------------------------------------------------------
class DiseaseListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._category = None

        with self.canvas.before:
            Color(*Colors.BACKGROUND)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd_bg, size=self._upd_bg)

    def _upd_bg(self, *_):
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def set_category(self, cat):
        self._category = cat

    def on_enter(self):
        self.clear_widgets()
        self._build_ui()

    def _build_ui(self):
        if not self._category:
            return

        cat = self._category
        diseases = CATEGORY_DISEASES.get(cat["id"], [])

        root = BoxLayout(orientation="vertical")

        # Header
        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(110),
            padding=[dp(Spacing.LG), dp(Spacing.MD)],
            spacing=dp(4),
        )
        with header.canvas.before:
            Color(*Colors.WHITE)
            rect = RoundedRectangle(pos=header.pos, size=header.size,
                                    radius=[0, 0, dp(20), dp(20)])
        header.bind(pos=lambda w, v: setattr(rect, "pos", v),
                    size=lambda w, v: setattr(rect, "size", v))

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

        title = Label(
            text=cat["name"],
            font_size=sp(Fonts.SIZE_LG),
            color=Colors.TEXT_DARK,
            bold=True,
            halign="left",
        )
        title.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

        back_row.add_widget(back_btn)
        back_row.add_widget(title)

        sub = Label(
            text=cat["desc"],
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

        # Category icon strip
        icon_strip = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=[dp(Spacing.LG), dp(Spacing.SM)],
        )
        icon_strip.add_widget(Widget())
        circle_lbl = Label(
            text=cat.get("icon_text", "?"),
            font_size=sp(28),
            color=cat.get("icon_color", Colors.PRIMARY),
            size_hint=(None, None),
            size=(dp(50), dp(50)),
        )
        icon_strip.add_widget(circle_lbl)
        icon_strip.add_widget(Widget())
        root.add_widget(icon_strip)

        # Disease list
        scroll = ScrollView(do_scroll_x=False)
        grid = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(10),
            padding=[dp(Spacing.LG), dp(Spacing.SM), dp(Spacing.LG), dp(Spacing.LG)],
        )
        grid.bind(minimum_height=grid.setter("height"))

        if diseases:
            for d in diseases:
                row = DiseaseRow(
                    disease_name=d,
                    category=cat,
                    on_tap=self._on_disease_tap,
                )
                grid.add_widget(row)
        else:
            grid.add_widget(Label(
                text="No diseases in this category yet.",
                color=Colors.TEXT_GRAY,
                font_size=sp(Fonts.SIZE_MD),
                size_hint_y=None,
                height=dp(60),
            ))

        scroll.add_widget(grid)
        root.add_widget(scroll)
        self.add_widget(root)

    def _go_back(self, *_):
        self.manager.transition.direction = "right"
        self.manager.current = "home"

    def _on_disease_tap(self, disease_name):
        form_screen = self.manager.get_screen("symptom_form")
        form_screen.set_disease(disease_name)
        self.manager.transition.direction = "left"
        self.manager.current = "symptom_form"
