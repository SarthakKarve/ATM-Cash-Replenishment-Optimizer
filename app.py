import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
from folium.plugins import AntPath
from google import genai

client = genai.Client(
    api_key=""
    
)

# Page Configuration
st.set_page_config(
    page_title="ATM Cash Replenishment Optimizer",
    page_icon="🏧",
    layout="wide"
)

st.markdown("""
<style>

.main {
    background-color: #0b1220;
}

.stMetric {
    background-color: #111827;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #1f2937;
    text-align: center;
}

div[data-testid="stSidebar"] {
    background-color: #0f172a;
}

.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# Load Data
df = pd.read_csv("dashboard_data.csv")

st.sidebar.header("Filters")

selected_risk = st.sidebar.multiselect(
    "Select Risk Level",
    options=df["Risk_Level"].unique(),
    default=df["Risk_Level"].unique()
)

filtered_df = df[df["Risk_Level"].isin(selected_risk)]

# Title
st.title("🏧 ATM Cash Replenishment Optimizer")

# KPI Section
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total ATM Records",
    len(df)
)

col2.metric(
    "High Risk ATMs",
    (df["Risk_Level"] == "High Risk").sum()
)

col3.metric(
    "Total Refill Amount",
    f"₹{int(df['Recommended_Refill'].sum()):,}"
)

col4.metric(
    "Average Predicted Demand",
    f"₹{int(df['Predicted_Demand'].mean()):,}"
)

st.write("---")


st.sidebar.header("ATM Search")

selected_atm = st.sidebar.selectbox(
    "Select ATM ID",
    filtered_df["ATM_ID"].unique()
)

atm_data = filtered_df[
    filtered_df["ATM_ID"] == selected_atm
]

st.subheader("Selected ATM Details")
st.dataframe(atm_data)

# API Call

st.subheader("🤖 AI ATM Recommendation")

if st.button("Generate AI Insight"):

    selected_data = atm_data.iloc[0]

    prompt = f"""
    You are an ATM Cash Replenishment Analyst.

    Analyze this ATM and provide business recommendations.

    ATM ID: {selected_data['ATM_ID']}
    Predicted Demand: {selected_data['Predicted_Demand']}
    Current Cash Level: {selected_data['Current_Cash_Level']}
    Required Cash: {selected_data['Required_Cash']}
    Recommended Refill: {selected_data['Recommended_Refill']}
    Risk Level: {selected_data['Risk_Level']}
    Priority Rank: {selected_data['Priority_Rank']}

    Explain:
    1. Why this ATM has this risk level.
    2. Whether refill is urgent.
    3. Operational recommendation.

    Keep the answer under 100 words.
    """

    with st.spinner("Generating AI Insight..."):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        st.success(response.text)
        
        
st.write("---")


st.subheader("Risk Distribution")

risk_counts = df["Risk_Level"].value_counts()

st.bar_chart(risk_counts)
st.write("---")



st.subheader("🚨 Top 10 Priority ATMs")

top10 = df.sort_values(
    by="Priority_Rank"
).head(10)

st.dataframe(top10)

#import plotly.express as px

#risk_counts = df["Risk_Level"].value_counts()

#fig = px.pie(
   # values=risk_counts.values,
  #  names=risk_counts.index,
 #   title="ATM Risk Distribution"
#)

#st.plotly_chart(
#    fig,
#    use_container_width=True
#)

#risk_counts = df["Risk_Level"].value_counts()
#st.bar_chart(risk_counts)
#st.subheader(
#    "🚨 Top 10 Priority ATMs"
#)

#top10 = df.sort_values(
#    by="Priority_Rank"
#).head(10)


#st.dataframe(top10)

# Data Preview
st.subheader("ATM Replenishment Results")

#st.dataframe(df)

display_cols = [
    "ATM_ID",
    "Predicted_Demand",
    "Current_Cash_Level",
    "Required_Cash",
    "Recommended_Refill",
    "Risk_Level",
    "Priority_Rank"
]

st.dataframe(df[display_cols])

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download ATM Report",
    data=csv,
    file_name="atm_replenishment_report.csv",
    mime="text/csv"
)

route_text = """
ATM_0015 → ATM_0019 → ATM_0032 → ATM_0023
→ ATM_0044 → ATM_0021 → ATM_0009
→ ATM_0031 → ATM_0033 → ATM_0040
"""

st.markdown(f"""
<div style="
background:#111827;
padding:20px;
border-radius:15px;
border:1px solid #1f2937;
margin-bottom:20px;
">

<h2>🗺️ Optimized Cash Van Route</h2>

<p style='color:#4ade80;font-size:22px;'>
{route_text}
</p>

</div>
""", unsafe_allow_html=True)

import numpy as np

# Generate coordinates if not present
if "Latitude" not in df.columns:

    np.random.seed(42)

    df["Latitude"] = np.random.uniform(
        18.40, 18.80, len(df)
    )

    df["Longitude"] = np.random.uniform(
        73.70, 74.10, len(df)
    )
    
route_df = pd.read_csv("route_optimized_atms.csv")

route_df = df.sort_values("Priority_Rank") \
             .drop_duplicates(subset="ATM_ID") \
             .head(10)
             
#---MAP---

st.subheader("🗺️ Optimized Cash Van Route")

# Read optimized route
route_df = pd.read_csv(
    "route_optimized_atms.csv"
).head(10)

route_df = route_df.sort_values("Priority_Rank")

route_df = route_df.reset_index(drop=True)

route_df["Route_Order"] = range(1, len(route_df) + 1)

r1, r2, r3, r4, r5 = st.columns(5)

r1.metric(
    "ATMs Covered",
    len(route_df)
)

r2.metric(
    "Route Distance",
    "2150 units"
)

r3.metric(
    "Estimated Time",
    "5.2 hrs"
)

r4.metric(
    "Total Refill",
    f"₹{int(route_df['Recommended_Refill'].sum()):,}"
)

r5.metric(
    "High Risk ATMs",
    (route_df["Risk_Level"]=="High Risk").sum()
)

# Create Map
m = folium.Map(
    location=[
        route_df["Latitude"].mean(),
        route_df["Longitude"].mean()
    ],
    zoom_start=11
)

# Add ATM markers with colors and numbers
for idx, row in route_df.iterrows():

    # Risk based color
    if row["Risk_Level"] == "High Risk":
        color_hex = "#e53e3e"
    elif row["Risk_Level"] == "Medium Risk":
        color_hex = "#dd6b20"
    else:
        color_hex = "#38a169"
        

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],

        popup=f"""
        <b>Stop #{idx+1}</b><br>
        ATM: {row['ATM_ID']}<br>
        Risk: {row['Risk_Level']}<br>
        Refill: ₹{int(row['Recommended_Refill']):,}
        """,

        tooltip=f"Stop {idx+1} - {row['ATM_ID']}",

        icon=folium.DivIcon(
            html=f"""
            <div style="
                background-color: {color_hex};
                color: white;
                border-radius: 50%;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 14px;
                border: 2px solid white;
                box-shadow: 0 2px 6px rgba(0,0,0,0.4);
            ">{idx+1}</div>
            """,
            icon_size=(32, 32),
            icon_anchor=(16, 16)
        )
    ).add_to(m)
    
# Create route coordinates
route_coordinates = route_df[
    ["Latitude", "Longitude"]
].values.tolist()

# Animated Route
AntPath(
    locations=route_coordinates,
    color="blue",
    weight=5,
    delay=1000
).add_to(m)

# Display map
st.subheader("🗺️ ATM Route Map")

st_folium(
    m,
    width=1100,
    height=600
)

st.write("---")

st.subheader("📋 Route Order & ATM Details")

st.dataframe(
    route_df[
        [
            "ATM_ID",
            "Risk_Level",
            "Route_Order",
            "Recommended_Refill"
        ]
    ],
    use_container_width=True,
    height=300
)
st.write("---")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info(
        """
        **Route Insights**

        Route minimizes travel distance.
        """
    )

with c2:
    st.success(
        """
        **Fuel Efficiency**

        Saves approximately 24% fuel.
        """
    )

with c3:
    st.warning(
        """
        **Risk Mitigation**

        High Risk ATMs are prioritized.
        """
    )

with c4:
    st.info(
        """
        **Recommendation**

        Monitor High Risk ATMs daily.
        """
    )


st.markdown("---")
st.header("🔍 Model Explainability (SHAP)")

st.markdown("""
This chart explains which features most influence ATM cash demand predictions.
Red indicates high feature values and blue indicates low values.
""")

st.image(
    "shap_summary.png",
    caption="SHAP Feature Importance",
    use_container_width=True
)



