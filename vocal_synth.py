import pandas as pd
import matplotlib.pyplot as plt


VOCALOIDS = ["Kagamine Rin", "Kasane Teto", "GUMI"]

def get_vocaloid(vocaloid):
    for voca in VOCALOIDS:
        if vocaloid.lower().find(voca.lower()) != -1:
            return voca


def get_voca_count(songs):
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
    valid_data = songs[["year", "vocaloid"]].dropna()
    voca_count_year = valid_data.groupby("year").apply(get_voca_count)

    #print(voca_count_year)
    return voca_count_year


def total_counts(songs):
    counts = count_per_year(songs).reset_index()
    total = {}
    for vocaloid in VOCALOIDS:
        total[vocaloid] = counts[vocaloid].sum()

    print(total)
    return total

def share_per_year(songs):
    valid_data = songs[["year", "vocaloid"]].dropna()
    voca_share_year = valid_data.groupby("year").apply(get_voca_count)
    total_songs = valid_data.groupby("year").count()
    for vocaloid in VOCALOIDS:
        voca_share_year[vocaloid] = (100 * voca_share_year[vocaloid] 
                                    / total_songs["vocaloid"])

    print(voca_share_year)
    return voca_share_year


def plot_total_counts(songs):
    data = pd.Series(total_counts(songs))
    fig, ax = plt.subplots(1)

    data.plot(ax=ax, kind="bar", rot=0)
    plt.xlabel("Vocal Synthesizer")
    plt.ylabel("Total Number of Songs with Synthesizer")
    plt.title("Selected Vocal Synthesizers Total Count")
    plt.savefig("vocal_synth_counts.png", bbox_inches="tight")

def plot_count_per_year(songs):
    data = count_per_year(songs).reset_index()
    # data = data.set_index("year")
    fig, ax = plt.subplots(1)

    data.plot(ax=ax, x="year")
    plt.xlabel("Published Year")
    plt.ylabel("Songs with Synthesizer")
    plt.xticks(data["year"], rotation=45)
    plt.title("Selected Vocal Synthesizers Count by Year")


    plt.savefig("vocal_synth_trends.png", bbox_inches="tight")


def main():
    songs = pd.read_csv("songs.csv")
    total_counts(songs)
    plot_count_per_year(songs)
    plot_total_counts(songs)


if __name__ == "__main__":
    main()
