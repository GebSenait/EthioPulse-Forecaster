# Task 3: Event Impact Modeling – Methodology Documentation

**EthioPulse-Forecaster | Selam Analytics**

---

## 1. Context Recap

Ethiopia’s financial inclusion growth slowed after 2021 despite rapid mobile money expansion (Telebirr, M-Pesa, interoperability). This document describes how events are translated into quantified impacts on inclusion indicators for use in event-augmented forecasting.

## 2. Objective

- Load enriched data and `impact_link` records
- Join `impact_link` → events via `source_event` (parent_id)
- Produce summary table: Event | Indicator | Direction | Magnitude | Lag
- Build Event–Indicator Association Matrix (rows=events, columns=indicators)
- Express impacts in functional form (immediate vs lagged, additive vs cumulative)
- Validate against historical data (e.g. Telebirr 2021–2024)

## 3. Data Used

- **Primary**: Enriched unified dataset from Task 1 (`ethiopia_fi_enriched.csv`) or reference data (`task34_reference_data.csv`)
- **Record types**: `observation`, `event`, `impact_link`
- **Events**: Pillar-agnostic (no pillar assignment)
- **Causality**: Only via `impact_link` records linking `source_event` → `target_observation`

## 4. Methodology

### 4.1 Join Structure

- `impact_link.source_event` (parent_id) → `event.record_id`
- `impact_link.target_observation` → `observation.record_id`
- Resolved event names and indicator metadata used for summary table and matrix

### 4.2 Functional Forms

| Type | Condition | Interpretation |
|------|-----------|----------------|
| **Immediate** | `lag_months = 0` | Additive shock in event year |
| **Lagged** | `lag_months > 0` | Effect distributed over subsequent periods |
| **Additive** | Per link | Magnitude (pp) added to indicator |
| **Cumulative** | Multiple links | Sum of contributions from all linked events |

### 4.3 Magnitude Interpretation

- Magnitudes in percentage points (pp)
- Positive direction: event increases indicator
- Negative direction: event decreases indicator

## 5. Sources & Assumptions

| Source | Use |
|--------|-----|
| Ethiopia data | IMF FAS, NBE, GSMA, operator reports |
| Comparable countries | Kenya (M-Pesa), Tanzania (Vodacom) for magnitude priors |
| Assumptions | Expert-based impact estimates; not econometrically identified |

## 6. Confidence vs Uncertainty

- **High confidence**: Official sources (IMF, NBE), well-documented events
- **Medium confidence**: Operator reports, comparable-country evidence
- **Low confidence**: Extrapolations, sparse evidence
- **Uncertainty**: Magnitudes are point estimates; consider ±30% for sensitivity

## 7. Validation – Telebirr (2021–2024)

- Telebirr launch: May 2021
- Model links: Access (+4.2pp immediate), Usage (+5.0pp, 6‑month lag)
- Historical: Access 46.2% (2021), 48.7% (2022); Usage 28.5% (2021), 31.2% (2023)
- Interpretation: Telebirr’s market entry aligns with observed jumps; comparable evidence supports positive impact

## 8. Limitations

1. Sparse `impact_link` coverage; many events lack explicit links
2. Magnitudes are expert estimates, not causal estimates
3. No formal identification strategy
4. Single-country reference data limits external validation

## 9. Recommendations

1. Refine estimates as Ethiopia-specific data becomes available
2. Use Task 4 event-augmented forecasts for validation
3. Document all assumptions and sources for auditability

---

*Document generated as part of EthioPulse-Forecaster Task 3 implementation.*
