import pandas as pd
import matplotlib.pyplot as plt

def main():
    songs = pd.read_csv("songs.csv")
    get_genre_data(songs)
    plot_genre_trends(songs)
    plot_popular_genre_trends(songs)

    
def get_genre_data(songs):
    valid_data = songs["genre"].dropna()
    select_genres = ["pop", "j-pop", "rock", "electropop", "edm", "jazz", "metal", "trance", "traditional japanese music style"]
    genre_count = {}

    for genre in select_genres:
        genre_count[genre] = 0

    for genre_tags in valid_data:
        song_genres = genre_tags.split("|")
        song_genres = [item.lower() for item in song_genres]

        for genre in song_genres:
            if genre in genre_count:
                genre_count[genre] += 1

    print(genre_count)


def plot_genre_trends(songs):
    valid_data = songs.dropna(subset=["year", "genre"])

    songs_by_year = valid_data.groupby("year")
    select_genres = ["pop", "j-pop", "rock", "electropop", "edm", "jazz", "metal", "trance", "traditional japanese music style"]
    yearly_genre_count = {}
  
    for year, year_data in songs_by_year:
        year_genre_count = {}
        for genre in select_genres:
            year_genre_count[genre] = 0
            for genre_tags in year_data["genre"]:
                song_genres = genre_tags.split("|")
                song_genres = [item.lower() for item in song_genres]
                for genre in song_genres:
                    if genre in year_genre_count:
                        year_genre_count[genre] += 1
        yearly_genre_count[year] = year_genre_count
    print(yearly_genre_count)

    years = sorted(yearly_genre_count)
    
    for genre in select_genres:
        counts = [yearly_genre_count[year][genre] for year in years]
        plt.plot(years, counts, label=genre)
    plt.title("Selected Genre Counts by Year")
    plt.xlabel("Publication year")
    plt.xticks(years, rotation=45)
    plt.ylabel("Number of songs with genre tag")
    plt.legend(title="Genre")
    plt.savefig("genre_trends.png", bbox_inches="tight")
    plt.close()

def plot_popular_genre_trends(songs):
    valid_data = songs.dropna(subset=["year", "genre", "popular"])
    valid_data = valid_data.loc[valid_data["popular"]==1]

    songs_by_year = valid_data.groupby("year")
    select_genres = ["pop", "j-pop", "rock", "electropop", "edm", "jazz", "metal", "trance", "traditional japanese music style"]
    yearly_genre_count = {}
  
    for year, year_data in songs_by_year:
        year_genre_count = {}
        for genre in select_genres:
            year_genre_count[genre] = 0
            for genre_tags in year_data["genre"]:
                song_genres = genre_tags.split("|")
                song_genres = [item.lower() for item in song_genres]
                for genre in song_genres:
                    if genre in year_genre_count:
                        year_genre_count[genre] += 1
        yearly_genre_count[year] = year_genre_count
    print(yearly_genre_count)

    years = sorted(yearly_genre_count)
    
    for genre in select_genres:
        counts = [yearly_genre_count[year][genre] for year in years]
        plt.plot(years, counts, label=genre)
    plt.title("Selected Genre Counts for Popular Songs by Year")
    plt.xlabel("Publication year")
    plt.xticks(years, rotation=45)
    plt.ylabel("Number of songs with genre tag")
    plt.legend(title="Genre")
    plt.savefig("pop_genre_trends.png", bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()