# ============================================================
#  C-LCC Platform – app.py
#  Dynamic Modular Dash Shell (Zero Hardcoding)
# ------------------------------------------------------------
#  ARCHITECTURE PHILOSOPHY
#
#  This file is intentionally designed as a *generic application shell*.
#  It does NOT know:
#   - how many tabs exist
#   - what their names are
#   - what logic they implement
#
#  Instead, it:
#   • discovers tabs dynamically (plugin-style architecture)
#   • preloads all tab layouts once at startup
#   • keeps tab state persistent across navigation
#   • delegates ALL business logic to the backend & tab modules
#
#  Tabs are treated as independent UI micro-applications
#  that coexist inside a unified presentation layer.
#
# ------------------------------------------------------------
#  KEY DESIGN PRINCIPLES
#
#  ✔ Preloaded tabs (no remounting → state preserved)
#  ✔ No direct tab-to-tab communication
#  ✔ Backend-mediated state & synchronization
#  ✔ Frontend = presentation only
#  ✔ Tabs can be added/removed without touching app.py
#
#  This mirrors:
#   - plugin-based systems (VS Code, browsers)
#   - micro-frontend architectures
#   - research dashboards with multiple independent workflows
#
# ============================================================
# ============================================================
# C-LCC Demo Platform – Contextual Tab Association & Metadata Layer

# This application dynamically discovers tab modules (*tabs/*.py) and builds:
# (A) UI-level tab metadata
# (B) Service-level execution metadata
# (C) Project-level metadata (Work Packages / Tasks / Partners)

# The goal is NOT to hard-code KPIs or deliverables,
# but to demonstrate architectural capability, traceability,
# and contextual relations between UI, services, and project structure.

# All metadata are:
# - auto-generated if missing (safe defaults, no crashes)
# - decoupled (tabVersion ≠ serviceVersion ≠ deliverableVersion)
# - suitable for evolving requirements in research projects

# This layer supports:
# - contextual highlighting of associated tabs
# - transparent versioning
# - mid-term demo readiness (M18) without locking partner obligations
# ============================================================
# ============================================================
#  C-LCC Platform – app.py
#  Dynamic Modular Dash Shell (SAFE VERSION)
# ============================================================
# ============================================================
#  C-LCC Platform – app.py
#  Dynamic Modular Dash Shell (SAFE VERSION)
#  Phase-1: Tab Orchestrator (Per Work Package)
# ============================================================

# ============================================================
#  ORCHESTRATOR CONTROL – SCADA UNIFIED SEARCH CONTROL
# ------------------------------------------------------------
#  This module implements a SCADA-grade Orchestrator Control
#  that unifies STATUS DISPLAY and MODE SELECTION into a single,
#  operator-driven search control.
#
#  The original dropdown-based orchestration logic is fully
#  preserved. Only the PRESENTATION LAYER has been replaced.
#
#  ------------------------------------------------------------
#  CORE PRINCIPLES
#  ------------------------------------------------------------
#  • Status-first, operator-driven interaction (SCADA / HMI)
#  • Explicit user actions only (no implicit auto-hide behavior)
#  • Single source of truth for orchestration mode
#  • Separation of STATE (logic) from PRESENTATION (UI)
#
#  ------------------------------------------------------------
#  ARCHITECTURE OVERVIEW
#  ------------------------------------------------------------
#  1. Hidden Dropdown (id="tab-view-mode")
#     - Remains the SINGLE authoritative orchestration state
#     - All existing callbacks continue to depend on it
#     - MUST NOT be removed, renamed, or conditionally rendered
#
#  2. Unified Orchestrator Search Control
#     - Replaces the visible dropdown UI
#     - Combines:
#         • Status display: "Orchestrator | <Current Mode>"
#         • Inline search input (always available)
#     - Serves as the ONLY entry point for operator interaction
#
#  3. Inline Orchestrator Panel (non-modal)
#     - Opens explicitly via operator click
#     - Never auto-hides on typing, re-rendering, or state changes
#     - Displays:
#         • Assistive search suggestions (additive)
#         • Full list of orchestration modes (always visible)
#
#  4. ORCHESTRATOR_OPTIONS Registry
#     - Centralized definition of orchestration modes
#     - Controls labels, values, and disabled (future) states
#     - Enables metadata-driven extensions without refactor
#
#  5. Safe, Deterministic Selection Logic
#     - Mode changes occur ONLY on explicit option clicks
#     - Disabled options are visually and logically blocked
#     - UI behavior is deterministic and SCADA-safe
#
#  ------------------------------------------------------------
#  INTENTIONAL DESIGN DECISIONS
#  ------------------------------------------------------------
#  • No modal dialogs
#  • No auto-hide behavior (typing, re-rendering, programmatic changes)
#  • No implicit state transitions
#
#  These decisions align with SCADA / HMI operator trust models
#  and prevent accidental configuration changes.
#
#  ------------------------------------------------------------
#  IMPORTANT
#  ------------------------------------------------------------
#  This control affects PRESENTATION ONLY.
#  Business logic, orchestration behavior, and tab rendering
#  remain untouched and backward-compatible.
#
#  Any future modifications MUST preserve:
#   - id="tab-view-mode" as the orchestration authority
#   - Explicit, operator-driven interaction semantics
# ============================================================

