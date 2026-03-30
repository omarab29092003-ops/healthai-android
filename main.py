"""
HealthAI — Main Entry Point
Kivy app with ScreenManager routing all screens.
"""

import os
import sys

# Ensure project root is on the path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from kivy.config import Config
# Set window size matching Figma (393×852) for desktop dev; ignored on Android
Config.set("graphics", "width",  "393")
Config.set("graphics", "height", "852")
Config.set("graphics", "resizable", "0")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.metrics import dp

from screens.onboarding    import OnboardingScreen
from screens.home          import HomeScreen
from screens.disease_list  import DiseaseListScreen
from screens.symptom_form  import SymptomFormScreen
from screens.results       import ResultsScreen
from utils.theme           import Colors


class HealthAIApp(App):
    title = "HealthAI"

    def build(self):
        Window.clearcolor = Colors.WHITE

        sm = ScreenManager(transition=SlideTransition(duration=0.25))

        # Onboarding slides
        sm.add_widget(OnboardingScreen(name="onboarding_0", slide_idx=0))
        sm.add_widget(OnboardingScreen(name="onboarding_1", slide_idx=1))
        sm.add_widget(OnboardingScreen(name="onboarding_2", slide_idx=2))

        # Main screens
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(DiseaseListScreen(name="disease_list"))
        sm.add_widget(SymptomFormScreen(name="symptom_form"))
        sm.add_widget(ResultsScreen(name="results"))

        sm.current = "onboarding_0"
        return sm


if __name__ == "__main__":
    HealthAIApp().run()
