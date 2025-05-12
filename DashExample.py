import dash 
from dash import dcc, html, Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Simulated Data
df = pd.DataFrame({
    "Time": pd.date_range(start='2023-01-01', periods=100, freq='h'),
    "Temperature": np.random.uniform(20, 30, 100),
    "Pressure": np.random.uniform(1, 2, 100),
    "Humidity": np.random.uniform(30, 60, 100)
})

# Line configuration
line_config = {
    "Temperature": {"color": "red", "yaxis": "y"},
    "Pressure": {"color": "blue", "yaxis": "y"},
    "Humidity": {"color": "green", "yaxis": "y2"}  # Secondary axis
}

# App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Multi-Line Interactive Plot with Custom Config"),

    dcc.Checklist(
        id="variables",
        options=[{"label": var, "value": var} for var in line_config.keys()],
        value=["Temperature", "Humidity"],
        labelStyle={'display': 'inline-block'}
    ),

    dcc.Graph(id="custom-graph", config={"scrollZoom": True})  # Zoom with scroll wheel
])

@app.callback(
    Output("custom-graph", "figure"),
    Input("variables", "value")
)
def update_graph(selected_vars):
    fig = go.Figure()

    for var in selected_vars:
        fig.add_trace(go.Scatter(
            x=df["Time"],
            y=df[var],
            name=var,
            line=dict(color=line_config[var]["color"]),
            yaxis=line_config[var]["yaxis"]
        ))

    # Configure axes
    fig.update_layout(
        xaxis=dict(title="Time"),
        yaxis=dict(title="Primary Axis"),
        yaxis2=dict(title="Secondary Axis", overlaying="y", side="right"),
        legend=dict(x=0, y=1),
        hovermode="x unified",  # Combine hover info across lines
        margin=dict(l=60, r=60, t=40, b=40)
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True)