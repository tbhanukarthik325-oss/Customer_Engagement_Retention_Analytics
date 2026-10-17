import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Customer Retention Analytics",
    page_icon="📊",
    layout="wide"
)



st.markdown("""
<style>

/* Neon sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #05070D, #0B1120, #0F172A);
    border-right: 1px solid #2563EB;
}

/* Sidebar headings */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #38BDF8 !important;
    text-shadow: 0 0 8px rgba(56, 189, 248, 0.5);
}

/* Sidebar labels */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: #FFFFFF !important;
}

/* Highlight sidebar controls */
[data-testid="stSidebar"] input:focus {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 8px rgba(56, 189, 248, 0.5);
}

/* Main black background */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #05070D;
    color: #FFFFFF;
}

/* Neon blue headings */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #38BDF8 !important;
    text-shadow: 0 0 8px rgba(56, 189, 248, 0.25);
}

/* Main text */
.stApp p,
.stApp li,
.stApp label {
    color: #E5E7EB;
}

/* Dark sidebar */
[data-testid="stSidebar"] {
    background-color: #0B1120;
    border-right: 1px solid #1E3A5F;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #FFFFFF !important;
}

/* Neon KPI cards */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #111827, #0B1220);
    border: 1px solid #2563EB;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 0 12px rgba(37, 99, 235, 0.12);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    animation: fadeInUp 0.7s ease both;
}

/* KPI hover effect */
[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
}

/* KPI labels */
[data-testid="stMetricLabel"] {
    color: #CBD5E1 !important;
}

/* KPI values */
[data-testid="stMetricValue"] {
    color: #38BDF8 !important;
    font-weight: bold;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #2563EB, #0284C7);
    color: white !important;
    border: 1px solid #38BDF8;
    border-radius: 8px;
    padding: 8px 16px;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    border-color: #7DD3FC;
}

/* Input fields */
[data-testid="stSelectbox"] div,
[data-testid="stMultiSelect"] div {
    border-radius: 8px;
}

/* Smooth entrance for KPI cards */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Respect reduced-motion preferences */
@media (prefers-reduced-motion: reduce) {
    [data-testid="stMetric"] {
        animation: none;
        transition: none;
    }
}

/* Neon dashboard title */
.stApp h1 {
    color: #38BDF8 !important;
    text-shadow:
        0 0 5px #0284C7,
        0 0 10px #0284C7,
        0 0 20px rgba(56, 189, 248, 0.7);
    animation: titleGlow 1.5s ease-in-out infinite alternate;
}

@keyframes titleGlow {
    from {
        text-shadow: 0 0 5px #0284C7;
    }
    to {
        text-shadow:
            0 0 12px #38BDF8,
            0 0 24px rgba(56, 189, 248, 0.8);
    }
}

@media (prefers-reduced-motion: reduce) {
    .stApp h1 {
        animation: none;
    }
}

/* Professional KPI card layout */
[data-testid="stMetric"] {
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #2563EB;
    background: linear-gradient(145deg, #0B1220, #111827);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

/* Lift the cards on hover */
[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 20px rgba(0, 191, 255, 0.45);
}

/* KPI labels */
[data-testid="stMetricLabel"] {
    color: #CBD5E1 !important;
    font-size: 14px !important;
}

/* KPI values */
[data-testid="stMetricValue"] {
    color: #38BDF8 !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}

/* Dashboard section headings */
.stApp h2,
.stApp h3 {
    color: #38BDF8 !important;
    border-bottom: 1px solid rgba(56, 189, 248, 0.35);
    padding-bottom: 8px;
    margin-top: 22px;
    text-shadow: 0 0 8px rgba(56, 189, 248, 0.25);
}

/* Subtle divider styling */
.stApp hr {
    border: none;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        #2563EB,
        #38BDF8,
        transparent
    );
    margin: 24px 0;
}

</style>
""", unsafe_allow_html=True)

# Dashboard title
st.title("📊 Customer Retention Analytics")
st.subheader("Customer Engagement & Product Utilization Intelligence")

st.markdown("""
Explore customer engagement, product utilization, and retention
patterns through interactive analytics.
""")

# Keep the rest of your existing dashboard code below

st.markdown(
    '<div class="main-title">📊 Customer Engagement & Retention Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Customer Engagement, Product Utilization & Retention Strategy'
    '</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Customer Engagement, Product Utilization & Retention Strategy"
)

st.write(
    """
    This dashboard analyzes customer engagement, product utilization,
    financial commitment, and relationship strength to understand
    customer retention patterns.
    """
)

# Load analysis dataset

df = pd.read_csv("data/customer_retention_analysis.csv")

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("🧭 Dashboard Navigation")

st.sidebar.markdown(
    "Use the options below to explore different areas of the analysis."
)

# =========================================================
# QUICK NAVIGATION
# =========================================================

st.sidebar.subheader("📌 Quick Navigation")

