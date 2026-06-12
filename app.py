import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="RMNP Timed Entry Impact", page_icon="🏔️", layout="wide")

# Theme colors
green = "#2D6A4F"
cream = "#F8F5EF"
brown = "#B08968"
gray = "#F1F1F1"
######################################################
st.markdown(
    """
    <style>

    .metric-card {
        background-color: #F8F5EF;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #2D6A4F;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.12);
        text-align: center;
    }

    .metric-title {
        font-size: 16px;
        color: #555555;
        font-weight: 600;
    }

    .metric-value {
        font-size: 36px;
        color: #2D6A4F;
        font-weight: 800;
    }

    .metric-caption {
        font-size: 13px;
        color: #777777;
    }

    </style>
    """,
    unsafe_allow_html=True)

######################################################

def styled_table(df):
    return (
        df.style
        .hide(axis="index")   # <-- removes index
        .set_table_styles([
            {
                "selector": "thead th",
                "props": [
                    ("background-color", green),
                    ("color", "white"),
                    ("font-weight", "bold"),
                    ("text-align", "center"),
                    ("padding", "8px")
                ]
            },
            {
                "selector": "tbody td",
                "props": [
                    ("background-color", cream),
                    ("color", "#222222"),
                    ("border", "1px solid #DDDDDD"),
                    ("padding", "8px"),
                    ("text-align", "center")
                ]
            },
            {
                "selector": "tbody th",
                "props": [
                    ("background-color", cream),
                    ("color", "#222222")
                ]
            }
        ])
    )

######################################################

st.markdown(
    """
    <h1 style="
        color:#2D6A4F;
        font-weight:800;
        font-size:42px;
    ">
    Did Timed Entry Reduce Crowding at Rocky Mountain National Park? 🏔️ 
    </h1>
    """,
    unsafe_allow_html=True)

st.markdown("""
National Parks have experienced record visitation growth, creating challenges around congestion, parking availability, and visitor experience.

This project evaluates whether Rocky Mountain National Park's timed-entry reservation system reduced visitor crowding using **synthetic control causal inference**.
""")

st.markdown("""
Instead of comparing before vs. after, the model estimates:

> What would RMNP visitation have looked like if timed entry had never been introduced?
""")

st.divider()


######################################################
# Load data
results = pd.read_csv("data/processed/synthetic_results.csv")
weights = pd.read_csv("data/processed/synthetic_weights.csv")
outcome = pd.read_csv("data/processed/outcome_sensitivity.csv")

post = results[results["year"] >= 2021].copy()

avg_effect = post["effect"].mean()
percent_effect = (post["effect"] / post["synthetic_rmnp"] * 100).mean()

######################################################
st.markdown(
    """
    <h2 style="color:#2D6A4F;">
    Key Findings:
    </h2>
    """,
    unsafe_allow_html=True)

# Metric Section
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-title">Peak Season Impact</div>
            <div class="metric-value">-13.4%</div>
            <div class="metric-caption">vs Synthetic RMNP</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-title">Annual Impact</div>
            <div class="metric-value">-16.6%</div>
            <div class="metric-caption">Estimated visitation change</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-title">Gap Ratio</div>
            <div class="metric-value">9.6</div>
            <div class="metric-caption">Model validation</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
- Peak-season visitation was estimated to be **13.4% lower** than the synthetic counterfactual.
- Annual visitation decreased by **16.6%**, suggesting reduced demand rather than seasonal redistribution.
- Peak-season share increased slightly, indicating remaining demand stayed concentrated during summer months.
""")

######################################################
st.divider()

st.markdown(
    """
    <h2 style="color:#2D6A4F;">
    Synthetic Control Results:
    </h2>
    """,
    unsafe_allow_html=True)

st.markdown(
    """
    A synthetic version of RMNP was created using a weighted combination of comparable National Parks. Donor weights were optimized to match RMNP's visitation patterns before timed entry implementation.
    """)

fig = go.Figure()

# Actual RMNP
fig.add_trace(
    go.Scatter(
        x=results["year"],
        y=results["actual_rmnp"],
        mode="lines+markers",
        name="Actual RMNP",
        line=dict(
            color="#2D6A4F",
            width=4),
        marker=dict(
            size=9),
        customdata=results["actual_visitors"],
        hovertemplate=(
            "<b>Actual RMNP</b><br>"
            "Year: %{x}<br>"
            "Index: %{y:.1f}<br>"
            "Visitors: %{customdata:,.0f}"
            "<extra></extra>"
        )
    )
)

# Synthetic RMNP
fig.add_trace(
    go.Scatter(
        x=results["year"],
        y=results["synthetic_rmnp"],
        mode="lines+markers",
        name="Synthetic RMNP",
        line=dict(
            color="#777777",
            width=3,
            dash="dash"),
        marker=dict(
            size=8),
        customdata=results["synthetic_visitors"],
        hovertemplate=(
            "<b>Synthetic RMNP</b><br>"
            "Year: %{x}<br>"
            "Index: %{y:.1f}<br>"
            "Expected Visitors: %{customdata:,.0f}"
            "<extra></extra>"
        )
    )
)

# Timed entry line
fig.add_vline(x=2021, line_dash="dash", line_color =brown, annotation_text="Timed Entry Begins", annotation_position="top")

# COVID shading
fig.add_vrect(x0=2019.5, x1=2020.5, annotation_text="COVID-19", fillcolor="gray", opacity=0.15, line_width=0)

fig.update_layout(title="Actual vs. Synthetic RMNP Peak-Season Visitation", xaxis_title="Year", yaxis_title="June–September Visits Index (2010 = 100)",hovermode="x unified",height=500, plot_bgcolor="white", paper_bgcolor="white")

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**Interpretation:** After timed entry implementation, actual RMNP visitation fell below its synthetic counterfactual, suggesting lower-than-expected peak-season visitation relative to comparable parks.
""")


