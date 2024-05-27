from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.core.window import Window

from recommendation_system import RecommendationSystem

from gui.pages.search_tab import SearchTab
from gui.pages.liked_tab import LikedTab
from gui.pages.stats_tab import StatsTab
from gui.pages.recommended_tab import RecommendedTab


recsys = RecommendationSystem()

class MainLayout(TabbedPanel):
    """Class containing the main container of the app."""
    
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        self.search_tab = SearchTab(recsys)
        self.liked_tab = LikedTab(recsys)
        self.stats_tab = StatsTab(recsys)
        self.recommended_tab = RecommendedTab(recsys)

        self.add_widget(self.search_tab)
        self.add_widget(self.liked_tab)
        self.add_widget(self.stats_tab)
        self.add_widget(self.recommended_tab)

        self.bind(current_tab=self.handle_tab_switch)


    def handle_tab_switch(self, obj, value):
        match value:

            case self.search_tab:
                self.search_tab.update()
            case self.stats_tab:
                self.stats_tab.update()
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
