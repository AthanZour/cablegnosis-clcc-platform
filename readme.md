# CABLEGNOSIS Dash Application

## Overview
This section provides an overview of the first stable alpha release of the platform, focusing on the UI/UX layer and the stabilization of the core codebase.  
The transition from version **0.8.x** to **1.0.1** marks the completion of the initial architectural foundation and interaction model.

Modular Dash-based demonstration platform for power cable monitoring,
synthetic data generation, and partner data integration.

This application is designed with a **production-oriented architecture**
while remaining lightweight and demo-friendly.

---

## Project Structure

├── app.py

├── README.md

├── assets/

├── tabs/

├── tabs_core/

├── logic/

├── utils/

└── data/

## High-Level Architecture

The application follows a strict separation of concerns to ensure
maintainability, scalability, and production readiness.

### app.py

- Application entry point
- Tab discovery and orchestration
- Global layout and navigation modes
- Metadata aggregation

`app.py` contains **no business logic and no UI-specific logic**.
Its sole responsibility is to wire together the application components.

---

### tabs/

- Discoverable UI tabs
- Each tab represents an isolated UI module
- Tabs are automatically discovered by the application

Each tab module must expose:

- `TAB_META`
- `layout()`
- `register_callbacks(app)`

Tabs must not:
- contain business logic
- manage filesystem paths directly
- depend on other tabs

---

### tabs_core/

- Shared UI logic used by tabs
- Reusable layouts, helpers, and callback logic
- Not scanned by the application

Modules in this folder **must not** expose `TAB_META`.

---

### logic/

- Pure business and data logic
- Synthetic data generators
- Computation and transformation functions

Modules in `logic/` must not:
- import Dash
- define callbacks
- access UI components

---

### utils/

- Cross-cutting utilities
- Centralized filesystem path registry
- Flask routes and lightweight helpers

All filesystem paths are defined in:
utils/paths.py

No other module should hard-code paths.

---

### data/

- All input and generated data used by the application
- No application logic resides here

See `data/README.md` for detailed data ownership and traceability.


## Change Log

### 2026-01-31

1. **Tab Orchestrator UI refinement**
   - Introduced explicit technical framing for the *Tab Orchestrator* control.
   - Replaced implicit separator with two independent visual lines:
     - Short delimiter line (`#A4ADB3`) under the label.
     - Longer closing line (`#92BEF7`) above the dropdown.
   - Lines are independently configurable (length, color, spacing).

2. **Primary & Secondary Tab Bar visual consistency**
   - Unified active-state styling across Work Package bar and Tool bar.
   - Active tabs now use strong industrial blue background with white text.
   - Non-active tabs remain light, improving hierarchy and readability.

3. **Scrollbar removal for horizontal tab navigation**
   - Native horizontal scrollbars hidden for WP and Tool tab bars.
   - Navigation is handled via click-based selection and drag-to-scroll.
   - Improves visual cleanliness and aligns with console-style UI.

4. **Separator system cleanup**
   - Removed deprecated `orchestrator-separator` element and CSS.
   - Introduced explicit, role-based separators with clear ownership:
     - Orchestrator ↔ WP bar
     - WP bar ↔ Tool bar
     - Tool bar ↔ Content area

5. **UX polishing and spacing normalization**
   - Normalized vertical spacing between orchestrator, tab bars, and content.
   - Reduced visual noise while preserving structural clarity.
   - Improved alignment consistency across horizontal sections.

---

## UI Tab Orchestrator – Architecture & Design Notes

The current UI Tab Orchestrator implementation (Per Work Package, Per Category)
follows a modular and extensible layout architecture.

Key design and UI decisions (layout structure, context handling, separators,
color system, and deprecation of legacy UI elements) have been documented
separately as private design notes
(note to the developer: see UI_Tab_Orchestrator_Architecture_Notes.pdf).

These notes capture the rationale behind architectural and UX decisions
and should be consulted before making structural changes to the UI orchestration layer.

---

## Current Status
- **Version:** 1.0.1  
- **Release stage:** Alpha  
- **Stability:** Core architecture stabilized, active development ongoing

---

## UI / UX
The user interface has been redesigned with a focus on clarity, usability, and scalability.

Key highlights include:
- Drag-to-scroll navigation for improved content interaction
- Clear separation of functional areas
- Improved visual hierarchy and readability
- Reserved layout space for future feature integrations

---

## Architecture
The platform is structured around clearly defined modules with explicit responsibilities.  
The orchestration layer has been reorganized into distinct sections, each serving a specific functional purpose.

This structure enables:
- Easier maintenance
- Predictable extensibility
- Clear ownership of functionality

---

## Repository Structure (High Level)

- **/documentation** – Technical and architectural documentation  
- **/meta** – Project metadata and internal conventions  
- **/overview** – High-level conceptual descriptions  
- **/planned** – Planned features and future improvements  
- **/deprecations** – Deprecated components and historical references  

---

## Development Notes
- This alpha release establishes the baseline for future iterations.
- Breaking changes should be documented and versioned accordingly.
- UI and architectural decisions should be reflected in the documentation.

---

## Next Steps

Further refinement, feature expansion, and performance optimization will continue in subsequent releases.



