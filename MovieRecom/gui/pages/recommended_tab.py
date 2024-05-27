
import requests

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from recommendation_system import RecommendationSystem
from gui.movie_list_element import MovieListElement
from gui.movie_list import MovieList

from tmdb_interface import TMDBInterface


class RecommendedTab(TabbedPanelItem):
    """Class used to display the recommendation."""

    def __init__(self, recsys:RecommendationSystem, **kwargs):
        super(RecommendedTab, self).__init__(text="Recommended")

        self.recsys = recsys

        self.tmdbi = TMDBInterface()

        self.recommended_layout = BoxLayout(orientation='vertical')
        self.movie_list = MovieList()
        self.movie_scroll = ScrollView(size_hint_y=1)

        self.movie_scroll.add_widget(self.movie_list)
        self.recommended_layout.add_widget(self.movie_scroll)


        self.add_widget(self.recommended_layout)


    def update(self):
        """Updates the recommended tab."""

        print("Updating recommendations tab...")

        self.movie_list.clear_widgets()
        recommendations = self.recsys.generate_recommendations()
    
        for _, row in recommendations.iterrows():
            imdb_id = row['tconst']

            movie = self.tmdbi.get_movie_from_imdb_id(imdb_id)
            self.movie_list.add_widget(MovieListElement(movie, self.recsys))
    
        print("Added recommended movies to the list")

        