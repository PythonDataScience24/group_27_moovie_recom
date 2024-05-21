import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""     liked_movie_list columns:
                'imdb_id'
                'title'
                'genre'
                'runtime'
                'release_date'
                'poster_url'
                'director'
                'writer'
                'actors'
                'liked'
"""


def create_liked_visualizations(liked_movie_list: pd.DataFrame) -> plt.Figure:
    """Create visualizations for liked movies:
        - pie plot of genre
        - box plot of runtime
        - bar chart of director
    """

    # create genre pie chart data
    genre_df = liked_movie_list[['imdb_id', 'genre']].groupby('genre').count()

    # create director bar chart data
    director_df = liked_movie_list[['imdb_id', 'director']].groupby('director').count()

    fig, ax = plt.subplots(3, 1) # size not fixed yet

    ax[0, 0].set_title("favourite genres")
    ax[0, 0].pie(x=genre_df['imdb_id'], labels=genre_df.index)

    ax[1, 0].set_title("movie runtime")
    ax[1, 0].boxplot(x=liked_movie_list['runtime'])

    ax[2, 0].set_title("directors")
    plt.bar(x=director_df.index, height=director_df['imdb_id'])

    return fig


