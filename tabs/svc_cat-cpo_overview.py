from dash import html, dcc, ClientsideFunction
from dash.dependencies import Input, Output

"""
Cable Performance & Optimization Overview Tool (Service Tab)

Purpose (platform-facing):
- Provides a consolidated, platform-level view of HVDC cable performance
  and optimization-relevant indicators, independent of specific Work Packages.
- Aggregates operational metrics, stress/load indicators, and derived
  performance signals to support high-level performance understanding
  and optimization-oriented reasoning.
- Acts as a category anchor tool for "Cable Performance & Optimization",
  offering a coherent overview across multiple services and data sources.

Platform role:
- This tool does not belong to a specific Work Package and is not tied to
  a development task or project phase.
- It serves as a stable, cross-cutting capability of the platform,
  supporting analysis, interpretation, and future decision-support tools.

Notes:
- This is not a workflow entry point nor a diagnostic algorithm.
- Detailed analytics and models are expected to be implemented in
  dedicated services linked to specific Work Packages.
"""

# ---------------------------------------------------------------------
# SERVICE METADATA OPTIONS
#
# Possible Work Packages:
#   - (none – category-level overview tool)
#
# Possible Categories:
#   - Cable Performance & Optimization
#
# Functions:
#   - (not defined yet – leave empty)
# ---------------------------------------------------------------------

TAB_META = {
    "id": "svc-cpo-overview",

    "label": "Cable Performance & Optimization Overview",

    "type": "service",
    "order": 300,

    # Category-level tool: not assigned to a specific WP
    "workpackages": [],

    # Anchored strictly to Cable Performance & Optimization
    "categories": [
        "Cable Performance & Optimization"
    ],

    "subcategories": [],

    # Functions intentionally not defined yet
    # "functions": [],

    "version": "v0.1 (platform overview)",
    "status": "active"
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