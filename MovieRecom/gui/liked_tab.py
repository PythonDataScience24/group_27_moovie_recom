
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from gui.movie_list_element import MovieListElement

from recommendation_system import RecommendationSystem
from movie import Movie


class VisualizationBox(BoxLayout):
    """Class used to display liked elements."""
    def __init__(self, recsys:RecommendationSystem, **kwargs):
        super(VisualizationBox, self).__init__(**kwargs)

        self.recsys = recsys
        self.figureCanvas = None

    def update_visualization(self):
        figure = self.recsys.get_liked_visualization()
        self.clear_widgets()
        self.figureCanvas = FigureCanvasKivyAgg(figure)
        self.add_widget(self.figureCanvas)



class LikedTab(TabbedPanelItem):
    """Class used to display a search tab."""

    def __init__(self, recsys:RecommendationSystem, **kwargs):
        super(LikedTab, self).__init__(text="Liked")

        self.recsys = recsys

        liked_layout = BoxLayout(orientation='horizontal')
        liked_scroll = ScrollView(size_hint=(2, 1))
        self.liked_movies_list = GridLayout(cols=1, spacing=100, size_hint_y=None)
        self.liked_movies_list.bind(minimum_height=self.liked_movies_list.setter('height'))
        self.visualization = VisualizationBox(self.recsys)
        
        liked_scroll.add_widget(self.liked_movies_list)
        liked_layout.add_widget(liked_scroll)
        liked_layout.add_widget(self.visualization)
        self.add_widget(liked_layout)


    def update(self):
        """Updates the liked tab."""
        # Clearing the movie list
        self.liked_movies_list.clear_widgets()

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
                liked=movie_row['liked'],)

            
            self.liked_movies_list.add_widget(MovieListElement(movie_obj, self.recsys))

            # Update the visualization
            self.recsys.update_liked_visualizations()
            self.visualization.update_visualization()
