# Bank Customer Churn Risk Scoring

A reproducible machine-learning project for estimating churn probability, exploring customer segments with interactive charts, explaining model behavior, and examining retention scenarios.

## Project status

The assignment dataset is included locally as `data/European_Bank.csv` and is excluded from Git commits. You can also upload a CSV in the Streamlit app. Model metrics and feature importance are computed from a stratified holdout; they are not hard-coded.

## Project structure

```text
.
├── .devcontainer/       # Optional VS Code Dev Container setup
├── .vscode/             # VS Code launch configuration
├── data/                # Local assignment CSV (excluded from Git)
├── images/              # Figures used in the paper or README
├── notebooks/           # Exploratory analysis notebook
├── outputs/
│   ├── figures/         # Exported charts
│   └── model_results/   # Saved evaluation results
├── app.py               # Interactive Streamlit dashboard
├── research_paper.md    # Project paper draft
├── requirements.txt     # Python dependencies
└── README.md
```

The local Python environment (`.venv` or `venv`) is not included in the repository; recreate it from `requirements.txt` on another computer.

## Dataset

Expected target: `Exited` (1 = churn, 0 = retained). Expected predictors include `CreditScore`, `Geography`, `Gender`, `Age`, `Tenure`, `Balance`, `NumOfProducts`, `HasCrCard`, `IsActiveMember`, and `EstimatedSalary`. `CustomerId` and `Surname` are identifiers and excluded.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Use the app's upload control or the included `data/European_Bank.csv`. The app preprocesses data inside a scikit-learn pipeline, creates a stratified holdout, supports Logistic Regression and Random Forest, and refreshes threshold-dependent metrics and charts dynamically. Interactive tabs include portfolio KPIs, outcome mix, histograms, box/violin plots, segment churn bars, salary-balance scatterplots, treemaps, correlation heatmaps, ROC and precision-recall curves, calibration and threshold diagnostics, feature importance, a risk gauge, and a what-if scenario heatmap. Sidebar filters update descriptive charts; model diagnostics remain on the full holdout. Constant fields such as `Year` (2025 in this file), customer IDs, and surnames are excluded. The holdout metrics are the honest evaluation; the final refit is for scoring customer profiles.

## Feature engineering

The pipeline adds balance-to-salary ratio (with safe handling of zero salary), product density, engagement-product interaction, and age-tenure interaction. Categorical values are one-hot encoded with unknown categories ignored. Numeric values are median-imputed and scaled for Logistic Regression. The tree model uses the same preprocessing for a fair, consistent workflow.

## Deliverables checklist

- [ ] GitHub repository with source and setup instructions
- [ ] Research paper with dataset provenance, EDA, evaluation, limitations, and retention recommendations
- [ ] Deployed Streamlit application
- [ ] Project explanation video
- [ ] Internship experience and feedback video

See [research_paper.md](research_paper.md) for a data-grounded paper draft. Add measured holdout metrics from the app before submission.

## Responsible use and limitations

This is an educational prototype. Churn probabilities depend on the dataset, sampling, calibration, and time period. A binary threshold is an operational choice, not a natural boundary. Evaluate calibration, subgroup performance, data drift, and intervention outcomes before any real customer use. The dataset's demographic fields can encode sensitive proxies; keep explanations and proposed interventions under human review.
