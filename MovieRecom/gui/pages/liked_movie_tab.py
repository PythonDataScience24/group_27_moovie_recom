
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from recommendation_system import RecommendationSystem

from gui.movie_list_element import MovieListElement
from gui.movie_list import MovieList
from gui.genre_selection import GenreSelectionWidget


from movie import Movie




class LikedMovieTab(TabbedPanelItem):
    """Class used to display a search tab."""

    def __init__(self, recsys:RecommendationSystem, **kwargs):
        super(LikedMovieTab, self).__init__(text="Movie")

        self.recsys = recsys

        self.liked_movie_layout = BoxLayout(orientation='horizontal')

        self.movie_list = MovieList()
        self.movie_scroll = ScrollView(size_hint=(2, 1))

        self.movie_scroll.add_widget(self.movie_list)
        self.liked_movie_layout.add_widget(self.movie_scroll)

        self.add_widget(self.liked_movie_layout)


    def update(self):
        """Updates the liked tab."""
        # Clearing the movie list
        self.movie_list.clear_widgets()

        # Creating the list of liked movies
        for _, movie_row in self.recsys.liked_movies.iterrows():
            movie_obj = Movie(
                id=movie_row['id'],
                title=movie_row['title'],
                runtime=movie_row['runtime'],
                poster_url=movie_row['poster_url'],
                genre=movie_row['genre'],
                director=movie_row['director'],
                actors=movie_row['actors'],
                release_date=movie_row['release_date'],
                liked=movie_row['liked'],
                rating=movie_row['rating'])

            
            self.movie_list.add_widget(MovieListElement(movie_obj, self.recsys))
