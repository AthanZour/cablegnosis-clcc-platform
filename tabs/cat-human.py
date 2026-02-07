from dash import html

TAB_META = {
    "id": "cat-human",
    "label": "Human Engagement",
    "type": "category",
    "order": 130,
    "category": "Human Engagement",
    "version": "conceptual"
}

def layout():
    return html.Div(
        className="tab-page",
        children=[
            html.H3("Human Engagement"),

            html.P(
                "This category focuses on human-in-the-loop interaction, "
                "including alerts, notifications, decision support, and "
                "operator engagement mechanisms."
            ),

            html.Hr(),

            html.Div(
                className="placeholder-box",
                children=[
                    html.Img(
                        src="/assets/hvdc_cable.jpg",
                        style={
                            "width": "60%",
                            "margin": "20px auto",
                            "display": "block"
                        }
                    ),

                    html.P(
                        "Alerting, reminders, task management, and human-centric "
                        "interfaces will be integrated here.",
                        style={
                            "textAlign": "center",
                            "fontStyle": "italic"
                        }
                    ),

                    html.P(
                        "Status: conceptual – human engagement workflows to be finalized.",
                        style={
                            "textAlign": "center",
                            "color": "#777"
                        }
                    )
                ]
            )
        ]
    )
