"""
Neha Mathew and Esther Wong
CSE 163, Section AE
Prints EDA data for the variables relevant to our research
questions.
Prints number of rows and columns in dataset.
Prints total genre counts, song length statistics,
and total vocal synth counts.
Also includes a method to print the percent of data missing from each column.
"""


import pandas as pd

from genre import get_genre_data
from song_length import get_song_length_data
from vocal_synth import total_counts


def main():
    """Read songs.csv and print each EDA result once."""
    songs = pd.read_csv("songs.csv")

    print(f"Number of rows: {len(songs)}")
    print(f"Number of col: {len(songs.columns)}")

    genre_counts = get_genre_data(songs)
    length_summary = get_song_length_data(songs)
    synth_counts = total_counts(songs)

    print("\nGenre counts:")
    for genre, count in genre_counts.items():
        print(f"{genre}: {count}")

    print("\nSong length statistics (seconds):")
    for statistic, value in length_summary.items():
        print(f"{statistic}: {value:.2f}")

    print("\nVocal synth counts:")
    for synth, count in synth_counts.items():
        print(f"{synth}: {int(count)}")

    print("\nMissing data per column:")
    eval_missing_data(songs)


def eval_missing_data(data):
    """Print the count and percentage of missing values in each column."""
    total_rows = len(data)
    if total_rows == 0:
        return

    for column in data.columns:
        na_count = data[column].isna().sum()
        percent_missing = 100 * na_count / total_rows
        print(f"{column}: {na_count} missing ({percent_missing:.1f}%)")


if __name__ == "__main__":
    main()
