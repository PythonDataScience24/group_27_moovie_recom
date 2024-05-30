import unittest
from recommendation_system import RecommendationSystem
from movie import Movie

class RecsysTestingMethods(unittest.TestCase):

    def test_movie_liked(self):
        movie = Movie('0', 'Test Movie')
        self.assertFalse(movie.liked)

        # Making sure the default state of a movie is unliked.
        recsys = RecommendationSystem()
        (liked, rating) = recsys.is_movie_liked(movie)
        
        # Making sure the movie is not like in the fresh new recommendation system
        self.assertFalse(liked)
        # Making sure the movie has 
        self.assertEqual(rating, 0)

        # Adding movie to recommendation system
        recsys.set_liked_movie(movie, True, 5)
        (liked, rating) = recsys.is_movie_liked(movie)
        
        # Making sure the movie is not like in the fresh new recommendation system
        self.assertTrue(liked)
        # Making sure the movie has 
        self.assertEqual(rating, 5)


if __name__ == '__main__':
    unittest.main()