from dash import html, dcc, ClientsideFunction
from dash.dependencies import Input, Output

"""
Cable System Awareness Overview Tool (Service Tab)

Purpose (platform-facing):
- Provides a unified, high-level situational awareness view of the HVDC cable
  system by aggregating key operational states, contextual indicators, and
  system-level signals.
- Focuses on understanding the current condition and context of the cable
  system rather than detailed analytics or diagnostics.
- Acts as a horizontal platform capability supporting multiple tools and
  workflows, without belonging to a specific Work Package.

Platform role:
- Serves as a system-awareness anchor across categories, enabling operators,
  engineers, and stakeholders to quickly grasp system status and context.
- Designed as a reusable overview service, not as an entry point or workflow.
"""

TAB_META = {
    "id": "tab-overview",
    "label": "System Overview",
    "order": 1,
}

TAB_ASSOCIATION = {
    "associated_tabs": [
        "tab-monitoring",
        "tab-partner_data",
        "tab-timeline"
    ],
    "services": ["system_overview_service"],
    "project": {
        "workpackages": ["WP1"],
        "tasks": ["T1.1"],
        "partners": ["ICCS"]
    },
    "description": "High-level system overview and architecture context"
}

TAB_META = {
    "id": "svc-cable-system-awareness-overview",

    "label": "Cable System Awareness Overview",

    "type": "service",
    "order": 300,

    # This service is platform-level and does NOT belong to a specific WP
    "workpackages": [],

    # Pure Cable System Awareness category
    "categories": [
        "Cable System Awareness"
    ],

    "subcategories": [],

    # Functions intentionally not defined yet
    # "functions": [],

    "version": "v0.1 (platform capability)",
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