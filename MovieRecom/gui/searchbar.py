from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from movie import PersonRole
from recommendation_system import RecommendationSystem

from gui.movie_list_element import MovieListElement
from gui.person_list_element import PersonListElement
from gui.movie_list import MovieList
from gui.person_list import PersonList



class MovieSearchBar(BoxLayout):
    """Class used to display a searchbar."""
    def __init__(self, recsys:RecommendationSystem, movie_list:MovieList, **kwargs):
        super(MovieSearchBar, self).__init__(**kwargs)

        self.recsys = recsys

        self.movie_list = movie_list

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

        self.movie_list.clear_widgets()
        self.movie_list.height = 0

        for movie_result in movie_result_list:
            new_movie_element = MovieListElement(movie_result, self.recsys)
            self.movie_list.add_widget(new_movie_element)

            # Update MovieList height dynamically
            self.movie_list.height += new_movie_element.height





class PersonSearchBar(BoxLayout):
    """Class used to display a searchbar."""
    def __init__(self, recsys:RecommendationSystem, person_list:PersonList, person_role:PersonRole, **kwargs):
        super(PersonSearchBar, self).__init__(**kwargs)

        self.recsys = recsys

        self.person_list = person_list
        self.person_role =  person_role

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

        person_result_list = self.recsys.person_query(search_query, self.person_role)
        if not person_result_list:
            return
        
        self.person_list.clear_widgets()
        self.person_list.height = 0

        for person_result in person_result_list:
            new_person_element = PersonListElement(person_result, self.recsys)
            self.person_list.add_widget(new_person_element)

            # Update MovieList height dynamically
            self.person_list.height += new_person_element.height
