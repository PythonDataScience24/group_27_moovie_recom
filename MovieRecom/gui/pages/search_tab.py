
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel

from recommendation_system import RecommendationSystem

from gui.pages.movie_search_tab import MovieSearchTab
from gui.pages.person_search_tab import PersonSearchTab
from movie import PersonRole




class SearchTab(TabbedPanelItem):

    def __init__(self, recsys:RecommendationSystem, **kwargs):
        super(SearchTab, self).__init__(text="Search")

        self.recsys = recsys

        self.search_layout = TabbedPanel()

        self.movie_search_tab = MovieSearchTab(recsys)
        self.actor_search_tab = PersonSearchTab(recsys, PersonRole.ACTOR)
        self.writer_search_tab = PersonSearchTab(recsys, PersonRole.WRITER)
        self.director_search_tab = PersonSearchTab(recsys, PersonRole.DIRECTOR)
        

        self.search_layout.add_widget(self.movie_search_tab)
        self.search_layout.add_widget(self.actor_search_tab)
        self.search_layout.add_widget(self.writer_search_tab)
        self.search_layout.add_widget(self.director_search_tab)

        self.search_layout.bind(current_tab=self.handle_search_tab_switch)

        self.add_widget(self.search_layout)

    def update(self):
        """Updates the search tab."""
        self.movie_search_tab.update()
        self.actor_search_tab.update()
        self.writer_search_tab.update()
        self.director_search_tab.update()

    def handle_search_tab_switch(self, obj, value):
        match value:
            case self.movie_search_tab:
                self.movie_search_tab.update()
            case self.actor_search_tab:
                self.actor_search_tab.update()
            case self.writer_search_tab:
                self.writer_search_tab.update()
            case self.director_search_tab:
                self.director_search_tab.update()