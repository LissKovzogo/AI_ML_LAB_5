import pandas as pd
import argparse
import os
from datetime import datetime

FILE_NAME = "data.parquet"


def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_parquet(FILE_NAME)
    else:
        return pd.DataFrame(columns=["last_name", "first_name", "zodiac", "birth_date"])


def save_data(df):
    df.to_parquet(FILE_NAME, index=False)
    print("Data saved to data.parquet")


def add_person(df, last_name, first_name, zodiac, day, month, year):
    try:
        birth_date = datetime(year, month, day)
        new_row = pd.DataFrame([{
            "last_name": last_name,
            "first_name": first_name,
            "zodiac": zodiac,
            "birth_date": birth_date
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        print(f"Added: {last_name} {first_name}")
        return df
    except Exception as e:
        print(f"Error: Invalid date - {e}")
        return df


def find_by_lastname(df, last_name):
    result = df[df["last_name"].str.lower() == last_name.lower()]
    if len(result) == 0:
        print(f"Person with last name '{last_name}' not found")
    else:
        print("\nFound:")
        for _, row in result.iterrows():
            birth = row["birth_date"].strftime("%d.%m.%Y")
            print(f"  {row['last_name']} {row['first_name']}, {row['zodiac']}, {birth}")


def show_sorted(df):
    if len(df) == 0:
        print("No data")
        return
    df_sorted = df.sort_values("birth_date")
    print("\nSorted by birth date:")
    for _, row in df_sorted.iterrows():
        birth = row["birth_date"].strftime("%d.%m.%Y")
        print(f"  {row['last_name']} {row['first_name']} - {birth} ({row['zodiac']})")


def delete_column(df, column):
    if column in df.columns:
        df.drop(columns=[column], inplace=True)
        print(f"Column '{column}' deleted")
        print(f"Remaining columns: {list(df.columns)}")
    else:
        print(f"Column '{column}' not found")
    return df


def main():
    parser = argparse.ArgumentParser(description="Person database management")

    parser.add_argument("--add", nargs=6, metavar=("LAST_NAME", "FIRST_NAME", "ZODIAC", "DAY", "MONTH", "YEAR"),
                        help="Add a new person")
    parser.add_argument("--find", metavar="LAST_NAME", help="Find person by last name")
    parser.add_argument("--show", action="store_true", help="Show all persons sorted by birth date")
    parser.add_argument("--delcol", metavar="COLUMN_NAME", help="Delete a column (e.g., zodiac)")

    args = parser.parse_args()

    df = load_data()

    if args.add:
        last_name, first_name, zodiac, day, month, year = args.add
        df = add_person(df, last_name, first_name, zodiac, int(day), int(month), int(year))
        save_data(df)

    if args.find:
        find_by_lastname(df, args.find)

    if args.show:
        show_sorted(df)

    if args.delcol:
        df = delete_column(df, args.delcol)
        save_data(df)

    if not (args.add or args.find or args.show or args.delcol):
        parser.print_help()


if __name__ == "__main__":
    main()