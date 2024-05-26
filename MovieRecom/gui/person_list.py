from kivy.uix.boxlayout import BoxLayout


class PersonList(BoxLayout):
    """Element used to display PersonListElements in a list."""
    def __init__(self, **kwargs):
        super(PersonList, self).__init__(**kwargs)
        self.orientation='vertical'
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
