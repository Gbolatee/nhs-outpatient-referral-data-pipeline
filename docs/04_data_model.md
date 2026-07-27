# NHS Outpatient Referral Data Model

## Purpose

This document defines the dimensional data model for the NHS Outpatient Referral Data Pipeline.

The model is designed as a star schema to support analysis of outpatient referral activity by reporting period, provider organisation, and commissioner organisation.

## Fact Table Grain

Each row in `fact_outpatient_referrals` represents aggregated outpatient referral activity for one reporting period, one provider organisation, and one commissioner organisation.

## Dimension Tables

### `dim_provider`

Stores descriptive information about NHS provider organisations.

| Column            | Data Type | Key Type                   | Description                                     |
| ----------------- | --------- | -------------------------- | ----------------------------------------------- |
| provider_key      | Integer   | Primary key, surrogate key | Warehouse-generated identifier for the provider |
| provider_org_code | String    | Business key               | NHS organisation code for the provider          |
| provider_name     | String    | Attribute                  | Name of the provider organisation               |

### `dim_commissioner`

Stores descriptive information about NHS commissioner organisations.

| Column                | Data Type | Key Type                   | Description                                         |
| --------------------- | --------- | -------------------------- | --------------------------------------------------- |
| commissioner_key      | Integer   | Primary key, surrogate key | Warehouse-generated identifier for the commissioner |
| commissioner_org_code | String    | Business key               | NHS organisation code for the commissioner          |
| commissioner_name     | String    | Attribute                  | Name of the commissioner organisation               |

### `dim_reporting_period`

Stores descriptive information about the reporting periods used in the source dataset.

| Column               | Data Type | Key Type                   | Description                                              |
| -------------------- | --------- | -------------------------- | -------------------------------------------------------- |
| reporting_period_key | Integer   | Primary key, surrogate key | Warehouse-generated identifier for the reporting period  |
| period_name          | String    | Business key               | Reporting period from the source dataset (e.g. Jan-2025) |

## Fact Table

### `fact_outpatient_referrals`

Stores aggregated outpatient referral measures for each reporting period, provider organisation, and commissioner organisation.

| Column               | Data Type | Key Type    | Description                                                                       |
| -------------------- | --------- | ----------- | --------------------------------------------------------------------------------- |
| reporting_period_key | Integer   | Foreign key | References `dim_reporting_period`                                                 |
| provider_key         | Integer   | Foreign key | References `dim_provider`                                                         |
| commissioner_key     | Integer   | Foreign key | References `dim_commissioner`                                                     |
| gp_referrals_made    | Integer   | Measure     | Number of outpatient referrals made by General Practitioners                      |
| gp_referrals_seen    | Integer   | Measure     | Number of GP outpatient referrals seen by the provider organisation               |
| other_referrals_made | Integer   | Measure     | Number of outpatient referrals made from sources other than General Practitioners |
| other_referrals_seen | Integer   | Measure     | Number of non-GP outpatient referrals seen by the provider organisation           |

### Fact Table Uniqueness

A row in `fact_outpatient_referrals` is uniquely identified by the combination of:

- `reporting_period_key`
- `provider_key`
- `commissioner_key`

Together, these columns represent the warehouse version of the source dataset's candidate composite business key.

## Table Relationships

The data model follows a star schema design.

The `fact_outpatient_referrals` table stores the referral measures and links to each dimension table using foreign keys.

| Fact Table Column      | References                                  |
| ---------------------- | ------------------------------------------- |
| `reporting_period_key` | `dim_reporting_period.reporting_period_key` |
| `provider_key`         | `dim_provider.provider_key`                 |
| `commissioner_key`     | `dim_commissioner.commissioner_key`         |

## Design Decisions

### Why a Star Schema?

A star schema was selected because it separates descriptive business information from measurable referral activity.

Dimension tables store descriptive attributes such as provider, commissioner, and reporting period, while the fact table stores the referral measures.

This structure reduces data duplication, simplifies analytical queries, and follows widely adopted dimensional modelling practices used in data warehouses.

### Why Surrogate Keys?

Surrogate keys are used as the primary keys for all dimension tables instead of the source system business keys.

This approach provides stable identifiers within the warehouse, improves join performance by using integer keys, and allows the warehouse to remain independent of changes to source system identifiers.

The original NHS organisation codes and reporting period values are retained as business keys within the dimension tables to preserve traceability to the source data.

### Why a Single Fact Table?

A single fact table was selected because all referral measures share the same business grain.

Each measure represents aggregated referral activity for one reporting period, one provider organisation, and one commissioner organisation.

Storing these measures together avoids unnecessary duplication, simplifies analytical queries, and ensures that all referral metrics can be analysed consistently across the same dimensions.

### Why Separate Facts and Dimensions?

The data model separates descriptive information from measurable referral activity.

Dimension tables store relatively stable business entities, while the fact table stores the numerical referral measures.

This approach reduces data duplication, improves data consistency, and makes the warehouse easier to maintain as descriptive information changes over time.
