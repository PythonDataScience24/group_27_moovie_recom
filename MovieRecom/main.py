from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.app import App

from recommendation_system import RecommendationSystem
from gui.searchbar import SearchBar
from gui.movie_list import MovieList


recsys = RecommendationSystem()

class MainLayout(GridLayout):
    pass

class MovieRecomApp(App):
    def build(self):

        Window.clearcolor = (1, 1, 1, 1) # Set background to white
        
        # Layouts
        main_layout = MainLayout(rows=2)
        body_layout = GridLayout(cols=1)

        # menu_layout = StackLayout(orientation='tb-lr')
        # menu_layout.add_widget(Label(text="Dashboard", height=200, color="black"))
        # menu_layout.add_widget(Label(text="Search", height=200, color="black"))
        # menu_layout.add_widget(Label(text="Liked", height=200, color="black"))
        # body_layout.add_widget(menu_layout)
        # body_layout.add_widget(Label(text='Page', color="black"))

        search_bar = SearchBar(recsys)

        movie_scroll = ScrollView()
        movie_scroll.size_hint_y = 1

        movie_list = MovieList()
        

        movie_scroll.add_widget(movie_list)
        body_layout.add_widget(movie_scroll)
        main_layout.add_widget(search_bar)
        main_layout.add_widget(body_layout)

        return main_layout

if __name__ == '__main__':
    MovieRecomApp().run()
