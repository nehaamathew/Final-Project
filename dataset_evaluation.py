"""
Neha Mathew and Esther Wong
CSE 163, Section AE
Prints the size of the song dataset and missing values in each column.
"""

import pandas as pd


def eval_missing_data(data):
    """Print the count and percentage of missing values in each column."""
    total_rows = len(data)
    if total_rows == 0:
        return

    for column in data.columns:
        na_count = data[column].isna().sum()
        percent_missing = 100 * na_count / total_rows
        print(f"{column}: {na_count} missing ({percent_missing:.1f}%)")


def main():
    songs = pd.read_csv("songs.csv")
    print(f"Number of rows: {len(songs)}")
    print(f"Number of col: {len(songs.columns)}")
    eval_missing_data(songs)


if __name__ == "__main__":
    main()
