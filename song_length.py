import pandas as pd
import matplotlib.pyplot as plt

def main():
    songs = pd.read_csv("songs.csv")
    get_song_length_data(songs)
    plot_song_length(songs)
    #evaluate_data(songs)
    #assert songs["song_id"].is_unique

def evaluate_data(data):
    assert data["song_id"].is_unique
    print("Number of songs collected: ", len(data))


def get_song_length_data(songs):
    valid_data = songs.dropna(subset=["duration_seconds"]).copy()
    valid_data = valid_data.loc[valid_data["duration_seconds"] > 0]
    #median_length = valid_data["duration_seconds"].median()
    #mean_length = valid_data["duration_seconds"].mean()
    #song_length_sd = valid_data["duration_seconds"].std()
    #print("median ", median_length)
    #print("mean ", mean_length)
    #print("sd ", song_length_sd)

    #tried collecting number summary using .describe()
    data_descript = valid_data["duration_seconds"].describe()
    number_summary = data_descript.loc[["min","25%","50%", "75%", "max", "std"]]
    print(number_summary)
    

def plot_song_length(songs):
    valid_data = songs.dropna(subset=["year", "duration_seconds"])
    valid_data = valid_data.loc[valid_data["duration_seconds"] > 0]
    mean_length_by_year = valid_data.groupby("year")["duration_seconds"].mean()
    print("Mean song length for each year:")
    print( mean_length_by_year)
    years = mean_length_by_year.index
    mean_song_lengths = mean_length_by_year.values

    plt.plot(years, mean_song_lengths)
    plt.title("Mean Song Length by Year")
    plt.xlabel("Publication year")
    plt.xticks(years, rotation=45)
    plt.ylabel("Song duration (seconds)")
    plt.savefig("mean_yearly_length.png", bbox_inches="tight")
    plt.close()
    

if __name__ == "__main__":
    main()