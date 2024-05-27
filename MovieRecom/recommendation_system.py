from movie import Movie, Genre, Person, PersonRole
from pandas import Series, DataFrame
import pandas as pd
import pickle
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

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
                'liked',
                'rating'
            ])
        
        self.tmdbi = TMDBInterface()
        
        self.liked_genres: Series[str] = Series()
        self.liked_directors: Series[str] = Series()
        self.liked_writers: Series[str] = Series()
        self.liked_actors: Series[str] = Series()

        self.liked_visual_figure = None

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
        
        loaded_movies: list[Movie] = []

        for new_movie in self.tmdbi.search_movie(query):
            # We check in our recommendation system if some elements are already liked by the user.
            (liked, rating) = self.is_movie_liked(new_movie)
            new_movie.liked = liked
            new_movie.rating = rating
            new_movie.genre = self.init_genres_liked(new_movie.genre)
            new_movie.director = self.init_person_liked(new_movie.director, PersonRole.DIRECTOR)
            new_movie.writer = self.init_person_liked(new_movie.writer, PersonRole.WRITER)
            new_movie.actors = self.init_person_liked(new_movie.actors, PersonRole.ACTOR)
            loaded_movies.append(new_movie)
        
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
            new_person = self.init_person_liked([new_person], person_role)[0]
            
            loaded_persons.append(new_person)
        
        return loaded_persons


    def is_movie_liked(self, movie: Movie) -> tuple[bool, Series]:
        """Returns whether the provided movie was liked by the user along with its rating."""
        is_liked = movie.id in self.liked_movies['id'].values
        
        rating = 0
        if is_liked: # Rating is 0 if we are not liked
            rating = self.liked_movies[self.liked_movies['id'] == movie.id]['rating'].values[0]
        
        return (is_liked, rating)

        
    def is_genre_liked(self, genre: Genre) -> bool:
        """Returns whether a genre was liked by the user."""
        return genre.name in self.liked_genres.values

    
    def is_person_liked(self, person: Person, person_role:PersonRole) -> bool:
        """Returns whether a director was liked by the user."""
        match person_role:
            case PersonRole.ACTOR:
                return person.name in self.liked_actors.values
            case PersonRole.WRITER:
                return person.name in self.liked_writers.values
            case PersonRole.DIRECTOR:
                return person.name in self.liked_directors.values


    def init_genres_liked(self, genre_list: list[Genre]) -> list[Genre]:
        """Sets the 'liked' field of each genre in the list based on user preference."""
        for i in range(len(genre_list)):
            genre_list[i].liked = self.is_genre_liked(genre_list[i])
        return genre_list

    def init_person_liked(self, person_list: list[Person], person_role:PersonRole):
        """Sets the 'liked' field of each person in the list based on user preference."""
        for i in range(len(person_list)):
            person_list[i].liked = self.is_person_liked(person_list[i], person_role)
        return person_list
    
    def set_liked_movie(self, movie: Movie, liked:bool, rating:int):
        """Likes or unlikes a movie."""
        movie.liked = liked
        movie.rating = rating

        (current_liked, current_rating) = self.is_movie_liked(movie)

        if liked and not current_liked:
            # Add the movie to the recommendation system if it wasn't liked before
            print("Adding movie to recommendation system")
            df_movie = DataFrame([movie.to_dict()])
            self.liked_movies = pd.concat([self.liked_movies, df_movie], ignore_index=True)

        elif not liked and current_liked:
            # Removes the movie from the recommendation system if it was liked before, but is now disliked
            print("Removing movie from recommendation system")
            self.liked_movies = self.liked_movies.drop(self.liked_movies[self.liked_movies['id'] == movie.id].index)

        elif liked and current_liked:
            # Updates the rating of the movie
            print("Updating movie rating")
            df_movie = DataFrame([movie.to_dict()])
            self.liked_movies.loc[self.liked_movies['id'] == movie.id, 'liked'] = movie.liked
            self.liked_movies.loc[self.liked_movies['id'] == movie.id, 'rating'] = movie.rating
        else:
            print("ERROR!!")
            
        
        print(self.liked_movies)


    def set_liked_genre(self, genre: Genre, liked: bool):
        """Likes or unlikes a genre."""
        genre.liked = liked
        if liked:
            self.liked_genres.add(genre.name)
        else:
            self.liked_genres = self.liked_genres.drop(self.liked_genres[self.liked_genres == genre.name].index)
        print(self.liked_genres)

    def set_liked_person(self, person: Person, liked: bool, person_role:PersonRole):
        """Likes or unlikes a person."""
        person.liked = liked

        selected_liked_person_list: list[Person] = []

        match person_role:
            case PersonRole.ACTOR:
                selected_liked_person_list = self.liked_actors
            case PersonRole.WRITER:
                selected_liked_person_list = self.liked_writers
            case PersonRole.DIRECTOR:
                selected_liked_person_list = self.liked_directors

        if liked:
            selected_liked_person_list = pd.concat([selected_liked_person_list, Series([person.name])], ignore_index=True)
        else:
            selected_liked_person_list = selected_liked_person_list.drop(selected_liked_person_list[selected_liked_person_list == person.name].index)
        
        print(selected_liked_person_list)
        match person_role:
            case PersonRole.ACTOR:
                self.liked_actors = selected_liked_person_list
            case PersonRole.WRITER:
                self.liked_writers = selected_liked_person_list
            case PersonRole.DIRECTOR:
                self.liked_directors = selected_liked_person_list



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
