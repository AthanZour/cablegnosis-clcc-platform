from dash import html, dcc, ClientsideFunction
from dash.dependencies import Input, Output

"""
Monitoring & Analytics Category Overview Tool (Service Tab)

Purpose (project-facing):
- Provides a consolidated, high-level overview of Monitoring & Analytics
  capabilities offered by the CABLEGNOSIS platform.
- Acts as an onboarding and orientation tool, helping users understand
  available telemetry, analytics outputs, and validation states before
  drilling down into specialised tools.
- Supports real-time situational awareness by aggregating key indicators,
  data availability status, and monitoring health summaries.

Platform role:
- Serves as the main category-level bridge between project work packages
  (WP4–WP6) and the operational platform layer.
- Designed to host summary views, data readiness checks, KPI snapshots,
  and alert summaries without implementing analytics algorithms directly.
- Intended as a stable entry point for the Monitoring & Analytics category,
  independent of specific tools or workflows.

Notes:
- This tool is category-specific and unique within Monitoring & Analytics.
- Detailed analytics, diagnostics, and validation logic will be implemented
  in specialised service tabs linked from this overview.
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
    # Stable identifier for the Monitoring & Analytics category overview
    "id": "svc-cat-ma-overview",

    # Category-level, non-algorithmic label
    "label": "Monitoring & Analytics – Overview",

    "type": "service",

    # Keep early in the service ordering
    "order": 190,

    # This overview spans development, validation, and demonstration phases
    "workpackages": [],

    # Single-category ownership by design
    "categories": [
        "Monitoring & Analytics"
    ],

    # Not structured yet
    "subcategories": [],

    # Functions intentionally not declared yet
    # "functions": [],

    "version": "v0.1 (category overview)",
    "status": "active",
}

SERVICE_ID = TAB_META["id"]

def sid(suffix: str) -> str:
    return f"{SERVICE_ID}-{suffix}"


# ------------------------------------------------------------------
# Layout
# ------------------------------------------------------------------
def layout():
    return html.Div(
        [
            # # trigger για JS init
            # dcc.Interval(
            #     id=sid("init"),
            #     interval=500,
            #     n_intervals=0,
            # ),

            # main interactive box
            html.Div(
                id=sid("box"),
                style={
                    "width": "800px",
                    "height": "400px",
                    "backgroundImage": "url('/assets/Undersea-Cables.jpeg')",
                    "backgroundSize": "cover",
                    "cursor": "pointer",
                },
            ),

            # output from JS (display only)
            html.Div(
                id=sid("cursor-position"),
                style={"marginTop": "10px", "fontWeight": "bold"},
            ),

            # dummy output required by clientside callback
            dcc.Input(
                id=sid("js-response"),
                value="",
                style={"display": "none"},
            ),
        ],
        className="overview-tab",
    )


# ------------------------------------------------------------------
# Callbacks
# ------------------------------------------------------------------
def register_callbacks(app):
    from dash import Input, Output, ClientsideFunction

    app.clientside_callback(
        ClientsideFunction(namespace="overview", function_name="init"),
        Output(sid("js-response"), "value"),
        #Declared @ app.py
        Input("selected-tool-store", "data"),
    )