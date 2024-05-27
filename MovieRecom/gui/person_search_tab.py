
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


class PersonSearchTab(TabbedPanelItem):
    """Class used to display a search tab."""

    def __init__(self, recsys:RecommendationSystem, person_role:PersonRole, **kwargs):

        tab_name = ""
        match person_role:
            case PersonRole.ACTOR:
                tab_name = "Actor search"
            case PersonRole.WRITER:
                tab_name = "Writer search"
            case PersonRole.DIRECTOR:
                tab_name = "Director search"

        super(PersonSearchTab, self).__init__(text=tab_name)

        self.recsys = recsys

        self.person_role = person_role

        self.search_layout = BoxLayout(orientation='vertical')
        self.person_list = PersonList()
        self.search_bar = PersonSearchBar(self.recsys, self.person_list, self.person_role)
        self.list_scroll = ScrollView(size_hint_y=1)

        self.list_scroll.add_widget(self.person_list)
        self.search_layout.add_widget(self.search_bar)
        self.search_layout.add_widget(self.list_scroll)
        self.add_widget(self.search_layout)


    def update(self):
        """Updates the search tab."""

        for person_list_element in self.person_list.children[:]:
            if isinstance(person_list_element, PersonListElement):
                person_list_element.update()