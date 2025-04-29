import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import os

# --- Load data ---
df = pd.read_csv(os.path.join("data", "processed_data.csv"))
df['Event Date'] = pd.to_datetime(df['Event Date'], errors='coerce')
df['Month'] = df['Event Date'].dt.to_period("M").astype(str)

# --- Init Dash app ---
app = dash.Dash(__name__)
app.title = "Transit Safety Dashboard"

# --- Layout ---
app.layout = html.Div([
    html.H1("🚇 Transit Safety Event Tracker", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Transit Mode:"),
        dcc.Dropdown(
            id="mode_selector",
            options=[{"label": m, "value": m} for m in sorted(df["Mode Name"].dropna().unique())],
            value=None,
            placeholder="All Modes",
            style={"width": "50%"}
        ),
    ], style={"padding": "20px"}),

    dcc.Graph(id="monthly_trend"),
    dcc.Graph(id="hazardous_by_location"),
])

# --- Callbacks ---
@app.callback(
    Output("monthly_trend", "figure"),
    Output("hazardous_by_location", "figure"),
    Input("mode_selector", "value")
)
def update_dashboard(selected_mode):
    filtered = df.copy()
    if selected_mode:
        filtered = filtered[filtered["Mode Name"] == selected_mode]

    # Monthly trend
    monthly = filtered.groupby("Month").size().reset_index(name="Incidents")
    fig_trend = px.line(monthly, x="Month", y="Incidents", title="📈 Monthly Incident Trend")

    # Hazardous events
    hazardous = filtered[filtered["hazardous_flag"] == 1]
    hazard_group = hazardous["Location Type"].value_counts().reset_index()
    hazard_group.columns = ["Location Type", "Count"]
    fig_hazard = px.bar(hazard_group, x="Location Type", y="Count", title="⚠️ Hazardous Events by Location Type")

    return fig_trend, fig_hazard

# --- Run ---
if __name__ == "__main__":
    app.run(debug=True)
