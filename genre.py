"""
Neha Mathew and Esther Wong
CSE 163, Section AE
Counts selected genre tags and plots how the percentages of 
songs with those genres change over time for both general
song data and popular song data.
"""

import pandas as pd
import matplotlib.pyplot as plt

SELECT_GENRES = ["pop", "j-pop", "rock", "electropop", "edm",
                 "jazz", "metal",
                 "traditional japanese music style"]


def get_genre_data(songs):
    """
    Return a dictionary of selected genre tag counts in songs.
    """
    valid_data = songs["genre"].dropna()
    genre_count = {}

    for genre in SELECT_GENRES:
        genre_count[genre] = 0

    for genre_tags in valid_data:
        song_genres = genre_tags.split("|")
        song_genres = [item.lower() for item in song_genres]

        for genre in song_genres:
            if genre in genre_count:
                genre_count[genre] += 1

    print(genre_count)
    return genre_count


def plot_genre_counts(songs):
    """
    Plots a bar chart of selected genre tag counts in songs.
    """
    genre_counts = get_genre_data(songs)
    counts = pd.Series(genre_counts).sort_values()

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(counts.index, counts.values)
    ax.bar_label(bars, padding=3)
    ax.margins(x=0.12)

    ax.set_title("Frequency of Selected Genre Tags")
    ax.set_xlabel("Number of tag occurrences")
    ax.set_ylabel("Genre tag")

    fig.tight_layout()
    fig.savefig("genre_counts.png", bbox_inches="tight")
    plt.close(fig)


def plot_genre_trends(songs, title, filename):
    """
    Plots the yearly percentage of tagged songs with each selected genre.
    Use title for the plot and save it to filename.
    """
    valid_data = songs.dropna(subset=["song_id", "year", "genre"])
    yearly_genre_share = {}

    for year, year_data in valid_data.groupby("year"):
        genre_counts = {genre: 0 for genre in SELECT_GENRES}
        total_tagged_songs = 0

        # Each song gets one vote per genre even if it has duplicate rows
        for _, song_rows in year_data.groupby("song_id"):
            song_genres = set()
            for genre_tags in song_rows["genre"]:
                for tag in genre_tags.split("|"):
                    tag = tag.strip().lower()
                    if tag:
                        song_genres.add(tag)

            if song_genres:
                total_tagged_songs += 1
                for genre in song_genres:
                    if genre in genre_counts:
                        genre_counts[genre] += 1

        if total_tagged_songs > 0:
            yearly_genre_share[year] = {
                genre: 100 * count / total_tagged_songs
                for genre, count in genre_counts.items()
            }

    years = sorted(yearly_genre_share)
    fig, ax = plt.subplots(figsize=(10, 5))

    for genre in SELECT_GENRES:
        shares = [yearly_genre_share[year][genre] for year in years]
        ax.plot(years, shares, label=genre)

    ax.set_title(title)
    ax.set_xlabel("Publication year")
    ax.set_ylabel("Songs with genre tag (%)")
    ax.set_xticks(years[::2])
    ax.legend(title="Genre", loc="upper left", bbox_to_anchor=(1, 1))
    fig.savefig(filename, bbox_inches="tight")
    plt.close(fig)


def main():
    songs = pd.read_csv("songs.csv")
    popular_songs = songs.loc[songs["popular"] == 1]
    plot_genre_counts(songs)

    plot_genre_trends(
        songs,
        "Genre Share Among All Tagged Songs",
        "genre_trends.png",
    )
    plot_genre_trends(
        popular_songs,
        "Genre Share Among Popular Tagged Songs",
        "pop_genre_trends.png",
    )


if __name__ == "__main__":
    main()
