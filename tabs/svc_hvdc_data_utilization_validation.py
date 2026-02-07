from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import time
import numpy as np
import pandas as pd

import shutil
from dash import html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from utils.paths import PARTNER_DATA_DIR

"""
HVDC Data Utilization & Validation Analytics Tool

Purpose:
This service provides an analytical and exploratory environment for assessing
how heterogeneous HVDC-related datasets (e.g. PMU, SCADA, laboratory and
partner-provided data) are integrated, utilized, and validated within the
CABLEGNOSIS platform.

The tool combines:
- Data utilization and integration analytics (KPIs, comparisons, Sankey-style
  data flow visualizations), and
- Data relevance and validation views, supporting assessment of data readiness
  for monitoring, diagnostics, and analytics workflows.

Role in the project:
The service bridges Work Package development and the CABLEGNOSIS platform by
making project-driven datasets and integration pipelines visible, measurable,
and reviewable. It directly supports WP4 activities related to data integration
and monitoring foundations, as well as WP5 validation and WP6 demonstration
activities (e.g. M18/M30 reviews).

Note:
This service intentionally combines utilization and validation aspects.
These may be separated into distinct tools in later project phases.
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
    "id": "svc-hvdc-data-utilization-validation",
    "label": "HVDC Data Utilization & Validation Analytics",
    "type": "service",

    # Keep close to other analytics services
    "order": 225,

    # Originates in monitoring tasks, used for validation and demos
    "workpackages": ["WP4", "WP5", "WP6"],

    # Cross-cutting by nature
    "categories": [
        "Monitoring & Analytics",
        "Cable System Awareness",
        "Cable Performance & Optimization"
    ],

    # Not structured yet
    "subcategories": [],

    # Future extension point
    # "functions": [],

    "version": "v0.1 (demo)",
    "status": "active"
}

# -----------------------------
# Demo dataset configuration
# -----------------------------
DATA_DIR = PARTNER_DATA_DIR
DATA_DIR.mkdir(parents=True, exist_ok=True)

# We'll generate/append a few small CSVs and always read the latest N files
CSV_PREFIX = "partner_cable_metrics"
NUM_FILES = 5
ROWS_PER_FILE = 60

# Cable-relevant dummy metrics (common HV cable insulation / construction indicators)
# (names are for demo; units are indicative)
CABLE_METRICS = [
    ("insulation_thickness_mm", "Insulation thickness (mm)"),
    ("insulation_layers", "Insulation layers (#)"),
    ("relative_permittivity_epsr", "Relative permittivity εr (-)"),
    ("dielectric_strength_kv_per_mm", "Dielectric strength (kV/mm)"),
    ("tan_delta", "Dielectric loss (tanδ) (-)"),
    ("volume_resistivity_ohm_cm", "Volume resistivity (Ω·cm)"),
]


def _metric_keys() -> list[str]:
    return [k for k, _ in CABLE_METRICS]


def _metric_label(key: str) -> str:
    for k, lbl in CABLE_METRICS:
        if k == key:
            return lbl
    return key


def _get_tz_display() -> str:
    now = datetime.now().astimezone()

    # UTC offset
    offset_sec = now.utcoffset().total_seconds()
    hours = int(offset_sec // 3600)
    minutes = int((offset_sec % 3600) // 60)
    sign = "+" if hours >= 0 else "-"
    offset = f"UTC{sign}{abs(hours):02d}:{abs(minutes):02d}"

    # DST / Standard
    is_dst = time.localtime().tm_isdst > 0
    season = "Daylight Saving Time" if is_dst else "Standard Time"

    # Controlled timezone short code (NO locale dependency)
    if hours == 2 and not is_dst:
        tz_code = "EET"
    elif hours == 3 and is_dst:
        tz_code = "EEST"
    else:
        tz_code = "Local"

    return f"{offset} ({season} | {tz_code})"

def _csv_path(idx: int) -> Path:
    return PARTNER_DATA_DIR / f"{CSV_PREFIX}.{idx}.csv"


def _rotate_files_if_needed(max_rows_per_file: int = 100) -> None:
    """
    Keep files small:
    - We write to the "latest" file (highest index that exists, else 1).
    - If it's above max_rows_per_file, we rotate (increment index up to NUM_FILES, then shift).
    """
    # Determine current file index
    existing = sorted(DATA_DIR.glob(f"{CSV_PREFIX}.*.csv"))
    if not existing:
        # create first file
        df = _generate_dummy_frame(ROWS_PER_FILE)
        df.to_csv(_csv_path(1), index=False)
        return

    # latest by numeric suffix
    def _idx(p: Path) -> int:
        try:
            return int(p.stem.split(".")[-1])
        except Exception:
            return 1

    existing = sorted(existing, key=_idx)
    latest = existing[-1]
    latest_idx = _idx(latest)

    # If latest too large, rotate
    try:
        rows = sum(1 for _ in open(latest, "r", encoding="utf-8")) - 1  # minus header
    except Exception:
        rows = max_rows_per_file + 1

    if rows <= max_rows_per_file:
        return

    # rotation: if we already have NUM_FILES, shift down (2->1, 3->2, ...)
    if latest_idx >= NUM_FILES:
        # rotate DOWNWARDS to avoid overwrite (Windows-safe)
        for i in range(NUM_FILES - 1, 0, -1):
            src = _csv_path(i)
            dst = _csv_path(i - 1)
            if src.exists():
                try:
                    if dst.exists():
                        dst.unlink()  # remove destination first
                    shutil.move(src, dst)
                except (PermissionError, FileExistsError, FileNotFoundError):
                    return
        # new latest becomes NUM_FILES
        df = _generate_dummy_frame(ROWS_PER_FILE)
        df.to_csv(_csv_path(NUM_FILES), index=False)
    else:
        # create next file
        df = _generate_dummy_frame(ROWS_PER_FILE)
        df.to_csv(_csv_path(latest_idx + 1), index=False)


def _generate_dummy_frame(n: int) -> pd.DataFrame:
    """
    Generates cable-like dummy metrics with some realistic-ish ranges and correlations.
    Not meant to be physically exact; just plausible demo data.
    """
    rng = np.random.default_rng()

    insulation_thickness = rng.normal(25, 4, n).clip(12, 40)  # mm (e.g., HVDC ~20-30mm typical bands)
    layers = rng.integers(3, 8, n)  # integer layers

    # XLPE relative permittivity around ~2.4 (varies slightly)
    epsr = rng.normal(2.4, 0.12, n).clip(2.0, 3.0)

    # dielectric strength kV/mm: loosely around 25-40 for XLPE-type insulation
    diel_strength = (rng.normal(32, 4, n) + (epsr - 2.4) * (-6)).clip(18, 45)

    # tan delta: very small; we keep it small but allow some outliers
    tan_delta = np.abs(rng.normal(3e-4, 2e-4, n)).clip(5e-5, 3e-3)

    # volume resistivity: huge range; use log-normal
    log_rho = rng.normal(16.5, 0.7, n)  # 10^16-ish order
    rho = (10 ** log_rho).clip(1e12, 1e19)

    df = pd.DataFrame(
        {
            "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * n,
            "insulation_thickness_mm": insulation_thickness,
            "insulation_layers": layers.astype(float),  # keep numeric for corr
            "relative_permittivity_epsr": epsr,
            "dielectric_strength_kv_per_mm": diel_strength,
            "tan_delta": tan_delta,
            "volume_resistivity_ohm_cm": rho,
        }
    )
    return df


def _read_last_files(n_files: int = 2) -> pd.DataFrame:
    """
    Read the last n_files (by index) and merge them.
    """
    paths = sorted(DATA_DIR.glob(f"{CSV_PREFIX}.*.csv"))
    if not paths:
        return pd.DataFrame(columns=["timestamp"] + _metric_keys())

    def _idx(p: Path) -> int:
        try:
            return int(p.stem.split(".")[-1])
        except Exception:
            return 0

    paths = sorted(paths, key=_idx)[-n_files:]
    frames = []
    for p in paths:
        try:
            df = pd.read_csv(p)
            frames.append(df)
        except Exception:
            continue

    if not frames:
        return pd.DataFrame(columns=["timestamp"] + _metric_keys())

    df_all = pd.concat(frames, ignore_index=True)
    # clean: keep only numeric columns for corr (and drop nulls)
    for k in _metric_keys():
        df_all[k] = pd.to_numeric(df_all.get(k, np.nan), errors="coerce")
    df_all = df_all.dropna(subset=_metric_keys(), how="any")
    return df_all


# -----------------------------
# Figures
# -----------------------------
def _make_pie_fig(seed: int | None = None) -> go.Figure:
    rng = np.random.default_rng(seed)

    labels = ["MQTT", "REST", "OPC UA", "IEC 61850 (mock)"]
    values = rng.integers(10, 50, size=len(labels))
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.45,
                textinfo="label+percent",
            )
        ]
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=320,
        title="Protocol Share (Demo)",
    )
    return fig


def _make_sankey_fig(seed: int | None = None) -> go.Figure:
    rng = np.random.default_rng(seed)

    # Dummy "Partner Data Flow" - consistent with this tab
    nodes = [
        "Devices",
        "Edge Gateway",
        "Partner API",
        "Data Lake",
        "Analytics",
        "Dashboard",
    ]
    # links: source->target with values
    links = [
        (0, 1, int(rng.integers(20, 60))),
        (1, 2, int(rng.integers(10, 50))),
        (2, 3, int(rng.integers(10, 50))),
        (3, 4, int(rng.integers(10, 50))),
        (4, 5, int(rng.integers(10, 50))),
        (1, 5, int(rng.integers(5, 20))),  # bypass demo
    ]
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    label=nodes,
                    pad=15,
                    thickness=18,
                ),
                link=dict(
                    source=[s for s, t, v in links],
                    target=[t for s, t, v in links],
                    value=[v for s, t, v in links],
                ),
            )
        ]
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=320,
        title="Partner Data Flow (Demo)",
    )
    return fig


def _make_corr_heatmap(df: pd.DataFrame, order: list[str]) -> go.Figure:
    # correlation only on selected metric columns
    cols = [c for c in order if c in df.columns]
    if len(cols) < 2 or df.empty:
        # return empty-ish fig
        fig = go.Figure()
        fig.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=40, b=20),
            title="Correlation Map (Demo)",
        )
        return fig

    corr = df[cols].corr(method="pearson")

    # heatmap without text labels (hover shows value)
    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=[_metric_label(c) for c in corr.columns],
            y=[_metric_label(c) for c in corr.index],
            zmin=-1,
            zmax=1,
            colorscale="RdBu",
            hovertemplate="X: %{x}<br>Y: %{y}<br>Corr: %{z:.3f}<extra></extra>",
        )
    )
    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=40, b=20),
        title="Correlation Map (Demo)",
    )
    return fig


def _dropdown_options(disable_key: str | None = None) -> list[dict]:
    opts = []
    for k, lbl in CABLE_METRICS:
        opts.append(
            {
                "label": lbl,
                "value": k,
                "disabled": (disable_key == k),
            }
        )
    return opts


# -----------------------------
# Layout
# -----------------------------
def layout():
    tz = _get_tz_display()

    return html.Div(
        className="partner-tab",
        children=[
            html.Div(
                style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"},
                children=[
                    html.H3("Partner Data Integration", className="tab-title"),
                    dbc.Badge(f"Timezone: {tz}", color="info", pill=True, style={"fontSize": "0.95rem"}),
                ],
            ),

            # Top row: Pie + Sankey with a refresh button (NO routes)
            dbc.Row(
                className="mt-2",
                children=[
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.Div(
                                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"},
                                        children=[
                                            html.Span("Partner Telemetry Snapshot"),
                                            dbc.Button("Refresh", id="partner-refresh-btn", n_clicks=0, color="primary", size="sm"),
                                        ],
                                    ),
                                    style={"background": "#eef6ff"},
                                ),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="partner-pie",
                                        figure=_make_pie_fig(seed=1),
                                        config={"displayModeBar": False},
                                    )
                                ),
                            ],
                            style={"borderRadius": "10px"},
                        ),
                        md=5,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Integration Path (Dummy)", style={"background": "#fff3e6"}),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="partner-sankey",
                                        figure=_make_sankey_fig(seed=1),
                                        config={"displayModeBar": False},
                                    )
                                ),
                            ],
                            style={"borderRadius": "10px"},
                        ),
                        md=7,
                    ),
                ],
            ),

            # Existing blocks (kept conceptually similar, but NO route buttons)
            html.Div(
                className="partner-controls",
                children=[
                    html.Div(
                        [
                            html.Img(src="/assets/iot_device.png", className="partner-icon"),
                            html.H4("Devices & Protocols"),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Select Device:"),
                            dcc.Dropdown(
                                id="device-dropdown",
                                options=[
                                    {"label": "UCY Thermal Node", "value": "UCY-001"},
                                    {"label": "UoS Strain Sensor", "value": "UOS-002"},
                                    {"label": "IWO Magnetic Probe", "value": "IWO-003"},
                                ],
                                value="UCY-001",
                                className="device-dropdown",
                            ),
                            # Keep UI simple: no routes / no popups
                            html.Button("↻ Refresh Details", id="device-refresh-btn", n_clicks=0, className="action-button"),
                        ]
                    ),
                ],
            ),

            html.Div(
                id="device-info",
                className="device-info",
                children=[
                    html.H4("Device Information"),
                    html.P("Select a device and click refresh to view details (dummy)."),
                ],
            ),

            html.Div(
                id="system-summary",
                className="system-summary",
                children=[
                    html.H4("System Summary"),
                    html.Ul(
                        [
                            html.Li("Active Devices: 3"),
                            html.Li("Total Alerts: 0"),
                            html.Li("Supported Protocols: MQTT / REST / OPC UA"),
                            html.Li("Last Update: Jan 2026"),
                        ]
                    ),
                ],
            ),

            # Correlation tool
            dbc.Card(
                className="mt-3",
                style={"borderRadius": "10px"},
                children=[
                    dbc.CardHeader(
                        html.Div(
                            style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"},
                            children=[
                                html.Span("Cable Metrics Correlation (Demo)"),
                                dbc.Badge("hover a cell to see value", color="secondary", pill=True),
                            ],
                        ),
                        style={"background": "#f0f7f2"},
                    ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label("Metric A"),
                                            dcc.Dropdown(
                                                id="corr-metric-a",
                                                options=_dropdown_options(disable_key=None),
                                                value=CABLE_METRICS[0][0],
                                                clearable=False,
                                            ),
                                        ],
                                        md=5,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Label("Metric B"),
                                            dcc.Dropdown(
                                                id="corr-metric-b",
                                                options=_dropdown_options(disable_key=CABLE_METRICS[0][0]),
                                                value=CABLE_METRICS[1][0],
                                                clearable=False,
                                            ),
                                        ],
                                        md=5,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Label("\u00A0"),
                                            html.Div(
                                                [
                                                    dbc.Button("Show", id="corr-show-btn", n_clicks=0, color="success", className="me-2"),
                                                    dbc.Button("Refresh Data", id="corr-refresh-btn", n_clicks=0, color="warning"),
                                                ]
                                            ),
                                        ],
                                        md=2,
                                    ),
                                ],
                                className="g-2",
                            ),
                            html.Hr(),
                            dcc.Graph(
                                id="corr-heatmap",
                                figure=_make_corr_heatmap(pd.DataFrame(), order=_metric_keys()),
                                config={"displayModeBar": False},
                            ),
                            html.Div(
                                id="corr-footnote",
                                style={"fontSize": "0.9rem", "opacity": 0.8},
                                children="Tip: choose two metrics; the same metric is disabled in the other dropdown.",
                            ),
                        ]
                    ),
                ],
            ),

            # Stores
            dcc.Store(id="partner-data-store"),
            dcc.Store(id="corr-data-seed-store"),
        ],
    )


# -----------------------------
# Callbacks
# -----------------------------
def register_callbacks(app):
    # Refresh pie + sankey (NO routes)
    @app.callback(
        Output("partner-pie", "figure"),
        Output("partner-sankey", "figure"),
        Input("partner-refresh-btn", "n_clicks"),
        prevent_initial_call=False,
    )
    def refresh_partner_charts(n):
        seed = int(n or 0) + 1
        return _make_pie_fig(seed=seed), _make_sankey_fig(seed=seed)

    # Dummy device info refresh
    @app.callback(
        Output("device-info", "children"),
        Input("device-refresh-btn", "n_clicks"),
        State("device-dropdown", "value"),
        prevent_initial_call=False,
    )
    def refresh_device_info(n, device_id):
        device_id = device_id or "UCY-001"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [
            html.H4("Device Information"),
            html.Ul(
                [
                    html.Li(f"Device ID: {device_id}"),
                    html.Li("Status: Online (demo)"),
                    html.Li("Sampling: 1 Hz (demo)"),
                    html.Li(f"Last refresh: {now}"),
                ]
            ),
        ]

    # Grey-out logic: when A changes, disable same value in B options
    @app.callback(
        Output("corr-metric-b", "options"),
        Input("corr-metric-a", "value"),
    )
    def disable_in_b(metric_a):
        return _dropdown_options(disable_key=metric_a)

    # And vice versa: when B changes, disable same in A options
    @app.callback(
        Output("corr-metric-a", "options"),
        Input("corr-metric-b", "value"),
    )
    def disable_in_a(metric_b):
        return _dropdown_options(disable_key=metric_b)

    # Refresh data: rotate files / generate new dummy CSV chunk
    @app.callback(
        Output("corr-data-seed-store", "data"),
        Input("corr-refresh-btn", "n_clicks"),
        prevent_initial_call=False,
    )
    def refresh_corr_data(_):
        _rotate_files_if_needed(max_rows_per_file=100)
        # Append a new chunk to the latest file to simulate "fresh" partner dataset
        # Find latest file index; if none, rotation created it.
        paths = sorted(DATA_DIR.glob(f"{CSV_PREFIX}.*.csv"))
        if not paths:
            return {"ok": True, "ts": datetime.now().isoformat()}

        def _idx(p: Path) -> int:
            try:
                return int(p.stem.split(".")[-1])
            except Exception:
                return 1

        latest = sorted(paths, key=_idx)[-1]
        df_new = _generate_dummy_frame(ROWS_PER_FILE)
        df_new.to_csv(latest, mode="a", header=False, index=False)
        return {"ok": True, "ts": datetime.now().isoformat()}

    # Show correlation heatmap
    @app.callback(
        Output("corr-heatmap", "figure"),
        Input("corr-show-btn", "n_clicks"),
        State("corr-metric-a", "value"),
        State("corr-metric-b", "value"),
        State("corr-data-seed-store", "data"),
        prevent_initial_call=False,
    )
    def show_corr(n, metric_a, metric_b, _seed_state):
        # Always ensure we have some data
        _rotate_files_if_needed(max_rows_per_file=100)

        df_all = _read_last_files(n_files=2)

        # If still empty, generate one file and re-read
        if df_all.empty:
            df = _generate_dummy_frame(ROWS_PER_FILE)
            df.to_csv(_csv_path(1), index=False)
            df_all = _read_last_files(n_files=2)

        # Build order: selected A, selected B, then the rest
        all_keys = _metric_keys()
        metric_a = metric_a or all_keys[0]
        metric_b = metric_b or all_keys[1]
        order = [metric_a, metric_b] + [k for k in all_keys if k not in (metric_a, metric_b)]

        return _make_corr_heatmap(df_all, order=order)