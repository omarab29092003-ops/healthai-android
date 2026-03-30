"""
HealthAI Theme Constants
Centralized design tokens for consistent UI across all screens.
"""

# ---------------------------------------------------------------------------
# Color Palette
# ---------------------------------------------------------------------------
class Colors:
    # Primary brand
    PRIMARY       = (0.133, 0.404, 0.902, 1)        # #2267E6 – blue CTA buttons
    PRIMARY_LIGHT = (0.878, 0.918, 1.0, 1)           # #E0EAFF – light blue bg
    PRIMARY_DARK  = (0.098, 0.302, 0.702, 1)         # #194DB3 – hover

    # Accent / status
    TEAL          = (0.055, 0.769, 0.682, 1)         # #0EC4AE
    TEAL_LIGHT    = (0.882, 0.976, 0.969, 1)         # #E1F9F7
    GREEN         = (0.133, 0.694, 0.298, 1)         # #22B14C
    GREEN_LIGHT   = (0.878, 0.973, 0.914, 1)         # #E0F8E9
    ORANGE        = (0.988, 0.600, 0.122, 1)         # #FC991F
    ORANGE_LIGHT  = (1.0,   0.945, 0.867, 1)         # #FFF1DD
    PURPLE        = (0.647, 0.392, 0.859, 1)         # #A563DB
    PURPLE_LIGHT  = (0.941, 0.878, 0.988, 1)         # #F0E0FC
    PINK          = (0.988, 0.224, 0.502, 1)         # #FC3980
    PINK_LIGHT    = (1.0,   0.882, 0.933, 1)         # #FFE1EE

    # Neutrals
    WHITE         = (1, 1, 1, 1)
    BACKGROUND    = (0.957, 0.961, 0.973, 1)         # #F4F5F8 app background
    CARD          = (1, 1, 1, 1)                     # card background
    BORDER        = (0.898, 0.906, 0.925, 1)         # #E5E7EC
    TEXT_DARK     = (0.098, 0.118, 0.173, 1)         # #191E2C headings
    TEXT_GRAY     = (0.471, 0.506, 0.596, 1)         # #788198 subtitles
    TEXT_LIGHT    = (0.686, 0.714, 0.784, 1)         # #AFB6C8 placeholders
    DIVIDER       = (0.933, 0.937, 0.953, 1)         # #EEEFF3

    # Risk levels
    RISK_LOW      = (0.133, 0.694, 0.298, 1)         # green
    RISK_MEDIUM   = (0.988, 0.600, 0.122, 1)         # orange
    RISK_HIGH     = (0.937, 0.267, 0.267, 1)         # red

    # Disabled / inactive
    INACTIVE_DOT  = (0.800, 0.820, 0.870, 1)         # progress dot inactive


# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
class Fonts:
    REGULAR  = "Roboto"
    BOLD     = "Roboto"        # Kivy bold variant
    SIZE_XS  = 10
    SIZE_SM  = 12
    SIZE_MD  = 14
    SIZE_LG  = 16
    SIZE_XL  = 20
    SIZE_XXL = 26
    SIZE_H1  = 30


# ---------------------------------------------------------------------------
# Spacing / Radius
# ---------------------------------------------------------------------------
class Spacing:
    XS   = 4
    SM   = 8
    MD   = 16
    LG   = 24
    XL   = 32
    XXL  = 48

    RADIUS_SM  = 8
    RADIUS_MD  = 14
    RADIUS_LG  = 20
    RADIUS_PILL = 50      # fully rounded buttons


# ---------------------------------------------------------------------------
# Category metadata (icon char, icon color, background color)
# ---------------------------------------------------------------------------
CATEGORIES = [
    {
        "id": "common",
        "name": "Common Diseases",
        "desc": "Frequently occurring conditions",
        "icon": "\ue6e1",     # thermometer placeholder (label fallback)
        "icon_text": "🌡",
        "icon_color": Colors.PRIMARY,
        "icon_bg":   Colors.PRIMARY_LIGHT,
    },
    {
        "id": "children",
        "name": "Children's Health",
        "desc": "Pediatric conditions and illnesses",
        "icon_text": "👶",
        "icon_color": Colors.PINK,
        "icon_bg":   Colors.PINK_LIGHT,
    },
    {
        "id": "chronic",
        "name": "Chronic Conditions",
        "desc": "Long-term health conditions",
        "icon_text": "💓",
        "icon_color": Colors.TEAL,
        "icon_bg":   Colors.TEAL_LIGHT,
    },
    {
        "id": "women",
        "name": "Women's Health",
        "desc": "Female-specific health concerns",
        "icon_text": "♀",
        "icon_color": Colors.PURPLE,
        "icon_bg":   Colors.PURPLE_LIGHT,
    },
    {
        "id": "mental",
        "name": "Mental Health",
        "desc": "Psychological and emotional wellbeing",
        "icon_text": "🧠",
        "icon_color": Colors.ORANGE,
        "icon_bg":   Colors.ORANGE_LIGHT,
    },
    {
        "id": "respiratory",
        "name": "Respiratory",
        "desc": "Breathing and lung conditions",
        "icon_text": "💨",
        "icon_color": Colors.PRIMARY,
        "icon_bg":   Colors.PRIMARY_LIGHT,
    },
    {
        "id": "heart",
        "name": "Heart Diseases",
        "desc": "Cardiovascular conditions",
        "icon_text": "❤",
        "icon_color": (0.937, 0.267, 0.267, 1),
        "icon_bg":   (1.0,  0.882, 0.882, 1),
    },
    {
        "id": "diabetes",
        "name": "Diabetes",
        "desc": "Blood sugar related conditions",
        "icon_text": "💉",
        "icon_color": Colors.GREEN,
        "icon_bg":   Colors.GREEN_LIGHT,
    },
]
