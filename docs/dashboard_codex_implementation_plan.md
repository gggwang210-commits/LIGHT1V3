# Dashboard Codex Implementation Plan

## Goal

Create a commercialization-ready blueprint without overbuilding production application code.

## Phase 1 — Documentation baseline

- Maintain non-medical positioning in README and docs.
- Keep role-based specs for Member, Trainer, and Admin dashboards.
- Use synthetic-only sample data.

## Phase 2 — Static prototype

- Keep `prototype/dashboards/` dependency-free.
- Use `dashboard_mock_data.js` as the only data source.
- Validate copy against `docs/dashboard_safety_copy_guidelines.md`.

## Phase 3 — Future implementation

- Map components from `docs/dashboard_component_library.md` to Django templates or a future frontend app.
- Add authentication and role-based access before any real data handling.
- Add audit logging and consent state checks before media or sensitive record uploads.

## Acceptance checks

- Required docs exist.
- Sample JSON parses successfully.
- README links to dashboard docs and prototype files.
- Prototype contains non-medical disclaimer.
- Tests pass under pytest.
