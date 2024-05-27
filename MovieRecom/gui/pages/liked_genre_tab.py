from pandas import Series, DataFrame

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView


from recommendation_system import RecommendationSystem

from gui.person_list import PersonList
from gui.person_list_element import PersonListElement
from gui.genre_selection import GenreSelectionWidget

from movie import Movie, PersonRole, Person




class LikedGenre(TabbedPanelItem):
    """Class used to display a search tab."""

    def __init__(self, recsys:RecommendationSystem, **kwargs):

        super(LikedGenre, self).__init__(text="Genre")

        self.recsys = recsys

        self.genre_selection = GenreSelectionWidget(recsys)

        self.add_widget(self.genre_selection)


    def update(self):
        """Updates the liked tab."""
        # Clearing the person list
        pass