# ------------------------------------------------------------
#  SEARCH BEHAVIOR – SCADA RATIONALE
# ------------------------------------------------------------
#  The orchestrator search field is intentionally NON-PERSISTENT.
#
#  Design intent:
#  • The search acts as a temporary keyword assistant
#  • It is NOT a filter, NOT a stored query, and NOT user state
#
#  SCADA PRINCIPLES APPLIED:
#  • Each panel open represents a new interaction session
#  • Search input is cleared on panel open and panel close
#  • No hidden or residual UI state is preserved
#
#  This ensures:
#  • Deterministic operator behavior
#  • Zero cognitive residue between interactions
#  • No ambiguity about why certain options are visible
#
#  Typical usage assumes short keyword probes (2–3 characters)
#  rather than full-text queries.
# ------------------------------------------------------------

import os
import json
from datetime import datetime
import sys
import importlib
import pkgutil

import dash

from dash import html, dcc, Input, Output, ALL, State

from utils.paths import ensure_dirs

import tabs

METADATA_DIR = "data/metadata"

PLATFORM_VERSION = "0.8.3.11-demo"

PY_VERSION = sys.version.split()[0]
DASH_VERSION = dash.__version__

ensure_dirs()

# ============================================================
# METADATA DIR
# ============================================================

def ensure_metadata_dir():
    os.makedirs(METADATA_DIR, exist_ok=True)


# ============================================================
# TAB DISCOVERY (SAFE)
# ============================================================

def discover_tabs():
    modules = []

    for _, module_name, _ in pkgutil.iter_modules(tabs.__path__):
        try:
            module = importlib.import_module(f"tabs.{module_name}")
            if hasattr(module, "TAB_META") and hasattr(module, "layout"):
                modules.append(module)
        except Exception as e:
            print(f"[TAB LOAD ERROR] tabs.{module_name}: {e}")

    modules.sort(key=lambda m: m.TAB_META.get("order", 999))
    return modules


TAB_MODULES = discover_tabs()

print("Discovered tabs:")
for t in TAB_MODULES:
    print(" -", t.__name__, t.TAB_META)


# ============================================================
# OPTIONAL META REGISTRIES (SAFE IMPORTS)
# ============================================================

try:
    from tabs.services_meta import SERVICES
except Exception:
    SERVICES = {}

try:
    from tabs.workpackages_meta import WORKPACKAGES
except Exception:
    WORKPACKAGES = {}


# ============================================================
# GENERATE METADATA (KEEP AS-IS)
# ============================================================

def generate_metadata():
    ensure_metadata_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    tab_relations = {}
    service_relations = {}
    wp_relations = {}

    for tab in TAB_MODULES:
        tab_id = tab.TAB_META["id"]
        assoc = getattr(tab, "TAB_ASSOCIATION", {})
        tab_relations[tab_id] = assoc

        for s in assoc.get("services", []):
            service_relations.setdefault(s, []).append(tab_id)

        for wp in assoc.get("project", {}).get("workpackages", []):
            wp_relations.setdefault(wp, []).append(tab_id)

    files = {
        "tab_relations": f"tab_relations_{ts}.json",
        "service_relations": f"service_relations_{ts}.json",
        "workpackage_relations": f"workpackage_relations_{ts}.json",
        "services_registry": f"services_registry_{ts}.json",
        "workpackages_registry": f"workpackages_registry_{ts}.json",
    }

    with open(os.path.join(METADATA_DIR, files["tab_relations"]), "w") as f:
        json.dump(tab_relations, f, indent=2)

    with open(os.path.join(METADATA_DIR, files["service_relations"]), "w") as f:
        json.dump(service_relations, f, indent=2)

    with open(os.path.join(METADATA_DIR, files["workpackage_relations"]), "w") as f:
        json.dump(wp_relations, f, indent=2)

    with open(os.path.join(METADATA_DIR, files["services_registry"]), "w") as f:
        json.dump(SERVICES, f, indent=2)

    with open(os.path.join(METADATA_DIR, files["workpackages_registry"]), "w") as f:
        json.dump(WORKPACKAGES, f, indent=2)

    with open(os.path.join(METADATA_DIR, "latest.json"), "w") as f:
        json.dump(files, f, indent=2)


generate_metadata()


# ============================================================
# HELPERS: TAB REGISTRY (TYPE FILTERS)
# ============================================================

def tabs_by_type(tab_type: str):
    """Return tab modules whose TAB_META.type == tab_type, sorted by order."""
    out = []
    for m in TAB_MODULES:
        if m.TAB_META.get("type") == tab_type:
            out.append(m)
    out.sort(key=lambda x: x.TAB_META.get("order", 999))
    return out


