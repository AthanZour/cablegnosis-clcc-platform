"""Synthetic Data Generator Tab — full UI and callbacks."""
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
from logic.synthetic_dataset_generator import generate_synthetic_dataset

"""
HVDC Scenario & Stress Exploration Tool

Purpose:
- Provides a platform-level capability for exploring HVDC cable system behaviour
  under controlled scenarios and stress conditions.
- Enables time-based scenario construction and modification (e.g. loading profiles,
  temperature evolution, noise, events) to support what-if analysis and feasibility
  assessment.
- Acts as a non-operational exploration tool that allows other monitoring, analytics
  and diagnostic services to be tested and demonstrated under reproducible conditions.

Project context:
- Supports scenario-based analysis and stress testing concepts referenced in the
  CABLEGNOSIS proposal, particularly in feasibility assessment, validation and
  demonstration activities.
- This tool is provided by the platform and is not an end-user workflow nor a
  Work Package entry point.
"""

# ---------------------------------------------------------------------
# SERVICE METADATA OPTIONS
#
# Possible Work Packages:
#   - WP1 – Requirements & System Framework
#   - WP2 – Advanced Cable Materials & Technologies
#   - WP3 – Superconducting Cable Design & Feasibility
#   - WP4 – Monitoring & Diagnostics
#   - WP5 – Validation, Deployment & Lifecycle Assessment
#   - WP6 – Demonstration & Replicability
#   - WP7 – Dissemination, Exploitation & Impact
#
# Possible Categories:
#   - Monitoring & Analytics
#   - Cable Performance & Optimization
#   - Cable System Awareness
#   - Human Engagement
#
# Functions:
#   - (not defined yet – leave empty)
# ---------------------------------------------------------------------

TAB_META = {
    "id": "svc-hvdc-scenario-explorer",

    "label": "HVDC Scenario & Stress Exploration",

    "type": "service",

    # Κοντά στα υπόλοιπα services, χωρίς να «φωνάζει»
    "order": 225,

    # Σενάρια & stress analysis συνδέονται φυσικά με feasibility, validation και demo
    "workpackages": ["WP3", "WP5", "WP6"],

    # Exploration εργαλείο που δίνει awareness και υποστηρίζει analytics & performance
    "categories": [
        "Cable System Awareness",
        "Monitoring & Analytics",
        "Cable Performance & Optimization"
    ],

    # Δεν έχουμε ακόμη δομή subcategories
    "subcategories": [],

    # Functions intentionally not defined yet
    # "functions": [],

    "version": "v0.1 (demo)",
    "status": "active",
}

def layout():
    """Layout for Synthetic Data Generator tab."""
    return html.Div(
        [
            html.H3("Synthetic Time Series Generator"),

            # Parameter controls
            html.Div(
                [
                    html.Label("Mode:"),
                    dcc.Dropdown(
                        id="gen-mode-dropdown",
                        options=[
                            {"label": "Random", "value": "random"},
                            {"label": "Sinusoidal", "value": "sinusoidal"},
                        ],
                        value="random",
                        clearable=False,
                        style={"width": "200px"},
                    ),
                    html.Br(),
                    html.Label("Number of points:"),
                    dcc.Input(id="gen-num-points", type="number", value=500, style={"width": "120px"}),
                    html.Br(),
                    html.Label("Frequency per day:"),
                    dcc.Input(id="gen-freq-per-day", type="number", value=24, style={"width": "120px"}),
                    html.Br(),
                    html.Label("Duration (days):"),
                    dcc.Input(id="gen-duration-days", type="number", value=30, style={"width": "120px"}),
                    html.Br(),
                    html.Label("Num sinusoids:"),
                    dcc.Input(id="gen-num-sinusoids", type="number", value=6, style={"width": "120px"}),
                    html.Br(),
                    html.Label("Max amplitude:"),
                    dcc.Input(id="gen-max-amp", type="number", value=40, style={"width": "120px"}),
                    html.Br(),
                    html.Label("Max DC offset:"),
                    dcc.Input(id="gen-max-dc", type="number", value=10, style={"width": "120px"}),
                    html.Br(),
                    html.Label("Noise range (min/max):"),
                    dcc.Input(id="gen-noise-min", type="number", value=-5, style={"width": "80px"}),
                    dcc.Input(id="gen-noise-max", type="number", value=20, style={"width": "80px", "marginLeft": "6px"}),
                    html.Br(),
                    html.Label("Clip range (min/max):"),
                    dcc.Input(id="gen-clip-min", type="number", value=-50, style={"width": "80px"}),
                    dcc.Input(id="gen-clip-max", type="number", value=150, style={"width": "80px", "marginLeft": "6px"}),
                    html.Br(),
                    html.Button("Generate", id="gen-generate-btn", n_clicks=0, style={"marginTop": "10px"}),
                    dcc.Checklist(
                        id="gen-auto-update",
                        options=[{"label": "Auto update", "value": "auto"}],
                        value=[],
                        style={"marginTop": "10px"},
                    ),
                ],
                style={"marginBottom": "20px"},
            ),

            # Output chart
            dcc.Graph(id="gen-dataset-graph", style={"height": "400px"}),
        ],
        style={"padding": "20px"},
    )


def register_callbacks(app):
    """Register callbacks for Synthetic Data Generator tab."""

    @app.callback(
        Output("gen-dataset-graph", "figure"),
        Input("gen-generate-btn", "n_clicks"),
        State("gen-mode-dropdown", "value"),
        State("gen-freq-per-day", "value"),
        State("gen-duration-days", "value"),
        State("gen-num-sinusoids", "value"),
        State("gen-max-amp", "value"),
        State("gen-max-dc", "value"),
        State("gen-noise-min", "value"),
        State("gen-noise-max", "value"),
        State("gen-clip-min", "value"),
        State("gen-clip-max", "value"),
        prevent_initial_call=True,
    )
    def generate_dataset(
        n, mode, freq, days, num_sin, amp, dc, nmin, nmax, cmin, cmax
    ):
        df = generate_synthetic_dataset(
            mode=mode,
            frequency_per_day=freq,
            duration_days=days,
            num_sinusoids=num_sin,
            max_amplitude=amp,
            max_dc_offset=dc,
            noise_min=nmin,
            noise_max=nmax,
            clip_min=cmin,
            clip_max=cmax,
        )
        fig = go.Figure(go.Scatter(x=df["timestamp"], y=df["value"], mode="lines"))
        fig.update_layout(title="Synthetic Dataset Preview", xaxis_title="Time", yaxis_title="Value")
        return fig
