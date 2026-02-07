"""
Data Timeline Viewer Tab
Uses tab_menu_template (implicit menu_layout)
"""

from dash import html

from tabs_core.menu_layout import menu_layout
from tabs_core.tab_menu_renderers import register_tab_menu_callbacks

from tabs_core.interactive_timeline_core import (
    get_tab,
    register_callbacks as interactive_register,
)

# ============================================================
# TAB META (for orchestrator)
# ============================================================

TAB_META = {
    "id": "svc-hvdc-data-timeline",
    "label": "Data Timeline Viewer",
    "type": "service",
    "order": 230,
    "workpackages": ["WP4", "WP5", "WP6"],
    "categories": [
        "Monitoring & Analytics",
        "Cable System Awareness",
    ],
    "subcategories": [],
    "version": "v0.1 (demo)",
    "status": "active",
}

# ============================================================
# TAB CONFIG (REQUIRED BY menu_layout)
# ============================================================

TAB_PREFIX = "svc-hvdc-data-timeline"

TAB_MENU_META = {
    "default": "overview",
    "items": [
        {"id": "overview", "label": "Overview"},
        {"id": "timeline", "label": "Timeline"},
        {"id": "details", "label": "Details"},
    ],
}

# ============================================================
# TAB CONTENT (REQUIRED BY menu_layout)
# ============================================================

def layout_content():
    """
    Main content for the timeline tab.
    menu_layout() will wrap this automatically.
    """
    return [
        html.Div(
            id=f"{TAB_PREFIX}-timeline-container",
            children=get_tab(),
        )
    ]

# ============================================================
# LAYOUT
# ============================================================

def layout():
    return menu_layout()

# ============================================================
# CALLBACKS
# ============================================================

def register_callbacks(app):
    # timeline interactive callbacks
    interactive_register(app)

    # tab menu hide / show callbacks
    register_tab_menu_callbacks(app, TAB_PREFIX)