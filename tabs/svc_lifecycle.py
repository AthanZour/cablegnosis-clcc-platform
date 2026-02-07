from dash import html, dcc, Input, Output, State, callback_context
# ============================================================
# TAB META (UNCHANGED – for orchestrator only)
# ============================================================

TAB_META = {
    "id": "svc-hvdc-asset-degradation",
    "label": "HVDC Asset Degradation & Remaining Life Estimation",
    "type": "service",
    "order": 220,
    "workpackages": ["WP4", "WP5", "WP6"],
    "categories": [
        "Cable Performance & Optimization",
        "Cable System Awareness",
        "Monitoring & Analytics",
    ],
    "version": "v0.1 (demo)",
    "status": "active",
}

# ============================================================
# TAB MENU META (NEW – tool-level only)
# ============================================================

TAB_MENU_META = {
    "default": "overview",
    "items": [
        {"id": "overview", "label": "Overview"},
        {"id": "inputs", "label": "Inputs"},
        {"id": "analysis", "label": "Analysis"},
        {"id": "results", "label": "Results"},
        {"id": "assumptions", "label": "Assumptions"},
    ],
}

TAB_PREFIX = "svc-lifecycle"

# ============================================================
# REUSABLE RENDERERS (LOCAL)
# ============================================================

def render_tab_menu(menu_meta):
    return html.Div(
        id=f"{TAB_PREFIX}-tab-tool-menu-container-shell",
        className="tab-tool-menu-container",
        children=[
            dcc.Store(id=f"{TAB_PREFIX}-menu-visible", data=True),

            html.Div(
                id=f"{TAB_PREFIX}-menu",
                className="tab-tool-menu",
                children=[
                    *[
                        html.Button(
                            item["label"],
                            className="tab-tool-menu-item",
                            **{"data-target": item["id"]},
                        )
                        for item in menu_meta["items"]
                    ],
                    html.Button(
                        html.Div(
                            className="tab-menu-hide-icon-wrapper",   # ⬅️ ΜΟΝΟ ΑΥΤΟ
                            children=html.Img(
                                src="/assets/hide_tab_menu.png",
                                alt="Hide menu",
                                className="tab-menu-icon",
                            ),
                        ),
                        id=f"{TAB_PREFIX}-menu-hide",
                        className="tab-tool-menu-hide",
                    ),
                ],
            ),

            html.Div(
                id=f"{TAB_PREFIX}-menu-show-wrapper",   # ⬅️ ΤΟ ΚΡΙΣΙΜΟ
                className="tab-tool-menu-show-wrapper",
                children=html.Button(
                    html.Img(
                        src="/assets/show_menu.png",
                        alt="Show menu",
                        className="tab-menu-icon",
                    ),
                    id=f"{TAB_PREFIX}-menu-show",
                    className="tab-tool-menu-collapsed",
                    style={"display": "none"},
                ),
            ),
        ],
    )


def render_section(section_id, title, content):
    return html.Div(
        id=section_id,
        style={"padding": "48px 0"},
        children=[html.H4(title), *content],
    )

# ============================================================
# LAYOUT
# ============================================================

def layout():
    return html.Div(
        id="svc-lifecycle-root",
        className="tab-page",
        children=[
            html.Div(
                id="svc-lifecycle-menu-wrapper",
                children=render_tab_menu(TAB_MENU_META),
            ),

            render_section(
                "overview",
                "Overview",
                [
                    html.P(
                        "This service provides lifecycle assessment and remaining "
                        "useful life estimation for HVDC cable assets."
                    )
                ],
            ),

            render_section(
                "inputs",
                "Inputs",
                [
                    html.P("Telemetry data, stress indicators, and configuration parameters.")
                ],
            ),

            render_section(
                "analysis",
                "Analysis",
                [
                    html.P("Degradation models and lifecycle computation logic.")
                ],
            ),

            render_section(
                "results",
                "Results",
                [
                    html.P("Remaining life indicators, trends, and diagnostic outputs.")
                ],
            ),

            render_section(
                "assumptions",
                "Assumptions",
                [
                    html.P("Model assumptions, limitations, and validity scope.")
                ],
            ),
        ],
    )

# ============================================================
# CALLBACKS (HIDE / SHOW ONLY – NO APP COUPLING)
# ============================================================

def register_callbacks(app):

    @app.callback(
        Output(f"{TAB_PREFIX}-menu", "style"),
        Output(f"{TAB_PREFIX}-menu-show", "style"),
        Output(f"{TAB_PREFIX}-menu-visible", "data"),
        Input(f"{TAB_PREFIX}-menu-hide", "n_clicks"),
        Input(f"{TAB_PREFIX}-menu-show", "n_clicks"),
        State(f"{TAB_PREFIX}-menu-visible", "data"),
        prevent_initial_call=True,
    )
    def toggle_menu(hide_clicks, show_clicks, visible):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate
        
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if trigger.endswith("menu-hide"):
            # return {"display": "none"}, {"display": "block"}, False
            return (
                {
                "visibility": "hidden",
                "opacity": 0,
                "pointerEvents": "none",
                "height": 0,
                "overflow": "hidden",
                },
                {
                "visibility": "visible",
                "opacity": 1,
                "pointerEvents": "auto",
                },
                False,
                )
        
        if trigger.endswith("menu-show"):
            # return {"display": "block"}, {"display": "none"}, True
            return (
                {
                    "visibility": "visible",
                    "opacity": 1,
                    "pointerEvents": "auto",
                    "height": "auto",
                },
                {
                    "visibility": "hidden",
                    "opacity": 0,
                    "pointerEvents": "none",
                },
                True,
            )
        
        raise PreventUpdate

