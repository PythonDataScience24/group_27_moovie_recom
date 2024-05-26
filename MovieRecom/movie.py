import datetime


class Person():
    """Class used to represents people"""
    def __init__(self, name:str='', portrait_url='', liked:bool=False):
        self.name = name
        self.liked = liked
        self.portrait_url = portrait_url
    def __str__(self) -> str:
        return self.name

class Genre():
    """Class used to represent movie genres"""
    def __init__(self, name:str='', liked:bool=False):
        self.name = name
        self.liked = liked
    def __str__(self) -> str:
        return self.name

class Movie():
    """Class used to represent movies"""
    def __init__(
            self,
            id:str='',
            title:str='',
            genre:list[Genre]=[],
            runtime: int = 0, # In minutes
            release_date:datetime.date=datetime.date.fromtimestamp(0),
            poster_url:str='',
            director:list[Person]=[],
            writer:list[Person]=[],
            actors:list[Person]=[],
            liked:bool=False
            ) -> None:

        self.id = id
        self.title = title
        self.genre = genre
        self.runtime = runtime
        self.release_date = release_date
        self.poster_url = poster_url
        self.director = director
        self.writer = writer
        self.actors = actors
        self.liked = liked

    # def from_omdb_dict(self, omdb_movie: dict):
    #     """Fills the object's fields with the given omdb dictionnary"""
        
    #     self.title = omdb_movie.get('Title', '')
    #     self.imdb_id = omdb_movie.get('imdbID', '')
    #     self.poster_url = omdb_movie.get('Poster', '')

    #     # Defaults to timestamp zero if release date cannot be figured out
    #     self.release_date = datetime.date.fromtimestamp(0)
    #     if omdb_movie.get('Released', '') and omdb_movie['Released'] != 'N/A':
    #         self.release_date = datetime.datetime.strptime(omdb_movie['Released'], "%d %b %Y")

    #     # Defaults to 0 minute if runtime cannot be figured out
    #     self.runtime = 0
    #     if omdb_movie.get('Runtime', '') and omdb_movie['Runtime'] != 'N/A':
    #         self.runtime = omdb_movie['Runtime'].split()[0] if omdb_movie.get('Runtime', '') else 0

    #     self.genre = [Genre(name=genre.strip()) for genre in omdb_movie.get('Genre', '').split(',')]
    #     self.director = [Person(name=director.strip()) for director in omdb_movie.get('Director', '').split(',')]
    #     self.writer = [Person(name=writer.strip()) for writer in omdb_movie.get('Writer', '').split(',')]
    #     self.actors = [Person(name=actor.strip()) for actor in omdb_movie.get('Actors', '').split(',')]
    
    def to_dict(self) -> dict:
        """Returns the object in the form of a dictionnary."""
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'runtime': self.runtime,
            'release_date': self.release_date,
            'poster_url': self.poster_url,
            'director': self.director,
            'writer': self.writer,
            'actors': self.actors,
            'liked': self.liked
        }

