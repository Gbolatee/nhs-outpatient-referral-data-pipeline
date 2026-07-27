from pathlib import Path

import pandas as pd


def extract_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Read a CSV file and return its contents as a pandas DataFrame.

    Args:
        file_path: Path to the source CSV file.

    Returns:
        A pandas DataFrame containing the source data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        PermissionError: If the file cannot be accessed.
        ValueError: If the CSV file contains no data.
    """

    try:
        dataframe = pd.read_csv(file_path)

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Source CSV file was not found: {file_path}"
        ) from error

    except PermissionError as error:
        raise PermissionError(
            f"Permission denied when accessing: {file_path}"
        ) from error

    except pd.errors.EmptyDataError as error:
        raise ValueError(
            f"Source CSV file is empty: {file_path}"
        ) from error

    if dataframe.empty:
        raise ValueError(
            f"Source CSV file contains no data rows: {file_path}"
        )

    return dataframe

if __name__ == "__main__":
    df = extract_csv("data/raw/outpatient_referrals_2023_24.csv")
    print(df.head())
    print(df.shape)
    print((df["Op Otherrefsmade Ga M"] != 0).sum())