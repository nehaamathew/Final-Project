"""
Neha Mathew & Esther Wong
CSE 163 AE
This file analyses data and provides statistics from songs.csv,
particularly for the vocal synthesizers found in the dataset.
"""
import pandas as pd
import matplotlib.pyplot as plt


VOCALOIDS = ["Kagamine Rin", "Kasane Teto", "GUMI"]


def get_vocaloid(vocaloid):
    """
    For a given vocal synthesizer, determines if it matches any
    vocal synthesizer in the selected list. If it matches,
    it returns the a string for the general name for the vocal synthesizer.
    """
    for voca in VOCALOIDS:
        if vocaloid.lower().find(voca.lower()) != -1:
            return voca


def get_voca_count(songs):
    """
    For a given dataset, returns a pandas series containing the count
    of selected vocal synthesizers in a song.
    """
    valid_data = songs["vocaloid"].dropna()
    vocaloid_count = {}

    for vocaloid in VOCALOIDS:
        vocaloid_count[vocaloid] = 0

    for vocal_synths_song in valid_data:
        vocal_synth = vocal_synths_song.split("|")
        vocal_synth = [item.lower() for item in vocal_synth]
        specific_voca = set()

        for vocaloid in vocal_synth:
            specific_voca.add(get_vocaloid(vocaloid))

        for voca in specific_voca:
            if voca in vocaloid_count:
                vocaloid_count[voca] += 1
    return pd.Series(vocaloid_count)


def count_per_year(songs):
    """
    For a given dataset, returns a pandas dataframe of the counts
    of selected vocal synthesizers for each year.
    """
    valid_data = songs[["year", "vocaloid"]].dropna()
    voca_count_year = valid_data.groupby("year").apply(get_voca_count)

    return voca_count_year


def total_counts(songs):
    """
    For a given dataset, finds and returns a dictionary of the total counts of
    selected vocal synthesizers.
    """
    counts = count_per_year(songs).reset_index()
    total = {}
    for vocaloid in VOCALOIDS:
        total[vocaloid] = counts[vocaloid].sum()

    return total


def share_per_year(songs):
    """
    For a given dataset, returns a pandas dataframe of the share
    of selected vocal synthesizers for each year.
    """
    valid_data = songs[["year", "vocaloid"]].dropna()
    voca_share_year = valid_data.groupby("year").apply(get_voca_count)
    total_songs = valid_data.groupby("year").count()
    for vocaloid in VOCALOIDS:
        voca_share_year[vocaloid] = (100 * voca_share_year[vocaloid]
                                     / total_songs["vocaloid"])

    return voca_share_year


def plot_total_counts(songs):
    """
    Plots a graph for the total counts of selected vocal synthesizers.
    """
    data = pd.Series(total_counts(songs))
    fig, ax = plt.subplots(1)

    data.plot(ax=ax, kind="bar", rot=0)
    plt.xlabel("Vocal Synthesizer")
    plt.ylabel("Total Number of Songs with Synthesizer")
    plt.title("Selected Vocal Synthesizers Total Count")

    plt.savefig("vocal_synth_counts.png", bbox_inches="tight")
    plt.close(fig)


def plot_count_per_year(songs):
    """
    Plots a graph for the counts per year for selected vocal synthesizers.
    """
    data = count_per_year(songs).reset_index()
    fig, ax = plt.subplots(1)

    data.plot(ax=ax, x="year")
    plt.xlabel("Published Year")
    plt.ylabel("Songs with Synthesizer")
    plt.xticks(data["year"], rotation=45)
    plt.title("Selected Vocal Synthesizers Count by Year")

    plt.savefig("vocal_synth_count_year.png", bbox_inches="tight")
    plt.close(fig)


def plot_share_per_year(songs):
    """
    Plots a graph for the share per year for selected vocal synthesizers.
    """
    data = share_per_year(songs).reset_index()
    fig, ax = plt.subplots(1)

    data.plot(ax=ax, x="year")
    plt.xlabel("Published Year")
    plt.ylabel("Songs with Synthesizer(%)")
    plt.xticks(data["year"], rotation=45)
    plt.title("Selected Vocal Synthesizers Share by Year")

    plt.savefig("vocal_synth_share_year.png", bbox_inches="tight")


def main():
    songs = pd.read_csv("songs.csv")
    print("Total number of songs featuring selected vocal synthesizers")
    print(pd.Series(total_counts(songs)))
    print()

    print("Total number of songs per year featuring selected vocal "
          "synthesizers")
    print(count_per_year(songs))
    print()

    print("Share of songs per year featuring selected vocal "
          "synthesizers")
    print(share_per_year(songs))
    print()

    plot_count_per_year(songs)
    plot_total_counts(songs)
    plot_share_per_year(songs)


if __name__ == "__main__":
    main()
