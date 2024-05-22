import pandas as pd
import matplotlib.pyplot as plt

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
        - bar chart of actors
    """

    genre_df = create_genre_data(liked_movie_list)
    actors_df = create_actor_data(liked_movie_list)
    runtime_data = create_runtime_data(liked_movie_list)

    fig = plot(genre_df, actors_df, runtime_data)

    return fig

def create_genre_data(liked_movie_list):
    # create genre pie chart data
    genre_df = liked_movie_list[['imdb_id', 'genre']]
    split_genre_df = pd.DataFrame()
    for index, entry in genre_df.iterrows():
        for genre in entry['genre']:
            split_genre_df = pd.concat(
                [pd.DataFrame(data=[[entry['imdb_id'], str(genre)]], columns=genre_df.columns), split_genre_df],
                ignore_index=True)
    split_genre_df = split_genre_df.groupby(['genre']).count()

    return split_genre_df

def create_actor_data(liked_movie_list):
    actors_df = liked_movie_list[['imdb_id', 'actors']]
    split_actors_df = pd.DataFrame()
    for index, entry in actors_df.iterrows():
        for actor in entry['actors']:
            split_actors_df = pd.concat(
                [pd.DataFrame(data=[[entry['imdb_id'], str(actor)]], columns=actors_df.columns), split_actors_df],
                ignore_index=True)
    split_actors_df = split_actors_df.groupby(['actors']).count()

    return split_actors_df

def create_runtime_data(liked_movie_list):
    return liked_movie_list['runtime'].astype(int)

def plot(genre_df, actors_df, runtime_data):
    fig, ax = plt.subplots(3, 1)  # size not fixed yet
    plt.close()
    fig.tight_layout(h_pad=1.0)

    ax[0].set_title("favorite genres")
    ax[0].pie(x=genre_df['imdb_id'], labels=genre_df.index)

    ax[1].set_title("movie runtime")
    ax[1].violinplot(dataset=runtime_data, vert=False, showmeans=True)
    # ax[1].boxplot(x=liked_movie_list['runtime'].astype(int), vert=False, notch=True)

    ax[2].set_title("favorite actors")
    ax[2].bar(x=actors_df.index, height=actors_df['imdb_id'])

    print("Visualization created!")

    return fig