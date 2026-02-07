# tabs/category_monitoring.py
from dash import html

TAB_META = {
    "id": "cat-monitoring",
    "label": "Monitoring & Analytics",
    "type": "category",
    "order": 100,
    "category": "Monitoring & Analytics",
    "version": "conceptual"
}

def layout():
    return html.Div(
        className="tab-page",
        children=[
            html.H3("Monitoring & Analytics"),

            html.P(
                "This category covers monitoring, data acquisition, "
                "analytics, and visualization services across the platform."
            ),

            html.Hr(),

            html.Img(
                src="/assets/cablegnosis_ring.png",
                style={"width": "70%", "margin": "20px auto", "display": "block"}
            ),

            html.P(
                "Related services (monitoring, KPIs, analytics, ML-based diagnostics) "
                "will appear here as they are integrated.",
                style={"textAlign": "center", "fontStyle": "italic"}
            )
        ]
    )