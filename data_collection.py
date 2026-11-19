"""
Neha Mathew and Esther Wong
CSE 163, Section AE
Collects highly rated songs from VocaDB and saves them to a CSV.
"""

import pandas as pd
import requests

START_COLLECTION = False

START_YEAR = 2007
END_YEAR = 2025
BATCHES_PER_YEAR = 3
BATCH_SIZE = 100
OUTPUT_FILE = "songs.csv"
API = "https://vocadb.net/api/"
# IDs corresponding to pools for
# YouTube >10M, YouTube >100M, Niconico >1M, Niconico >10M respectively
POPULAR_IDS = [6478, 10463, 30, 6477]
COLUMNS = ["song_id", "title", "year", "duration_seconds",
           "rating_score", "popular", "genre", "vocaloid"]


def get_data(url, parameters):
    """
    Requests data according to a dictionary of parameters and
    returns a dictionary.
    """
    response = requests.get(url, params=parameters, timeout=60)
    response.raise_for_status()
    return response.json()


def get_popular_ids():
    """
    Return the set of song IDs in the selected VocaDB popularity pools.
    """
    popular_ids = set()
    for id in POPULAR_IDS:
        parameters = {"songTypes": "Original", "maxResults": 1,
                      "getTotalCount": "true", "sort": "Name"}
        total = get_data(API + "songLists/" + str(id) +
                         "/songs", parameters)["totalCount"]
        popular_songs = set()
        for start in range(0, total, BATCH_SIZE):
            parameters = {"songTypes": "Original", "start": start,
                          "maxResults": BATCH_SIZE, "sort": "Name"}
            items = get_data(API + "songLists/" + str(id) +
                             "/songs", parameters)["items"]
            if len(items) != min(BATCH_SIZE, total - start):
                raise ValueError("Popularity pool page is incomplete.")
            for item in items:
                popular_songs.add(item["song"]["id"])
        if len(popular_songs) != total:
            raise ValueError("Popularity-pool pages changed during download.")
        popular_ids.update(popular_songs)
    print("Found ", len(popular_ids), " popular songs")
    return popular_ids


def make_row(song, year, popular_ids):
    """
    Return a CSV row for the song and year, using popular_ids to keep
    track of which songs are popular. 
    """
    genres = []
    for usage in song.get("tags", []) or []:
        tag = usage["tag"]
        # Checks if a tag is a genre tag and adds to list of genres
        if tag.get("categoryName") == "Genres":
            genres.append(tag["name"])
    vocaloids = []
    for credit in song.get("artists", []) or []:
        if ("Vocalist" in (credit.get("categories") or "")
                and not credit.get("isSupport", False)):
            artist = credit.get("artist") or {}
            name = artist.get("name") or credit.get("name")
            if name:
                vocaloids.append(name)
    return {"song_id": song["id"], "title": song.get("name"),
            "year": year,
            "duration_seconds": song.get("lengthSeconds") or None,
            "rating_score": song.get("ratingScore"),
            "popular": int(song["id"] in popular_ids),
            "genre": "|".join(sorted(set(genres))),
            "vocaloid": "|".join(sorted(set(vocaloids)))
            }


def main():
    """
    Collect the top score ranked songs in batches for each year
    and saves song data in a CSV.
    """
    if not START_COLLECTION:
        print("Set START_COLLECTION = True to run data collection")
        return
    popular_ids = get_popular_ids()
    rows = []
    seen_ids = set()
    # Collect data for each year
    for year in range(START_YEAR, END_YEAR + 1):
        # Filter for songs that are original, published within the year,
        # and collect in order of rating
        # Requests the artist and tags of each song
        # Limit amoount of results to the batch size
        filters = {"songTypes": "Original",
                   "lang": "English",
                   "afterDate": str(year) + "-01-01T00:00:00Z",
                   "beforeDate": str(year + 1) + "-01-01T00:00:00Z",
                   "sort": "RatingScore",
                   "fields": "Artists,Tags",
                   "maxResults": BATCH_SIZE}
        for batch in range(BATCHES_PER_YEAR):
            parameters = filters.copy()
            # Update start with which batch you are currently on
            # to avoid collecting the same data over
            parameters.update({"start": batch * BATCH_SIZE})
            # Request song data with the parameters
            # and stores songs as a list of dictionaries
            songs = get_data(API + "songs", parameters)["items"]
            for song in songs:
                if song["id"] not in seen_ids:
                    seen_ids.add(song["id"])
                    rows.append(make_row(song, year, batch, popular_ids))
            # If not enough songs in this batch, then quit
            # collecting songs from this year
            if len(songs) < BATCH_SIZE:
                break
        print("Finished", year)
        data = pd.DataFrame(rows, columns=COLUMNS)
        data.to_csv(OUTPUT_FILE, index=False)
        print("Saved", len(data), "unique songs to", OUTPUT_FILE)


if __name__ == "__main__":
    main()
