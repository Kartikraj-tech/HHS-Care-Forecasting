import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="HHS Care Load Forecast",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Load data
# --------------------------------------------------

forecast_df = pd.read_csv("forecast_output.csv")
discharge_forecast_df = pd.read_csv("discharge_forecast_output.csv")
model_comparison = pd.read_csv(
    "model_comparison.csv",
    index_col=0
)

# Convert dates
forecast_df["Date"] = pd.to_datetime(forecast_df["Date"])

discharge_forecast_df["Date"] = pd.to_datetime(
    discharge_forecast_df["Date"]
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("HHS Care Load Forecasting Dashboard")

st.markdown(
    """
    Forecasting dashboard for HHS care load, discharge demand,
    model performance, uncertainty, and scenario analysis.
    """
)

st.divider()

# --------------------------------------------------
# Sidebar controls
# --------------------------------------------------

st.sidebar.header("Forecast Controls")

horizon = st.sidebar.selectbox(
    "Forecast Horizon",
    [7, 14, 30, 60, 90, 142],
    index=1
)

model_options = model_comparison.index.tolist()

selected_model = st.sidebar.selectbox(
    "Model",
    model_options,
    index=(
        model_options.index("Gradient Boosting")
        if "Gradient Boosting" in model_options
        else 0
    )
)

# --------------------------------------------------
# Model Performance
# --------------------------------------------------

st.header("Model Performance")

selected_metrics = model_comparison.loc[selected_model]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "MAE",
        f"{selected_metrics['MAE']:.2f}"
    )

with col2:
    st.metric(
        "RMSE",
        f"{selected_metrics['RMSE']:.2f}"
    )

with col3:
    st.metric(
        "MAPE",
        f"{selected_metrics['MAPE']:.2f}%"
    )

# --------------------------------------------------
# Model Selection & Comparison
# --------------------------------------------------

st.header("Model Selection & Comparison")

display_columns = [
    "MAE",
    "RMSE",
    "MAPE",
    "MAE_1_step",
    "MAE_7_step",
    "MAE_14_step",
    "Robustness"
]

available_columns = [
    column
    for column in display_columns
    if column in model_comparison.columns
]

st.dataframe(
    model_comparison[available_columns].round(2),
    use_container_width=True
)

st.success(
    f"Selected model: {selected_model}"
)

# --------------------------------------------------
# Future Care Load Forecast
# --------------------------------------------------

st.header("Future Care Load Forecast")

plot_df = forecast_df.tail(horizon)

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    plot_df["Date"],
    plot_df["Actual"],
    label="Actual"
)

ax.plot(
    plot_df["Date"],
    plot_df["Forecast"],
    label="Gradient Boosting Forecast"
)

ax.fill_between(
    plot_df["Date"],
    plot_df["Lower_95"],
    plot_df["Upper_95"],
    alpha=0.2,
    label="95% Prediction Interval"
)

ax.set_xlabel("Date")
ax.set_ylabel("Children in HHS Care")

ax.set_title(
    f"HHS Care Load Forecast - {horizon} Observations"
)

ax.legend()

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# --------------------------------------------------
# Confidence Interval Visualization
# --------------------------------------------------

st.header("Confidence Interval Visualization")

st.markdown(
    """
    The shaded region represents the approximate 95% prediction
    interval based on historical validation residual variability.
    """
)

ci_df = forecast_df.tail(horizon)

fig_ci, ax_ci = plt.subplots(figsize=(14, 5))

ax_ci.plot(
    ci_df["Date"],
    ci_df["Forecast"],
    label="Forecast"
)

ax_ci.fill_between(
    ci_df["Date"],
    ci_df["Lower_95"],
    ci_df["Upper_95"],
    alpha=0.25,
    label="95% Prediction Interval"
)

ax_ci.set_xlabel("Date")
ax_ci.set_ylabel("Children in HHS Care")

ax_ci.set_title(
    "Forecast Uncertainty"
)

ax_ci.legend()

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig_ci)

# --------------------------------------------------
# Discharge Demand Forecast
# --------------------------------------------------

st.header("Discharge Demand Forecast")

discharge_plot = discharge_forecast_df.tail(horizon)

fig2, ax2 = plt.subplots(figsize=(14, 5))

ax2.plot(
    discharge_plot["Date"],
    discharge_plot["Actual_Discharge"],
    label="Actual Discharges"
)

ax2.plot(
    discharge_plot["Date"],
    discharge_plot["Forecast_Discharge"],
    label="Forecast Discharges"
)

ax2.set_xlabel("Date")
ax2.set_ylabel("Children Discharged")

ax2.set_title(
    f"HHS Discharge Demand - {horizon} Observations"
)

ax2.legend()

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig2)

# --------------------------------------------------
# Scenario Comparison
# --------------------------------------------------

st.header("Scenario Comparison")

st.markdown(
    """
    Analytical scenarios are applied to the selected forecast
    to illustrate lower-demand, baseline, and higher-demand conditions.
    """
)

scenario_df = forecast_df.tail(horizon)[
    ["Date", "Forecast"]
].copy()

scenario_df["Lower Demand"] = scenario_df["Forecast"] * 0.90
scenario_df["Baseline"] = scenario_df["Forecast"]
scenario_df["Higher Demand"] = scenario_df["Forecast"] * 1.10

fig3, ax3 = plt.subplots(figsize=(14, 6))

ax3.plot(
    scenario_df["Date"],
    scenario_df["Lower Demand"],
    label="Lower Demand (-10%)"
)

ax3.plot(
    scenario_df["Date"],
    scenario_df["Baseline"],
    label="Baseline"
)

ax3.plot(
    scenario_df["Date"],
    scenario_df["Higher Demand"],
    label="Higher Demand (+10%)"
)

ax3.set_xlabel("Date")
ax3.set_ylabel("Children in HHS Care")

ax3.set_title(
    "Care Load Scenario Comparison"
)

ax3.legend()

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig3)

# --------------------------------------------------
# Scenario summary
# --------------------------------------------------

st.subheader("Scenario Summary")

scenario_summary = pd.DataFrame({
    "Scenario": [
        "Lower Demand",
        "Baseline",
        "Higher Demand"
    ],
    "Adjustment": [
        "-10%",
        "0%",
        "+10%"
    ],
    "Average Forecast": [
        scenario_df["Lower Demand"].mean(),
        scenario_df["Baseline"].mean(),
        scenario_df["Higher Demand"].mean()
    ],
    "Peak Forecast": [
        scenario_df["Lower Demand"].max(),
        scenario_df["Baseline"].max(),
        scenario_df["Higher Demand"].max()
    ]
})

st.dataframe(
    scenario_summary.round(2),
    use_container_width=True
)

# --------------------------------------------------
# Summary metrics
# --------------------------------------------------

st.header("Forecast Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Latest Care Load",
        f"{forecast_df['Actual'].iloc[-1]:,.0f}"
    )

with col2:
    st.metric(
        "Latest Forecast",
        f"{forecast_df['Forecast'].iloc[-1]:,.0f}"
    )

with col3:
    st.metric(
        "Forecast Horizon",
        f"{horizon} days"
    )