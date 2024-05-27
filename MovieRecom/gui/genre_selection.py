
from kivy.uix.stacklayout import StackLayout
from kivy.uix.togglebutton import ToggleButton

from recommendation_system import RecommendationSystem
from movie import Genre



class GenreSelectionWidget(StackLayout):
    def __init__(self, recsys:RecommendationSystem, **kwargs):
        super(GenreSelectionWidget, self).__init__(**kwargs)

        self.recsys = recsys
        self.genre_list = self.recsys.genre_query()

        for genre in self.genre_list:
            genre_button = ToggleButton()
            genre_button.text = genre.name
            genre_button.state = "down" if genre.liked else "normal"
            genre_button.size_hint=(None, None)

            genre_button.bind(on_press=self.on_genre_press)

            self.add_widget(genre_button)
        
    def on_genre_press(self, instance:ToggleButton):
        
        liked = instance.state == "down"
        name = instance.text

        self.recsys.set_liked_genre(Genre(name), liked)
        
        