def get_wp_tabs():
    """Workpackage tabs are those with TAB_META.type == 'workpackage'."""
    return tabs_by_type("workpackage")


def get_service_tabs():
    """Service/tool tabs are those with TAB_META.type == 'service'."""
    return tabs_by_type("service")


def get_category_tabs():
    """Category tabs (outer ring) - not used in phase-1, but already present."""
    return tabs_by_type("category")


def services_for_wp(wp_code: str):
    """
    Return services that declare this WP in TAB_META['workpackages'].
    Example TAB_META['workpackages'] = ['WP4','WP5'].
    """
    services = []
    for m in get_service_tabs():
        wps = m.TAB_META.get("workpackages", []) or []
        if wp_code in wps:
            services.append(m)
    services.sort(key=lambda x: x.TAB_META.get("order", 999))
    return services
     
def default_wp_id():
    wps = get_wp_tabs()
    if not wps:
        return None
    return wps[0].TAB_META["id"]


def wp_code_from_wp_tab_id(wp_tab_id: str):
    for m in get_wp_tabs():
        if m.TAB_META["id"] == wp_tab_id:
            if m.TAB_META.get("wp"):
                return m.TAB_META["wp"]
            _id = wp_tab_id.lower()
            if _id.startswith("wp"):
                return "WP" + _id.replace("wp", "")
    if wp_tab_id:
        _id = wp_tab_id.lower()
        if _id.startswith("wp"):
            return "WP" + _id.replace("wp", "")
    return wp_tab_id


def default_service_for_wp(wp_tab_id: str):
    wp_code = wp_code_from_wp_tab_id(wp_tab_id)
    services = services_for_wp(wp_code)
    if not services:
        return None
    return services[0].TAB_META["id"]

def default_category_id():
    cats = get_category_tabs()
    if not cats:
        return None
    return cats[0].TAB_META["id"]
    
def category_label_from_tab_id(cat_tab_id: str):
    for c in get_category_tabs():
        if c.TAB_META["id"] == cat_tab_id:
            return c.TAB_META.get("category") or c.TAB_META.get("label")
    return None   
     
def services_for_category(category_name: str):
    services = []
    for m in get_service_tabs():
        cats = m.TAB_META.get("categories", []) or []
        if category_name in cats:
            services.append(m)
    services.sort(key=lambda x: x.TAB_META.get("order", 999))
    return services
    
# ============================================================
# HELPERS: SCROLLABLE BAR RENDERING
# ============================================================

ORCHESTRATOR_OPTIONS = [
    {"label": "Per Work Package", "value": "per_wp", "disabled": False},
    {"label": "Per Category", "value": "per_category", "disabled": False},
    {"label": "Per Function", "value": "per_function", "disabled": True},
    {"label": "Favorites", "value": "favorites", "disabled": True},
]

def bar_style():
    # Same behavior as your current scrollable custom bar (#custom-tab-bar),
    # but we keep unique ids to avoid duplicates.
    return {
        "display": "flex",
        "flexWrap": "nowrap",
        "overflowX": "auto",
        "borderBottom": "1px solid #ddd",
        "background": "#ffffff",
    }


def render_wp_bar(active_wp_tab_id):
    """
    Render Work Package bar as a SCADA-style horizontal strip.
    Items are NOT buttons – they are draggable timeline items.
    """

    items = []

    for wp in get_wp_tabs():
        tab_id = wp.TAB_META["id"]
        cls = "tab-btn active" if tab_id == active_wp_tab_id else "tab-btn"

        items.append(
            html.Div(
                wp.TAB_META["label"],
                id={"type": "wp-btn", "id": tab_id},
                className=cls,
                tabIndex=0,
            )
        )

    return html.Div(
        items,
        className="wp-tab-bar"
    )


def render_tools_bar(active_wp_tab_id, active_tool_tab_id):
    """
    Render Tools bar as a SCADA-style horizontal strip.
    Tools are NOT buttons – they are draggable timeline items.
    """

    if not active_wp_tab_id:
        return html.Div(className="tool-tab-bar")

    wp_code = wp_code_from_wp_tab_id(active_wp_tab_id)
    tools = services_for_wp(wp_code)

    items = []

    for tool in tools:
        tab_id = tool.TAB_META["id"]

        is_active = tab_id == active_tool_tab_id
        cls = "tab-btn active" if is_active else "tab-btn"

        items.append(
            html.Div(
                tool.TAB_META["label"],
                id={"type": "tool-btn", "id": tab_id},
                className=cls,
                tabIndex=0,
            )
        )

    return html.Div(
        items,
        className="tool-tab-bar"
    )

def render_category_bar(active_cat_tab_id):
    items = []

    for cat in get_category_tabs():
        tab_id = cat.TAB_META["id"]
        cls = "tab-btn active" if tab_id == active_cat_tab_id else "tab-btn"

        items.append(
            html.Div(
                cat.TAB_META["label"],
                id={"type": "cat-btn", "id": tab_id},
                className=cls,
                tabIndex=0,
            )
        )

    return html.Div(items, className="wp-tab-bar")

