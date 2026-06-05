# Source Scripts Overview

This folder contains the original analysis scripts, reorganized without changing their analytical logic.

## File Roles

- `data_preparation_brouillon.py`: the most complete draft pipeline. It loads the CSV, builds the EDA table, creates combined features, prepares the logistic-regression tables, balances the data, and evaluates a logistic regression model.
- `eda_with_plot_test.py`: a lighter EDA script that ends with one focused plot on general health and diabetes rate.
- `plot_generation.py`: the main plotting script for EDA charts and correlation visualizations.
- `feature_combination_experiments.py`: a focused experiment script used to justify combined variables such as `Metabolic_Risk`.
- `logistic_regression_balanced_vs_imbalanced.py`: a compact script dedicated to comparing model behavior on balanced versus full imbalanced data.
- `features_reference.py`: a reference list of engineered and retained final features.
- `diabetes_eda_table.sql`: SQL definition for the `diabetes_eda` transformation table.

## Overlap Notes

Some overlap between scripts is intentional because they represent different project stages:

- exploration
- visualization
- feature-combination validation
- final model comparison

Only obvious duplication was cleaned up. The analytical workflow itself was left unchanged.
