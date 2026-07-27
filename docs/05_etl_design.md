# NHS Outpatient Referral ETL Design

## Purpose

This document describes the Extract, Transform and Load (ETL) process used to populate the NHS Outpatient Referral Data Warehouse.

The ETL pipeline extracts referral data from the raw source file, validates and transforms the data, and loads it into a dimensional data model consisting of three dimension tables and one fact table.

## ETL Process Overview

The pipeline consists of five stages:

1. Extract the source data from the NHS CSV file.
2. Validate the source data to ensure it meets expected quality standards.
3. Transform the data into the warehouse format.
4. Load the dimension tables.
5. Load the fact table using the generated surrogate keys.

## Data Validation

Before any data is loaded into the warehouse, the source dataset is validated to ensure it meets the expected quality standards.

The pipeline performs the following validation checks:

| Validation                | Purpose                                                                                                                               |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Schema validation         | Ensure all expected columns are present in the source file.                                                                           |
| Required field validation | Check that business keys and referral measures are not null or empty.                                                                 |
| Data type validation      | Ensure referral measures contain numeric values.                                                                                      |
| Business rule validation  | Ensure referral measures are non-negative values.                                                                                     |
| Duplicate detection       | Check for duplicate records based on the composite business key (Reporting Period, Provider Organisation, Commissioner Organisation). |

## Data Transformation

During the transformation stage, the source dataset is prepared for loading into the dimensional model.

The transformation process includes:

- Separating descriptive attributes into dimension datasets.
- Removing duplicate dimension records.
- Generating surrogate keys for each dimension.
- Mapping business keys to surrogate keys.
- Preparing the referral measures for loading into the fact table.

## Loading Strategy

The dimension tables are loaded before the fact table because the fact table depends on the surrogate keys generated for each dimension.

The loading sequence is:

1. Load `dim_reporting_period`.
2. Load `dim_provider`.
3. Load `dim_commissioner`.
4. retrieve the generated surrogate keys.
5. Map the source business keys to the corresponding surrogate keys.
6. Load `fact_outpatient_referrals`.

The pipeline should stop if validation fails or if a source business key cannot be matched to a dimension record.

## Failure Handling

The pipeline should stop immediately when a critical validation or loading error occurs.

Critical failures include:

- Missing required source columns.
- Null values in required business key fields.
- Invalid or negative referral measures.
- Duplicate records at the defined fact table grain.
- Unmatched dimension business keys during surrogate key mapping.
- Database insertion failures.

If a failure occurs before loading begins, no warehouse tables are changed.

If a failure occurs during the database load, the transaction should be rolled back so that partial data is not committed.

## Transaction Strategy

The database loading process should run within a transaction.

The transaction begins before the dimension tables are loaded and is committed only after:

1. All dimensions have loaded successfully.
2. All surrogate key lookups have succeeded.
3. The fact table has loaded successfully.

If any stage fails, the transaction is rolled back.

This ensures that the warehouse remains in a consistent state and prevents partial pipeline loads.