def render_tools_bar_from_services(services, active_tool_tab_id):
    items = []

    for tool in services:
        tab_id = tool.TAB_META["id"]
        cls = "tab-btn active" if tab_id == active_tool_tab_id else "tab-btn"

        items.append(
            html.Div(
                tool.TAB_META["label"],
                id={"type": "tool-btn", "id": tab_id},
                className=cls,
                tabIndex=0,
            )
        )

    return html.Div(items, className="tool-tab-bar")
    
def empty_state_block(title: str, subtitle: str):
    return html.Div(
        className="placeholder-box",
        style={"marginTop": "16px"},
        children=[
            html.H4(title, style={"marginTop": 0}),
            html.P(subtitle, style={"color": "#666", "fontStyle": "italic"}),
        ],
    )


# ============================================================
# DASH APP
# ============================================================

from backend.app_backend import create_backend_app
# 1️⃣ Φτιάχνεις ΠΡΩΤΑ το Flask backend
server = create_backend_app()

# 2️⃣ Δίνεις αυτό το server στο Dash
app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    title="C-LCC Demo Platform",
   update_title=None
)


# ============================================================
# LAYOUT
# ============================================================

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f9f9f9",
        "minHeight": "100vh",
    },
    children=[
        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------
        
        html.Div(
            id="app-header",
            style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "backgroundColor": "white",
                "padding": "10px 20px",
                "borderBottom": "2px solid #e0e0e0",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.05)",
            },
            children=[
        
                # ----------------------------------------------------
                # LEFT: LOGO (click = full page refresh)
                # ----------------------------------------------------
                html.Button(
                    html.Img(
                        id="app-header-logo",
                        src="/assets/CG_main_icon.jpg",
                        style={"borderRadius": "6px"},
                    ),
                    id="app-header-logo-btn",
                    className="app-header-logo-button",
                ),
                # ----------------------------------------------------
                # CENTER: TITLE + VERSION (already styled via CSS)
                # ----------------------------------------------------
                html.Div(
                    id="app-header-text",
                    children=[
                        html.H2(
                            [
                                html.Span("CableGnosis", className="app-header-system"),
                                html.Span("•", className="app-header-separator"),
                                html.Span("Life Cycle", className="app-header-scope"),
                                html.Span("•", className="app-header-separator"),
                                html.Span("CENTER", className="app-header-unit"),
                            ],
                            id="app-header-title",
                        ),
                        html.Hr(id="app-header-separator", className="header-separator"),
                        html.Div(
                            id="app-header-version-trigger",
                            children=[
                                dcc.Store(id="app-header-version-visible", data=False),
                        
                                html.Button(
                                    html.Img(
                                        src="/assets/version_info_icon.png",
                                        className="version-info-icon",
                                    ),
                                    id="app-header-version-btn",
                                    className="version-info-button",
                                    n_clicks=0,
                                ),
                        
                                # BACKDROP (FULL SCREEN) – sibling of the panel
                                html.Div(
                                    id="app-header-version-backdrop",
                                    n_clicks=0,
                                    style={"display": "none"},
                                ),
                        
                                # PANEL (popover)
                                html.Div(
                                    id="app-header-version-panel",
                                    className="version-info-panel",
                                    style={"display": "none"},
                                    children=[
                                        html.Div("Platform information", className="vip-title"),
                                        html.Div(
                                            [
                                                html.Em("c-lcc platform version "),
                                                html.Span(PLATFORM_VERSION),
                                            ],
                                            className="vip-row",
                                        ),
                                        html.Div(f"Python: {PY_VERSION}", className="vip-row"),
                                        html.Div(f"Dash: {DASH_VERSION}", className="vip-row"),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
        
                # ----------------------------------------------------
                # RIGHT: SCADA HEADER ACTION ICONS
                # ----------------------------------------------------
                html.Div(
                    id="app-header-actions",
                    children=[
                        html.Img(
                            src="/assets/home_icon.svg",
                            id="header-icon-home",
                            title="Home",
                        ),
                        html.Img(
                            src="/assets/settings_icon.png",
                            id="header-icon-preferences",
                            title="Settings",
                        ),
                        html.Img(
                            src="/assets/log_in_icon.png",
                            id="header-icon-login",
                            title="Log in",
                        ),
                    ],
                ),
            ],
        ),

        # ----------------------------------------------------
        # ORCHESTRATOR HEADER ROW
        # ----------------------------------------------------
        html.Div(
            className="tab-header-row",
            children=[
                html.Div(
                    className="tab-view-mode",
                    children=[
                        ### Deprecation Starts###
                        # # Title
                        # html.Em(
                        #     "Tab Orchestrator",
                        #     style={
                        #         "fontSize": "12px",
                        #         "letterSpacing": "0.3px",
                        #     },
                        # ),
                        
                        # # Separator between title and control
                        # # html.Div(className="orchestrator-separator"),
                        # html.Div(className="orch-line-delimiter"),
                        # html.Div(className="orch-line-closing"), 
                        ###Deprecation Ends###
                        # ----------------------------------------------------
                        # HIDDEN DROPDOWN (SOURCE OF TRUTH – DO NOT REMOVE)
                        # ----------------------------------------------------
                        dcc.Dropdown(
                            id="tab-view-mode",
                            options=[
                                {"label": "Per Work Package", "value": "per_wp"},
                                {"label": "Per Category", "value": "per_category", "disabled": False},
                                {"label": "Per Function", "value": "per_function", "disabled": True},
                                {"label": "Favorites", "value": "favorites", "disabled": True},
                            ],
                            # value="per_wp",
                            clearable=False,
                            style={"display": "none"},
                        ),
                        html.Div(
                            id="orchestrator-control",
                            children=[
                                html.Div(
                                    id="orchestrator-status",
                                    n_clicks=0,
                                    className="orchestrator-status orchestrator-input-wrapper",
                                    children=[
                                        # LEFT ICON
                                        html.Div(className="orchestrator-icon"),
                                
                                        # TEXT
                                        html.Div(
                                            id="orchestrator-status-label",
                                            className="orchestrator-status-label",
                                            children=[
                                                html.Span("Orchestrator", className="orch-label-muted"),
                                                html.Span("|", className="orch-label-sep"),
                                                html.Span("Per Work Package", className="orch-label-active"),
                                            ],
                                        ),
                                
                                        # INVISIBLE INPUT (events μόνο)
                                        dcc.Input(
                                            id="orchestrator-search",
                                            className="orchestrator-search",
                                            type="text",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="orchestrator-panel",
                                    className="orchestrator-panel",
                                    style={"display": "none"},
                                    children=[
                                        # ---------------------------------
                                        # PANEL HEADER (CONTRACTION CONTROL)
                                        # ---------------------------------
                                        html.Div(
                                            className="orchestrator-panel-header",
                                            children=[
                                                html.Button(
                                                    "",
                                                    id="orchestrator-panel-hide",
                                                    n_clicks=0,
                                                    className="orchestrator-panel-hide-btn",
                                                )
                                            ],
                                        ),                                
                                        html.Div(className="orch-divider"),
                                        html.Div(id="orchestrator-options"),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),

                # Right side summary (keep minimal for phase-1)
                # DEPRECATED (UI-only):
                # Orchestrator-level context summary.
                # Logic is still computed for backward compatibility,
                # but rendering is intentionally disabled.
                html.Div(
                    id="orchestrator-summary",
                    className="contextual-info",
                    children=None,
                ),
            ],
        ),

        # ----------------------------------------------------
        # STORES (selected wp/tool)
        # ----------------------------------------------------
        dcc.Store(id="selected-wp-store", data=default_wp_id()),
        dcc.Store(id="selected-tool-store", data=None),
        dcc.Store(id="selected-category-store", data=None),
        dcc.Store(
                id="tab-view-mode-store",
                data="per_wp",
                storage_type="session",  # 👈 ΤΟ ΚΛΕΙΔΙ
            ),
        # ----------------------------------------------------
        # BARS CONTAINERS
        # ----------------------------------------------------
        html.Div(className="sep-orch-wp"),
        
        html.Div(id="wp-bar-container", style={"marginTop": "0px"}),
        
        html.Div(className="sep-wp-tool"),
        
        html.Div(id="tool-bar-container"),
        
        html.Div(className="sep-tool-content"),
        
        html.Div(id="content-container"),
       
        # Empty-state area (when WP has no tools)
        html.Div(id="orchestrator-empty-state", style={"padding": "0 20px"}),
        # ----------------------------------------------------
        # TAB CONTENT (PRELOADED)
        # ----------------------------------------------------
        html.Div(
            id="tabs-content",
            className="tabs-content-container",
            children=[
                html.Div(
                    [
                        html.Div(
                            id={"type": "tab-context", "id": tab.TAB_META["id"]},
                            className="tab-context-header",
                        ),
                         # ⬇️ SEPARATOR: κάτω από το context
                        html.Div(
                            className="tab-content-separator",
                            children=[
                                html.Div(className="tab-sep-primary"),
                                html.Div(className="tab-sep-secondary"),
                            ],
                        ),
                        tab.layout(),
                    ],
                    id={"type": "tab-content", "id": tab.TAB_META["id"]},
                    style={"display": "none"},
                )
                for tab in TAB_MODULES
            ],
        ),
    ],
)


# ============================================================
# INIT DEFAULT TOOL WHEN APP STARTS / STORE EMPTY
# ============================================================

# @app.callback(
#     Output("selected-tool-store", "data"),
#     Input("selected-wp-store", "data"),
#     State("selected-tool-store", "data"),
# )
# def ensure_default_tool_for_wp(selected_wp, selected_tool):
#     # If tool not set, pick default tool for this WP (may be None).
#     if selected_tool:
#         return selected_tool
#     if not selected_wp:
#         return None
#     return default_service_for_wp(selected_wp)

# ============================================================
# CLICK HANDLER: WP BUTTONS + TOOL BUTTONS
# ============================================================

@app.callback(
    Output("selected-wp-store", "data"),
    Output("selected-tool-store", "data"),
    Output("selected-category-store", "data"),
    Input({"type": "wp-btn", "id": ALL}, "n_clicks"),
    Input({"type": "cat-btn", "id": ALL}, "n_clicks"),
    Input({"type": "tool-btn", "id": ALL}, "n_clicks"),
    State("selected-wp-store", "data"),
    State("selected-category-store", "data"),
    State("selected-tool-store", "data"),
    prevent_initial_call=True
)
def handle_bar_clicks(
    wp_clicks,
    cat_clicks,
    tool_clicks,
    selected_wp,
    selected_category,
    selected_tool
):
    ctx = dash.callback_context
    if not ctx.triggered:
        return selected_wp, selected_tool, selected_category

    trigger = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger.startswith("{"):
        tid = json.loads(trigger)
        ttype = tid.get("type")
        tid_value = tid.get("id")

        # -------------------------
        # WP CLICK
        # -------------------------
        if ttype == "wp-btn":
            new_wp = tid_value
            new_tool = default_service_for_wp(new_wp)
            return new_wp, new_tool, selected_category

        # -------------------------
        # CATEGORY CLICK
        # -------------------------
        if ttype == "cat-btn":
            new_cat = tid_value
            cat_label = category_label_from_tab_id(new_cat)
            services = services_for_category(cat_label)
            new_tool = services[0].TAB_META["id"] if services else None
            return selected_wp, new_tool, new_cat

        # -------------------------
        # TOOL CLICK
        # -------------------------
        if ttype == "tool-btn":
            return selected_wp, tid_value, selected_category

    return selected_wp, selected_tool, selected_category

# ============================================================
# CLICK HANDLER: HEADER VERSION INFO (POPOVER TOGGLE)
# ============================================================

@app.callback(
    Output("app-header-version-visible", "data"),
    Input("app-header-version-btn", "n_clicks"),
    State("app-header-version-visible", "data"),
    prevent_initial_call=True,
)
def toggle_version_visibility(_, is_visible):
    return not is_visible


@app.callback(
    Output("app-header-version-panel", "style"),
    Input("app-header-version-visible", "data"),
)
def apply_version_panel_visibility(is_visible):
    return {"display": "block"} if is_visible else {"display": "none"}


@app.callback(
    Output("app-header-version-backdrop", "style"),
    Input("app-header-version-visible", "data"),
)
def render_version_backdrop(is_visible):
    return {"display": "block"} if is_visible else {"display": "none"}


@app.callback(
    Output("app-header-version-visible", "data", allow_duplicate=True),
    Input("app-header-version-backdrop", "n_clicks"),
    State("app-header-version-visible", "data"),
    prevent_initial_call=True,
)
def close_on_outside_click(n, is_visible):
    if is_visible:
        return False
    return is_visible

# ============================================================
# RENDER BARS + SWITCH CONTENT
# ============================================================

@app.callback(
    Output("wp-bar-container", "children"),
    Output("tool-bar-container", "children"),
    Output("orchestrator-summary", "children"),
    Output("orchestrator-empty-state", "children"),
    Output({"type": "tab-content", "id": ALL}, "style"),
    Input("tab-view-mode-store", "data"),
    Input("selected-wp-store", "data"),
    Input("selected-category-store", "data"),
    Input("selected-tool-store", "data"),
)
def render_orchestrator(mode, selected_wp, selected_category, selected_tool):
    # print("ro")
    # print(1)
    # print(mode)
    # Fallback: show WP content if no tool is selected
    if mode == "per_wp" and not selected_tool and selected_wp:
        active_tab_id = selected_wp
    else:
        active_tab_id = selected_tool
    
    empty_state = None
    active_tab_id = selected_tool

    # =====================================================
    # MODE: PER WORK PACKAGE (unchanged behavior)
    # =====================================================
    if mode == "per_wp":

        if not selected_wp:
            selected_wp = default_wp_id()
    
        wp_code = wp_code_from_wp_tab_id(selected_wp)
    
        wp_bar = render_wp_bar(selected_wp)
    
        tools = services_for_wp(wp_code)
        tool_bar = render_tools_bar_from_services(tools, selected_tool)
        # DEPRECATED OUTPUT:
        # Orchestrator-level summary is no longer rendered.
        # Context is now handled per-tab via `render_tab_context`.
        # TODO (cleanup):
        # Remove orchestrator summary computation after Phase-2
        # once per-function mode is finalized.
        summary = html.Span([
            html.Span("Mode: ", className="context-strong"),
            html.Span("Per Work Package"),
            html.Span(" • "),
            html.Span("Selected: ", className="context-strong"),
            html.Span(wp_code),
        ])
    
        if not tools:
            empty_state = empty_state_block(
                f"{wp_code} has no tools yet",
                "This is expected for the demo. Tools will be integrated later."
            )
            active_tab_id = None

    # =====================================================
    # MODE: PER CATEGORY
    # =====================================================
    elif mode == "per_category":

        if not selected_category:
            selected_category = default_category_id()

        wp_bar = render_category_bar(selected_category)

        cat_label = category_label_from_tab_id(selected_category)
        tools = services_for_category(cat_label)

        # Reuse existing tool bar logic pattern
        items = []
        for tool in tools:
            tab_id = tool.TAB_META["id"]
            cls = "tab-btn active" if tab_id == selected_tool else "tab-btn"

            items.append(
                html.Div(
                    tool.TAB_META["label"],
                    id={"type": "tool-btn", "id": tab_id},
                    className=cls,
                    tabIndex=0,
                )
            )

        tool_bar = render_tools_bar_from_services(tools, selected_tool)

        summary = html.Span([
            html.Span("Mode: ", className="context-strong"),
            html.Span("Per Category"),
            html.Span(" • "),
            html.Span("Selected: ", className="context-strong"),
            html.Span(cat_label),
        ])

        if not tools:
            empty_state = empty_state_block(
                f"{cat_label} has no tools yet",
                "This category will be populated as services are integrated."
            )
            active_tab_id = None

    # =====================================================
    # CONTENT VISIBILITY (shared)
    # =====================================================
    styles = []
    for tab in TAB_MODULES:
        styles.append(
            {"display": "block"}
            if active_tab_id and tab.TAB_META["id"] == active_tab_id
            else {"display": "none"}
        )
    # return wp_bar, tool_bar, summary, empty_state, styles
    return wp_bar, tool_bar, None, empty_state, styles

@app.callback(
    Output({"type": "tab-context", "id": ALL}, "children"),
    Input("tab-view-mode-store", "data"),
    Input("selected-wp-store", "data"),
    Input("selected-category-store", "data"),
    Input("selected-tool-store", "data"),
)
def render_tab_context(mode, selected_wp, selected_category, selected_tool):
    # print("rtc")
    # print(2)
    # print(mode)
    outputs = []

    for tab in TAB_MODULES:
        tab_id = tab.TAB_META["id"]

        # Default: nothing in context header
        content = None

        # Only populate context for ACTIVE tab
        if selected_tool and tab_id == selected_tool:

            # -------------------------
            # PER WP
            # -------------------------
            if mode == "per_wp" and selected_wp:
                wp_code = wp_code_from_wp_tab_id(selected_wp)

                content = html.Div(
                    [
                        html.Div(
                            [
                                html.Span(
                                    "Mode: Per Work Package • Selected: ",
                                    className="context-inline-label",
                                ),
                                html.Span(
                                    wp_code,
                                    className="context-inline-value",
                                ),
                                html.Span(
                                    "?",
                                    className="context-info-circle",
                                    title="Click to show full description",
                                ),
                            ],
                            className="tab-context-inline",
                        )
                    ],
                    className="tab-context-container",
                    style={
                        "marginTop": "-6px",
                        "marginBottom": "4px",
                    },
                )

            # -------------------------
            # PER CATEGORY
            # -------------------------
            elif mode == "per_category" and selected_category:
                cat_label = category_label_from_tab_id(selected_category)
                content = html.Div(
                    [
                        html.Div(
                            [
                                html.Span(
                                    "Mode: Per Category • Selected: ",
                                    className="context-inline-label",
                                ),
                                html.Span(
                                    cat_label,
                                    className="context-inline-value",
                                ),
                                html.Span(
                                    "?",
                                    className="context-info-circle",
                                    title="Click to show full description",
                                ),
                            ],
                            className="tab-context-inline",
                        )
                    ],
                    className="tab-context-container",
                    style={
                        "marginTop": "-6px",
                        "marginBottom": "4px",
                    },
                )

        outputs.append(content)

    return outputs

@app.callback(
    Output("orchestrator-status-label", "children"),
    Input("tab-view-mode-store", "data"),
)
def update_orchestrator_status(mode):
    # print("uos")
    # print(3)
    # print(mode)
    label_map = {
        "per_wp": "Per Work Package",
        "per_category": "Per Category",
        "per_function": "Per Function",
        "favorites": "Favorites",
    }
    label = label_map.get(mode, "Not configured")

    return [
        html.Span("Orchestrator", className="orch-label-muted"),
        html.Span(" | ", className="orch-label-sep"),
        html.Span(label, className="orch-label-active"),
    ]


@app.callback(
    Output("orchestrator-options", "children"),
    Input("orchestrator-search", "value"),
)
def render_orchestrator_options(search):
    # print("roo")
    # print(4)
    # print(search)
    search = (search or "").lower()

    children = []
    search_matches = []

    # ------------------------------
    # SEARCH MATCHES (ADDITIVE)
    # ------------------------------
    if search:
        for opt in ORCHESTRATOR_OPTIONS:
            label = opt["label"]
            value = opt["value"]
            disabled = opt["disabled"]

            if search in label.lower():
                search_matches.append(
                    html.Div(
                        label,
                        id={"type": "orch-option", "value": value, "scope": "match"},
                        className=f"orch-option {'disabled' if disabled else ''}",
                    )
                )

    if search_matches:
        children.extend(search_matches)
        children.append(html.Div(className="orch-divider"))

    # ------------------------------
    # FULL LIST (ALWAYS VISIBLE)
    # ------------------------------
    for opt in ORCHESTRATOR_OPTIONS:
        label = opt["label"]
        value = opt["value"]
        disabled = opt["disabled"]

        children.append(
            html.Div(
                label,
                id={"type": "orch-option", "value": value, "scope": "all"},
                className=f"orch-option {'disabled' if disabled else ''}",
            )
        )

    return children


# @app.callback(
#     Output("tab-view-mode", "value"),
#     Output("orchestrator-panel", "style"),
#     Input("orchestrator-status", "n_clicks"),
#     Input({"type": "orch-option", "value": ALL}, "n_clicks"),
#     State("orchestrator-panel", "style"),
#     prevent_initial_call=True,
# )
# def orchestrator_panel_controller(status_clicks, option_clicks, panel_style):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         raise dash.exceptions.PreventUpdate

#     trigger = ctx.triggered_id

#     # ---------------------------------
#     # CLICK ON STATUS → TOGGLE PANEL
#     # ---------------------------------
#     if trigger == "orchestrator-status":
#         is_open = panel_style and panel_style.get("display") == "block"
#         return dash.no_update, {"display": "none" if is_open else "block"}

#     # ---------------------------------
#     # CLICK ON OPTION → SELECT + CLOSE
#     # ---------------------------------
#     if isinstance(trigger, dict) and trigger.get("type") == "orch-option":
#         value = trigger.get("value")

#         # ignore disabled options
#         for opt in ORCHESTRATOR_OPTIONS:
#             if opt["value"] == value and opt["disabled"]:
#                 raise dash.exceptions.PreventUpdate

#         return value, {"display": "none"}

#     raise dash.exceptions.PreventUpdate

@app.callback(
    Output("orchestrator-panel", "style"),
    Output("orchestrator-search", "value"),
    Input("orchestrator-status", "n_clicks"),
    Input("orchestrator-panel-hide", "n_clicks"),
    State("orchestrator-panel", "style"),
    prevent_initial_call=True,
)
def toggle_orchestrator_panel(status_clicks, hide_clicks, style):
    # print("top")
    # print(5)
    # print(status_clicks)
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    trigger = ctx.triggered_id
    is_open = style and style.get("display") == "block"

    # ---------------------------------
    # CLICK ON STATUS → TOGGLE PANEL
    # ---------------------------------
    if trigger == "orchestrator-status":
        if is_open:
            # closing → reset search
            return {"display": "none"}, ""
        else:
            # opening → reset search
            return {"display": "block"}, ""

    # ---------------------------------
    # CLICK ON HIDE BUTTON → CLOSE
    # ---------------------------------
    if trigger == "orchestrator-panel-hide":
        if is_open:
            return {"display": "none"}, ""
        raise dash.exceptions.PreventUpdate

    raise dash.exceptions.PreventUpdate

@app.callback(
    Output("tab-view-mode-store", "data"),
    Input({"type": "orch-option", "value": ALL, "scope": ALL}, "n_clicks_timestamp"),
    State("tab-view-mode-store", "data"),
    prevent_initial_call=True,
)
def select_orchestrator_option(timestamps, current_mode):

    # Αν όλα είναι None → ΔΕΝ υπήρξε click
    if not timestamps or all(t is None for t in timestamps):
        raise dash.exceptions.PreventUpdate

    # Πάρε το πιο πρόσφατο click
    idx = max(
        range(len(timestamps)),
        key=lambda i: timestamps[i] or -1
    )

    ctx = dash.callback_context
    trigger = ctx.inputs_list[0][idx]["id"]

    value = trigger.get("value")

    if value == current_mode:
        raise dash.exceptions.PreventUpdate

    return value

@app.callback(
    Output("tab-view-mode", "value"),
    Input("tab-view-mode-store", "data"),
)
def sync_mode_store_to_dropdown(mode):
    # print("smstd")
    # print(7)
    return mode
# ============================================================
# AUTO REGISTER TAB CALLBACKS
# ============================================================

for tab in TAB_MODULES:
    if hasattr(tab, "register_callbacks"):
        tab.register_callbacks(app)


# ============================================================
# FLASK ROUTES
# ============================================================

from utils import routes, routes_partnerdata

routes.register_routes(app.server)
routes_partnerdata.register_partner_routes(app.server)

if __name__ == "__main__":
    app.run(debug=True)