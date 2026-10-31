from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.calibration import calibration_curve
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, average_precision_score, brier_score_loss, confusion_matrix,
    f1_score, precision_recall_curve, precision_score, recall_score, roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

st.set_page_config(page_title="Bank Churn Intelligence", page_icon="🏦", layout="wide")
APP_DIR = Path(__file__).resolve().parent
TARGET = "Exited"
IDENTIFIERS = {"CustomerId", "Surname"}


def add_features(frame: pd.DataFrame) -> pd.DataFrame:
    x = frame.copy()
    if {"Balance", "EstimatedSalary"}.issubset(x.columns):
        x["BalanceToSalary"] = x["Balance"] / x["EstimatedSalary"].replace(0, np.nan)
    if {"NumOfProducts", "Tenure"}.issubset(x.columns):
        x["ProductDensity"] = x["NumOfProducts"] / (x["Tenure"] + 1)
    if {"NumOfProducts", "IsActiveMember"}.issubset(x.columns):
        x["EngagementProduct"] = x["NumOfProducts"] * x["IsActiveMember"]
    if {"Age", "Tenure"}.issubset(x.columns):
        x["AgeTenure"] = x["Age"] * x["Tenure"]
    return x


def build_pipeline(features: pd.DataFrame, model_name: str) -> Pipeline:
    numeric = list(features.select_dtypes(include=np.number).columns)
    categorical = [c for c in features.columns if c not in numeric]
    numeric_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="median", add_indicator=True)),
        ("scale", StandardScaler()),
    ])
    category_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore")),
    ])
    prep = ColumnTransformer([
        ("numeric", numeric_pipe, numeric),
        ("categorical", category_pipe, categorical),
    ])
    if model_name == "Logistic Regression":
        model = LogisticRegression(max_iter=1500, class_weight="balanced")
    else:
        model = RandomForestClassifier(
            n_estimators=350, min_samples_leaf=3, class_weight="balanced_subsample",
            random_state=42, n_jobs=-1,
        )
    return Pipeline([("features", prep), ("model", model)])


def load_data(upload):
    if upload is not None:
        return pd.read_csv(upload)
    csv_path = APP_DIR / "data" / "European_Bank.csv"
    return pd.read_csv(csv_path) if csv_path.exists() else None


def plot(fig, height=500):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=55, b=10), font=dict(size=13))
    st.plotly_chart(fig, use_container_width=True)


def churn_summary(frame: pd.DataFrame, field: str) -> pd.DataFrame:
    result = frame.groupby(field, observed=True)[TARGET].agg(["mean", "size"]).reset_index()
    return result.rename(columns={"mean": "Rate", "size": "Customers"})


