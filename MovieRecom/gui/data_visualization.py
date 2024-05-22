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
    genre_df = liked_movie_list[['imdb_id', 'genre']]
    split_genre_df = pd.DataFrame()
    for index, entry in genre_df.iterrows():
        for genre in entry['genre']:
            split_genre_df = pd.concat(
                [pd.DataFrame(data=[[entry['imdb_id'], str(genre)]], columns=genre_df.columns), split_genre_df], 
                ignore_index=True)
    split_genre_df = split_genre_df.groupby(['genre']).count()

    # create director bar chart data
    director_df = liked_movie_list[['imdb_id', 'director']]
    split_director_df = pd.DataFrame()
    for index, entry in director_df.iterrows():
        for director in entry['director']:
            split_director_df = pd.concat(
                [pd.DataFrame(data=[[entry['imdb_id'], str(director)]], columns=director_df.columns), split_director_df], 
                ignore_index=True)
    split_director_df = split_director_df.groupby(['director']).count()

    fig, ax = plt.subplots(3, 1) # size not fixed yet
    plt.close()
    fig.tight_layout(h_pad=1.0)

    ax[0].set_title("favourite genres")
    ax[0].pie(x=split_genre_df['imdb_id'], labels=split_genre_df.index)

    ax[1].set_title("movie runtime")
    print(liked_movie_list['runtime'])
    ax[1].violinplot(dataset=liked_movie_list['runtime'].astype(int), vert=False, showmeans=True)
    #ax[1].boxplot(x=liked_movie_list['runtime'].astype(int), vert=False, notch=True)

    ax[2].set_title("directors")
    ax[2].bar(x=split_director_df.index, height=split_director_df['imdb_id'])

    print("Visualization created!")

    return fig


