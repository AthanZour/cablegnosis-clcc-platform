from dash import html, dcc, ClientsideFunction
from dash.dependencies import Input, Output

"""
WP4 Overview Tool (Service Tab)

Purpose (project-facing):
- Provides a concise overview of Work Package 4 (Monitoring & Diagnostics)
  within the CABLEGNOSIS project.
- Acts as a contextual anchor inside the platform, explaining the scope,
  objectives, and role of WP4 in relation to the implemented monitoring,
  analytics, and diagnostic tools.
- Bridges project-level structure (work packages) with platform-level
  capabilities without introducing user workflows or operational logic.

Platform role:
- This tool is intentionally not bound to any category.
- It serves as a framing and orientation layer for WP4-related services,
  supporting validation, demonstration, and dissemination activities.
"""

# ---------------------------------------------------------------------
# SERVICE METADATA OPTIONS
#
# Possible Work Packages:
#   - WP4 – Monitoring & Diagnostics
#
# Possible Categories:
#   - (none – this service is not category-bound)
#
# Functions:
#   - (not defined – overview/context tool)
# ---------------------------------------------------------------------

TAB_META = {
    "id": "svc-wp4-overview",

    "label": "WP4 – Monitoring & Diagnostics Overview",

    "type": "service",
    "order": 190,

    # This overview is strictly tied to WP4
    "workpackages": ["WP4"],

    # Intentionally empty: this tool does not belong to a category
    "categories": [],

    "subcategories": [],

    "version": "v0.1 (overview)",
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
