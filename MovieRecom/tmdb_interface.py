
import requests
import datetime

from movie import Movie, Genre, Person, PersonRole

class TMDBInterface:

    def __init__(self) -> None:
        # TODO Move those keys somewhere better (and safer)
        self.api_key = "d5a45f5c8a011d4b27da28e922f1cd57"
        self.api_read_access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkNWE0NWY1YzhhMDExZDRiMjdkYTI4ZTkyMmYxY2Q1NyIsInN1YiI6IjY2NTMxNGZkN2VjMzIzZjY4ZjkwNmMzMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0OrqRG85hpXhJT9YB4-X7QEcUAFh0DR82cvinjuT-a0"
        self.api_url = "https://api.themoviedb.org/3"
        self.img_url = "https://image.tmdb.org/t/p/w500"

    
    def __api_request__(self, get_request) -> any:
        """Base method used to make API requests to TMDB."""
        url = f"{self.api_url}{get_request}"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_read_access_token}"
        }

        return requests.get(url, headers=headers).json()
    

    def __get_movie_from_tmdb_json(self, json_movie_details: any):
        # Get genres
        genre_list: list[Genre] = []
        for json_genre in json_movie_details['genres']:
            genre_list.append(Genre(json_genre['name']))
        
        # Get release date
        release_date = datetime.date.fromtimestamp(0)
        if json_movie_details.get('release_date', ''):
            release_date = datetime.datetime.strptime(json_movie_details['release_date'], "%Y-%m-%d")
        
        # Get actors
        actor_list: list[Person] = []
        for json_actor in json_movie_details['credits']['cast'][:5]:
            actor_list.append(Person(json_actor['name'], PersonRole.ACTOR))
        
        # Get director and writers
        director_list: list[Person] = []
        writer_list: list[Person] = []
        for json_crew in json_movie_details['credits']['crew']:
            if json_crew['job'] == "Director":
                director_list.append(Person(json_crew['name'], PersonRole.DIRECTOR))
            if json_crew['department'] == "Writing":
                writer_list.append(Person(json_crew['name'], PersonRole.WRITER))

        poster_url = ""
        if json_movie_details['poster_path']:
            poster_url = f'{self.img_url}{json_movie_details['poster_path']}'

        return Movie(
            json_movie_details['imdb_id'],
            json_movie_details['original_title'],
            genre_list,
            json_movie_details['runtime'],
            release_date,
            poster_url,
            director_list,
            writer_list,
            actor_list,
            False
        )
    

    def get_movie_from_imdb_id(self, imdb_id:str) -> Movie:
        """Returns a Movie object for a given imdb_id."""

        get_request = f"/find/{imdb_id}?external_source=imdb_id"

        json_movie = self.__api_request__(get_request)["movie_results"][0] # TODO Handle case when we have no results

        get_request_details = f"/movie/{json_movie['id']}?&append_to_response=credits"
        json_movie_details = self.__api_request__(get_request_details)
        
        return self.__get_movie_from_tmdb_json(json_movie_details)

    
    

    def search_movie(self, query:str) -> list[Movie]:
        """Returns a list of Movie objects given a certain search query."""
        get_request = f"/search/movie?query={query}&include_adult=false"
        json_movie_list = self.__api_request__(get_request)['results']
        movie_list:list[Movie] = []

        for json_movie in json_movie_list:
            get_request_details = f"/movie/{json_movie['id']}?&append_to_response=credits"
            json_movie_details = self.__api_request__(get_request_details)

            movie_list.append(self.__get_movie_from_tmdb_json(json_movie_details))
        
        return movie_list
        

    def search_person(self, query:str, personRole:PersonRole)->list[Person]:
        """Returns a list of director Person objects given a certain search query."""

        get_request = f"/search/person?query={query}"
        json_person_list = self.__api_request__(get_request)['results']

        person_list: list[Person] = []

        for json_person in json_person_list:
            
            hasRole = False
            match personRole:
                case PersonRole.ACTOR:
                    hasRole = json_person['known_for_department'] == "Acting"
                case PersonRole.WRITER:
                    hasRole = json_person['known_for_department'] == "Writing"
                case PersonRole.DIRECTOR:
                    hasRole = json_person['known_for_department'] == "Directing"

            if hasRole:
                poster_url = ""
                if json_person['profile_path']:
                    poster_url = f'{self.img_url}{json_person['profile_path']}'
                person_list.append(Person(json_person['name'], personRole, poster_url))

        return person_list
