from pandas import Series, DataFrame

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView


from recommendation_system import RecommendationSystem

from gui.person_list import PersonList
from gui.person_list_element import PersonListElement

from movie import PersonRole, Person




class LikedPersonTab(TabbedPanelItem):
    """Class used to display a search tab."""

    def __init__(self, recsys:RecommendationSystem, person_role:PersonRole, **kwargs):
        tab_name = ""
        match person_role:
            case PersonRole.ACTOR:
                tab_name = "Actor"
            case PersonRole.WRITER:
                tab_name = "Writer"
            case PersonRole.DIRECTOR:
                tab_name = "Director"
        
        super(LikedPersonTab, self).__init__(text=tab_name)

        self.recsys = recsys
        self.person_role = person_role

        self.liked_person_layout = BoxLayout(orientation='horizontal')

        self.person_list = PersonList()
        self.person_scroll = ScrollView()


        self.person_scroll.add_widget(self.person_list)
        self.liked_person_layout.add_widget(self.person_scroll)

        self.add_widget(self.liked_person_layout)


    def update(self):
        """Updates the liked tab."""
        # Clearing the person list
        self.person_list.clear_widgets()
        

        person_df: DataFrame[Person] = DataFrame()

        match self.person_role:
            case PersonRole.ACTOR:
                person_df =  self.recsys.liked_actors
            case PersonRole.WRITER:
                person_df = self.recsys.liked_writers
            case PersonRole.DIRECTOR:
                person_df = self.recsys.liked_directors
        
        for _, person_row in person_df.iterrows():
            person_obj = Person(
                id=person_row['id'],
                name=person_row['name'],
                role=self.person_role,
                portrait_url=person_row['portrait_url'],
                liked=True)

            self.person_list.add_widget(PersonListElement(person_obj, self.recsys))
