import pandas as pd


def main():
    songs = pd.read_csv("songs.csv")
    print(f"Number of rows: {len(songs)}")
    print(f"Number of col: {len(songs.columns)}")
    eval_missing_data(songs)


def eval_missing_data(data):
    total_rows = len(data)
    if total_rows == 0:
        return

    for column in data.columns:
        na_count = data[column].isna().sum()
        percent_missing = 100 * na_count / total_rows
        print(f"{column}: {na_count} missing ({percent_missing:.1f}%)")


if __name__ == "__main__":
    main()
