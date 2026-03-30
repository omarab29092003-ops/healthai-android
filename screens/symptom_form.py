"""
Symptom Form Screen
Dynamically builds a form based on the disease's field schema.
Supports: text, number, spinner, slider, toggle field types.
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
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp, sp
from kivy.animation import Animation

from utils.theme import Colors, Fonts, Spacing
from data.form_schemas import DISEASE_FORMS


# ---------------------------------------------------------------------------
# Form field factory helpers
# ---------------------------------------------------------------------------

def make_section_label(text):
    lbl = Label(
        text=text,
        font_size=sp(Fonts.SIZE_SM),
        color=Colors.TEXT_DARK,
        bold=True,
        halign="left",
        size_hint_y=None,
        height=dp(28),
    )
    lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
    return lbl


def make_label(text):
    lbl = Label(
        text=text,
        font_size=sp(Fonts.SIZE_SM),
        color=Colors.TEXT_GRAY,
        halign="left",
        size_hint_y=None,
        height=dp(22),
    )
    lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
    return lbl


def _card_wrap(child, extra_height=0):
    """Wrap a widget in a white card background."""
    height = child.height + dp(32) + extra_height
    card = BoxLayout(
        orientation="vertical",
        size_hint_y=None,
        height=height,
        padding=[dp(14), dp(12)],
    )
    with card.canvas.before:
        Color(*Colors.CARD)
        rect = RoundedRectangle(pos=card.pos, size=card.size,
                                radius=[dp(Spacing.RADIUS_MD)])
    card.bind(pos=lambda w, v: setattr(rect, "pos", v),
              size=lambda w, v: setattr(rect, "size", v))
    card.add_widget(child)
    return card


# ---------------------------------------------------------------------------
# Styled TextInput
# ---------------------------------------------------------------------------
class StyledInput(TextInput):
    def __init__(self, is_number=False, **kwargs):
        kwargs.setdefault("foreground_color", Colors.TEXT_DARK)
        kwargs.setdefault("hint_text_color",  Colors.TEXT_LIGHT)
        kwargs.setdefault("background_color", (0, 0, 0, 0))
        kwargs.setdefault("cursor_color",     Colors.PRIMARY)
        kwargs.setdefault("font_size",        sp(Fonts.SIZE_MD))
        kwargs.setdefault("multiline",        False)
        kwargs.setdefault("size_hint_y",      None)
        kwargs.setdefault("height",           dp(44))
        if is_number:
            kwargs.setdefault("input_filter", "float")
        super().__init__(**kwargs)
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*Colors.BORDER)
            RoundedRectangle(pos=self.pos, size=self.size,
                             radius=[dp(Spacing.RADIUS_SM)])
            Color(*Colors.WHITE)
            inner_pos  = (self.x + dp(1), self.y + dp(1))
            inner_size = (self.width - dp(2), self.height - dp(2))
            RoundedRectangle(pos=inner_pos, size=inner_size,
                             radius=[dp(Spacing.RADIUS_SM)])


# ---------------------------------------------------------------------------
# Styled Spinner
# ---------------------------------------------------------------------------
class StyledSpinner(Spinner):
    def __init__(self, **kwargs):
        kwargs.setdefault("background_color", Colors.WHITE)
        kwargs.setdefault("color",            Colors.TEXT_DARK)
        kwargs.setdefault("font_size",        sp(Fonts.SIZE_SM))
        kwargs.setdefault("size_hint_y",      None)
        kwargs.setdefault("height",           dp(44))
        super().__init__(**kwargs)
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*Colors.BORDER)
            RoundedRectangle(pos=self.pos, size=self.size,
                             radius=[dp(Spacing.RADIUS_SM)])


# ---------------------------------------------------------------------------
# Slider with value label
# ---------------------------------------------------------------------------
class LabeledSlider(BoxLayout):
    def __init__(self, min_val, max_val, default, step=1, **kwargs):
        super().__init__(
            orientation="vertical",
            size_hint_y=None,
            height=dp(60),
            spacing=dp(4),
            **kwargs,
        )
        self._min  = min_val
        self._max  = max_val
        self._step = step

        top_row = BoxLayout(size_hint_y=None, height=dp(20))
        min_lbl = Label(text=str(min_val), font_size=sp(10),
                        color=Colors.TEXT_LIGHT, halign="left")
        min_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

        self._val_lbl = Label(
            text=str(default),
            font_size=sp(Fonts.SIZE_SM),
            color=Colors.PRIMARY,
            bold=True,
        )
        max_lbl = Label(text=str(max_val), font_size=sp(10),
                        color=Colors.TEXT_LIGHT, halign="right")
        max_lbl.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

        top_row.add_widget(min_lbl)
        top_row.add_widget(self._val_lbl)
        top_row.add_widget(max_lbl)
        self.add_widget(top_row)

        self.slider = Slider(
            min=min_val,
            max=max_val,
            value=default,
            step=step,
            size_hint_y=None,
            height=dp(36),
            cursor_size=(dp(20), dp(20)),
        )
        self.slider.bind(value=self._on_value)
        self.add_widget(self.slider)

    def _on_value(self, instance, val):
        if self._step >= 1:
            self._val_lbl.text = str(int(val))
        else:
            self._val_lbl.text = f"{val:.2f}"

    @property
    def value(self):
        return self.slider.value


# ---------------------------------------------------------------------------
# Toggle (Yes/No)
# ---------------------------------------------------------------------------
class YesNoToggle(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(44),
            spacing=dp(8),
            **kwargs,
        )
        self._value = False

        self._no_btn = Button(
            text="No",
            size_hint_x=0.5,
            background_color=(0, 0, 0, 0),
            font_size=sp(Fonts.SIZE_SM),
            color=Colors.TEXT_GRAY,
        )
        self._yes_btn = Button(
            text="Yes",
            size_hint_x=0.5,
            background_color=(0, 0, 0, 0),
            font_size=sp(Fonts.SIZE_SM),
            color=Colors.TEXT_GRAY,
        )
        self._no_btn.bind(pos=self._draw_no,   size=self._draw_no)
        self._yes_btn.bind(pos=self._draw_yes, size=self._draw_yes)
        self._no_btn.bind(on_release=self._select_no)
        self._yes_btn.bind(on_release=self._select_yes)

        self.add_widget(self._no_btn)
        self.add_widget(self._yes_btn)
        self._update_state()

    def _draw_no(self, *_):
        w = self._no_btn
        w.canvas.before.clear()
        with w.canvas.before:
            if not self._value:
                Color(*Colors.PRIMARY)
            else:
                Color(*Colors.BORDER)
            RoundedRectangle(pos=w.pos, size=w.size, radius=[dp(Spacing.RADIUS_SM)])

    def _draw_yes(self, *_):
        w = self._yes_btn
        w.canvas.before.clear()
        with w.canvas.before:
            if self._value:
                Color(*Colors.PRIMARY)
            else:
                Color(*Colors.BORDER)
            RoundedRectangle(pos=w.pos, size=w.size, radius=[dp(Spacing.RADIUS_SM)])

    def _update_state(self):
        self._no_btn.color  = Colors.WHITE if not self._value else Colors.TEXT_GRAY
        self._yes_btn.color = Colors.WHITE if self._value else Colors.TEXT_GRAY
        self._draw_no()
        self._draw_yes()

    def _select_no(self, *_):
        self._value = False
        self._update_state()

    def _select_yes(self, *_):
        self._value = True
        self._update_state()

    @property
    def value(self):
        return self._value


# ---------------------------------------------------------------------------
# Symptom Form Screen
# ---------------------------------------------------------------------------
class SymptomFormScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._disease = None
        self._field_widgets = {}

        with self.canvas.before:
            Color(*Colors.BACKGROUND)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd_bg, size=self._upd_bg)

    def _upd_bg(self, *_):
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def set_disease(self, disease_name):
        self._disease = disease_name

    def on_enter(self):
        self.clear_widgets()
        self._field_widgets = {}
        self._build_ui()

    def _build_ui(self):
        if not self._disease:
            return

        schema = DISEASE_FORMS.get(self._disease, {})
        fields = schema.get("fields", [])

        root = BoxLayout(orientation="vertical")

        # ---------- Header ----------
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

        title = Label(
            text=self._disease,
            font_size=sp(Fonts.SIZE_LG),
            color=Colors.TEXT_DARK,
            bold=True,
            halign="left",
        )
        title.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))

        back_row.add_widget(back_btn)
        back_row.add_widget(title)

        desc = schema.get("description", "Answer the questions below")
        sub = Label(
            text=desc,
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

        # ---------- Scrollable form ----------
        scroll = ScrollView(do_scroll_x=False)
        form   = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(10),
            padding=[dp(Spacing.LG), dp(Spacing.MD), dp(Spacing.LG), dp(Spacing.MD)],
        )
        form.bind(minimum_height=form.setter("height"))

        for field in fields:
            field_name = field["name"]
            field_type = field["type"]
            label_text = field["label"]

            # Card container
            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                padding=[dp(14), dp(12)],
                spacing=dp(6),
            )
            with card.canvas.before:
                Color(*Colors.CARD)
                crect = RoundedRectangle(pos=card.pos, size=card.size,
                                         radius=[dp(Spacing.RADIUS_MD)])
            card.bind(pos=lambda w, v, r=crect: setattr(r, "pos", v),
                      size=lambda w, v, r=crect: setattr(r, "size", v))

            lbl = make_label(label_text)
            card.add_widget(lbl)

            if field_type in ("text", "number"):
                widget = StyledInput(
                    is_number=(field_type == "number"),
                    hint_text=str(field.get("hint", "")),
                )
                card.add_widget(widget)
                card.height = dp(90)

            elif field_type == "spinner":
                options = field.get("options", [])
                widget = StyledSpinner(
                    text=options[0] if options else "",
                    values=options,
                )
                card.add_widget(widget)
                card.height = dp(90)

            elif field_type == "slider":
                widget = LabeledSlider(
                    min_val = field.get("min", 0),
                    max_val = field.get("max", 100),
                    default = field.get("default", 50),
                    step    = field.get("step", 1),
                )
                card.add_widget(widget)
                card.height = dp(105)

            elif field_type == "toggle":
                widget = YesNoToggle()
                card.add_widget(widget)
                card.height = dp(100)

            else:
                widget = StyledInput()
                card.add_widget(widget)
                card.height = dp(90)

            self._field_widgets[field_name] = (field_type, widget)
            form.add_widget(card)

        # ---------- Analyze button ----------
        btn_box = BoxLayout(
            size_hint_y=None,
            height=dp(70),
            padding=[0, dp(Spacing.SM)],
        )
        analyze_btn = Button(
            text="Analyze My Symptoms  →",
            font_size=sp(Fonts.SIZE_MD),
            bold=True,
            color=Colors.WHITE,
            background_color=(0, 0, 0, 0),
            size_hint_y=None,
            height=dp(52),
        )
        analyze_btn.bind(pos=self._draw_btn, size=self._draw_btn)
        self._analyze_btn = analyze_btn
        analyze_btn.bind(on_release=self._submit)
        btn_box.add_widget(analyze_btn)
        form.add_widget(btn_box)

        scroll.add_widget(form)
        root.add_widget(scroll)
        self.add_widget(root)

    def _draw_btn(self, *_):
        w = self._analyze_btn
        w.canvas.before.clear()
        with w.canvas.before:
            Color(*Colors.PRIMARY)
            RoundedRectangle(pos=w.pos, size=w.size,
                             radius=[dp(Spacing.RADIUS_PILL)])

    def _collect_inputs(self):
        result = {}
        schema = DISEASE_FORMS.get(self._disease, {})
        for field in schema.get("fields", []):
            name      = field["name"]
            ftype, widget = self._field_widgets.get(name, (None, None))
            if widget is None:
                continue

            if ftype in ("text", "number"):
                val = widget.text.strip()
                if field.get("type") == "number":
                    try:
                        val = float(val) if "." in val else int(val)
                    except ValueError:
                        val = field.get("default", 0)
                result[name] = val

            elif ftype == "spinner":
                result[name] = widget.text

            elif ftype == "slider":
                result[name] = widget.value

            elif ftype == "toggle":
                result[name] = widget.value

        return result

    def _submit(self, *_):
        anim = Animation(opacity=0.7, duration=0.1) + Animation(opacity=1, duration=0.1)
        anim.start(self._analyze_btn)

        inputs = self._collect_inputs()
        schema = DISEASE_FORMS.get(self._disease, {})
        model_type = schema.get("model", "rule_based")

        from models.predictor import Predictor

        if model_type == "diabetes":
            result = Predictor.predict_diabetes(inputs)
        elif model_type == "heart":
            result = Predictor.predict_heart(inputs)
        else:
            result = Predictor.predict_rule_based(self._disease, inputs)

        # Navigate to results
        results_screen = self.manager.get_screen("results")
        results_screen.set_result(self._disease, result)
        self.manager.transition.direction = "left"
        self.manager.current = "results"

    def _go_back(self, *_):
        self.manager.transition.direction = "right"
        self.manager.current = "disease_list"
