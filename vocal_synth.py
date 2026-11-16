import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

VOCALOIDS = ["Kagamine Rin", "Kasane Teto", "GUMI"]

def get_voca_count(songs):
    valid_data = songs["vocaloid"].dropna()
    vocaloid_count = {}

    for vocaloid in VOCALOIDS:
        vocaloid_count[vocaloid] = 0

    for vocal_synths in valid_data:
        vocal_synth = vocal_synths.split("|")
        vocal_synth = [item.lower() for item in vocal_synth]
        
        for vocaloid in vocal_synth:
            for voca in VOCALOIDS:
                if vocaloid.lower().find(voca.lower()) != -1:
                    vocaloid_count[voca] += 1
    return pd.Series(vocaloid_count)


def count_per_year(songs):
    valid_data = songs[["year", "vocaloid"]].dropna()
    voca_count_year = valid_data.groupby("year").apply(get_voca_count)
    #voca_count_year["Number of Songs"] = valid_data.groupby("year").count()

    print(voca_count_year)
    return voca_count_year


def plot_count_per_year(songs):
    data = count_per_year(songs).reset_index()
    #data = data.set_index("year")
    fig, ax = plt.subplots(1)
    
    data.plot(ax=ax, x="year")
    plt.xlabel("Published Year")
    plt.ylabel("Number of songs with synthesizer")
    plt.xticks(data["year"], rotation=45)
    plt.title("Selected Vocal Synthesizers Count by Year")
    #sns.relplot(x="year", y="Kagamine Rin", data=data, kind="line")

    plt.savefig("vocal_synth_trends.png")


def main():
    songs = pd.read_csv("songs.csv")
    plot_count_per_year(songs)


if __name__ == "__main__":
    main()