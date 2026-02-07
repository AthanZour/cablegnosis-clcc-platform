from dash import html

"""
HVDC Anomaly Detection & Event Classification Tool (Service Tab)

Purpose (project-facing):
- Provides automated detection of abnormal operational behaviour in HVDC
  cable systems based on monitoring data streams and derived indicators.
- Focuses on early-stage anomaly detection and event classification rather
  than direct fault localisation, supporting pre-fault awareness and
  operator decision making.
- Serves as a platform-level diagnostic intelligence tool bridging WP4
  monitoring concepts with WP5 validation and WP6 demonstration activities.

Project context:
- Aligned with CABLEGNOSIS objectives on advanced diagnostics, data-driven
  fault anticipation, and enhanced situational awareness for HVDC assets.
- Designed as an enabling service, not a user workflow or control action.
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
    "id": "svc-hvdc-anomaly-detection",

    "label": "HVDC Anomaly Detection & Event Classification",

    "type": "service",
    "order": 210,

    # Core development in WP4, strong validation/demo usage
    "workpackages": ["WP4", "WP5", "WP6"],

    # Analytics-driven diagnostics with awareness & performance impact
    "categories": [
        "Monitoring & Analytics",
        "Cable System Awareness",
        "Cable Performance & Optimization"
    ],

    "subcategories": [],

    # Functions intentionally not defined yet
    # "functions": [],

    "version": "v0.1 (demo)",
    "status": "active"
}

def layout():
    return html.Div(
        className="tab-page",
        children=[
            html.H3("Diagnostics & Fault Detection Service"),

            html.P(
                "This service focuses on fault detection, diagnostics, "
                "and early warning mechanisms for HVDC cable systems."
            ),

            html.Hr(),

            html.P(
                "Associated Work Packages: WP5, WP6",
                style={"fontStyle": "italic"}
            ),

            html.P(
                "Associated Categories: Monitoring & Analytics, "
                "Cable Performance & Optimization, Cable System Awareness",
                style={"fontStyle": "italic"}
            ),

            html.Div(
                className="placeholder-box",
                children=[
                    html.P(
                        "Diagnostics and fault detection algorithms will be added here.",
                        style={"textAlign": "center"}
                    )
                ]
            )
        ]
    )