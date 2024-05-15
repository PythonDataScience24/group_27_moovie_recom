from movie import Movie, Genre, Person
from pandas import Series, DataFrame
import pandas as pd
import requests

class RecommendationSystem():
    """Class used to handle user preferances and API calls"""
    def __init__(self) -> None:
        self.liked_movies: DataFrame = DataFrame(
            columns=[
                'imdb_id',
                'title',
                'genre',
                'runtime',
                'release_date',
                'poster_url',
                'director',
                'writer',
                'actors',
                'liked'])
        
        self.liked_genres: Series[str] = Series()
        self.liked_directors: Series[str] = Series()
        self.liked_writers: Series[str] = Series()
        self.liked_actors: Series[str] = Series()

        # Contains all the movies loaded from the latest API call
        self.loaded_movies: list[Movie] = []


    def movie_query(self, query:str) -> list[Movie]:
        """Makes an API call from an user's query and return a list of Movie objects."""
        if not query:
            return

        # Make API request to OMDB
        api_key = '3ade98ca'  # Replace with your OMDB API key
        url = f'http://www.omdbapi.com/?apikey={api_key}&s={query}&type=movie'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            self.loaded_movies.clear()

            
            # Display search results in MovieList
            if 'Search' in data:
                for movie in data['Search']:
                    new_movie = Movie()
                    new_movie.from_omdb_dict(movie)
                    

                    url2 = f'http://www.omdbapi.com/?apikey={api_key}&i={new_movie.imdb_id}'
                    response2 = requests.get(url2)
                    if response2.status_code == 200:
                        data2 = response2.json()
                        new_movie.from_omdb_dict(data2)

                    new_movie.liked = self.is_movie_liked(new_movie)
                    new_movie.genre = self.init_genres_liked(new_movie.genre)
                    new_movie.director = self.init_directors_liked(new_movie.director)
                    new_movie.writer = self.init_writers_liked(new_movie.writer)
                    new_movie.actors = self.init_actors_liked(new_movie.actors)

                    self.loaded_movies.append(new_movie)
        else:
            print(f"Error: {response.status_code} - {response.text}")
        
        return self.loaded_movies


    def is_movie_liked(self, movie:Movie) -> bool:
        """Returns whether the provided movie was liked by the user (i.e. is stored in the "liked_movie" DataFrame)."""
        return movie.imdb_id in self.liked_movies['imdb_id'].values

    def is_genre_liked(self, genre:Genre) -> bool:
        """Returns whether a genre was liked by the user (i.e. is stored in the "liked_genres" Series)."""
        return genre.name in self.liked_genres.values

    def is_director_liked(self, director:Person) -> bool:
        """Returns whether a director was liked by the user (i.e. is stored in the "liked_directors" Series)."""
        return director.name in self.liked_directors.values
    
    
    def is_writer_liked(self, writer:Person) -> bool:
        """Returns whether a writer was liked by the user (i.e. is stored in the "liked_writers" Series)."""
        return writer.name in self.liked_writers.values
    
    
    def is_actor_liked(self, actor:Person) -> bool:
        """Returns whether a actor was liked by the user (i.e. is stored in the "liked_actors" Series)."""
        return actor.name in self.liked_actors.values
    

    def init_genres_liked(self, genre_list:list[Genre]) -> list[Genre]:
        """Sets the "liked" field of each genre in the list to true or false depending on if they were liked by the user."""
        for i in range(len(genre_list)):
            genre_list[i].liked = self.is_genre_liked(genre_list[i])
        return genre_list
        
    
    def init_directors_liked(self, director_list:list[Person]) -> list[Person]:
        """Sets the "liked" field of each director in the list to true or false depending on if they were liked by the user."""
        for i in range(len(director_list)):
            director_list[i].liked = self.is_director_liked(director_list[i])
        return director_list
        
    
    
    def init_writers_liked(self, writer_list:list[Person]) -> list[Person]:
        """Sets the "liked" field of each writer in the list to true or false depending on if they were liked by the user."""
        for i in range(len(writer_list)):
            writer_list[i].liked = self.is_writer_liked(writer_list[i])
        return writer_list

    
    def init_actors_liked(self, actor_list:list[Person]) -> list[Person]:
        """Sets the "liked" field of each actor in the list to true or false depending on if they were liked by the user."""
        for i in range(len(actor_list)):
            actor_list[i].liked = self.is_actor_liked(actor_list[i])
        return actor_list


    def set_liked_movie(self, movie:Movie, liked:bool):
        """Likes or unlikes a movie."""
        movie.liked = liked
        if liked:
            df_movie  = DataFrame([movie.to_dict()])
            self.liked_movies = pd.concat(
                [self.liked_movies, df_movie],
                ignore_index=True)
        else:
            self.liked_movies = self.liked_movies.drop(self.liked_movies[self.liked_movies['imdb_id'] == movie.imdb_id].index)
        print(self.liked_movies)

    def set_liked_genre(self, genre:Genre, liked:bool):
        """Likes or unlikes a genre."""
        genre.liked = liked
        if liked:
            self.liked_genres.add(genre.name)
        else:
            self.liked_genres = self.liked_genres.drop(self.liked_genres[self.liked_genres == genre.name].index)

    
    def set_liked_director(self, director:Person, liked:bool):
        """Likes or unlikes a director."""
        director.liked = liked
        if liked:
            self.liked_directors.add(director.name)
        else:
            self.liked_directors = self.liked_directors.drop(self.liked_directors[self.liked_directors == director.name].index)

    def set_liked_writer(self, writer:Person, liked:bool):
        """Likes or unlikes a writer."""
        writer.liked = liked
        if liked:
            self.liked_writers.add(writer.name)
        else:
            self.liked_writers = self.liked_writers.drop(self.liked_writers[self.liked_writers == writer.name].index)

        
    def set_liked_actor(self, actor:Person, liked:bool):
        """Likes or unlikes an actor."""
        actor.liked = liked
        if liked:
            self.liked_directors.add(actor.name)
        else:
            self.liked_actors = self.liked_actors.drop(self.liked_actors[self.liked_actors == actor.name].index)