st.sidebar.markdown("""
<a href="#executive-overview">📊 Executive Overview</a><br>
<a href="#customer-engagement">👤 Customer Behavior</a><br>
<a href="#product-utilization">📦 Product Utilization</a><br>
<a href="#financial-analysis">💰 Financial Analysis</a><br>
<a href="#relationship-analysis">💳 Relationship Analysis</a><br>
<a href="#geography-analysis">🌍 Geography & Tenure</a><br>
<a href="#customer-explorer">🔎 Customer Explorer</a><br>
<a href="#executive-insights">💡 Executive Insights</a><br>
<a href="#kpi-methodology">📘 KPI Methodology</a>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.info(
    "📊 **Dataset**\n\n"
    f"Customers: **{len(df):,}**\n\n"
    f"Regions: **{df['Geography'].nunique()}**"
)

st.sidebar.markdown("---")

st.sidebar.subheader("ℹ️ Project Information")

st.sidebar.write(
    "This dashboard analyzes customer engagement, "
    "product utilization, financial commitment, "
    "and observed exit patterns."
)

st.sidebar.caption(
    "Customer Engagement & Product Utilization Analytics"
)

# =========================================================
# SELECTED SECTION INDICATOR
# =========================================================


# =========================================================
# ACTIVE SECTION INDICATOR
# =========================================================


st.success("Dataset loaded successfully!")

# Executive KPI Section

st.markdown('<div id="executive-overview"></div>', unsafe_allow_html=True)

st.header("📌 Executive Overview")

# KPI calculations
overall_exit_rate = df["Exited"].mean() * 100

active_customers = df[df["IsActiveMember"] == 1]

engagement_retention_ratio = (
    (active_customers["Exited"] == 0).mean() * 100
)

product_depth_index = df["NumOfProducts"].mean()

high_balance_threshold = df["Balance"].quantile(0.75)

high_balance_disengagement_rate = (
    (
        df.loc[
            df["Balance"] >= high_balance_threshold,
            "IsActiveMember"
        ] == 0
    ).mean() * 100
)

credit_card_customers = df[df["HasCrCard"] == 1]

credit_card_stickiness = (
    (credit_card_customers["Exited"] == 0).mean() * 100
)

relationship_strength_index = (
    df["RelationshipStrengthScore"].mean()
)

# KPI cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Overall Exit Rate",
        f"{overall_exit_rate:.2f}%"
    )

with col2:
    st.metric(
        "Engagement Retention Ratio",
        f"{engagement_retention_ratio:.2f}%"
    )

with col3:
    st.metric(
        "Product Depth Index",
        f"{product_depth_index:.2f}"
    )

st.markdown("---")

st.subheader("📌 Executive Summary")

st.markdown("""
<div style="
    background: linear-gradient(135deg, #0B1220, #111827);
    border: 1px solid #38BDF8;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
">
    <h4 style="color: #38BDF8;">Key Business Findings</h4>
    <p style="color: white;">
        This dashboard explores customer engagement, product utilization,
        financial relationships, and customer exit patterns.
    </p>
    <p style="color: white;">
        The analysis helps identify customer segments with different levels
        of product usage and retention, supporting more informed business decisions.
    </p>
    <p style="color: #93C5FD;">
        <b>Objective:</b> Understand customer behavior and identify opportunities
        to improve engagement and retention.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📊 Customer Engagement Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="
        background: #0B1220;
        border: 1px solid #38BDF8;
        border-radius: 12px;
        padding: 18px;
        min-height: 150px;
    ">
        <h4 style="color: #38BDF8;">👥 Customer Engagement</h4>
        <p style="color: white;">
            Explore customer activity and understand differences
            between customer groups.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background: #0B1220;
        border: 1px solid #38BDF8;
        border-radius: 12px;
        padding: 18px;
        min-height: 150px;
    ">
        <h4 style="color: #38BDF8;">📦 Product Utilization</h4>
        <p style="color: white;">
            Examine product usage patterns and compare the number
            of products held by customers.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
        background: #0B1220;
        border: 1px solid #38BDF8;
        border-radius: 12px;
        padding: 18px;
        min-height: 150px;
    ">
        <h4 style="color: #38BDF8;">🎯 Customer Retention</h4>
        <p style="color: white;">
            Analyze customer exit patterns to identify groups
            that may need further investigation.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.subheader("📥 Download Analysis Data")

st.download_button(
    label="📥 Download Customer Data (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="customer_engagement_analysis.csv",
    mime="text/csv",
    use_container_width=True
)

st.markdown("---")
st.subheader("🎯 Customer Retention Insights")

# Calculate customer exit rate
exit_rate = (df["Exited"].mean() * 100)

st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, #0B1220, #111827);
        border: 1px solid #38BDF8;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
    ">
        <h4 style="color: #38BDF8;">Overall Customer Exit Rate</h4>
        <h2 style="color: white;">{exit_rate:.2f}%</h2>
        <p style="color: #CBD5E1;">
            This percentage represents the share of customers marked as exited
            in the dataset. Use it as a descriptive indicator of customer retention.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "High-Balance Disengagement",
        f"{high_balance_disengagement_rate:.2f}%"
    )

with col5:
    st.metric(
        "Credit Card Stickiness",
        f"{credit_card_stickiness:.2f}%"
    )

with col6:
    st.metric(
        "Relationship Strength",
        f"{relationship_strength_index:.2f} / 3"
    )


    # =========================================================
# CUSTOMER ENGAGEMENT ANALYSIS
# =========================================================

st.markdown('<div id="customer-engagement"></div>', unsafe_allow_html=True)
st.header("👥 Customer Engagement Analysis")

# Active vs Inactive Customers
activity_counts = (
    df["IsActiveMember"]
    .value_counts()
    .sort_index()
    .reset_index()
)

activity_counts.columns = ["IsActiveMember", "Customers"]

activity_counts["Engagement"] = activity_counts[
    "IsActiveMember"
].map({
    0: "Inactive",
    1: "Active"
})

# Exit rate by engagement
engagement_exit = (
    df.groupby("IsActiveMember")["Exited"]
    .mean()
    .reset_index()
)

engagement_exit["Engagement"] = engagement_exit[
    "IsActiveMember"
].map({
    0: "Inactive",
    1: "Active"
})

engagement_exit["ExitRate"] = (
    engagement_exit["Exited"] * 100
)

# Create two columns
col1, col2 = st.columns(2)

with col1:

    fig1 = px.bar(
        activity_counts,
        x="Engagement",
        y="Customers",
        title="Active vs Inactive Customers",
        text="Customers"
    )

    fig1.update_traces(
        textposition="outside"
    )

    fig1.update_yaxes(
        title="Number of Customers"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:

    fig2 = px.bar(
        engagement_exit,
        x="Engagement",
        y="ExitRate",
        title="Exit Rate by Customer Engagement",
        text="ExitRate"
    )

    fig2.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig2.update_yaxes(
        title="Exit Rate (%)"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )



    # Engagement and Product Depth

engagement_product_exit = (
    df.groupby(
        ["EngagementGroup", "ProductDepthGroup"]
    )["Exited"]
    .mean()
    .reset_index()
)

engagement_product_exit["ExitRate"] = (
    engagement_product_exit["Exited"] * 100
)

fig3 = px.bar(
    engagement_product_exit,
    x="EngagementGroup",
    y="ExitRate",
    color="ProductDepthGroup",
    barmode="group",
    title="Exit Rate by Engagement and Product Depth",
    text="ExitRate"
)

fig3.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig3.update_xaxes(
    title="Customer Engagement"
)

fig3.update_yaxes(
    title="Exit Rate (%)"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =========================================================
# PRODUCT UTILIZATION ANALYSIS
# =========================================================

st.markdown('<div id="product-utilization"></div>', unsafe_allow_html=True)
st.header("📦 Product Utilization Analysis")

# Customer distribution by number of products
product_counts = (
    df["NumOfProducts"]
    .value_counts()
    .sort_index()
    .reset_index()
)

product_counts.columns = [
    "NumOfProducts",
    "Customers"
]

# Exit rate by number of products
product_exit = (
    df.groupby("NumOfProducts")["Exited"]
    .agg(["count", "mean"])
    .reset_index()
)

product_exit.columns = [
    "NumOfProducts",
    "Customers",
    "ExitRate"
]

product_exit["ExitRate"] = (
    product_exit["ExitRate"] * 100
)

# Average product depth by customer status
product_depth_status = (
    df.groupby("Exited")["NumOfProducts"]
    .mean()
    .reset_index()
)

product_depth_status["CustomerStatus"] = (
    product_depth_status["Exited"]
    .map({
        0: "Retained",
        1: "Exited"
    })
)

# Create two columns
col1, col2 = st.columns(2)

with col1:

    fig4 = px.bar(
        product_counts,
        x="NumOfProducts",
        y="Customers",
        title="Customer Distribution by Number of Products",
        text="Customers"
    )

    fig4.update_traces(
        textposition="outside"
    )

    fig4.update_xaxes(
        title="Number of Products"
    )

    fig4.update_yaxes(
        title="Number of Customers"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

with col2:

    fig5 = px.bar(
        product_exit,
        x="NumOfProducts",
        y="ExitRate",
        title="Exit Rate by Number of Products",
        text="ExitRate"
    )

    fig5.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig5.update_xaxes(
        title="Number of Products"
    )

    fig5.update_yaxes(
        title="Exit Rate (%)"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )
    fig5.update_layout(
    template="plotly_dark",
    paper_bgcolor="#05070D",
    plot_bgcolor="#05070D",
    font=dict(
        color="#FFFFFF",
        family="Arial",
        size=12
    ),
    title_font=dict(
        color="#38BDF8",
        size=20
    ),
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    ),
    transition=dict(
        duration=700,
        easing="cubic-in-out"
    )
)

fig5.update_traces(
    marker_color=[
        "#00BFFF",
        "#2563EB",
        "#7C3AED",
        "#00E5FF"
    ],
    marker_line_color="#FFFFFF",
    marker_line_width=1,
    textfont=dict(
        color="#FFFFFF",
        size=13
    )
)


    # Average product depth by customer status

fig6 = px.bar(
    product_depth_status,
    x="CustomerStatus",
    y="NumOfProducts",
    title="Average Product Depth by Customer Status",
    text="NumOfProducts"
)
fig6.update_layout(
    template="plotly_dark",
    paper_bgcolor="#05070D",
    plot_bgcolor="#05070D",
    font=dict(
        color="#FFFFFF",
        family="Arial",
        size=12
    ),
    title_font=dict(
        color="#38BDF8",
        size=20
    ),
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    ),
    transition=dict(
        duration=300,
        easing="cubic-in-out"
    )
)

fig6.update_traces(
    marker_color="#2563EB",
    marker_line_color="#38BDF8",
    marker_line_width=1.5,
    textfont=dict(color="#FFFFFF")
)
fig6.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig6.update_xaxes(
    title="Customer Status"
)

fig6.update_yaxes(
    title="Average Number of Products"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# =========================================================
# FINANCIAL COMMITMENT & HIGH-BALANCE DISENGAGEMENT
# =========================================================

st.markdown('<div id="financial-analysis"></div>', unsafe_allow_html=True)
st.header("💰 Financial Commitment & High-Balance Customers")

# Average balance by customer status
balance_status = (
    df.groupby("Exited")["Balance"]
    .agg(["count", "mean", "median"])
    .reset_index()
)

balance_status["CustomerStatus"] = (
    balance_status["Exited"]
    .map({
        0: "Retained",
        1: "Exited"
    })
)

# High-balance threshold
high_balance_threshold = df["Balance"].quantile(0.75)

# High-balance customers
high_balance_customers = df[
    df["Balance"] >= high_balance_threshold
]

# High-balance disengaged customers
high_balance_disengaged = df[
    (df["Balance"] >= high_balance_threshold) &
    (df["IsActiveMember"] == 0)
]

# High-balance disengagement rate
high_balance_disengagement_rate = (
    (high_balance_customers["IsActiveMember"] == 0).mean()
    * 100
)

# Exit rate among high-balance disengaged customers
high_balance_disengaged_exit_rate = (
    high_balance_disengaged["Exited"].mean()
    * 100
)

# Overall exit rate
overall_exit_rate = df["Exited"].mean() * 100

# Comparison dataframe
financial_comparison = pd.DataFrame({
    "Customer Group": [
        "All Customers",
        "High-Balance Disengaged"
    ],
    "Exit Rate": [
        overall_exit_rate,
        high_balance_disengaged_exit_rate
    ]
})
col1, col2 = st.columns(2)

with col1:

    fig7 = px.bar(
        balance_status,
        x="CustomerStatus",
        y="mean",
        title="Average Balance by Customer Status",
        text="mean"
    )

    fig7.update_traces(
        texttemplate="%{text:,.2f}",
        textposition="outside"
    )

    fig7.update_xaxes(
        title="Customer Status"
    )

    fig7.update_yaxes(
        title="Average Balance"
    )

    fig7.update_layout(
        template="plotly_dark",
        paper_bgcolor="#05070D",
        plot_bgcolor="#05070D",
        font=dict(
            color="#FFFFFF",
            family="Arial",
            size=12
        ),
        title_font=dict(
            color="#38BDF8",
            size=20
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        transition=dict(
            duration=700,
            easing="cubic-in-out"
        )
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )

with col2:

    fig8 = px.bar(
        financial_comparison,
        x="Customer Group",
        y="Exit Rate",
        title="Exit Rate: All Customers vs High-Balance Disengaged",
        text="Exit Rate"
    )

    fig8.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig8.update_yaxes(
        title="Exit Rate (%)"
    )

    st.plotly_chart(
        fig8,
        use_container_width=True
    )
    st.subheader("🔎 High-Balance Customer Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "High-Balance Threshold",
        f"{high_balance_threshold:,.2f}"
    )

with col2:
    st.metric(
        "High-Balance Disengagement",
        f"{high_balance_disengagement_rate:.2f}%"
    )

with col3:
    st.metric(
        "Exit Rate of High-Balance Disengaged",
        f"{high_balance_disengaged_exit_rate:.2f}%"
    )

    # =========================================================
# CREDIT CARD & RELATIONSHIP STRENGTH ANALYSIS
# =========================================================

st.markdown('<div id="relationship-analysis"></div>', unsafe_allow_html=True)
st.header("💳 Credit Card & Relationship Strength")

# Credit card distribution
card_counts = (
    df["HasCrCard"]
    .value_counts()
    .sort_index()
    .reset_index()
)

card_counts.columns = [
    "HasCrCard",
    "Customers"
]

card_counts["CreditCardStatus"] = card_counts[
    "HasCrCard"
].map({
    0: "No Credit Card",
    1: "Has Credit Card"
})

# Exit rate by credit card ownership
card_exit = (
    df.groupby("HasCrCard")["Exited"]
    .mean()
    .reset_index()
)

card_exit["CreditCardStatus"] = card_exit[
    "HasCrCard"
].map({
    0: "No Credit Card",
    1: "Has Credit Card"
})

card_exit["ExitRate"] = (
    card_exit["Exited"] * 100
)

# Credit Card Stickiness
credit_card_customers = df[
    df["HasCrCard"] == 1
]

credit_card_stickiness = (
    (credit_card_customers["Exited"] == 0).mean()
    * 100
)
col1, col2 = st.columns(2)

with col1:

    fig9 = px.bar(
        card_counts,
        x="CreditCardStatus",
        y="Customers",
        title="Customer Distribution by Credit Card Ownership",
        text="Customers"
    )

    fig9.update_traces(
        textposition="outside"
    )

    fig9.update_xaxes(
        title="Credit Card Status"
    )

    fig9.update_yaxes(
        title="Number of Customers"
    )

    st.plotly_chart(
        fig9,
        use_container_width=True
    )

with col2:

    fig10 = px.bar(
        card_exit,
        x="CreditCardStatus",
        y="ExitRate",
        title="Exit Rate by Credit Card Ownership",
        text="ExitRate"
    )

    fig10.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig10.update_xaxes(
        title="Credit Card Status"
    )

    fig10.update_yaxes(
        title="Exit Rate (%)"
    )

    st.plotly_chart(
        fig10,
        use_container_width=True
    )
    st.metric(
    "💳 Credit Card Stickiness Score",
    f"{credit_card_stickiness:.2f}%"
)

    # Relationship Strength Score

relationship_exit = (
    df.groupby("RelationshipStrengthScore")["Exited"]
    .mean()
    .reset_index()
)

relationship_exit["ExitRate"] = (
    relationship_exit["Exited"] * 100
)

relationship_strength_index = (
    df["RelationshipStrengthScore"].mean()
)
fig11 = px.bar(
    relationship_exit,
    x="RelationshipStrengthScore",
    y="ExitRate",
    title="Exit Rate by Relationship Strength",
    text="ExitRate"
)

fig11.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig11.update_xaxes(
    title="Relationship Strength Score"
)

fig11.update_yaxes(
    title="Exit Rate (%)"
)

st.plotly_chart(
    fig11,
    use_container_width=True
)
st.metric(
    "🤝 Relationship Strength Index",
    f"{relationship_strength_index:.2f} / 3"
)

# =========================================================
# CUSTOMER BEHAVIORAL SEGMENTATION
# =========================================================

st.markdown('<div id="customer-behavioral-segmentation"></div>', unsafe_allow_html=True)
st.header("🎯 Customer Behavioral Segmentation")

# Create customer segments
df["CustomerSegment"] = np.select(
    [
        (df["EngagementGroup"] == "Active") &
        (df["ProductDepthGroup"] == "Multi-Product"),

        (df["EngagementGroup"] == "Active") &
        (df["ProductDepthGroup"] == "Single-Product"),

        (df["EngagementGroup"] == "Inactive") &
        (df["ProductDepthGroup"] == "Multi-Product"),

        (df["EngagementGroup"] == "Inactive") &
        (df["ProductDepthGroup"] == "Single-Product")
    ],
    [
        "Engaged & Multi-Product",
        "Engaged & Single-Product",
        "Disengaged & Multi-Product",
        "Disengaged & Single-Product"
    ],
    default="Other"
)

# Segment summary
segment_summary = (
    df.groupby("CustomerSegment")
    .agg(
        Customers=("CustomerId", "count"),
        AverageBalance=("Balance", "mean"),
        ExitRate=("Exited", "mean")
    )
    .reset_index()
)

segment_summary["ExitRate"] = (
    segment_summary["ExitRate"] * 100
)

# Segment distribution
segment_counts = (
    df["CustomerSegment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "CustomerSegment",
    "Customers"
]

col1, col2 = st.columns(2)

with col1:

    fig12 = px.bar(
        segment_counts,
        x="CustomerSegment",
        y="Customers",
        title="Customer Distribution by Behavioral Segment",
        text="Customers"
    )

    fig12.update_traces(
        textposition="outside"
    )

    fig12.update_xaxes(
        title="Customer Segment"
    )

    fig12.update_yaxes(
        title="Number of Customers"
    )

    st.plotly_chart(
        fig12,
        use_container_width=True
    )

with col2:

    fig13 = px.bar(
        segment_summary,
        x="CustomerSegment",
        y="ExitRate",
        title="Exit Rate by Customer Behavioral Segment",
        text="ExitRate"
    )

    fig13.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig13.update_xaxes(
        title="Customer Segment"
    )

    fig13.update_yaxes(
        title="Exit Rate (%)"
    )

    st.plotly_chart(
        fig13,
        use_container_width=True
    )
    st.subheader("📋 Segment Summary")

st.dataframe(
    segment_summary,
    use_container_width=True
)

# =========================================================
# INTERACTIVE CUSTOMER EXPLORER
# =========================================================

st.markdown('<div id="customer-explorer"></div>', unsafe_allow_html=True)
st.header("🔎 Interactive Customer Explorer")

st.write(
    "Use the filters below to explore customer behavior, "
    "product usage, financial commitment, and engagement."
)

# Filter columns
filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
    engagement_filter = st.selectbox(
        "Customer Engagement",
        ["All", "Active", "Inactive"]
    )

with filter_col2:
    product_filter = st.selectbox(
        "Number of Products",
        ["All"] + sorted(df["NumOfProducts"].unique().tolist())
    )

with filter_col3:
    balance_filter = st.number_input(
        "Minimum Balance",
        min_value=0.0,
        value=0.0,
        step=1000.0
    )

with filter_col4:
    salary_filter = st.number_input(
        "Minimum Estimated Salary",
        min_value=0.0,
        value=0.0,
        step=5000.0
    )

    # Apply filters
filtered_df = df.copy()

if engagement_filter != "All":
    engagement_value = 1 if engagement_filter == "Active" else 0
    filtered_df = filtered_df[
        filtered_df["IsActiveMember"] == engagement_value
    ]

if product_filter != "All":
    filtered_df = filtered_df[
        filtered_df["NumOfProducts"] == product_filter
    ]

filtered_df = filtered_df[
    filtered_df["Balance"] >= balance_filter
]

filtered_df = filtered_df[
    filtered_df["EstimatedSalary"] >= salary_filter
]

st.subheader("📊 Filtered Customer Overview")

st.metric(
    "Customers Matching Filters",
    f"{len(filtered_df):,}"
)

status_distribution = (
    filtered_df["Exited"]
    .map({
        0: "Retained",
        1: "Exited"
    })
    .value_counts()
    .reset_index()
)

status_distribution.columns = [
    "CustomerStatus",
    "Customers"
]

fig14 = px.pie(
    status_distribution,
    names="CustomerStatus",
    values="Customers",
    title="Customer Status Distribution"
)

fig14.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(
    fig14,
    use_container_width=True,
   key="explorer_status_pie_01"
)
status_distribution = (
    filtered_df["Exited"]
    .map({
        0: "Retained",
        1: "Exited"
    })
    .value_counts()
    .reset_index()
)

status_distribution.columns = [
    "CustomerStatus",
    "Customers"
]

fig14 = px.pie(
    status_distribution,
    names="CustomerStatus",
    values="Customers",
    title="Customer Status Distribution"
)

fig14.update_traces(
    textposition="inside",
    textinfo="percent+label"
)


st.subheader("💰 Financial Relationship")

fig15 = px.scatter(
    filtered_df,
    x="EstimatedSalary",
    y="Balance",
    color="CustomerSegment",
    size="NumOfProducts",
    hover_data=[
        "CustomerId",
        "Geography",
        "Age",
        "Exited"
    ],
    title="Salary vs Account Balance by Customer Segment",
    labels={
        "EstimatedSalary": "Estimated Salary",
        "Balance": "Account Balance",
        "CustomerSegment": "Customer Segment",
        "NumOfProducts": "Products"
    },
    opacity=0.65
)

fig15.update_layout(
    height=550,
    margin=dict(l=40, r=40, t=70, b=40)
)

st.plotly_chart(
    fig15,
    use_container_width=True,
    key="financial_scatter"
)

st.subheader("👤 Customer Details")

display_columns = [
    "CustomerId",
    "Surname",
    "Geography",
    "Gender",
    "Age",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
    "Exited",
    "CustomerSegment"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)
# =========================================================
# CUSTOMER GEOGRAPHY ANALYSIS
# =========================================================

st.markdown('<div id="geography-analysis"></div>', unsafe_allow_html=True)
st.header("🌍 Customer Geography Analysis")

st.write(
    "Explore customer distribution and observed exit rates across regions."
)

geography_summary = (
    df.groupby("Geography")
    .agg(
        Customers=("CustomerId", "count"),
        ExitRate=("Exited", "mean"),
        AverageBalance=("Balance", "mean")
    )
    .reset_index()
)

geography_summary["ExitRate"] = (
    geography_summary["ExitRate"] * 100
)

# ---------------------------------------------------------
# Geography Distribution - Donut Chart
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig16 = px.pie(
        geography_summary,
        names="Geography",
        values="Customers",
        hole=0.55,
        title="Customer Distribution by Geography"
    )

    fig16.update_traces(
        textinfo="percent+label"
    )

    fig16.update_layout(
        height=450
    )

    st.plotly_chart(
        fig16,
        use_container_width=True,
        key="geography_donut_01"
    )

with col2:

    fig17 = px.bar(
        geography_summary,
        x="Geography",
        y="ExitRate",
        text="ExitRate",
        title="Exit Rate by Geography"
    )

    fig17.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig17.update_yaxes(
        title="Exit Rate (%)",
        ticksuffix="%"
    )

    fig17.update_layout(
        height=450
    )

    st.plotly_chart(
        fig17,
        use_container_width=True,
        key="geography_exit_bar_01"
    )

# ---------------------------------------------------------
# Average Balance by Geography
# ---------------------------------------------------------

st.subheader("💰 Average Customer Balance by Geography")

fig18 = px.bar(
    geography_summary,
    x="Geography",
    y="AverageBalance",
    color="Geography",
    text="AverageBalance",
    title="Average Balance by Geography"
)

fig18.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig18.update_yaxes(
    title="Average Balance"
)

fig18.update_layout(
    height=450
)

st.plotly_chart(
    fig18,
    use_container_width=True,
    key="geography_balance_bar_01"
)
# =========================================================
# TENURE & RETENTION ANALYSIS
# =========================================================

st.header("⏳ Tenure & Retention Analysis")
st.markdown('<div id="tenure-retention-analysis"></div>', unsafe_allow_html=True)

st.write(
    "Explore observed exit rates across customer tenure and geography."
)

tenure_geo = (
    df.groupby(["Tenure", "Geography"])["Exited"]
    .mean()
    .reset_index()
)

tenure_geo["ExitRate"] = (
    tenure_geo["Exited"] * 100
)

# Convert to matrix for heatmap
tenure_heatmap = tenure_geo.pivot(
    index="Tenure",
    columns="Geography",
    values="ExitRate"
)

# Heatmap
fig19 = px.imshow(
    tenure_heatmap,
    text_auto=".2f",
    aspect="auto",
    title="Exit Rate Heatmap: Tenure vs Geography",
    labels={
        "x": "Geography",
        "y": "Tenure (Years)",
        "color": "Exit Rate (%)"
    }
)

fig19.update_layout(
    height=550,
    margin=dict(
        l=40,
        r=40,
        t=70,
        b=40
    )
)

st.plotly_chart(
    fig19,
    use_container_width=True,
    key="tenure_geography_heatmap_01"
)
st.subheader("📦 Customer Tenure Distribution by Status")

fig20 = px.box(
    df,
    x="Exited",
    y="Tenure",
    color="Exited",
    points="outliers",
    title="Tenure Distribution: Retained vs Exited Customers",
    labels={
        "Exited": "Customer Status",
        "Tenure": "Tenure (Years)"
    }
)

fig20.update_xaxes(
    tickmode="array",
    tickvals=[0, 1],
    ticktext=["Retained", "Exited"]
)

fig20.update_layout(
    height=500
)

st.plotly_chart(
    fig20,
    use_container_width=True,
    key="tenure_status_box_01"
)

# =========================================================
# AGE & GENDER ANALYSIS
# =========================================================

st.markdown('<div id="age-gender-analysis"></div>', unsafe_allow_html=True)
st.header("👤 Age & Gender Analysis")

st.write(
    "Explore customer age patterns and observed exit rates across gender."
)

# Age distribution
fig21 = px.violin(
    df,
    x="Exited",
    y="Age",
    color="Exited",
    box=True,
    points=False,
    title="Age Distribution by Customer Status",
    labels={
        "Exited": "Customer Status",
        "Age": "Age"
    }
)

fig21.update_xaxes(
    tickmode="array",
    tickvals=[0, 1],
    ticktext=["Retained", "Exited"]
)

fig21.update_layout(
    height=500
)

st.plotly_chart(
    fig21,
    use_container_width=True,
    key="age_status_violin_01"
)
# Gender and customer status
gender_status = (
    df.groupby(["Gender", "Exited"])
    .size()
    .reset_index(name="Customers")
)

gender_status["CustomerStatus"] = (
    gender_status["Exited"]
    .map({
        0: "Retained",
        1: "Exited"
    })
)

fig22 = px.bar(
    gender_status,
    x="Gender",
    y="Customers",
    color="CustomerStatus",
    barmode="stack",
    text="Customers",
    title="Customer Status Distribution by Gender"
)

fig22.update_traces(
    textposition="inside"
)

fig22.update_layout(
    height=500
)

st.plotly_chart(
    fig22,
    use_container_width=True,
    key="gender_status_stacked_01"
)

# =========================================================
# DYNAMIC EXECUTIVE INSIGHTS
# =========================================================

st.markdown('<div id="dynamic-executive-insights"></div>', unsafe_allow_html=True)
st.header("💡 Dynamic Executive Insights")

st.write(
    "Key observations generated dynamically from the customer engagement, "
    "product utilization, and financial data."
)

# ---------------------------------------------------------
# Dynamic calculations
# ---------------------------------------------------------

overall_exit_rate = df["Exited"].mean() * 100

active_exit_rate = (
    df.loc[df["IsActiveMember"] == 1, "Exited"].mean() * 100
)

inactive_exit_rate = (
    df.loc[df["IsActiveMember"] == 0, "Exited"].mean() * 100
)

active_inactive_gap = inactive_exit_rate - active_exit_rate

high_balance_disengaged = df[
    (df["Balance"] >= high_balance_threshold) &
    (df["IsActiveMember"] == 0)
]

high_balance_disengaged_count = len(high_balance_disengaged)

retained_product_avg = (
    df.loc[df["Exited"] == 0, "NumOfProducts"].mean()
)

exited_product_avg = (
    df.loc[df["Exited"] == 1, "NumOfProducts"].mean()
)

# ---------------------------------------------------------
# Insight Cards
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 Overall Exit Rate",
        f"{overall_exit_rate:.2f}%"
    )

with col2:
    st.metric(
        "🟢 Active Exit Rate",
        f"{active_exit_rate:.2f}%"
    )

with col3:
    st.metric(
        "🔴 Inactive Exit Rate",
        f"{inactive_exit_rate:.2f}%"
    )

with col4:
    st.metric(
        "💰 High-Balance Disengaged",
        f"{high_balance_disengaged_count:,}"
    )

# ---------------------------------------------------------
# Dynamic Insight Messages
# ---------------------------------------------------------

st.subheader("📌 Key Observations")

insight_col1, insight_col2 = st.columns(2)

with insight_col1:

    st.info(
        f"🟢 **Engagement Observation**\n\n"
        f"Active customers have an observed exit rate of "
        f"**{active_exit_rate:.2f}%**, while inactive customers have "
        f"an observed exit rate of **{inactive_exit_rate:.2f}%**. "
        f"The difference is **{active_inactive_gap:.2f} percentage points**."
    )

    st.success(
        f"📦 **Product Utilization Observation**\n\n"
        f"Retained customers have an average of "
        f"**{retained_product_avg:.2f} products**, compared with "
        f"**{exited_product_avg:.2f} products** among exited customers."
    )

with insight_col2:

    st.warning(
        f"💰 **High-Balance Disengagement Observation**\n\n"
        f"There are **{high_balance_disengaged_count:,} customers** "
        f"with balances at or above the 75th-percentile threshold "
        f"who are currently classified as inactive."
    )

    st.error(
        f"📈 **Dataset Exit Overview**\n\n"
        f"The overall observed exit rate in the dataset is "
        f"**{overall_exit_rate:.2f}%** across "
        f"**{len(df):,} customers**."
    )

    # =========================================================
# KPI DEFINITIONS & METHODOLOGY
# =========================================================

st.header("📘 KPI Definitions & Methodology")

st.write(
    "The following KPIs summarize customer engagement, product utilization, "
    "financial commitment, and relationship strength."
)

with st.expander("🔍 View KPI Definitions", expanded=False):

    st.markdown("""
    ### 🟢 1. Engagement Retention Ratio

    Measures the percentage of active customers who remained retained.

    **Formula:**

    `Engagement Retention Ratio = Retained Active Customers / Total Active Customers × 100`

    This metric describes the observed retention level among customers classified
    as active.

    ---

    ### 📦 2. Product Depth Index

    Measures the average number of products held by customers.

    **Formula:**

    `Product Depth Index = Average Number of Products per Customer`

    A higher value indicates greater average product holding within the dataset.

    ---

    ### 💰 3. High-Balance Disengagement Rate

    Measures the proportion of customers with high account balances who are
    classified as inactive.

    **Formula:**

    `High-Balance Disengagement Rate = High-Balance Inactive Customers / High-Balance Customers × 100`

    The high-balance threshold is defined using the 75th percentile of
    customer balances.

    ---

    ### 💳 4. Credit Card Stickiness Score

    Measures the percentage of customers with a credit card who remained retained.

    **Formula:**

    `Credit Card Stickiness Score = Retained Credit Card Customers / Total Credit Card Customers × 100`

    This provides a descriptive view of retention among credit-card holders.

    ---

    ### 🤝 5. Relationship Strength Index

    A simple analytical score based on three observable relationship indicators:

    - Active membership
    - Holding two or more products
    - Credit card ownership

    **Score range:** `0–3`

    Each qualifying characteristic contributes one point.

    **Formula:**

    `Relationship Strength Score = Active Member + Multi-Product + Credit Card`

    This is an analytical segmentation measure and is **not a predictive model**.

    ---

    ### ⚠️ Interpretation Note

    These KPIs describe patterns observed in the provided customer dataset.
    They should not be interpreted as proof that a particular behavior directly
    causes customer exit.
    """)

st.success(
    "✅ KPI methodology is documented and ready for dashboard interpretation."
)
# =========================================================
# FINAL DASHBOARD SUMMARY
# =========================================================

st.header("🎯 Dashboard Summary")

st.write(
    "This dashboard provides a descriptive view of customer engagement, "
    "product utilization, financial commitment, and observed customer exit patterns."
)

# ---------------------------------------------------------
# Summary Cards
# ---------------------------------------------------------

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.info(
        f"👥 **Customer Base**\n\n"
        f"**{len(df):,}** customers were analyzed across "
        f"**{df['Geography'].nunique()}** geographical regions."
    )

with summary_col2:
    st.success(
        f"📦 **Product Utilization**\n\n"
        f"Average product depth is "
        f"**{df['NumOfProducts'].mean():.2f}** products per customer."
    )

with summary_col3:
    st.warning(
        f"📊 **Observed Exit Rate**\n\n"
        f"The dataset has an observed exit rate of "
        f"**{overall_exit_rate:.2f}%**."
    )

# ---------------------------------------------------------
# Analysis Coverage
# ---------------------------------------------------------

st.subheader("🔎 Analysis Coverage")

coverage_col1, coverage_col2 = st.columns(2)

with coverage_col1:
    st.markdown("""
    ### 👤 Customer Behavior
    - Customer engagement
    - Age and gender patterns
    - Geography
    - Customer tenure
    - Observed exit rates
    """)

with coverage_col2:
    st.markdown("""
    ### 💼 Relationship & Utilization
    - Product utilization
    - Credit card ownership
    - Account balance
    - High-balance disengagement
    - Relationship strength
    """)

# ---------------------------------------------------------
# Final Interpretation
# ---------------------------------------------------------

st.subheader("📌 Overall Interpretation")

st.info(
    "The analysis brings together customer engagement, product utilization, "
    "financial characteristics, and relationship indicators into a single "
    "analytical dashboard. The results describe patterns observed in the "
    "provided dataset and can support further investigation of customer "
    "retention behavior."
)

st.markdown("---")

st.caption(
    "Customer Engagement & Product Utilization Analytics | "
    "Descriptive Customer Retention Analysis"
)
# =========================================================
# CUSTOM DASHBOARD STYLING
# =========================================================

st.markdown("""
<style>

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .main-subtitle {
        font-size: 20px;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Section headings */
    h1, h2, h3 {
        font-weight: 700;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(128,128,128,0.25);
    }

    /* Expanders */
    [data-testid="stExpander"] {
        border-radius: 10px;
    }

    /* Horizontal divider */
    hr {
        margin-top: 25px;
        margin-bottom: 25px;
    }

    /* Neon glow for KPI cards */
[data-testid="stMetric"] {
    border: 1px solid #00BFFF;
    border-radius: 15px;
    background: linear-gradient(135deg, #0B1220, #111827);
    padding: 18px;
    box-shadow: 0 0 10px rgba(0, 191, 255, 0.25);
    animation: neonPulse 1.2s ease-in-out infinite alternate;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* Make cards lift when hovered */
[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 25px rgba(0, 191, 255, 0.65);
}

/* Animated neon border glow */
@keyframes neonPulse {
    from {
        box-shadow: 0 0 5px rgba(0, 191, 255, 0.2);
    }
    to {
        box-shadow: 0 0 18px rgba(0, 191, 255, 0.5);
    }
}

/* Bright KPI values */
[data-testid="stMetricValue"] {
    color: #38BDF8 !important;
    font-weight: bold;
}

/* Smooth appearance for dashboard headings */
.stApp h1,
.stApp h2,
.stApp h3 {
    text-shadow: 0 0 10px rgba(56, 189, 248, 0.35);
}

/* Respect reduced-motion preferences */
@media (prefers-reduced-motion: reduce) {
    [data-testid="stMetric"] {
        animation: none;
        transition: none;
    }
}
    
</style>
""", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📘 Project Information & Methodology")

with st.expander("🎯 Project Objective"):
    st.write("""
    The objective of this project is to analyze customer engagement,
    product utilization, financial characteristics, and customer exit patterns.

    The dashboard presents descriptive insights to help users understand
    customer behavior and identify areas for further investigation.
    """)

with st.expander("📊 Dataset Overview"):
    st.write("""
    The analysis uses customer-level data containing demographic,
    account, financial, product, and customer exit information.

    The dashboard uses these attributes to compare customer groups
    and explore patterns in the available dataset.
    """)

with st.expander("⚙️ Analytical Methodology"):
    st.write("""
    1. Load and inspect the dataset.
    2. Prepare the data for analysis.
    3. Calculate summary metrics.
    4. Group customers by relevant characteristics.
    5. Create interactive visualizations.
    6. Interpret patterns using descriptive analysis.
    """)

with st.expander("⚠️ Limitations"):
    st.write("""
    This dashboard describes patterns in the available data.
    Observed relationships do not establish causation.

    The analysis does not guarantee future customer behavior
    and should be interpreted in the context of the dataset.
    """)

# ==============================
# PROJECT FOOTER
# ==============================

st.markdown("---")

st.markdown("""
<div style="
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #0B1220, #111827);
    border: 1px solid #38BDF8;
    border-radius: 12px;
    margin-top: 20px;
">
    <h4 style="color: #38BDF8;">
        Customer Engagement & Product Utilization Analytics
    </h4>
    <p style="color: #CBD5E1;">
        A descriptive analytics dashboard for exploring customer behavior,
        product usage, and customer exit patterns.
    </p>
    <p style="color: #94A3B8; font-size: 13px;">
        Built with Python, Pandas, Plotly, and Streamlit
    </p>
</div>
""", unsafe_allow_html=True)    
