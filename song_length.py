import pandas as pd


def main():
    songs = pd.read_csv("songs.csv")
    get_song_length_data(songs)
    plot_song_length(songs)
    evaluate_data(songs)
    #assert songs["song_id"].is_unique

def evaluate_data(data):
    assert data["song_id"].is_unique
    print("Number of songs collected: ", len(data))


def get_song_length_data(songs):
    valid_data = songs.dropna(subset=["duration_seconds"])
    valid_data = valid_data.loc[valid_data["duration_seconds"] > 0]
    #median_length = valid_data["duration_seconds"].median()
    #mean_length = valid_data["duration_seconds"].mean()
    #song_length_sd = valid_data["duration_seconds"].std()
    #print("median ", median_length)
    #print("mean ", mean_length)
    #print("sd ", song_length_sd)

    #tried collecting five number summary using .describe()
    summary = valid_data["duration_seconds"].describe()
    number_summary = summary.loc[["min","25%","50%", "75%", "max", "std"]]

    print(number_summary)

    

def plot_song_length(songs):
    valid_data = songs.dropna(subset=["year", "duration_seconds"])
    valid_data = valid_data.loc[valid_data["duration_seconds"] > 0]
    median_length_by_year = valid_data.groupby("year")["duration_seconds"].median()
    
    print("yearly median", median_length_by_year)
    

if __name__ == "__main__":
    main()