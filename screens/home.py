"""
Home Screen — Disease Categories
Matches Figma design: search bar + scrollable category cards
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp, sp
from kivy.animation import Animation

from utils.theme import Colors, Fonts, Spacing, CATEGORIES


# ---------------------------------------------------------------------------
# Category Card
# ---------------------------------------------------------------------------
class CategoryCard(Button):
    def __init__(self, category_data, on_tap=None, **kwargs):
        super().__init__(
            background_color=(0, 0, 0, 0),
            size_hint_y=None,
            height=dp(78),
            **kwargs,
        )
        self._cat  = category_data
        self._on_tap = on_tap

        self.bind(pos=self._draw, size=self._draw)

        # Card layout inside button
        layout = BoxLayout(orientation="horizontal",
                           spacing=dp(14),
                           padding=[dp(14), dp(10), dp(10), dp(10)])
        layout.bind(pos=lambda w, v: setattr(w, "pos", self.pos))
        layout.bind(size=lambda w, v: setattr(w, "size", self.size))

        # Icon box
        icon_box = Widget(size_hint=(None, None), size=(dp(48), dp(48)))
        with icon_box.canvas:
            Color(*category_data.get("icon_bg", Colors.PRIMARY_LIGHT))
            RoundedRectangle(pos=icon_box.pos, size=icon_box.size,
                             radius=[dp(12)])

        def _upd_icon(w, _):
            w.canvas.clear()
            with w.canvas:
                Color(*category_data.get("icon_bg", Colors.PRIMARY_LIGHT))
                RoundedRectangle(pos=w.pos, size=w.size, radius=[dp(12)])
            icon_lbl.pos  = w.pos
            icon_lbl.size = w.size

        icon_lbl = Label(
            text=category_data.get("icon_text", "?"),
            font_size=sp(22),
            color=category_data.get("icon_color", Colors.PRIMARY),
        )
        icon_box.bind(pos=_upd_icon, size=_upd_icon)
        icon_box.add_widget(icon_lbl)

        layout.add_widget(icon_box)

        # Text column
        text_col = BoxLayout(orientation="vertical", spacing=dp(2))
        name_lbl = Label(
            text=category_data["name"],
            font_size=sp(Fonts.SIZE_MD),
            color=Colors.TEXT_DARK,
            bold=True,
            halign="left",
            valign="bottom",
        )
        name_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

        desc_lbl = Label(
            text=category_data["desc"],
            font_size=sp(Fonts.SIZE_XS),
            color=Colors.TEXT_GRAY,
            halign="left",
            valign="top",
        )
        desc_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

        text_col.add_widget(name_lbl)
        text_col.add_widget(desc_lbl)
        layout.add_widget(text_col)

        # Chevron
        chevron = Label(
            text="›",
            font_size=sp(24),
            color=Colors.TEXT_LIGHT,
            size_hint_x=None,
            width=dp(24),
        )
        layout.add_widget(chevron)

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
            self._on_tap(self._cat)


# ---------------------------------------------------------------------------
# Guided Diagnosis Card
# ---------------------------------------------------------------------------
class GuidedDiagnosisCard(BoxLayout):
    def __init__(self, on_tap=None, **kwargs):
        super().__init__(
            orientation="vertical",
            size_hint_y=None,
            height=dp(100),
            padding=[dp(16), dp(14)],
            spacing=dp(6),
            **kwargs,
        )
        self._on_tap = on_tap
        self.bind(pos=self._draw, size=self._draw)

        row = BoxLayout(spacing=dp(10))
        icon_lbl = Label(
            text="ℹ",
            font_size=sp(18),
            color=Colors.PRIMARY,
            size_hint_x=None,
            width=dp(28),
        )
        title_lbl = Label(
            text="Guided Diagnosis",
            font_size=sp(Fonts.SIZE_MD),
            color=Colors.TEXT_DARK,
            bold=True,
            halign="left",
        )
        title_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
        row.add_widget(icon_lbl)
        row.add_widget(title_lbl)
        self.add_widget(row)

        desc = Label(
            text=("Select a category and condition to answer specific questions. "
                  "Our AI will provide tailored insights based on your responses."),
            font_size=sp(Fonts.SIZE_XS),
            color=Colors.TEXT_GRAY,
            halign="left",
        )
        desc.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
        self.add_widget(desc)

    def _draw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*Colors.PRIMARY_LIGHT)
            RoundedRectangle(pos=self.pos, size=self.size,
                             radius=[dp(Spacing.RADIUS_MD)])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self._on_tap:
                self._on_tap()
        return super().on_touch_down(touch)


# ---------------------------------------------------------------------------
# Home Screen
# ---------------------------------------------------------------------------
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._all_categories = CATEGORIES
        self._filtered = list(CATEGORIES)

        with self.canvas.before:
            Color(*Colors.BACKGROUND)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd_bg, size=self._upd_bg)

        self._build_ui()

    def _upd_bg(self, *_):
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def _build_ui(self):
        root = BoxLayout(orientation="vertical", spacing=dp(0))

        # ---- Header card (white) ---
        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(110),
            padding=[dp(Spacing.LG), dp(Spacing.MD), dp(Spacing.LG), dp(Spacing.SM)],
            spacing=dp(4),
        )
        with header.canvas.before:
            Color(*Colors.WHITE)
            self._hdr_rect = RoundedRectangle(pos=header.pos, size=header.size,
                                              radius=[0, 0, dp(20), dp(20)])
        header.bind(pos=lambda w, v: setattr(self._hdr_rect, "pos", v),
                    size=lambda w, v: setattr(self._hdr_rect, "size", v))

        # Back row
        back_row = BoxLayout(size_hint_y=None, height=dp(36))
        back_btn = Button(
            text="←",
            font_size=sp(22),
            size_hint_x=None,
            width=dp(36),
            background_color=(0, 0, 0, 0),
            color=Colors.TEXT_DARK,
        )
        title_lbl = Label(
            text="Disease Categories",
            font_size=sp(Fonts.SIZE_LG),
            color=Colors.TEXT_DARK,
            bold=True,
            halign="left",
            valign="middle",
        )
        title_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
        back_row.add_widget(back_btn)
        back_row.add_widget(title_lbl)

        sub_lbl = Label(
            text="Select a category to explore",
            font_size=sp(Fonts.SIZE_XS),
            color=Colors.TEXT_GRAY,
            halign="left",
            size_hint_y=None,
            height=dp(18),
            padding=[dp(36), 0, 0, 0],
        )
        sub_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

        header.add_widget(back_row)
        header.add_widget(sub_lbl)
        root.add_widget(header)

        # ---- Search bar ---
        search_box = BoxLayout(
            size_hint_y=None,
            height=dp(52),
            padding=[dp(Spacing.LG), dp(Spacing.SM)],
        )
        search_inner = BoxLayout(
            spacing=dp(8),
            padding=[dp(12), 0],
        )
        with search_inner.canvas.before:
            Color(*Colors.WHITE)
            self._srch_rect = RoundedRectangle(pos=search_inner.pos,
                                               size=search_inner.size,
                                               radius=[dp(Spacing.RADIUS_MD)])
        search_inner.bind(
            pos=lambda w, v: setattr(self._srch_rect, "pos", v),
            size=lambda w, v: setattr(self._srch_rect, "size", v),
        )

        search_icon = Label(
            text="🔍",
            font_size=sp(14),
            size_hint_x=None,
            width=dp(24),
            color=Colors.TEXT_LIGHT,
        )
        self._search_input = TextInput(
            hint_text="Search categories...",
            hint_text_color=Colors.TEXT_LIGHT,
            foreground_color=Colors.TEXT_DARK,
            background_color=(0, 0, 0, 0),
            multiline=False,
            cursor_color=Colors.PRIMARY,
            font_size=sp(Fonts.SIZE_SM),
        )
        self._search_input.bind(text=self._on_search)
        search_inner.add_widget(search_icon)
        search_inner.add_widget(self._search_input)
        search_box.add_widget(search_inner)
        root.add_widget(search_box)

        # ---- Scrollable category list ---
        scroll = ScrollView(do_scroll_x=False)
        self._list_layout = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(10),
            padding=[dp(Spacing.LG), dp(Spacing.SM), dp(Spacing.LG), dp(Spacing.LG)],
        )
        self._list_layout.bind(minimum_height=self._list_layout.setter("height"))
        self._rebuild_list()

        scroll.add_widget(self._list_layout)
        root.add_widget(scroll)

        self.add_widget(root)

    def _rebuild_list(self):
        self._list_layout.clear_widgets()
        for cat in self._filtered:
            card = CategoryCard(
                category_data=cat,
                on_tap=self._on_category_tap,
            )
            self._list_layout.add_widget(card)

        # Separator
        self._list_layout.add_widget(Widget(size_hint_y=None, height=dp(10)))

        # Guided diagnosis card
        guided = GuidedDiagnosisCard()
        self._list_layout.add_widget(guided)

        # "Not sure" footer link
        self._list_layout.add_widget(
            Widget(size_hint_y=None, height=dp(8))
        )
        not_sure = Label(
            text="Not sure which category?",
            font_size=sp(Fonts.SIZE_XS),
            color=Colors.TEXT_GRAY,
            size_hint_y=None,
            height=dp(20),
        )
        self._list_layout.add_widget(not_sure)

        free_btn = Button(
            text="Describe your symptoms freely instead",
            font_size=sp(Fonts.SIZE_SM),
            color=Colors.PRIMARY,
            background_color=(0, 0, 0, 0),
            size_hint_y=None,
            height=dp(30),
        )
        self._list_layout.add_widget(free_btn)

    def _on_search(self, instance, text):
        q = text.strip().lower()
        if q:
            self._filtered = [c for c in self._all_categories
                              if q in c["name"].lower() or q in c["desc"].lower()]
        else:
            self._filtered = list(self._all_categories)
        self._rebuild_list()

    def _on_category_tap(self, cat):
        app = self.manager.get_screen("disease_list")
        app.set_category(cat)
        self.manager.transition.direction = "left"
        self.manager.current = "disease_list"