######################################################
st.divider()

st.markdown(
    """
    <h2 style="color:#2D6A4F;">
    Data & Methods
    </h2>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
        #### Data

        **Study Period**
        - Training: 2010–2019
        - COVID disruption excluded: 2020
        - Evaluation: 2021–2025
        
        **Primary Outcome**
        - June–September recreation visits
        """
    )

    st.link_button("View NPS Dataset", "https://catalog.data.gov/dataset/nps-visitor-use-statistics-data-package-2025")

with col2:
    st.markdown(
        """
        #### Modeling Approach
        
        A synthetic version of RMNP was created using a weighted combination of comparable National Parks without major reservation systems.
        
        Methods:
        - Synthetic control modeling
        - Donor optimization
        - Placebo testing
        - Sensitivity analysis
        """
    )

######################################################


st.divider()

st.markdown(
    """
    <h2 style="color:#2D6A4F;">
    Donor Construction & Validation
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    A synthetic version of Rocky Mountain National Park was created by combining comparable National Parks that did not implement major access restrictions.

    Donor park weights were optimized to closely match RMNP's visitation trends during the pre-treatment period (2010–2019). Model reliability was evaluated using pre-treatment fit, placebo testing, and sensitivity analysis.
    """
)


# Donor weights and outcome sensitivity
col1, col2 = st.columns(2)

with col1:
    st.markdown(
    """
    <h4 style="
        color:#B08968;
        font-weight:700;
        margin-bottom:10px;
    ">
    Model Construction
    </h4>
    """,
    unsafe_allow_html=True)
#################
    # Keep meaningful donors only

    top_weights = (weights[weights["weight"] > 0.01].sort_values("weight"))

    fig_weights = px.bar(top_weights,x="weight",y="park_code", orientation="h", title="Synthetic RMNP Donor Composition",
        labels={"weight": "Synthetic Control Weight", "park_code": "Donor Park"},
        text=top_weights["weight"].apply(lambda x: f"{x:.1%}"),
        custom_data=["park_name"])

    fig_weights.update_traces(marker_color="#2D6A4F",textposition="outside",
        hovertemplate=("<b>%{customdata[0]}</b><br>""Weight: %{x:.1%}""<extra></extra>"))

    fig_weights.update_layout(height=450, xaxis_tickformat=".0%", showlegend=False, margin=dict(l=40,r=40,t=60,b=40))

    st.plotly_chart(fig_weights,use_container_width=True)



with col2:
    st.markdown(
    """
    <h4 style="
        color:#B08968;
        font-weight:700;
        margin-bottom:10px;
    ">
    Validation Summary
    </h4>
    """,
    unsafe_allow_html=True)

    validation = pd.DataFrame({
        "Test": [
            "Pre-treatment RMSE",
            "Post/pre gap ratio",
            "Directional placebo p-value",
            "Donor pool sensitivity",
            "Training-window sensitivity"
        ],
        "Result": [
            "2.55",
            "9.6",
            "0.107",
            "Stable",
            "Stable" ]
    })

    
    validation_table = styled_table(validation)

    st.markdown(
        validation_table.to_html(),
        unsafe_allow_html=True
    )


st.markdown(
    """
    **Interpretation:** The synthetic control closely reproduced RMNP's pre-treatment visitation trends. Placebo and sensitivity tests suggest the estimated decline was larger than most untreated comparisons and was robust across alternative modeling choices.
    """
)

######################################################
st.divider()

st.markdown(
    """
    <h2 style="color:#2D6A4F;">
    Outcome Sensitivity
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    To evaluate whether conclusions depended on the choice of outcome variable, the synthetic control model was repeated using multiple measures of visitor use.
    """
)

# Format outcome sensitivity results
outcome_display = (
    outcome
    .rename(
        columns={
            "outcome": "Outcome",
            "pre_rmse": "Pre-treatment RMSE",
            "avg_effect": "Average Effect",
            "percent_effect": "Estimated Change"
        }
    )
    .round(
        {
            "Pre-treatment RMSE": 2,
            "Average Effect": 2,
            "Estimated Change": 1
        }
    )
)

# Apply styling
outcome_table = (
    styled_table(outcome_display)
    .format(
        {
            "Pre-treatment RMSE": "{:.2f}",
            "Average Effect": "{:.2f}",
            "Estimated Change": "{:.1f}%"
        }
    )
)

st.markdown(
    outcome_table.to_html(),
    unsafe_allow_html=True
)

st.markdown(
    """
    **Interpretation:** Results were consistent across alternative measures of visitation. Both peak-season and annual visitation declined relative to the synthetic counterfactual, suggesting timed entry primarily reduced overall visitor volume rather than shifting visits into other seasons.
    """
)

######################################################
st.divider()
st.markdown(
    """
    <h2 style="color:#2D6A4F;">
    Policy Interpretation:
    </h2>
    """,
    unsafe_allow_html=True)

st.markdown("""
The results suggest that timed entry was associated with a meaningful reduction in RMNP visitation relative to expected trends. However, the mechanism appears to be reduced visitor volume rather than redistribution.

While peak-season visitation declined by 13.4%, annual visitation declined by a similar magnitude and peak-season share increased slightly. This suggests that remaining visitor demand continued to concentrate during traditional high-use months.

For park managers, timed entry may help reduce absolute visitor pressure, but additional strategies may be needed to encourage visitation outside peak periods.

""")


st.divider()

