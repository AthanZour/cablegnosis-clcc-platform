from dash import html

TAB_META = {
    "id": "cat-awareness",
    "label": "Cable System Awareness",
    "type": "category",
    "order": 120,
    "category": "Cable System Awareness",
    "version": "conceptual"
}

def layout():
    return html.Div(
        className="tab-page",
        children=[
            html.H3("Cable System Awareness"),

            html.P(
                "This category addresses system-level awareness, including "
                "fault detection, pre-fault diagnostics, and situational awareness "
                "of HVDC cable assets."
            ),

            html.Hr(),

            html.Div(
                className="placeholder-box",
                children=[
                    html.Img(
                        src="/assets/cablegnosis_ring.png",
                        style={
                            "width": "70%",
                            "margin": "20px auto",
                            "display": "block"
                        }
                    ),

                    html.P(
                        "Fault detection, pre-fault analysis, and system awareness "
                        "tools will be accessible through this section.",
                        style={
                            "textAlign": "center",
                            "fontStyle": "italic"
                        }
                    ),

                    html.P(
                        "Status: research-oriented modules planned.",
                        style={
                            "textAlign": "center",
                            "color": "#777"
                        }
                    )
                ]
            )
        ]
    )