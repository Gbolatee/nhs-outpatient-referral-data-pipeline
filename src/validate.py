import pandas as pd


def validate_data(dataframe):
    required_columns = [
        "Periodname",
        "Provider Org code",
        "Provider Org name",
        "Commissioner Org Code",
        "Commissioner Org Name",
    ]

    missing_columns = []

    for column in required_columns:
        if column not in dataframe.columns:
            missing_columns.append(column)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if dataframe.empty:
        raise ValueError(
            "The extracted DataFrame contains no rows."
        )

    required_fields = [
        "Periodname",
        "Provider Org code",
        "Commissioner Org Code",
    ]

    null_counts = dataframe[required_fields].isnull().sum()
    columns_with_nulls = null_counts[null_counts > 0]

    if not columns_with_nulls.empty:
        raise ValueError(
            f"Required fields contain null values: "
            f"{columns_with_nulls.to_dict()}"
        )

    business_key = [
        "Periodname",
        "Provider Org code",
        "Commissioner Org Code",
    ]

    duplicate_count = dataframe.duplicated(
        subset=business_key
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Found {duplicate_count} duplicate business-key rows."
        )

    return dataframe


if __name__ == "__main__":
    from extract import extract_csv

    df = extract_csv(
        "data/raw/outpatient_referrals_2023_24.csv"
    )
    
    validated_df = validate_data(df)
    print("Validation successful!")
    print(validated_df.head())                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      