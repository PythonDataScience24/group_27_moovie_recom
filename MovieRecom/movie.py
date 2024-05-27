import datetime
from enum import Enum

# class syntax
class PersonRole(Enum):
    DIRECTOR = 0,
    WRITER = 1,
    ACTOR = 1


class Person():
    """Class used to represents people"""
    def __init__(self, name:str, role: PersonRole, portrait_url='', liked:bool=False):
        self.name = name
        self.role = role
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

