
import requests

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from recommendation_system import RecommendationSystem
from gui.movie_list_element import MovieListElement

from tmdb_interface import TMDBInterface

from movie import Movie

class RecommendedTab(TabbedPanelItem):
    """Class used to display the recommendation."""

    def __init__(self, recsys:RecommendationSystem, **kwargs):
        super(RecommendedTab, self).__init__(text="Recommended")

        self.recsys = recsys

        self.tmdbi = TMDBInterface()

        recommended_layout = BoxLayout(orientation='vertical')
        recommended_scroll = ScrollView(size_hint=(1, 1))
        self.recommended_movies_list = GridLayout(cols=1, spacing=100, size_hint_y=None)
        self.recommended_movies_list.bind(minimum_height=self.recommended_movies_list.setter('height'))
        recommended_scroll.add_widget(self.recommended_movies_list)
        recommended_layout.add_widget(recommended_scroll)

        self.add_widget(recommended_layout)


    def update(self):
        """Updates the recommended tab."""

        print("Updating recommendations tab...")

        self.recommended_movies_list.clear_widgets()
        recommendations = self.recsys.generate_recommendations()
    
        for _, row in recommendations.iterrows():
            imdb_id = row['tconst']

            movie = self.tmdbi.get_movie_from_imdb_id(imdb_id)
            self.recommended_movies_list.add_widget(MovieListElement(movie, self.recsys))


            # url = f"http://www.omdbapi.com/?apikey=3ade98ca&i={imdb_id}"
            # response = requests.get(url)
            
            # if response.status_code == 200:
            #     data = response.json()
                
            #     # Create the Movie object using the existing method
            #     movie = Movie()
            #     movie.from_omdb_dict(data)  # Populate movie using the existing method
                
            #     # Create and add the MovieListElement to the UI
            #     movie_element = MovieListElement(movie, self.recsys)
            #     self.recommended_movies_list.add_widget(movie_element)
            #     print(f"Adding recommended movie: {movie.title}")
            # else:
            #     print(f"Failed to fetch details for movie with ID {imdb_id}")
    
        print("Added recommended movies to the list")

        