from dash import html, dcc, ClientsideFunction
from dash.dependencies import Input, Output

"""
WP6 Demonstration & Replicability Overview Tool (Service Tab)

Purpose (project-facing):
- Provides a consolidated overview of WP6 demonstration activities,
  pilot scenarios, and replicability contexts within the CABLEGNOSIS platform.
- Acts as an entry context for understanding how monitoring, analytics,
  and diagnostic tools are showcased and validated during demonstrations.

Platform role:
- Serves as a contextual anchor for WP6, linking demonstration scenarios
  with the underlying platform capabilities without introducing new workflows.
- Designed as a lightweight overview tool supporting dissemination,
  validation, and replication discussions rather than operational use.
"""

TAB_META = {
    "id": "svc-wp6-overview",

    "label": "WP6 Demonstration Overview",

    "type": "service",

    # Το βάζουμε ψηλά στα WP6-related services
    "order": 180,

    # Μοναδικό WP
    "workpackages": ["WP6"],

    # ❗ Δεν ανήκει σε category
    "categories": [],

    "subcategories": [],

    # Functions intentionally not defined
    # "functions": [],

    "version": "v0.1 (demo)",
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
            dcc.Interval(
                id=sid("init"),
                interval=500,
                n_intervals=0,
            ),

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