st.markdown("""
<style>
@keyframes titleGlow {
  0%, 100% { text-shadow: 0 0 12px rgba(79, 209, 197, .22), 0 0 28px rgba(56, 120, 168, .16); }
  50% { text-shadow: 0 0 22px rgba(79, 209, 197, .62), 0 0 48px rgba(56, 120, 168, .38); }
}
@keyframes titleSweep {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}
@keyframes floatOrb {
  0%, 100% { transform: translate3d(0, 0, 0) scale(1); }
  50% { transform: translate3d(10px, -18px, 0) scale(1.08); }
}
@keyframes pulseDot {
  0%, 100% { box-shadow: 0 0 5px #4fd1c5; opacity: .8; }
  50% { box-shadow: 0 0 15px #4fd1c5, 0 0 25px #4fd1c5; opacity: 1; }
}
.churn-hero {
  position: relative; overflow: hidden; min-height: 205px; padding: 30px 34px;
  margin: 4px 0 24px; border-radius: 22px;
  background: radial-gradient(ellipse at 12% 0%, rgba(44,122,123,.30), transparent 44%),
              radial-gradient(ellipse at 92% 105%, rgba(56,120,168,.28), transparent 45%),
              linear-gradient(120deg, rgba(18,34,48,.98), rgba(17,27,42,.96));
  border: 1px solid rgba(127, 220, 214, .20);
  box-shadow: 0 12px 42px rgba(0,0,0,.22), inset 0 0 30px rgba(79,209,197,.035);
}
.churn-hero-copy { position: relative; z-index: 2; max-width: 780px; }
.churn-kicker { color: #9de8df; font-size: .76rem; letter-spacing: .20em; font-weight: 800; text-transform: uppercase; }
.churn-title { margin: 9px 0 7px; color: #f4fbff; font-size: clamp(2rem, 4vw, 3.35rem); line-height: 1.08; font-weight: 850; animation: titleGlow 3.8s ease-in-out infinite; }
.churn-title span { background: linear-gradient(100deg, #fff 5%, #92f4e6 28%, #8ebcff 50%, #fff 68%, #92f4e6 88%); background-size: 200% auto; color: transparent; -webkit-background-clip: text; background-clip: text; animation: titleSweep 7s linear infinite; }
.churn-subtitle { color: #c1cfdd; font-size: 1rem; margin: 0; }
.churn-status { display: inline-flex; align-items: center; gap: 9px; margin-top: 18px; padding: 7px 12px; border: 1px solid rgba(157,232,223,.22); border-radius: 999px; color: #c7f4ee; background: rgba(20,54,62,.58); font-size: .78rem; letter-spacing: .04em; }
.churn-status-dot { width: 8px; height: 8px; border-radius: 50%; background: #4fd1c5; animation: pulseDot 1.8s ease-in-out infinite; }
.churn-orb { position: absolute; display: grid; place-items: center; border-radius: 50%; color: rgba(191,245,239,.84); border: 1px solid rgba(157,232,223,.24); background: radial-gradient(circle at 35% 30%, rgba(116,231,220,.28), rgba(35,92,111,.08) 70%); box-shadow: 0 0 28px rgba(79,209,197,.12), inset 0 0 20px rgba(79,209,197,.1); animation: floatOrb 6s ease-in-out infinite; }
.churn-orb.one { width: 82px; height: 82px; right: 20%; top: 22px; font-size: 1.65rem; }
.churn-orb.two { width: 54px; height: 54px; right: 9%; top: 105px; font-size: 1.1rem; animation-delay: -2s; }
.churn-orb.three { width: 34px; height: 34px; right: 34%; top: 132px; font-size: .8rem; animation-delay: -4s; }
[data-testid="stMetric"] { border: 1px solid rgba(127,220,214,.13); border-radius: 15px; padding: 13px 16px; background: linear-gradient(145deg, rgba(37,51,66,.50), rgba(24,34,47,.38)); transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease; }
[data-testid="stMetric"]:hover { transform: translateY(-3px); border-color: rgba(127,220,214,.44); box-shadow: 0 8px 25px rgba(25,150,145,.12); }
[data-testid="stPlotlyChart"] { border-radius: 14px; }
@media (prefers-reduced-motion: reduce) {
  .churn-title, .churn-title span, .churn-orb, .churn-status-dot { animation: none !important; }
  [data-testid="stMetric"] { transition: none !important; }
}
</style>
<div class="churn-hero">
  <div class="churn-orb one">✦</div><div class="churn-orb two">⌁</div><div class="churn-orb three">●</div>
  <div class="churn-hero-copy">
    <div class="churn-kicker">Customer analytics · risk intelligence</div>
    <div class="churn-title">Bank Churn <span>Intelligence</span></div>
    <p class="churn-subtitle">Explore customer patterns, evaluate churn models, and interactively examine risk scenarios.</p>
    <div class="churn-status"><span class="churn-status-dot"></span> MODEL WORKSPACE · LIVE INTERACTIVE VIEW</div>
  </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Dashboard controls")
    uploaded = st.file_uploader("Upload churn data (CSV)", type="csv")
    model_name = st.selectbox("Scoring model", ["Random Forest", "Logistic Regression"])
    threshold = st.slider("Churn alert threshold", 0.05, 0.95, 0.50, 0.01)

data = load_data(uploaded)
if data is None:
    st.info("Upload the assignment CSV or place European_Bank.csv in the data folder beside app.py.")
    st.stop()
data.columns = data.columns.astype(str).str.strip()
if TARGET not in data.columns:
    st.error("The data needs an Exited column containing 0 and 1.")
    st.stop()
data[TARGET] = pd.to_numeric(data[TARGET], errors="coerce")
data = data.dropna(subset=[TARGET])
data = data[data[TARGET].isin([0, 1])].copy()
y = data[TARGET].astype(int)
base_features = [c for c in data.columns if c not in IDENTIFIERS | {TARGET}]
base_features = [c for c in base_features if data[c].nunique(dropna=False) > 1]
X = add_features(data[base_features])
if X.empty or y.nunique() != 2 or y.value_counts().min() < 2:
    st.error("The dataset needs predictor columns and at least two examples of both target classes.")
    st.stop()

# Segment filters apply to descriptive charts. Holdout diagnostics use all rows.
filtered = data.copy()
with st.sidebar:
    st.divider()
    st.subheader("Customer segment")
    for field in ["Geography", "Gender"]:
        if field in data:
            opts = sorted(data[field].dropna().astype(str).unique())
            selected = st.multiselect(field, opts, default=opts)
            filtered = filtered[filtered[field].astype(str).isin(selected)]
    if "IsActiveMember" in data:
        activity = st.multiselect("Engagement", ["Inactive", "Active"], default=["Inactive", "Active"])
        active_values = [v for v, label in [(0, "Inactive"), (1, "Active")] if label in activity]
        filtered = filtered[filtered.IsActiveMember.isin(active_values)]
    if "Age" in data and data.Age.nunique() > 1:
        lo, hi = int(data.Age.min()), int(data.Age.max())
        age_range = st.slider("Age range", lo, hi, (lo, hi))
        filtered = filtered[filtered.Age.between(*age_range)]
if filtered.empty:
    st.warning("No customers match the filters. Widen the sidebar selections.")
    st.stop()

data_hash = hashlib.sha1(pd.util.hash_pandas_object(data, index=True).values.tobytes()).hexdigest()
model_key = f"{data_hash}|{model_name}"
refresh = st.sidebar.button("Train / refresh model", type="primary")
if st.session_state.get("model_key") != model_key or refresh:
    with st.spinner(f"Training {model_name} on a stratified split…"):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        holdout = build_pipeline(X_train, model_name)
        holdout.fit(X_train, y_train)
        holdout_prob = holdout.predict_proba(X_test)[:, 1]
        full_model = build_pipeline(X, model_name)
        full_model.fit(X, y)
    st.session_state.update(
        model_key=model_key, full_model=full_model, y_test=y_test.to_numpy(),
        holdout_prob=holdout_prob,
    )

prob = st.session_state.holdout_prob
y_test = st.session_state.y_test
pred = (prob >= threshold).astype(int)
auc = roc_auc_score(y_test, prob)
precision = precision_score(y_test, pred, zero_division=0)
recall = recall_score(y_test, pred, zero_division=0)
f1 = f1_score(y_test, pred, zero_division=0)

overview, patterns, diagnostics, simulator, explorer = st.tabs(
    ["Overview", "Explore patterns", "Model diagnostics", "Risk simulator", "Data explorer"]
)

with overview:
    churn_rate = float(filtered[TARGET].mean())
    churners = int(filtered[TARGET].sum())
    st.subheader("Portfolio snapshot")
    a, b, c, d = st.columns(4)
    a.metric("Customers in segment", f"{len(filtered):,}")
    b.metric("Churn rate", f"{churn_rate:.1%}", delta=f"{churn_rate - float(y.mean()):+.1%} vs all customers")
    c.metric("Churned customers", f"{churners:,}")
    d.metric("Retained customers", f"{len(filtered) - churners:,}")

    left, right = st.columns(2)
    with left:
        pie = filtered[TARGET].map({0: "Retained", 1: "Churned"}).value_counts().rename_axis("Outcome").reset_index(name="Customers")
        fig = px.pie(pie, names="Outcome", values="Customers", hole=.6, title="Customer outcome mix",
                     color="Outcome", color_discrete_map={"Retained": "#3878A8", "Churned": "#F06449"})
        fig.update_traces(textinfo="label+percent")
        plot(fig)
    with right:
        if "Age" in filtered:
            view = filtered.assign(Outcome=filtered[TARGET].map({0: "Retained", 1: "Churned"}))
            fig = px.histogram(view, x="Age", color="Outcome", nbins=24, barmode="overlay",
                               marginal="box", opacity=.7, title="Age distribution by outcome")
            plot(fig)

    left, right = st.columns(2)
    with left:
        if "Geography" in filtered:
            geo = churn_summary(filtered, "Geography")
            fig = px.bar(geo, x="Geography", y="Rate", color="Rate", text=geo.Rate.map(lambda n: f"{n:.1%}"),
                         hover_data={"Customers": True, "Rate": ":.1%"}, color_continuous_scale="Tealrose",
                         title="Churn rate by geography")
            fig.update_yaxes(tickformat=".0%", title="Churn rate")
            plot(fig)
        elif "NumOfProducts" in filtered:
            pass
    with right:
        if {"Balance", "EstimatedSalary"}.issubset(filtered.columns):
            scatter = filtered.sample(min(len(filtered), 3000), random_state=42).copy()
            scatter["Outcome"] = scatter[TARGET].map({0: "Retained", 1: "Churned"})
            fig = px.scatter(scatter, x="EstimatedSalary", y="Balance", color="Outcome",
                             size="NumOfProducts" if "NumOfProducts" in scatter else None,
                             opacity=.6, render_mode="webgl", title="Balance vs salary (sample up to 3,000)")
            plot(fig)

    st.subheader("Segment churn rates")
    cols = st.columns(3)
    for col, field in zip(cols, ["IsActiveMember", "NumOfProducts", "Gender"]):
        if field in filtered:
            summary = churn_summary(filtered, field)
            summary[field] = summary[field].astype(str)
            fig = px.bar(summary, x=field, y="Rate", color="Rate", text=summary.Rate.map(lambda n: f"{n:.1%}"),
                         hover_data={"Customers": True, "Rate": ":.1%"}, title=f"Churn by {field}")
            fig.update_yaxes(tickformat=".0%", title="Churn rate")
            with col:
                plot(fig, 380)

with patterns:
    st.subheader("Explore customer behavior and segments")
    st.caption("Descriptive associations help generate questions; they do not establish causes.")
    categories = [c for c in ["Geography", "Gender", "NumOfProducts", "IsActiveMember", "HasCrCard", "Tenure"] if c in filtered]
    if categories:
        group = st.selectbox("Group customers by", categories)
        summary = churn_summary(filtered, group)
        summary[group] = summary[group].astype(str)
        fig = px.bar(summary, x=group, y="Rate", color="Customers", text=summary.Rate.map(lambda n: f"{n:.1%}"),
                     hover_data={"Customers": True, "Rate": ":.1%"}, title=f"Churn rate by {group}", color_continuous_scale="Blues")
        fig.update_yaxes(tickformat=".0%", title="Churn rate")
        plot(fig)

    left, right = st.columns(2)
    with left:
        if {"NumOfProducts", "IsActiveMember"}.issubset(filtered.columns):
            heat = filtered.pivot_table(index="NumOfProducts", columns="IsActiveMember", values=TARGET, aggfunc="mean")
            fig = px.imshow(heat, text_auto=".1%", aspect="auto", color_continuous_scale="RdYlBu_r",
                            title="Churn rate: activity × product count", labels=dict(color="Churn rate"))
            fig.update_coloraxes(colorbar_tickformat=".0%")
            plot(fig)
    with right:
        if {"Geography", "Gender"}.issubset(filtered.columns):
            tree = filtered.assign(Outcome=filtered[TARGET].map({0: "Retained", 1: "Churned"}))
            fig = px.treemap(tree, path=["Geography", "Gender", "Outcome"], color="Exited",
                             color_continuous_scale="RdYlBu_r", title="Portfolio composition")
            plot(fig)

    numeric = list(filtered.select_dtypes(include=np.number).columns)
    numeric = [c for c in numeric if c != TARGET]
    if numeric:
        xcol, ycol = st.columns(2)
        with xcol:
            x_axis = st.selectbox("Scatterplot horizontal axis", numeric, key="scatter_x")
        with ycol:
            y_choices = [c for c in numeric if c != x_axis]
            y_axis = st.selectbox("Scatterplot vertical axis", y_choices or numeric, key="scatter_y")
        view = filtered.sample(min(4000, len(filtered)), random_state=42).copy()
        view["Outcome"] = view[TARGET].map({0: "Retained", 1: "Churned"})
        fig = px.scatter(view, x=x_axis, y=y_axis, color="Outcome", opacity=.6,
                         marginal_x="histogram", marginal_y="box", render_mode="webgl",
                         title=f"{y_axis} vs {x_axis}")
        plot(fig)
        corr = filtered[numeric + [TARGET]].corr(numeric_only=True)
        fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                        title="Numeric feature correlation heatmap")
        plot(fig, 520)

    if "Age" in filtered:
        age_data = filtered.assign(Outcome=filtered[TARGET].map({0: "Retained", 1: "Churned"}))
        fig = px.violin(age_data, x="Outcome", y="Age", color="Outcome", box=True, points="outliers",
                        title="Age spread by churn outcome")
        plot(fig)

with diagnostics:
    st.subheader("Model diagnostics")
    st.caption(f"{model_name} · stratified 80/20 holdout · alert threshold {threshold:.2f}")
    metric_cols = st.columns(7)
    values = [
        ("Accuracy", accuracy_score(y_test, pred)), ("Precision", precision),
        ("Recall", recall), ("F1", f1), ("ROC-AUC", auc),
        ("Avg precision", average_precision_score(y_test, prob)),
        ("Brier score", brier_score_loss(y_test, prob)),
    ]
    for col, (label, value) in zip(metric_cols, values):
        col.metric(label, f"{value:.3f}")
    st.caption("Precision, recall, F1 and confusion counts change with the threshold. ROC-AUC and average precision use probabilities. Lower Brier scores indicate better probability calibration.")

    left, right = st.columns(2)
    with left:
        cm = confusion_matrix(y_test, pred, labels=[0, 1])
        fig = px.imshow(cm, text_auto=True, x=["Retained", "Churned"], y=["Retained", "Churned"],
                        labels=dict(x="Predicted", y="Actual", color="Customers"), color_continuous_scale="Blues",
                        title="Confusion matrix")
        plot(fig)
    with right:
        fpr, tpr, _ = roc_curve(y_test, prob)
        fig = go.Figure()
        fig.add_scatter(x=fpr, y=tpr, mode="lines", name=f"ROC-AUC {auc:.3f}", line=dict(width=3, color="#E76F51"))
        fig.add_scatter(x=[0, 1], y=[0, 1], mode="lines", name="Chance", line=dict(dash="dash"))
        fig.update_layout(title="ROC curve", xaxis_title="False positive rate", yaxis_title="True positive rate")
        plot(fig)

    left, right = st.columns(2)
    with left:
        pcurve, rcurve, _ = precision_recall_curve(y_test, prob)
        fig = go.Figure(go.Scatter(x=rcurve, y=pcurve, mode="lines", name="Precision–recall", line=dict(width=3)))
        fig.update_layout(title="Precision–recall curve", xaxis_title="Recall", yaxis_title="Precision",
                          xaxis=dict(range=[0, 1]), yaxis=dict(range=[0, 1]))
        plot(fig)
    with right:
        observed, predicted = calibration_curve(y_test, prob, n_bins=10, strategy="quantile")
        fig = go.Figure()
        fig.add_scatter(x=predicted, y=observed, mode="lines+markers", name="Model")
        fig.add_scatter(x=[0, 1], y=[0, 1], mode="lines", name="Ideal", line=dict(dash="dash"))
        fig.update_layout(title="Probability calibration", xaxis_title="Mean predicted probability",
                          yaxis_title="Observed churn rate", xaxis=dict(range=[0, 1]), yaxis=dict(range=[0, 1]))
        plot(fig)

    cuts = np.linspace(.05, .95, 91)
    sweep = []
    for cut in cuts:
        flags = (prob >= cut).astype(int)
        sweep.append({"Threshold": cut, "Precision": precision_score(y_test, flags, zero_division=0),
                      "Recall": recall_score(y_test, flags, zero_division=0),
                      "F1": f1_score(y_test, flags, zero_division=0)})
    sweep = pd.DataFrame(sweep).melt("Threshold", var_name="Metric", value_name="Score")
    fig = px.line(sweep, x="Threshold", y="Score", color="Metric", title="Threshold trade-offs")
    fig.add_vline(x=threshold, line_dash="dash", line_color="#F06449", annotation_text="Current threshold")
    fig.update_yaxes(range=[0, 1])
    plot(fig)

    try:
        fitted = st.session_state.full_model
        names = fitted.named_steps["features"].get_feature_names_out()
        estimator = fitted.named_steps["model"]
        importance = np.abs(estimator.coef_[0]) if hasattr(estimator, "coef_") else estimator.feature_importances_
        top = pd.DataFrame({"Feature": names, "Importance": importance}).nlargest(18, "Importance").sort_values("Importance")
        top["Feature"] = top["Feature"].str.replace(r"^(numeric|categorical)__", "", regex=True)
        fig = px.bar(top, x="Importance", y="Feature", orientation="h", color="Importance",
                     color_continuous_scale="Tealrose", title="Top model feature contributions")
        plot(fig, 530)
        st.caption("Feature importance describes this fitted model; it is not causal evidence.")
    except Exception as exc:
        st.warning(f"Feature importance unavailable: {exc}")

with simulator:
    st.subheader("Customer risk simulator")
    st.write("Set a customer profile to see the estimated probability and how modeled risk varies across activity and product scenarios.")
    defaults = {}
    for field in base_features:
        if pd.api.types.is_numeric_dtype(data[field]):
            defaults[field] = float(data[field].median())
        else:
            mode = data[field].mode(dropna=True)
            defaults[field] = str(mode.iloc[0]) if not mode.empty else ""
    with st.form("customer_profile"):
        profile = {}
        cols = st.columns(3)
        for i, field in enumerate(base_features):
            with cols[i % 3]:
                if pd.api.types.is_numeric_dtype(data[field]):
                    low, high = float(data[field].min()), float(data[field].max())
                    if high <= low:
                        high = low + 1
                    profile[field] = st.number_input(field, min_value=low, max_value=high,
                                                     value=min(max(defaults[field], low), high))
                else:
                    options = sorted(data[field].dropna().astype(str).unique())
                    profile[field] = st.selectbox(field, options or [""])
        submit = st.form_submit_button("Calculate customer risk", type="primary")
    if submit:
        one = add_features(pd.DataFrame([profile])).reindex(columns=X.columns)
        risk = float(st.session_state.full_model.predict_proba(one)[0, 1])
        c1, c2 = st.columns([1, 2])
        with c1:
            c1.metric("Estimated churn probability", f"{risk:.1%}",
                      delta="Above threshold" if risk >= threshold else "Below threshold",
                      delta_color="inverse")
            c1.write("Churn flag:", "Likely churn risk" if risk >= threshold else "Below threshold")
            gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=risk * 100, number={"suffix": "%"},
                title={"text": "Churn risk"},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#F06449"},
                       "steps": [{"range": [0, threshold * 100], "color": "#D9EEE8"},
                                 {"range": [threshold * 100, 100], "color": "#FCE2D9"}],
                       "threshold": {"line": {"color": "#333", "width": 3}, "value": threshold * 100}},
            ))
            plot(gauge, 360)
        if {"NumOfProducts", "IsActiveMember"}.issubset(profile):
            rows = []
            for active in sorted(data.IsActiveMember.dropna().unique()):
                for product_count in sorted(data.NumOfProducts.dropna().unique()):
                    scenario = profile.copy()
                    scenario["IsActiveMember"] = active
                    scenario["NumOfProducts"] = product_count
                    sx = add_features(pd.DataFrame([scenario])).reindex(columns=X.columns)
                    rows.append({"Active member": str(active), "Products": product_count,
                                 "Risk": float(st.session_state.full_model.predict_proba(sx)[0, 1])})
            with c2:
                fig = px.density_heatmap(pd.DataFrame(rows), x="Products", y="Active member", z="Risk",
                                         histfunc="avg", text_auto=".1%", color_continuous_scale="RdYlBu_r",
                                         title="What-if risk: activity × product count")
                fig.update_coloraxes(colorbar_tickformat=".0%")
                plot(fig, 360)
        st.caption("These are model sensitivity scenarios, not the causal effect of changing customer behavior.")

with explorer:
    st.subheader("Data explorer")
    st.caption(f"Showing {len(filtered):,} of {len(data):,} rows after filters.")
    st.dataframe(filtered.head(500), use_container_width=True, hide_index=True)
    quality = pd.DataFrame({
        "Column": data.columns, "Data type": data.dtypes.astype(str).values,
        "Missing": data.isna().sum().values, "Distinct values": data.nunique(dropna=True).values,
    })
    st.markdown("#### Data quality profile")
    st.dataframe(quality, use_container_width=True, hide_index=True)
    st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"),
                       file_name="filtered_bank_customers.csv", mime="text/csv")

st.divider()
st.caption("Educational decision-support demo. Validate calibration, fairness, and data freshness before any real customer use.")
st.subheader("About the Author")
st.markdown(
    "My name is **T. Bhanu Karthik**, and I am a **Data Science student**. "
    "I created this project to apply data analysis, machine learning, and interactive visualization "
    "to the study of bank customer churn and retention."
)
