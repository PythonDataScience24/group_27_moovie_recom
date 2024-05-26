import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


PALETTE = palette = np.array([
    "#E85A46",
    "#EDF6F9",
    "#64B6AC",
    "#DBBBF5",
    "#FDCFF3",
    "#FFEAEE",
    "#d6fa35",
    "#f12d8a",
    "#ef5d2f",
    "#3574fa",
    "#EC6F3E",
    "#4F646F",
    "#535657",
    "#685044",
    "#783f8e",
    "#090C02",
    "#345511",
    "#7B817E"
])

"""     liked_movie_list columns:
                'id'
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
    genre_df = liked_movie_list[['id', 'genre']]
    split_genre_df = pd.DataFrame()
    for index, entry in genre_df.iterrows():
        for genre in entry['genre']:
            split_genre_df = pd.concat(
                [pd.DataFrame(data=[[entry['id'], str(genre)]], columns=genre_df.columns), split_genre_df],
                ignore_index=True)
    
    split_genre_df = split_genre_df.groupby(['genre']).count()

    return split_genre_df

def create_actor_data(liked_movie_list):
    actors_df = liked_movie_list[['id', 'actors']]
    split_actors_df = pd.DataFrame()
    for index, entry in actors_df.iterrows():
        for actor in entry['actors']:
            split_actors_df = pd.concat(
                [pd.DataFrame(data=[[entry['id'], str(actor)]], columns=actors_df.columns), split_actors_df],
                ignore_index=True)
    split_actors_df = split_actors_df.groupby(['actors']).count()

    return split_actors_df

def create_runtime_data(liked_movie_list):
    return liked_movie_list['runtime'].astype(int)

def plot(genre_df, actors_df, runtime_data):
    fig, ax = plt.subplots(3, 1)  # size not fixed yet
    plt.close()
    fig.tight_layout(h_pad=1.0)

    plot_genre_pie(fig, ax[0], genre_df)
    plot_violin_runtime(ax[1], runtime_data)
    plot_actors_bar(ax[2], actors_df)

    print("Visualization created!")

    return fig

def plot_genre_pie(fig, ax, genre_df):
    if len(genre_df) > len(palette):
        colors_to_plot = np.random.choice(PALETTE, size=len(genre_df))
    else:
        colors_to_plot = np.random.choice(PALETTE, size=len(genre_df), replace=False)

    explode = [0.05 for _ in range(len(genre_df))]

    ax.set_title("Favorite genres", color="#ddf0ff")
    # ax.pie(x=genre_df['id'], labels=genre_df.index)
    ax.pie(
        x=genre_df['id'],
        labels=genre_df.index,
        colors=colors_to_plot,
        startangle=60,
        explode=explode,
        textprops={'color': "#ddf0ff", "fontsize": 10},
        wedgeprops=dict(width=0.5),
    )
    centre_circle = plt.Circle((0, 0), 0.60, fc='#23262B')
    plt.gca().add_artist(centre_circle)

    fig.patch.set_facecolor('#23262B')

def plot_violin_runtime(ax, runtime_data):
    ax.set_title("Movie runtime", color="#ddf0ff")
    violinplot = ax.violinplot(dataset=runtime_data, vert=False, showmeans=True)
    ax.set_facecolor('#23262B')
    # ax[1].boxplot(x=liked_movie_list['runtime'].astype(int), vert=False, notch=True)
    # Make all the violin statistics marks red:

    for partname in ('cbars', 'cmins', 'cmaxes', 'cmeans'):
        vp = violinplot[partname]
        vp.set_edgecolor("#ddf0ff")
        vp.set_linewidth(1)


    for pc in violinplot['bodies']:
        pc.set_facecolor('#7B817E')


    ax.tick_params(color="#ddf0ff", labelcolor="#ddf0ff")
    for spine in ax.spines.values():
        spine.set_edgecolor("#23262B")

def plot_actors_bar(ax, actors_df):
    # colors_to_plot = np.random.choice(PALETTE, size=len(actors_df), replace=False)

    ax.set_title("Favorite actors", color="#ddf0ff")
    # ax.bar(x=actors_df.index, height=actors_df['id'], color=colors_to_plot)
    ax.bar(x=actors_df.index, height=actors_df['id'])

    ax.set_facecolor('#23262B')
    ax.tick_params(color="#ddf0ff", labelcolor="#ddf0ff")
    ax.tick_params(axis='x', labelrotation=-45)
    for spine in ax.spines.values():
        spine.set_edgecolor("#23262B")

