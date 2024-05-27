
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel

from recommendation_system import RecommendationSystem

from gui.pages.liked_movie_tab import LikedMovieTab
from gui.pages.liked_person_tab import LikedPersonTab
from gui.pages.liked_genre_tab import LikedGenre

from movie import PersonRole




class LikedTab(TabbedPanelItem):

    def __init__(self, recsys:RecommendationSystem, **kwargs):
        super(LikedTab, self).__init__(text="Liked")

        self.recsys = recsys

        self.liked_layout = TabbedPanel()

        self.liked_movie_tab = LikedMovieTab(recsys)
        self.liked_actor_tab = LikedPersonTab(recsys, PersonRole.ACTOR)
        self.liked_writer_tab = LikedPersonTab(recsys, PersonRole.WRITER)
        self.liked_director_tab = LikedPersonTab(recsys, PersonRole.DIRECTOR)
        self.liked_genre_tab = LikedGenre(recsys)
        

        self.liked_layout.add_widget(self.liked_movie_tab)
        self.liked_layout.add_widget(self.liked_actor_tab)
        self.liked_layout.add_widget(self.liked_writer_tab)
        self.liked_layout.add_widget(self.liked_director_tab)
        self.liked_layout.add_widget(self.liked_genre_tab)

        self.liked_layout.bind(current_tab=self.handle_search_tab_switch)

        self.add_widget(self.liked_layout)

    def update(self):
        """Updates the search tab."""
        self.liked_movie_tab.update()
        self.liked_actor_tab.update()
        self.liked_writer_tab.update()
        self.liked_director_tab.update()
        self.liked_genre_tab.update()

    def handle_search_tab_switch(self, obj, value):
        match value:
            case self.liked_movie_tab:
                self.liked_movie_tab.update()
            case self.liked_actor_tab:
                self.liked_actor_tab.update()
            case self.liked_writer_tab:
                self.liked_writer_tab.update()
            case self.liked_director_tab:
                self.liked_director_tab.update()
            case self.liked_genre_tab:
                self.liked_genre_tab.update()