import pandas as pd

def main():
    songs = pd.read_csv("songs.csv")
    get_genre_data(songs)
    #evaluate_data(songs)
    #assert songs["song_id"].is_unique

def get_genre_data(songs):
    valid_data = songs["genre"].dropna()
    genres = ["pop", "j-pop", "rock", "electropop", "technopop", "edm", "jazz", "metal", "trance", "traditional japanese music style"]
    genre_count = {}

    for genre in genres:
        genre_count[genre] = 0

    for genre_tags in valid_data:
        genres = genre_tags.split("|")
        genres = [item.lower() for item in genres]

        for genre in genres:
            if genre in genre_count:
                genre_count[genre] += 1

    print(genre_count)


if __name__ == "__main__":
    main()