from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label

from movie import Movie, Person, PersonRole
from recommendation_system import RecommendationSystem



class PersonListElement(GridLayout):
    """Element used to display information about a person."""

    def __init__(self, person:Person, recsys:RecommendationSystem, **kwargs):
        super(PersonListElement, self).__init__(**kwargs)

        # Person object
        self.person = person

        # Recommendation system
        self.recsys = recsys

        # Layout
        self.cols = 2
        self.height = 200
        self.size_hint=(1, None)

    
        # Load poster image from URL
        self.poster_img = AsyncImage(
            source=self.person.portrait_url,
            size_hint=(None, 1),
            allow_stretch=False,
            keep_ratio=True
            )
        
        
        # Set movie title
        person_title_string = "[b]{0}[/b]".format(self.person.name)
        self.title_label = Label(text=person_title_string, color="black", markup=True)
        self.title_label.font_size = 40
        self.title_label.padding = [10,0,0,0]

        # Set "liked" icon
        self.liked_img_path = 'images/heart-outline.png' if not self.person.liked else 'images/heart-off-outline.png'
        self.liked_img = Image(
            source=self.liked_img_path,
            size_hint=(None, 1),
            width=50,
            height=50,
            allow_stretch=False,
            keep_ratio=True
            )
        
        self.liked_img.bind(on_touch_down=self.on_heart_click)

        # Layouts
        self.body_layout = GridLayout(rows=2)
        self.title_layout = GridLayout(cols=2)

        # Title layout
        self.title_layout.add_widget(self.liked_img)
        self.title_layout.add_widget(self.title_label)

        # Body layout
        self.body_layout.add_widget(self.title_layout)
        

        # Add to layout
        self.add_widget(self.poster_img)
        self.add_widget(self.body_layout)

    def on_heart_click(self, instance, touch):
        """Toggle liked on heart click."""
        if self.liked_img.collide_point(*touch.pos):
            self.person.liked = not self.person.liked
            self.liked_img.source = 'images/heart-outline.png' if not self.person.liked else 'images/heart-off-outline.png'
            
            match self.person.role:
                case PersonRole.ACTOR:
                    self.recsys.set_liked_actor(self.person, self.person.liked)
                case PersonRole.DIRECTOR:
                    self.recsys.set_liked_director(self.person, self.person.liked)
                case PersonRole.WRITER:
                    self.recsys.set_liked_writer(self.person, self.person.liked)

        
    def update(self):
        match self.person.role:
            case PersonRole.ACTOR:
                self.person.liked = self.recsys.is_actor_liked(self.person)
            case PersonRole.DIRECTOR:
                self.person.liked = self.recsys.is_director_liked(self.person)
            case PersonRole.WRITER:
                self.person.liked = self.recsys.is_writer_liked(self.person)
        self.liked_img.source = 'images/heart-outline.png' if not self.person.liked else 'images/heart-off-outline.png'

