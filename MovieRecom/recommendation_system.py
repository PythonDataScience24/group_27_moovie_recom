from movie import Movie, Genre, Person, PersonRole
from pandas import Series, DataFrame
import pandas as pd
import requests
import pickle
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from kivy.app import App
from kivy.uix.label import Label

from gui.data_visualization import create_liked_visualizations

from tmdb_interface import TMDBInterface

class RecommendationSystem():
    """Class used to handle user preferences and API calls"""
    def __init__(self) -> None:
        self.liked_movies: DataFrame = DataFrame(
            columns=[
                'id',
                'title',
                'genre',
                'runtime',
                'release_date',
                'poster_url',
                'director',
                'writer',
                'actors',
                'liked'
            ])
        
        self.tmdbi = TMDBInterface()
        
        self.liked_genres: Series[str] = Series()
        self.liked_directors: Series[str] = Series()
        self.liked_writers: Series[str] = Series()
        self.liked_actors: Series[str] = Series()

        self.liked_visual_figure = None

        # Contains all the movies loaded from the latest API call
        # self.loaded_movies: list[Movie] = []

        # CountVectorizer
        with open('./data/finalized_model.pkl', 'rb') as f:
            self.vectorizer = pickle.load(f)

        # Already vectorized all the movies in dataset of recommendations
        self.vectorized_dataset = sparse.load_npz('./data/vectorized_dataset.npz')

        # Dataset with all data about movie for recommendations
        self.df_full = pd.read_csv("./data/finalized_dataset.csv")
        print(self.df_full)


    def update_liked_visualizations(self) -> None:
        """Update the saved visualization figure to represent current liked movies"""
        self.liked_visual_figure = create_liked_visualizations(self.liked_movies)


    def get_liked_visualization(self):
        """Return the saved pyplot figure with liked movie visualizations"""
        return self.liked_visual_figure


    def movie_query(self, query: str) -> list[Movie]:
        """Makes an API call from a user's query and returns a list of Movie objects."""
        if not query:
            return []
        
        # Clear previous search results
        # self.loaded_movies.clear()
        loaded_movies: list[Movie] = []

        for new_movie in self.tmdbi.search_movie(query):
            # We check in our recommendation system if some elements are already liked by the user.
            new_movie.liked = self.is_movie_liked(new_movie)
            new_movie.genre = self.init_genres_liked(new_movie.genre)
            new_movie.director = self.init_directors_liked(new_movie.director)
            new_movie.writer = self.init_writers_liked(new_movie.writer)
            new_movie.actors = self.init_actors_liked(new_movie.actors)
            # self.loaded_movies.append(new_movie)
            loaded_movies.append(new_movie)
        
        # return self.loaded_movies
        return loaded_movies
    
    def person_query(self, query: str, person_role: PersonRole) -> list[Person]:
        """Makes an API call from a user's query and returns a list of Person objects."""
        if not query:
            return []
        
        # Clear previous search results
        loaded_persons: list[Person] = []
        new_person_list: list[Person] = []
        
        new_person_list = self.tmdbi.search_person(query, person_role)

        for new_person in new_person_list:
            
            # We check in our recommendation system if some elements are already liked by the user.
            match person_role:
                case PersonRole.ACTOR:
                    new_person = self.init_actors_liked([new_person])[0]
                    
                case PersonRole.WRITER:
                    new_person = self.init_writers_liked([new_person])[0]
                case PersonRole.DIRECTOR:
                    new_person = self.init_directors_liked([new_person])[0]
            
            loaded_persons.append(new_person)
        
        # return self.loaded_movies
        return loaded_persons


    def is_movie_liked(self, movie: Movie) -> bool:
        """Returns whether the provided movie was liked by the user."""
        return movie.id in self.liked_movies['id'].values


    def is_genre_liked(self, genre: Genre) -> bool:
        """Returns whether a genre was liked by the user."""
        return genre.name in self.liked_genres.values


    def is_director_liked(self, director: Person) -> bool:
        """Returns whether a director was liked by the user."""
        return director.name in self.liked_directors.values


    def is_writer_liked(self, writer: Person) -> bool:
        """Returns whether a writer was liked by the user."""
        return writer.name in self.liked_writers.values


    def is_actor_liked(self, actor: Person) -> bool:
        """Returns whether an actor was liked by the user."""
        return actor.name in self.liked_actors.values


    def init_genres_liked(self, genre_list: list[Genre]) -> list[Genre]:
        """Sets the 'liked' field of each genre in the list based on user preference."""
        for i in range(len(genre_list)):
            genre_list[i].liked = self.is_genre_liked(genre_list[i])
        return genre_list


    def init_directors_liked(self, director_list: list[Person]) -> list[Person]:
        """Sets the 'liked' field of each director in the list based on user preference."""
        for i in range(len(director_list)):
            director_list[i].liked = self.is_director_liked(director_list[i])
        return director_list


    def init_writers_liked(self, writer_list: list[Person]) -> list[Person]:
        """Sets the 'liked' field of each writer in the list based on user preference."""
        for i in range(len(writer_list)):
            writer_list[i].liked = self.is_writer_liked(writer_list[i])
        return writer_list


    def init_actors_liked(self, actor_list: list[Person]) -> list[Person]:
        """Sets the 'liked' field of each actor in the list based on user preference."""
        for i in range(len(actor_list)):
            actor_list[i].liked = self.is_actor_liked(actor_list[i])
        return actor_list


    def set_liked_movie(self, movie: Movie, liked: bool):
        """Likes or unlikes a movie."""
        movie.liked = liked
        if liked:
            df_movie = DataFrame([movie.to_dict()])
            self.liked_movies = pd.concat([self.liked_movies, df_movie], ignore_index=True)
        else:
            self.liked_movies = self.liked_movies.drop(self.liked_movies[self.liked_movies['id'] == movie.id].index)
        print(self.liked_movies)


    def set_liked_genre(self, genre: Genre, liked: bool):
        """Likes or unlikes a genre."""
        genre.liked = liked
        if liked:
            self.liked_genres.add(genre.name)
        else:
            self.liked_genres = self.liked_genres.drop(self.liked_genres[self.liked_genres == genre.name].index)
        print(self.liked_genres)

    def set_liked_director(self, director: Person, liked: bool):
        """Likes or unlikes a director."""
        director.liked = liked
        if liked:
            self.liked_directors = pd.concat([self.liked_directors, Series([director.name])], ignore_index=True)
            # self.liked_directors.append(director.name)
        else:
            self.liked_directors = self.liked_directors.drop(self.liked_directors[self.liked_directors == director.name].index)
        print(self.liked_directors)

    def set_liked_writer(self, writer: Person, liked: bool):
        """Likes or unlikes a writer."""
        writer.liked = liked
        if liked:
            self.liked_writers = pd.concat([self.liked_writers, Series([writer.name])], ignore_index=True)
            # self.liked_writers.append(writer.name)
        else:
            self.liked_writers = self.liked_writers.drop(self.liked_writers[self.liked_writers == writer.name].index)
        print(self.liked_writers)

    def set_liked_actor(self, actor: Person, liked: bool):
        """Likes or unlikes an actor."""
        actor.liked = liked
        if liked:
            self.liked_actors = pd.concat([self.liked_actors, Series([actor.name])], ignore_index=True)
            # self.liked_actors.append(actor.name)
        else:
            self.liked_actors = self.liked_actors.drop(self.liked_actors[self.liked_actors == actor.name].index)
        print(self.liked_actors)

    def update_liked_movies_ui(self, movie: Movie, add: bool):
        """Updates the UI to reflect changes in the liked movies list."""
        print("Attempting to update UI...")
        try:
            from gui.movie_list_element import MovieListElement  # Local import to avoid circular dependency
            app = App.get_running_app()
            print("App instance:", app)
            root_widget = app.root
            print("Root widget:", root_widget)
            print("Root ids available:", root_widget.ids)

            if 'liked_movies_list' in root_widget.ids:
                movie_list_widget = root_widget.ids.liked_movies_list
                print("Movie list widget found:", movie_list_widget)

                if add:
                    movie_element = MovieListElement(movie, self)
                    movie_list_widget.add_widget(movie_element)
                    print(f"Added movie to liked list: {movie.title}")
                else:
                    for child in movie_list_widget.children[:]:
                        if isinstance(child, Label) and child.text == movie.title:
                            movie_list_widget.remove_widget(child)
                            print(f"Removed movie from liked list: {movie.title}")
                            break
            else:
                print("liked_movies_list id not found")

        except Exception as e:
            print(f"Error during UI update: {e}")


    def generate_recommendations(self) -> DataFrame:
        """Generates movie recommendations based on liked movies."""

        if self.liked_movies.empty:
            # Return empty liked movie list if we don't have any to display.
            return DataFrame(columns=[
                'id',
                'title',
                'genre',
                'runtime',
                'release_date',
                'poster_url',
                'director',
                'writer',
                'actors',
                'liked'
            ])
        

        df_liked_movies = self.df_full[self.df_full['tconst'].isin(self.liked_movies["id"])]
        user_movie_idx = df_liked_movies.index
        movies_soup = df_liked_movies['soup']
        count_user_matrix = self.vectorizer.transform(movies_soup)
        count_user_vec = count_user_matrix.sum(axis=0) / count_user_matrix.sum(axis=0).max()
        
        


        similarity = cosine_similarity(sparse.csr_matrix(count_user_vec), self.vectorized_dataset)[0]
        scores = similarity * self.df_full['weightedAverage']

        similar_scores = list(enumerate(scores))
        similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)

        recommend_movie_indices = [idx for idx, score in similar_scores if idx not in user_movie_idx][:10]
        
        return self.df_full.iloc[recommend_movie_indices]
