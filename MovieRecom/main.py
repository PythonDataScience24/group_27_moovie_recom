from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.core.window import Window

from gui.movie_search_tab import MovieSearchTab
from gui.person_search_tab import PersonSearchTab
from gui.liked_tab import LikedTab
from gui.recommended_tab import RecommendedTab

from recommendation_system import RecommendationSystem
from movie import PersonRole


recsys = RecommendationSystem()


class MainLayout(TabbedPanel):
    """Class containing the main container of the app."""
    
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        self.movie_search_tab = MovieSearchTab(recsys)
        self.actor_search_tab = PersonSearchTab(recsys, PersonRole.ACTOR)
        self.writer_search_tab = PersonSearchTab(recsys, PersonRole.WRITER)
        self.director_search_tab = PersonSearchTab(recsys, PersonRole.DIRECTOR)
        self.liked_tab = LikedTab(recsys)
        self.recommended_tab = RecommendedTab(recsys)

        self.add_widget(self.movie_search_tab)
        self.add_widget(self.actor_search_tab)
        self.add_widget(self.writer_search_tab)
        self.add_widget(self.director_search_tab)
        self.add_widget(self.liked_tab)
        self.add_widget(self.recommended_tab)

        self.bind(current_tab=self.handle_tab_switch)


    def handle_tab_switch(self, obj, value):
        match value:
            case self.movie_search_tab:
                self.movie_search_tab.update()
            case self.actor_search_tab:
                self.actor_search_tab.update()
            case self.liked_tab:
                self.liked_tab.update()
            case self.recommended_tab:
                self.recommended_tab.update()

class MovieRecomApp(App):
    """Application class of the program."""
    
    def build(self):
        
        Window.clearcolor = (1, 1, 1, 1) # Set background to white
        
        
        main_layout = MainLayout()
        return main_layout


if __name__ == '__main__':
    MovieRecomApp().run()
