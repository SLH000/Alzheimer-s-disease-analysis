# Alzheimer's Disease Clinical Trial Dashboard

## Overview

This project is a Streamlit dashboard that provides insights into industry-sponsored clinical trials for Alzheimer's Disease. The dashboard allows users to visualize the data related to trial registration and completion over selected year ranges.

## Features

- **Interactive Filters**: Users can filter trials by start and completion year.
- **Visualizations**:
  - **Bar chart** of registered clinical trials by year started and study status.
  - **Pie chart** showing the distribution of trial phases for completed trials within a selected year range.
  - **Bar charts** comparing sponsors against phases and conditions of completed trials.
  - **Bar chart** for the expected number of studies to complete by year and sponsor.

## Requirements

Ensure you have the following libraries installed:

- `pandas`
- `streamlit`
- `plotly`
- `matplotlib`
- `seaborn`

You can install the required packages using the following command:

```bash
pip install pandas streamlit plotly matplotlib seaborn

streamlit run AD.py
