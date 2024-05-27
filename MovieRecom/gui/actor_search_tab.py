
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from recommendation_system import RecommendationSystem
from gui.movie_list import MovieList
from gui.searchbar import PersonSearchBar
from gui.person_list import PersonList
from gui.movie_list_element import MovieListElement
from gui.person_list_element import PersonListElement

from movie import PersonRole


class ActorSearchTab(TabbedPanelItem):
    """Class used to display a search tab."""

    def __init__(self, recsys:RecommendationSystem, **kwargs):
        super(ActorSearchTab, self).__init__(text="Actor search")

        self.recsys = recsys

        self.search_layout = BoxLayout(orientation='vertical')
        self.actor_list = PersonList()
        self.search_bar = PersonSearchBar(self.recsys, self.actor_list, PersonRole.ACTOR)
        self.list_scroll = ScrollView(size_hint_y=1)

        self.list_scroll.add_widget(self.actor_list)
        self.search_layout.add_widget(self.search_bar)
        self.search_layout.add_widget(self.list_scroll)
        self.add_widget(self.search_layout)


    def update(self):
        """Updates the search tab."""

        for actor_list_element in self.actor_list.children[:]:
            if isinstance(actor_list_element, PersonListElement):
                actor_list_element.update()


