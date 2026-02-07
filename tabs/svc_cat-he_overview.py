from dash import html, dcc, ClientsideFunction
from dash.dependencies import Input, Output

"""
Human Engagement – Operational Context & System Overview Tool (Service Tab)

Purpose (platform-facing):
- Provides a human-centric overview of the HVDC cable system state by
  translating technical indicators, analytics outputs, and system events
  into interpretable operational context.
- Aims to support understanding, trust, and situational awareness for
  human stakeholders (operators, engineers, decision-makers), without
  exposing raw technical complexity.

Platform role:
- Acts as a cross-cutting explanatory layer rather than an analytical or
  monitoring engine.
- Supports interpretation of platform outputs, onboarding of new users,
  and communication of system state during demonstrations or reviews.

Notes:
- This tool is intentionally not bound to a specific Work Package.
- It represents a platform-level Human Engagement capability rather than
  a project development activity.
"""

TAB_META = {
    "id": "svc-human-engagement-overview",

    "label": "Human Engagement – System Overview & Explanation",

    "type": "service",
    "order": 300,

    # Intentionally not linked to any Work Package
    "workpackages": [],

    # Human Engagement is the primary category
    "categories": [
        "Human Engagement"
    ],

    "subcategories": [],

    # Functions not defined yet
    # "functions": [],

    "version": "v0.1 (conceptual)",
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
            # trigger για JS init
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