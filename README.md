# HHS Care Forecasting

> Time-series forecasting of children in HHS care using statistical and machine learning models, with walk-forward validation, multi-horizon forecasting, and an interactive Streamlit dashboard.

## Overview

This project develops and evaluates forecasting models for estimating the number of children in U.S. Department of Health and Human Services (HHS) care.

The project compares classical time-series forecasting methods with tree-based machine learning models and uses time-aware walk-forward validation to evaluate how well the models generalize to future observations.

### Project Workflow

Raw Data → Data Cleaning → Feature Engineering → Time-Series Modeling → Walk-Forward Validation → Model Comparison → Forecasting → Streamlit Dashboard

---

## Objectives

The main objectives of this project are to:

- Analyze the historical HHS care population.
- Understand temporal patterns and changes in the series.
- Perform data cleaning and feature engineering.
- Create lagged, rolling, calendar, and operational features.
- Compare classical statistical forecasting methods with machine learning models.
- Avoid temporal data leakage through chronological validation.
- Evaluate forecasting performance across multiple horizons.
- Identify the best-performing forecasting model.
- Develop an interactive Streamlit application for exploring forecasts and model performance.

---

## Dataset

The project uses the HHS Unaccompanied Alien Children Program dataset.

The primary forecasting target is:

`Children in HHS Care`

### Dataset Files

- `HHS_Unaccompanied_Alien_Children_Program.csv` — Original dataset
- `HHS_cleaned.csv` — Cleaned dataset used for modeling

The dataset contains operational measures associated with the unaccompanied children care system.

The cleaned dataset contains **720 observations** covering approximately:

`January 12, 2023 – December 21, 2025`

The dataset contains some gaps between dates, meaning the observations are not perfectly continuous daily observations.

---

## Methodology

### 1. Data Cleaning

The raw dataset was prepared through:

- Date parsing
- Chronological sorting
- Missing-value checks
- Target-variable preparation
- Data consistency checks
- Preparation of forecasting outputs

### 2. Feature Engineering

The machine learning models use temporal and operational features derived from historical information.

Features include:

- Lag 1
- Lag 7
- Lag 30
- Rolling mean
- Rolling standard deviation
- Month
- Year
- Day of week
- Operational variables associated with the HHS care process

The features are constructed using information available at or before the forecast origin to reduce the risk of temporal data leakage.

---

## Walk-Forward Validation

Random train-test splitting was avoided because forecasting data is time-dependent.

Instead, the project uses walk-forward validation.

The process is:

1. Train the model using historical observations.
2. Forecast future observation(s).
3. Move the forecast origin forward.
4. Refit the model using the information available at that point.
5. Repeat the process across multiple validation windows.
6. Aggregate the forecasting errors.

This provides a more realistic estimate of how the models would perform when predicting future observations.

---

## Models Evaluated

### Statistical Forecasting Models

- Naïve Forecast
- Moving Average
- ARIMA(1,1,2)
- SARIMA(1,1,2)(1,0,0,14)
- Holt Exponential Smoothing

### Machine Learning Models

- Random Forest
- Gradient Boosting

---

## Evaluation Metrics

The models were evaluated using three primary metrics.

### Mean Absolute Error (MAE)

Measures the average absolute difference between actual and predicted values.

**Lower is better.**

### Root Mean Squared Error (RMSE)

Measures the square root of the average squared prediction error and gives greater weight to larger errors.

**Lower is better.**

### Mean Absolute Percentage Error (MAPE)

Measures the average prediction error relative to the actual value.

**Lower is better.**

### Forecast Horizons

The project evaluates:

- 1-step forecasting
- 7-step forecasting
- 14-step forecasting

---

## Results

The final model comparison produced the following results:

| Model | MAE | RMSE | MAPE | 1-step MAE | 7-step MAE | 14-step MAE |
|---|---:|---:|---:|---:|---:|---:|
| Gradient Boosting | 50.04 | 76.42 | 0.83% | 1.59 | 33.63 | 50.04 |
| Naïve | 58.81 | 82.06 | 1.31% | 79.18 | 61.92 | 58.81 |
| Random Forest | 59.78 | 77.84 | 0.99% | 46.60 | 54.31 | 59.78 |
| SARIMA(1,1,2)(1,0,0,14) | 130.72 | 149.98 | 2.16% | 42.80 | 99.23 | 130.72 |
| Moving Average | 166.19 | 185.95 | 4.13% | 173.70 | 184.12 | 166.19 |
| ARIMA(1,1,2) | 269.55 | 305.35 | 6.67% | 56.88 | 170.01 | 269.55 |
| Holt Exponential Smoothing | 320.27 | 357.55 | 5.32% | 61.77 | 187.65 | 320.27 |

---

## Best Performing Model

### Gradient Boosting

Gradient Boosting achieved the best overall performance among the evaluated models.

**Overall performance:**

- MAE: **50.04**
- RMSE: **76.42**
- MAPE: **0.83%**

It also achieved the lowest 1-step MAE and maintained strong performance across the 7-step and 14-step forecasting horizons.

### Multi-Horizon Performance

| Forecast Horizon | Gradient Boosting MAE |
|---|---:|
| 1-step | 1.59 |
| 7-step | 33.63 |
| 14-step | 50.04 |

---

## Key Findings

### 1. Gradient Boosting performed best overall

Gradient Boosting achieved the lowest overall MAE and MAPE among the evaluated models.

### 2. Machine learning models were highly competitive

Random Forest and Gradient Boosting performed substantially better than most classical statistical models.

### 3. The Naïve baseline was strong

The Naïve model achieved an overall MAE of 58.81, indicating that the HHS care series contains substantial temporal persistence.

### 4. Forecasting becomes more difficult at longer horizons

Forecast errors generally increase as the forecasting horizon becomes longer because uncertainty accumulates further into the future.

### 5. The series contains a substantial level change

The HHS care series shows a pronounced change in level during early 2025. This demonstrates why time-aware validation and monitoring for changes in the underlying data distribution are important.

### 6. Feature-based nonlinear models are promising

The results indicate that combining temporal features with nonlinear machine learning methods can provide strong forecasting performance for this operational forecasting problem.

---

## Forecast Output

The final forecast output contains approximately **142 observations**, covering:

`May 18, 2025 – December 21, 2025`

The forecast results are stored in:

- `forecast_output.csv`
- `discharge_forecast_output.csv`

---

## Project Structure

```text
HHS-Care-Forecasting/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── Feature_Engineering.ipynb
├── Time_Series_Structure.ipynb
│
├── HHS_Unaccompanied_Alien_Children_Program.csv
├── HHS_cleaned.csv
│
├── model_comparison.csv
├── forecast_output.csv
└── discharge_forecast_output.csv
