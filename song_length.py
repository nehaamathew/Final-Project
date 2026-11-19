
"""
Neha Mathew and Esther Wong
CSE 163, Section AE
Summarizes song durations and plots mean song length by publication year.
"""

import pandas as pd
import matplotlib.pyplot as plt


def get_song_length_data(songs):
    """
    Print and return summary statistics of a 5 number summary and
    standard deviation for positive song lengths in seconds.
    """
    valid_data = songs.dropna(subset=["duration_seconds"]).copy()
    valid_data = valid_data.loc[valid_data["duration_seconds"] > 0]
    data_descript = valid_data["duration_seconds"].describe()
    number_summary = data_descript.loc[[
        "min", "25%", "50%", "75%", "max", "std"
    ]]
    return (number_summary)


def plot_yearly_song_length(songs):
    """
    Print mean song length by year and save a line plot.
    """
    valid_data = songs.dropna(subset=["year", "duration_seconds"])
    valid_data = valid_data.loc[valid_data["duration_seconds"] > 0]
    mean_length_by_year = valid_data.groupby("year")["duration_seconds"].mean()
    years = mean_length_by_year.index
    mean_song_lengths = mean_length_by_year.values

    plt.plot(years, mean_song_lengths)
    plt.title("Mean Song Length by Year")
    plt.xlabel("Publication year")
    plt.xticks(years, rotation=45)
    plt.ylabel("Song duration (seconds)")
    plt.savefig("mean_yearly_length.png", bbox_inches="tight")
    plt.close()


def main():
    songs = pd.read_csv("songs.csv")
    get_song_length_data(songs)
    plot_yearly_song_length(songs)


if __name__ == "__main__":
    main()
