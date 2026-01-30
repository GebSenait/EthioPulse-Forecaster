# EthioPulse-Forecaster

**Financial Inclusion Forecasting System for Ethiopia**

A production-ready analytical system designed to forecast Ethiopia's digital financial transformation trajectory, aligned with the World Bank Global Findex framework. This system supports decision-making for the National Bank of Ethiopia, mobile money operators, and development finance institutions.

## Project Overview

This repository implements a comprehensive forecasting system focusing on two core pillars of financial inclusion:

- **Access**: Account Ownership Rate
- **Usage**: Digital Payment Adoption Rate

The system analyzes historical trends (2011-2024), identifies structural constraints and leading indicators, and prepares the foundation for time-series forecasting (2025-2027).

## Repository Structure

```
EthioPulse-Forecaster/
├── .github/workflows/     # CI/CD workflows
├── data/
│   ├── raw/               # Original datasets
│   └── processed/        # Enriched and cleaned data
├── notebooks/            # Analysis notebooks
├── src/                  # Python modules
├── dashboard/            # Interactive dashboard
├── models/               # Trained forecasting models
├── reports/              # Analysis reports and insights
└── tests/                # Unit tests
```

## Key Features

- **Unified Schema Dataset**: Works with `ethiopia_fi_unified_data.csv` containing observations, events, impact links, and targets
- **Event-Driven Analysis**: Pillar-agnostic events with causal logic through impact_link records
- **Data Enrichment Pipeline**: Automated enrichment from IMF FAS, GSMA, ITU, NBE, and operator reports
- **Policy-Aware EDA**: Exploratory analysis with Ethiopia-specific market context
- **Forecast-Ready Outputs**: Prepared data and insights for time-series modeling

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd EthioPulse-Forecaster

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Task 1: Data Exploration & Enrichment

```bash
# Run data enrichment pipeline
jupyter notebook notebooks/task1_data_exploration.ipynb
```

### Task 2: Exploratory Data Analysis

```bash
# Run EDA analysis
jupyter notebook notebooks/task2_eda.ipynb
```

### Dashboard

```bash
# Launch interactive dashboard
python dashboard/app.py
```

## Data Sources

- **IMF Financial Access Survey (FAS)**
- **GSMA Mobile Money Reports**
- **ITU Telecommunications Statistics**
- **National Bank of Ethiopia (NBE) Reports**
- **Mobile Money Operator Reports**

## Methodology

The system follows a rigorous analytical approach:

1. **Data Enrichment**: Systematic addition of observations, events, and impact links
2. **Trend Analysis**: Historical trajectory analysis (2011-2024)
3. **Structural Analysis**: Infrastructure and enabler variable examination
4. **Event Overlay**: Temporal correlation of events with trends
5. **Forecast Preparation**: Data gap identification and hypothesis formation

## Contributing

This project follows strict Git/GitHub best practices:

- All development on `task-12-dev` branch
- Merges to `main` via Pull Request only
- Small, descriptive commits
- Comprehensive documentation

## License

[Specify license]

## Contact

Selam Analytics - Financial Inclusion Analytics Team
