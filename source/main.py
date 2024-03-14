from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from json import load
from kivy.clock import Clock
from functools import partial # allow arguments in Clock.schedule_once
"""
Author Ludvig Ekdahl, 2024 
PathPoints is a Kivy app for keeping track of weighted points in a cyto- and/or 
histopathology lab. It's based on guidelines released by the Swedish Society of Pathology, https://svfp.se/, 
and is intended to be used by pathologists in Sweden to monitor their workload.
"""

# Unicode chars for the subject files
# ä = \u00E4
# ö = \u00F6
# å = \u00E5

def get_subject_dict(subject_name):
    # Get the dictionary of the subject from the .json file
    # These dictionaries contain samples as keys and their points as values
    with open(f"subject_lists/subjects/{subject_name}.json", "r") as file:
        return load(file)

def get_subject_list(subject_name):
    # Get the list of subjects from the .json file
    with open(f"subject_lists/{subject_name}.json", "r") as file:
        subjects_json = load(file)
        return subjects_json["subjects"]

class WindowManager(ScreenManager):
    pass

class PathPointsMain(Screen):
    """
    This is the main screen of the app. It contains the following buttons and labels:
    Label: "Diagnostik / mikroskopi"
    Button: "Alla ämnesområden"
    Button: "Favoriter"
    Label: "Utskärning / makroskopi"
    Button: "Alla ämnesområden"
    Button: "Favoriter"
    What's in the screens for both "Alla ämnesområden" for both "Diagnostik" and "Utskärning" is dynamically
    generated upon loading the app. Favoriter can additionally be modified by the user during runtime, so it's
    generated every time those screens are selected/entered.
    """
    # After loading, all subject screens should be set up with their subjects based on the .json files
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Have to delay the initialization of the subject screens to until PathPointsMain is fully loaded
        Clock.schedule_once(partial(self.initialize_subscreens, "all_diagnostic_subjects", "subject_lists/diagnostics_subjects.json"))
        Clock.schedule_once(partial(self.initialize_subscreens, "all_grossing_subjects", "subject_lists/grossing_subjects.json"))
        # ToDO set up favorites

    def initialize_subscreens(self, screen_name, subject_file, *args):
        # Collect the all_subjects_screen handle
        all_subjects_screen = self.manager.get_screen(screen_name)
        # Collect the all_subjects_grid element from the all_subjects_screen handle
        all_subjects_grid = all_subjects_screen.ids.all_subjects_grid
        # Load the list of subjects from source/subject_lists/subjects/diagnostics_subjects.json
        with open(subject_file, "r") as file:
            subjects_json = load(file)
            subjects_dict = subjects_json["subjects"]
        # Initialize rows in all_subjects_grid to number of keys in subjects
        all_subjects_grid.rows = len(subjects_dict)
        # Initialize columns in all_subjects_grid to 1
        all_subjects_grid.cols = 1
        # For each subject in the list, add a button to the all_subjects_grid
        # This button should have a call back to the view_subject function in the all_subjects_screen
        for subject, subject_file in subjects_dict.items():
            # Create a button with the text of the subject
            subject_button = Button(text=subject)
            # Bind the view_subject function to the button as a callback
            subject_button.bind(on_press=lambda x: self.view_subject(subject_file))
            # Add the button to the all_subjects_grid
            all_subjects_grid.add_widget(subject_button)

    def view_subject(self, subject_name):
        """
        This function is called when a subject button is pressed. Upon clicking, the following happens:
        #1 It loads the json file for the subject into a dictionary
        #2 It collects the SubjectScreen handle from the window manager
        #3 It collects the grid_layout element from the SubjectScreen handle and clears it from any previous buttons.
        #4 For each sample in this subject, it adds a button and plus/minus/favorite buttons.
        #5 It changes the user view to the SubjectScreen
        """
        # Collect SubjectScreen handle
        other = self.manager.get_screen("subject")
        # Collect the subject_grid element from the SubjectScreen handle
        subject_grid = other.ids.subject_grid
        # Clear the subject_grid handle from any previous buttons
        subject_grid.clear_widgets()
        # Load the dictionary of the subject
        subject_dict = get_subject_dict(subject_name)
        # Initialize rows in subject_grid to number of keys in subject_dict
        subject_grid.rows = len(subject_dict)
        # Initialize columns in subject_grid to 4
        subject_grid.cols = 4
        # add padding and spacing between buttons in the subject_grid
        subject_grid.padding = 5
        subject_grid.spacing = 20

        # For each key in subject_dict, add a button to the subject_grid
        # after each such button, add a plus button, a minus button, and a favorite button
        # like this: <sample name> <plus> <minus> <favorite>
        for key, value in subject_dict.items():
            # 0.05 padding between buttons
            subject_grid.add_widget(Label(text=key, size_hint=(0.5, 0.1)))
            subject_grid.add_widget(Button(text="+", size_hint=(0.1, 0.1)))
            subject_grid.add_widget(Button(text="-", size_hint=(0.1, 0.1)))
            subject_grid.add_widget(Button(text="Add favorite", size_hint=(0.5, 0.1)))
        # Change the user view to the SubjectScreen
        self.manager.current = "subject"

    pass

    def generate_report(self):
        # Generate a text report (preferably pdf though)
        # With the users points and statistics
        pass


class AllDiagnosticSubjectsScreen(Screen):
    pass

class AllGrossingSubjectsScreen(Screen):
    pass

class SubjectScreen(Screen):
    # Screen for showing buttons for a specific subject,
    # Each defined in a .json
    def add_favorite(self):
        # Check if button name is in favorites json, otherwise add it
        pass

    pass

#help screen
class HelpScreen(Screen):
    pass

class FavoritesScreen(Screen):
    # Screen for showing buttons for user-defined favorites
    # defined in a locally stored .json

    def remove_favorite(self):
        # favorites screen cannot add favorites, just remove them
        pass

    pass

kv = Builder.load_file("pathpoints.kv")

class PathPoints(App):
    def build(self):
        return kv

    
if __name__ == '__main__':
    PathPoints().run()