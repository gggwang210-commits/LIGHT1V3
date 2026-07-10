<!--
ARCHIVE NOTICE:
이 파일은 레거시 보관본입니다. 최신 기준은 루트 README.md와 docs/README.md를 우선합니다.
본 자료는 비의료 운동상담 참고용이며, 의료 진단·치료·처방 목적이 아닙니다. 모든 판단은 담당 트레이너가 검토합니다.
-->

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
