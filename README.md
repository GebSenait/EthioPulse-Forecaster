# EthioPulse-Forecaster

**Financial Inclusion Forecasting System for Ethiopia**

Analytical system designed to forecast Ethiopia's digital financial transformation trajectory, aligned with the World Bank Global Findex framework. This system supports decision-making for the National Bank of Ethiopia, mobile money operators, and development finance institutions.

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
  - [Task 1: Data Exploration & Enrichment](#task-1-data-exploration--enrichment)
  - [Task 2: Exploratory Data Analysis](#task-2-exploratory-data-analysis)
  - [Task 3: Event Impact Modeling](#task-3-event-impact-modeling)
  - [Task 4: Forecasting Access & Usage](#task-4-forecasting-access--usage)
- [Task 5: Interactive Dashboard](#task-5-interactive-dashboard)
- [Task 1: Detailed Documentation](#task-1-detailed-documentation)
  - [Description](#description)
  - [Implementation](#implementation)
  - [Files Created](#files-created)
  - [Execution Results](#execution-results)
  - [Key Insights](#key-insights)
- [Task 2: Detailed Documentation](#task-2-detailed-documentation)
  - [Description](#description-1)
  - [Implementation](#implementation-1)
  - [Files Created](#files-created-1)
  - [Execution Results](#execution-results-1)
  - [Key Insights](#key-insights-1)
- [Task 3: Detailed Documentation](#task-3-detailed-documentation)
  - [Description](#description-2)
  - [Implementation](#implementation-2)
  - [Files Created](#files-created-2)
  - [Insights](#insights)
- [Task 4: Detailed Documentation](#task-4-detailed-documentation)
  - [Description](#description-3)
  - [Implementation](#implementation-3)
  - [Files Created](#files-created-3)
  - [Forecast Results & Interpretation](#forecast-results--interpretation)
- [Task 5: Detailed Documentation](#task-5-detailed-documentation)
  - [Description](#description-4)
  - [Implementation](#implementation-4)
  - [Execution](#execution)
  - [Files Created](#files-created-4)
  - [Dashboard Visualizations & Insights](#dashboard-visualizations--insights)
- [Tools & Technologies](#tools--technologies)
- [Data Sources](#data-sources)
- [Methodology](#methodology)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

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
│   ├── processed/         # Enriched and cleaned data
│   └── reference/         # Reference data for Tasks 3 & 4
├── notebooks/            # Analysis notebooks
├── src/                  # Python modules
├── dashboard/            # Interactive dashboard
├── models/               # Trained forecasting models
├── reports/              # Analysis reports and insights
└── tests/                # Unit tests
```

## Key Features

- **Unified Schema Dataset**: Works with `ethiopia_fi_unified_data.xlsx` containing observations, events, impact links, and targets
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
# Activate virtual environment (if not already active)
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate  # Linux/Mac

# Run data enrichment pipeline
jupyter notebook notebooks/task1_data_exploration.ipynb
```

### Task 2: Exploratory Data Analysis

```bash
# Run EDA analysis (ensure Task 1 has been completed first)
jupyter notebook notebooks/task2_eda.ipynb
```

### Task 3: Event Impact Modeling

```bash
# Run event impact modeling (uses enriched data or reference dataset)
jupyter notebook notebooks/task3_event_impact_modeling.ipynb
```

### Task 4: Forecasting Access & Usage

```bash
# Run forecasting (2025-2027 baseline, optimistic, pessimistic scenarios)
jupyter notebook notebooks/task4_forecasting_access_usage.ipynb
```

### Task 5: Interactive Dashboard

```bash
# From project root (EthioPulse-Forecaster/)
streamlit run dashboard/app.py
# Opens in browser at http://localhost:8501
```

---

## Task 1: Detailed Documentation

### Description

Task 1 implements a comprehensive data exploration and enrichment pipeline for Ethiopia's financial inclusion dataset. The task focuses on:

1. **Schema Interpretation**: Understanding and validating the unified schema structure
2. **Data Enrichment**: Systematically adding observations, events, and impact links from multiple authoritative sources
3. **Quality Assurance**: Validating data integrity and maintaining analytical neutrality
4. **Documentation**: Creating comprehensive enrichment logs for auditability

**Key Principles:**
- Events remain pillar-agnostic (no pillar assignment)
- Causal logic expressed through impact_link records
- Analytical neutrality preserved in event categorization

### Implementation

The implementation follows a structured pipeline:

1. **Data Loading & Validation**
   - Load unified schema dataset (`ethiopia_fi_unified_data.xlsx`)
   - Load reference codes for interpretation
   - Validate schema compliance using `UnifiedSchemaValidator`

2. **Composition Analysis**
   - Quantify dataset by record_type, pillar, source_type, confidence
   - Identify data gaps and coverage areas

3. **Enrichment Pipeline**
   - **IMF FAS**: Official financial access survey data
   - **GSMA**: Mobile money industry statistics
   - **ITU**: Telecommunications infrastructure indicators
   - **NBE**: National Bank of Ethiopia policy and regulatory data
   - **Operator Reports**: Mobile money operator statistics

4. **Impact Link Creation**
   - Connect events to observations via impact_link records
   - Express causal relationships while maintaining pillar-agnostic events

5. **Output Generation**
   - Save enriched dataset to `data/processed/ethiopia_fi_unified_data.xlsx`
   - Generate comprehensive enrichment log (`reports/data_enrichment_log.md`)

### Files Created

| File | Location | Description |
|------|----------|-------------|
| `task1_data_exploration.ipynb` | `notebooks/` | Main enrichment pipeline notebook |
| `ethiopia_fi_unified_data.xlsx` | `data/processed/` | Enriched dataset output |
| `data_enrichment_log.md` | `reports/` | Detailed enrichment documentation |

**Supporting Files:**
- `src/data_utils.py`: Core utility functions for data operations
- `src/__init__.py`: Package initialization

### Execution Results

**Expected Outputs:**

1. **Dataset Composition Summary**
   - Total records by type (observations, events, impact_links)
   - Distribution by pillar (access, usage)
   - Source type breakdown
   - Confidence level distribution
   - Year range coverage

2. **Enrichment Statistics**
   - Number of new observations added
   - Number of new events added
   - Number of impact links created
   - Source-wise contribution breakdown

3. **Validation Results**
   - Schema validation pass/fail status
   - Data quality checks (missing values, completeness)
   - Impact link integrity verification

**Sample Output:**
```
✓ Loaded X records from unified dataset
✓ Added Y IMF FAS observations
✓ Added Z GSMA records
✓ Created N impact links
✓ Enriched dataset saved to: data/processed/ethiopia_fi_unified_data.xlsx
✓ Enrichment log saved to: reports/data_enrichment_log.md
```

### Key Insights

1. **Schema Compliance**: All enrichments maintain strict adherence to unified schema rules
2. **Source Diversity**: Multiple authoritative sources ensure data reliability
3. **Event Neutrality**: Pillar-agnostic events enable flexible causal analysis
4. **Audit Trail**: Complete enrichment log provides full traceability
5. **Data Quality**: Validation ensures consistency and completeness

---

## Task 2: Detailed Documentation

### Description

Task 2 performs comprehensive exploratory data analysis (EDA) on Ethiopia's financial inclusion trajectory, focusing on:

1. **Trend Analysis**: Historical trajectory of Access and Usage pillars (2011-2024)
2. **Slowdown Explanation**: Analysis of 2021-2024 growth deceleration
3. **Infrastructure Examination**: Analysis of enabler variables and infrastructure indicators
4. **Event Correlation**: Temporal overlay of policy/market events on trends
5. **Statistical Analysis**: Correlation analysis between pillars
6. **Policy Insights**: Extraction of at least 5 policy-relevant insights
7. **Forecasting Preparation**: Documentation of data gaps and hypotheses

### Implementation

The EDA follows a systematic analytical approach:

1. **Data Loading**
   - Load enriched dataset from Task 1 output
   - Extract observations by pillar (access, usage)
   - Extract events and infrastructure indicators

2. **Trend Visualization**
   - Time-series plots for Access and Usage (2011-2024)
   - Growth rate calculations (pre-2021 vs post-2021)
   - Identification of inflection points

3. **Slowdown Analysis**
   - Year-over-year growth rate calculations
   - Comparative analysis of pre-2021 and post-2021 periods
   - Identification of contributing factors

4. **Infrastructure Analysis**
   - Extraction of ITU and GSMA infrastructure indicators
   - Correlation with inclusion metrics
   - Gap analysis (infrastructure vs usage)

5. **Event Overlay**
   - Temporal visualization of policy, market, and infrastructure events
   - Correlation with trend changes
   - Lag analysis (event timing vs metric response)

6. **Correlation Analysis**
   - Pearson correlation between Access and Usage
   - Statistical significance testing
   - Heatmap visualization

7. **Insight Extraction**
   - Systematic identification of policy-relevant findings
   - Evidence-based interpretation
   - Implication analysis for decision-makers

8. **Gap Documentation**
   - Temporal coverage gaps
   - Source diversity assessment
   - Geographic granularity limitations

9. **Hypothesis Formation**
   - Forecasting hypotheses based on patterns
   - Rationale documentation
   - Forecast implications

### Files Created

| File | Location | Description |
|------|----------|-------------|
| `task2_eda.ipynb` | `notebooks/` | Main EDA analysis notebook |
| `trends_access_usage.png` | `reports/figures/` | Access and Usage trend visualization |
| `trends_with_events.png` | `reports/figures/` | Trends with event overlay |
| `correlation_matrix.png` | `reports/figures/` | Correlation heatmap |
| `insights.md` | `reports/` | Synthesized policy insights document |

**Supporting Files:**
- Uses enriched data from Task 1
- Leverages `src/data_utils.py` for data operations

### Execution Results

**Expected Outputs:**

1. **Trend Analysis**
   - Access trend: Account ownership rate over time
   - Usage trend: Digital payment adoption rate over time
   - Growth rate comparisons (pre/post 2021)

2. **Visualizations**
   - Separate trend plots for Access and Usage
   - Combined plot with event overlay
   - Correlation heatmap

3. **Statistical Summary**
   - Correlation coefficient between Access and Usage
   - P-value for statistical significance
   - Growth rate statistics

4. **Policy Insights**
   - Access-Usage Gap analysis
   - Post-2021 Growth Deceleration explanation
   - Policy Event Impact Timing
   - Infrastructure-Usage Mismatch
   - Market Competition Effects

5. **Data Gaps Documentation**
   - Temporal coverage gaps
   - Source diversity limitations
   - Geographic granularity constraints

6. **Forecasting Hypotheses**
   - Usage catch-up hypothesis
   - Policy lag hypothesis
   - Infrastructure saturation hypothesis

**Sample Output:**
```
✓ Loaded X records
Access observations: Y
Usage observations: Z
=== ACCESS PILLAR ANALYSIS ===
Pre-2021 average growth: X.XX%
Post-2021 average growth: Y.YY%
Growth slowdown: Z.ZZ percentage points

=== POLICY-RELEVANT INSIGHTS ===
1. Access-Usage Gap Persists
2. Post-2021 Growth Deceleration
3. Policy Events Show Delayed Impact
4. Infrastructure Growth Outpaces Usage
5. Market Competition Drives Access but Not Usage
```

### Key Insights

1. **Access-Usage Gap**: Account ownership significantly exceeds digital payment usage, indicating a substantial activation gap
2. **Growth Deceleration**: Post-2021 slowdown despite infrastructure expansion suggests structural barriers
3. **Policy Lag**: 18-24 month delay before measurable policy impact requires patient evaluation frameworks
4. **Infrastructure Mismatch**: Infrastructure growth outpaces usage, indicating need for activation focus
5. **Market Dynamics**: Competition improves access but usage requires network effects and habit formation

**Why Inclusion Slowed Despite Mobile Money Growth:**
- Structural barriers (literacy, trust, network effects) constrain adoption
- Infrastructure saturation effects as penetration increases
- Usage activation gap: accounts opened but not actively used
- Policy implementation lag: interventions need time to show impact
- Market dynamics: competition improves access but usage requires habit formation

---

## Task 3: Detailed Documentation

### Description

Task 3 quantifies how policy, market, and infrastructure events affect Ethiopia's financial inclusion indicators. It builds the event-indicator association framework required for event-augmented forecasting.

### Implementation

1. **Data Loading**: Load enriched data and impact_link records
2. **Join Logic**: Join impact_link → events via source_event (parent_id)
3. **Summary Table**: Event | Indicator | Direction | Magnitude | Lag
4. **Association Matrix**: Rows=Events, Columns=Indicators (Access, Usage, MM accounts)
5. **Functional Forms**: Immediate vs lagged effects, additive vs cumulative impacts
6. **Validation**: Telebirr 2021–2024 historical validation

### Files Created

| File | Location | Description |
|------|----------|-------------|
| `task3_event_impact_modeling.ipynb` | `notebooks/` | Event impact modeling notebook |
| `task3_impact_summary_table.csv` | `reports/` | Summary table output |
| `task3_association_matrix.csv` | `reports/` | Association matrix output |
| `task3_association_matrix_heatmap.png` | `reports/figures/` | Heatmap visualization |
| `task3_event_impact_methodology.md` | `reports/` | Methodology documentation |

### Insights

- Policy events (NFIS, Interoperability) show 12–18 month lags
- Telebirr has largest estimated impact on Access and Usage
- Event magnitudes are expert-estimated; use ±30% for sensitivity

---

## Task 4: Detailed Documentation

### Description

Task 4 forecasts Ethiopia's Access (Account Ownership) and Usage (Digital Payments) for 2025–2027 using Global Findex definitions, with baseline, optimistic, and pessimistic scenarios.

### Implementation

1. **Target Definition**: Access = Account ownership (%), Usage = Digital payments (%) – Global Findex aligned
2. **Methods**: Trend-only model, event-augmented model, scenario analysis
3. **Scenarios**: Baseline, optimistic (+20% event impact), pessimistic (-20% event impact)
4. **Uncertainty**: Confidence intervals via scenario ranges
5. **Interpretation**: Key drivers, largest-impact events, structural constraints

### Files Created

| File | Location | Description |
|------|----------|-------------|
| `task4_forecasting_access_usage.ipynb` | `notebooks/` | Forecasting notebook |
| `task4_forecast_table_2025_2027.csv` | `reports/` | Forecast table output |
| `task4_forecast_scenarios.png` | `reports/figures/` | Scenario visualizations |
| `task4_forecast_interpretation.md` | `reports/` | Policy-focused interpretation |

### Forecast Results & Interpretation

**2025–2027 Baseline (approximate):**
- Access: 56% → 58% → 60%
- Usage: 34% → 36% → 38%

**Key Drivers:** M-Pesa (2023), Telebirr scale-up, interoperability  
**Risks:** Usage activation gap, infrastructure saturation, macro/regulatory headwinds

---

## Task 5: Detailed Documentation

### Description

Task 5 delivers a **stakeholder-ready, interactive dashboard** that visualizes Ethiopia's financial inclusion indicators, event impacts, and forecasts. It enables the consortium (development finance institutions, mobile money operators, National Bank of Ethiopia) to answer:

- Which events most affected financial inclusion indicators?
- How did account ownership and digital payment usage evolve over time?
- What is the forecast for Access and Usage through 2027?
- What progress has Ethiopia made toward financial inclusion targets (e.g. 60% account ownership)?

The dashboard is built with **Streamlit** for clarity, interactivity, and reproducibility.

### Implementation

1. **Dashboard setup**: Streamlit app in `dashboard/app.py` with modular data loading in `dashboard/data_loader.py`.
2. **Overview page**: Key metrics (current Access/Usage), **Usage-to-Access Ratio** (digital activation), growth highlights, and event-impact magnitude chart.
3. **Trends page**: Interactive time series with date range selector and channel (Access vs Usage) comparison; events timeline.
4. **Forecasts page**: Forecasts with confidence intervals; model/scenario selection (baseline with CI, or baseline/optimistic/pessimistic comparison); key projected milestones.
5. **Inclusion Projections page**: Financial inclusion rate projections, **progress toward 60% target**, scenario selector (optimistic/base/pessimistic), and expandable answers to the four consortium questions.
6. **Technical**: At least four interactive Plotly charts; clear labels and explanations; **data download** (observations, baseline forecast, scenario forecast) in the sidebar; scenario selection throughout.

### Execution

From the project root:

```bash
# Activate environment
.\venv\Scripts\Activate.ps1   # Windows
# source venv/bin/activate    # Linux/Mac

# Run dashboard
streamlit run dashboard/app.py
```

The app opens in the default browser at **http://localhost:8501**. No separate server port configuration is required.

### Files Created

| File | Location | Description |
|------|----------|-------------|
| `dashboard/app.py` | `dashboard/` | Main Streamlit app (Overview, Trends, Forecasts, Inclusion Projections) |
| `dashboard/data_loader.py` | `dashboard/` | Data loading for reference data, observations, events, impact links, forecasts |
| `reports/task4_forecast_scenarios.csv` | `reports/` | Scenario forecasts (baseline, optimistic, pessimistic) for 2025–2027 |

**Data dependencies:** `data/reference/task34_reference_data.csv`, `reports/task4_forecast_table_2025_2027.csv`, `reports/task4_forecast_scenarios.csv`.

### Dashboard Visualizations & Insights

| Section | Visualizations | Insights |
|--------|----------------|----------|
| **Overview** | Metric cards (Access %, Usage %, Usage-to-Access Ratio, Access–Usage gap); ratio over time; event-impact magnitude bar chart | Current levels and digital activation trend; which events have largest measured impact on indicators |
| **Trends** | Interactive Access vs Usage time series; year range slider; channel comparison bar chart; events table | Evolution of account ownership and digital payments; channel comparison by year; event timeline |
| **Forecasts** | Baseline + confidence intervals; scenario comparison (baseline/optimistic/pessimistic); milestone table | 2025–2027 trajectories; uncertainty and scenario range; key projected values |
| **Inclusion Projections** | Access projection vs 60% target line; scenario selector; expandable Q&A | Progress toward target; scenario-based outlook; direct answers to consortium questions |

**Validation:** Dashboard uses the same reference and report outputs as Tasks 1–4; metrics and forecasts are traceable to notebooks and CSVs.  
**Limitations:** Dashboard assumes reference and forecast files exist; event names depend on `task34_reference_data.csv` schema.  
**Recommendations:** Re-run Task 4 after model changes to refresh `task4_forecast_scenarios.csv`; use data download for external reporting.  
**Next steps:** Optional: deploy to a shared URL; add filters (e.g. by region if data becomes available); link to methodology docs from the app.

#### Task 5 — Mandatory response structure

1. **Context recap**: Consortium (NBE, mobile money operators, development finance institutions) needs a single place to explore FI indicators, event impacts, and forecasts from Tasks 1–4.
2. **Objective**: Build a stakeholder-ready, interactive dashboard answering which events affected FI, how Access/Usage evolved, what the 2025–2027 forecast is, and progress toward the 60% target.
3. **Data used**: `data/reference/task34_reference_data.csv` (observations, events, impact_links), `reports/task4_forecast_table_2025_2027.csv`, `reports/task4_forecast_scenarios.csv`.
4. **Methodology**: Streamlit for UI; Plotly for interactive charts; cached data load from reference and reports; scenario selection for policy-relevant ranges.
5. **Dashboard design**: Four pages (Overview, Trends, Forecasts, Inclusion Projections); sidebar for navigation and data download; metric cards and time series with clear labels.
6. **Implementation**: `dashboard/app.py` (Streamlit), `dashboard/data_loader.py` (load and reshape); scenario CSV generated for baseline/optimistic/pessimistic.
7. **Execution steps**: From project root, `streamlit run dashboard/app.py`; browser opens at http://localhost:8501.
8. **Interactive visualizations**: Overview (metrics, Usage-to-Access ratio, event-impact bar); Trends (time series + date range, channel comparison); Forecasts (baseline + CI, scenario comparison); Inclusion Projections (60% target line, scenario selector, Q&A expanders).
9. **Insights & interpretation**: Access leads Usage; ratio shows activation gap; event-impact magnitudes identify Telebirr, NFIS, M-Pesa; baseline 2027 Access ~82%, above 60% target.
10. **Validation**: Same inputs as Tasks 1–4; numbers traceable to notebooks and CSVs; download allows external audit.
11. **Limitations**: Depends on reference and forecast files; event names from schema; no geographic or demographic breakdown in current data.
12. **Recommendations**: Re-run Task 4 when models change; use downloads for reporting; document assumptions in expanders.
13. **Next steps**: Deploy to shared URL; add region/segment filters if data available; link methodology docs from app.

---

## Tools & Technologies

- **Python**: pandas, numpy, scipy, statsmodels, scikit-learn
- **Visualization**: matplotlib, seaborn, plotly
- **Time Series**: prophet, pmdarima
- **Dashboard**: Streamlit (Task 5), Dash, dash-bootstrap-components
- **Data**: openpyxl (Excel), great-expectations (validation)

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

- **main** branch is protected
- Task 5 development on `task-5-dev` branch; Tasks 3 & 4 on `task-34-dev`
- Merges to `main` via Pull Request only
- Small, descriptive commits
- Comprehensive documentation

### Git Branching

```bash
git checkout -b task-5-dev    # Create branch
# ... implement Task 5 dashboard ...
git add .
git commit -m "feat(task5): add Streamlit dashboard (Overview, Trends, Forecasts, Inclusion Projections)"
# Open Pull Request to main
```

### Git Branching

```bash
git checkout -b task-34-dev   # Create branch
# ... implement Task 3 and Task 4 ...
git add . && git commit -m "feat: add event impact modeling and forecasting"
# Open Pull Request to main
```

## Contact

Selam Analytics - Financial Inclusion Analytics Team