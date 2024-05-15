from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

from recommendation_system import RecommendationSystem
from gui.movie_list_element import MovieListElement
from gui.movie_list import MovieList


class SearchBar(BoxLayout):
    def __init__(self, recsys:RecommendationSystem, **kwargs):
        super(SearchBar, self).__init__(**kwargs)

        self.recsys = recsys

        self.size_hint_y = None
        self.height = 50

        # Create TextInput for search input
        self.search_input = TextInput(hint_text='Search...', multiline=False, size_hint=(1, 1))
        self.search_input.bind(on_text_validate=self.user_search_query)

        self.add_widget(self.search_input)


    def user_search_query(self, instance):
        """Updates the UI from the user query"""
        search_query = instance.text.strip()
        if not search_query:
            return

        movie_result_list = self.recsys.movie_query(search_query)
        if not movie_result_list:
            return

        movie_list = self.find_movie_list(App.get_running_app().root)
        if movie_list:
            movie_list.clear_widgets()
            movie_list.height = 0

        for movie_result in movie_result_list:
            new_movie_element = MovieListElement(movie_result, self.recsys)
            movie_list.add_widget(new_movie_element)

            # Update MovieList height dynamically
            movie_list.height += new_movie_element.height



    def find_movie_list(self, widget):
        """Recursively find and return the MovieList widget within the widget tree."""
        if isinstance(widget, MovieList):
            return widget
        for child in widget.children:
            found = self.find_movie_list(child)
            if found:
                return found
        return None

