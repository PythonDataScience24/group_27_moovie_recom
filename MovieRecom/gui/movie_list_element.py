from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label

from movie import Movie, PersonRole
from recommendation_system import RecommendationSystem



class MovieListElement(GridLayout):
    """Element used to display information about a movie."""

    def __init__(self, movie:Movie, recsys:RecommendationSystem, **kwargs):
        super(MovieListElement, self).__init__(**kwargs)

        self.img_star_not_liked = "images/star-outline.png"
        self.img_star_liked = "images/star.png"

        self.star_1_img_path = self.img_star_not_liked
        self.star_2_img_path = self.img_star_not_liked
        self.star_3_img_path = self.img_star_not_liked
        self.star_4_img_path = self.img_star_not_liked
        self.star_5_img_path = self.img_star_not_liked

        # Movie object
        self.movie = movie

        # Recommendation system
        self.recsys = recsys

        # Layout
        self.cols = 2
        self.height = 200
        self.size_hint=(1, None)

    
        # Load poster image from URL
        self.poster_img = AsyncImage(
            source=self.movie.poster_url,
            size_hint=(None, 1),
            allow_stretch=False,
            keep_ratio=True
            )
        
        
        # Set movie title
        movie_title_string = "[b]{0}[/b] ({1})".format(self.movie.title, self.movie.release_date.year)
        self.title_label = Label(text=movie_title_string, color="black", markup=True)
        self.title_label.font_size = 40
        self.title_label.halign = 'left'
        
        self.star_1_img = Image(source=self.star_1_img_path,size_hint=(None, 1),width=50,height=50,allow_stretch=False,keep_ratio=True)
        self.star_2_img = Image(source=self.star_2_img_path,size_hint=(None, 1),width=50,height=50,allow_stretch=False,keep_ratio=True)
        self.star_3_img = Image(source=self.star_3_img_path,size_hint=(None, 1),width=50,height=50,allow_stretch=False,keep_ratio=True)
        self.star_4_img = Image(source=self.star_4_img_path,size_hint=(None, 1),width=50,height=50,allow_stretch=False,keep_ratio=True)
        self.star_5_img = Image(source=self.star_5_img_path,size_hint=(None, 1),width=50,height=50,allow_stretch=False,keep_ratio=True)

        self.bind(on_touch_down=self.on_star_click)


        # Set "liked" icon
        self.update_displayed_rating()

        # Set tags area
        genre_list = [genre.name for genre in self.movie.genre]
        self.tag_label = Label(text="[b]Tags:[/b] {0}".format(', '.join(genre_list)), color="black", markup=True)
        self.tag_label.halign = 'left'

        # Set director area
        director_list = [director.name for director in self.movie.director]
        self.director_label = Label(text="[b]Directed by:[/b] {0}".format(', '.join(director_list)), color="black", markup=True)
        self.director_label.halign = 'left'

        # Set actor area
        actor_list = [actor.name for actor in self.movie.actors[:5]]
        self.actor_label = Label(text="[b]Featuring:[/b] {0}".format(', '.join(actor_list)), color="black", markup=True)
        self.actor_label.halign = 'left'
        
        # Set misc area
        self.misc_layout = GridLayout(rows=1)
        self.misc_layout.add_widget(Label(text="[b]Runtime:[/b] {0} min".format(self.movie.runtime), color="black", markup=True))
        # self.misc_layout.add_widget(Label(text="Country: ", color="black"))


        # Layouts
        self.body_layout = GridLayout(rows=2)
        self.title_layout = GridLayout(cols=7)
        self.detail_layout = GridLayout(cols=4)


        # Title layout
        self.title_layout.add_widget(self.title_label)
        self.title_layout.add_widget(self.star_1_img)
        self.title_layout.add_widget(self.star_2_img)
        self.title_layout.add_widget(self.star_3_img)
        self.title_layout.add_widget(self.star_4_img)
        self.title_layout.add_widget(self.star_5_img)

        # Detail layout
        self.detail_layout.add_widget(self.tag_label)
        self.detail_layout.add_widget(self.director_label)
        self.detail_layout.add_widget(self.actor_label)
        self.detail_layout.add_widget(self.misc_layout)

        # Body layout
        self.body_layout.add_widget(self.title_layout)
        self.body_layout.add_widget(self.detail_layout)
        self.body_layout.padding = [10,0,0,0]
        

        # Add to layout
        self.add_widget(self.poster_img)
        self.add_widget(self.body_layout)
        self.padding =[10,10,10,10]

    def update_displayed_rating(self):

        self.star_1_img_path = self.img_star_not_liked
        self.star_2_img_path = self.img_star_not_liked
        self.star_3_img_path = self.img_star_not_liked
        self.star_4_img_path = self.img_star_not_liked
        self.star_5_img_path = self.img_star_not_liked

        # TODO: Optimize
        if self.movie.rating > 0:
            self.star_1_img_path = self.img_star_liked
        if self.movie.rating > 1:
            self.star_2_img_path = self.img_star_liked
        if self.movie.rating > 2:
            self.star_3_img_path = self.img_star_liked
        if self.movie.rating > 3:
            self.star_4_img_path = self.img_star_liked
        if self.movie.rating > 4:
            self.star_5_img_path = self.img_star_liked

        self.star_1_img.source = self.star_1_img_path
        self.star_2_img.source = self.star_2_img_path
        self.star_3_img.source = self.star_3_img_path
        self.star_4_img.source = self.star_4_img_path
        self.star_5_img.source = self.star_5_img_path



    def on_star_click(self, instance, touch):
        """Toggle liked on heart click."""

        
        if not self.collide_point(*touch.pos):
            return
        
        star_clicked = 0

        if self.star_1_img.collide_point(*touch.pos):
            star_clicked = 1
        if self.star_2_img.collide_point(*touch.pos):
            star_clicked = 2
        if self.star_3_img.collide_point(*touch.pos):
            star_clicked = 3
        if self.star_4_img.collide_point(*touch.pos):
            star_clicked = 4
        if self.star_5_img.collide_point(*touch.pos):
            star_clicked = 5

        if star_clicked == 0:
            # We did not click on a star
            return
        
        if self.movie.rating == star_clicked:
            self.movie.rating = star_clicked-1
        else:
            self.movie.rating = star_clicked
        self.movie.liked = self.movie.rating > 0

        self.recsys.set_liked_movie(self.movie, self.movie.liked, self.movie.rating)
        self.update_displayed_rating()
    

    def update(self):
        (liked, rating) = self.recsys.is_movie_liked(self.movie)
        self.movie.liked = liked
        self.movie.rating = rating

        self.movie.genre = self.recsys.init_genres_liked(self.movie.genre)
        self.movie.director = self.recsys.init_person_liked(self.movie.director, PersonRole.DIRECTOR)
        self.movie.writer = self.recsys.init_person_liked(self.movie.writer, PersonRole.WRITER)
        self.movie.actors = self.recsys.init_person_liked(self.movie.actors, PersonRole.ACTOR)

        self.update_displayed_rating()