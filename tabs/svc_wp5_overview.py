from dash import html, dcc, ClientsideFunction
from dash.dependencies import Input, Output

"""
WP5 Validation & Lifecycle Assessment Overview (Service Tab)

Purpose (project-facing):
- Provides a structured, platform-level overview of Work Package 5
  (Validation, Deployment & Lifecycle Assessment) within CABLEGNOSIS.
- Explains how WP5 validation activities relate to the developed tools,
  data inputs, and performance indicators exposed by the platform.
- Serves as a contextual anchor linking project validation objectives
  with concrete platform capabilities, without acting as a user workflow
  or operational tool.

Platform role:
- Acts as a documentation and orientation layer inside the platform,
  helping users understand how WP5 validation is supported by the
  available monitoring, analytics, and assessment services.
- Designed as a static, explanatory service tab rather than an
  interactive or category-driven tool.

Notes:
- This overview does not belong to any functional category.
- It exists solely to provide project and validation context.
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
#   - (Not applicable for this overview service)
#
# Functions:
#   - (not defined – not applicable)
# ---------------------------------------------------------------------

TAB_META = {
    "id": "svc-wp5-overview",

    "label": "WP5 – Validation & Lifecycle Assessment Overview",

    "type": "service",

    # Place early in WP5-related services
    "order": 190,

    # This service is strictly tied to WP5
    "workpackages": ["WP5"],

    # Explicitly no category association
    "categories": [],

    "subcategories": [],

    "version": "v1.0 (project overview)",
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