"""
Neha Mathew and Esther Wong
CSE 163, Section AE
Prints EDA data for the variables relevant to our research
questions. Prints total genre counts, song length statistics,
and total vocal synth counts.
"""


import pandas as pd

from genre import get_genre_data
from song_length import get_song_length_data
from vocal_synth import total_counts


def main():
    """Read songs.csv and print each EDA result once."""
    songs = pd.read_csv("songs.csv")
    genre_counts = get_genre_data(songs)
    length_summary = get_song_length_data(songs)
    synth_counts = total_counts(songs)

    print("Genre counts:")
    for genre, count in genre_counts.items():
        print(f"{genre}: {count}")

    print("\nSong length statistics (seconds):")
    for statistic, value in length_summary.items():
        print(f"{statistic}: {value:.2f}")

    print("\nVocal synth counts:")
    for synth, count in synth_counts.items():
        print(f"{synth}: {int(count)}")


if __name__ == "__main__":
    main()
