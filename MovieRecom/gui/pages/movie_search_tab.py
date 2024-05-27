
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from recommendation_system import RecommendationSystem
from gui.searchbar import MovieSearchBar
from gui.movie_list import MovieList
from gui.movie_list_element import MovieListElement


class MovieSearchTab(TabbedPanelItem):
    """Class used to display a search tab."""

    def __init__(self, recsys:RecommendationSystem, **kwargs):
        super(MovieSearchTab, self).__init__(text="Movie")


        self.recsys = recsys

        self.search_layout = BoxLayout(orientation='vertical')
        self.movie_list = MovieList()
        self.search_bar = MovieSearchBar(self.recsys, self.movie_list)
        self.movie_scroll = ScrollView(size_hint_y=1)

        self.movie_scroll.add_widget(self.movie_list)
        self.search_layout.add_widget(self.search_bar)
        self.search_layout.add_widget(self.movie_scroll)
        self.add_widget(self.search_layout)


    def update(self):
        """Updates the search tab."""

        for movie_list_element in self.movie_list.children[:]:
            if isinstance(movie_list_element, MovieListElement):
                movie_list_element.update()