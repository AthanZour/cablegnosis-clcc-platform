# System Documentation

This directory represents the **single semantic source of truth**
for the system.

The documentation is organized by **conceptual relevance** rather than
code structure, while still describing the **current implementation**
where it is part of stable system behavior.

There is intentionally **no separation** between "conceptual" and
"developer" documentation.  
All content here contributes to a unified understanding of:
- what the system is
- how it operates today
- how it evolves over time

---

## Directory Overview

### `overview/`
High-level understanding of the system.

Contains:
- purpose and scope
- mental model
- system-wide context

No implementation details.

---

### `meta/`
Canonical definitions and invariants.

Contains:
- terminology
- naming conventions
- stable concepts that define the system language

Changes here affect the entire system.

---

### `system/`
Documentation of the **current operating system**.

Describes how the system is structured and behaves today, including:
- layout organization
- callback responsibilities
- provided services
- shared utilities

This section reflects the active implementation from a semantic perspective,
not as a code reference.

---

### `roadmap/`
Intent and planned evolution.

Contains:
- future directions
- planned extensions
- architectural intentions

Does not describe current behavior.

---

### `deprecated/`
Historical record of removed or retired elements.

Contains:
- what was removed
- why it was removed
- what should not be reintroduced

This section exists to preserve system memory and prevent regression.

---

## Guiding Principle

> If something is hard to locate in this documentation,
> the system itself is not yet clearly defined.