# Configuration Management Plan — Personal Expense Tracker

| | |
|---|---|
| **Project** | Personal Expense Tracker |
| **Document** | SCM Plan (CI-10) |
| **Version** | 1.0 |
| **Applies to** | All project configuration items |

---

## 1. Purpose
This plan defines how configuration items (CIs) are identified, controlled, status-accounted, and audited across the project's releases (v1.0 → v4.0). It is itself a configuration item and evolves with the project.

## 2. Configuration Items

| CI ID | Configuration Item | Location | Baseline |
|---|---|---|---|
| CI-01 | Software Requirements Specification | `docs/SRS/SRS.md` | v1.0 |
| CI-02 | Use Case Diagram | `docs/Design/UseCaseDiagram.md` | v1.0 |
| CI-03 | Class Diagram | `docs/Design/ClassDiagram.md` | v1.0 |
| CI-04 | Database Design | `docs/Design/ERDiagram.md` | v1.0 |
| CI-05 | Source Code | `src/` | v1.0 |
| CI-06 | SQL Scripts | `src/database/` | v1.0 |
| CI-07 | Test Cases | `test/test-cases.md`, `test/test_validation.py` | v1.0 |
| CI-08 | User Manual | `docs/User-Manual/UserManual.md` | v1.0 |
| CI-09 | Release Notes | `releases/v*/release-notes-*.md` | v1.0 |
| CI-10 | Configuration Management Plan | `docs/SCM-Plan/ConfigurationManagementPlan.md` | v1.0 |

## 3. Version Numbering
- **SemVer** `MAJOR.MINOR.PATCH` for releases; Git tags `vMAJOR.MINOR.PATCH` (annotated).
- Planned release ladder: v1.0.0 → v1.1.0 → v2.0.0 → v2.1.0 → v3.0.0 → v4.0.0.
- Documents carry their own version in the header table and are re-baselined with the release that changes them.

## 4. Branching Strategy

```
main ─────────────●────────●─────►   (tagged releases only)
                   \      /
develop ───●───●───●────●───●────►   (integration branch)
            \ /
feature/… ───●───●                 (short-lived work branches)
```

- `main` always points at the latest tagged release; only merge `develop` into `main` to cut a release.
- `develop` integrates completed features.
- Branch names: `feature/<topic>` (e.g. `feature/edit-transactions` for v1.1), `fix/<topic>`, `docs/<topic>`.
- Merges: `--no-ff` into `develop`; resolve conflicts in the feature branch first.

## 5. Change Control
1. **Raise:** Note the needed change (issue, task, or course-change-request form).
2. **Assess:** Identify affected CIs (code + docs + tests must move together).
3. **Approve:** For a semester project, the developer acts as the Change Control Board; record the decision in the change note or commit body.
4. **Implement:** On a `feature/*` or `fix/*` branch; update the SRS/SCM doc rows and test cases for any behavior change.
5. **Verify:** Run `pytest` before every merge; add new test cases for new behavior.
6. **Close:** Merge, reference the change in the release notes of the next version.

## 6. Release Process
1. On `develop`, confirm all release features and tests are green.
2. Merge `develop` → `main` with `--no-ff`.
3. Update CI-09: write `releases/vX.Y/release-notes-vX.Y.md`.
4. Tag: `git tag -a vX.Y.0 -m "Release vX.Y.0: <theme>"`.
5. Update version string in the app footer and this plan's affected-CI table.
6. Archive the release folder (`releases/vX.Y/`) with notes and, where required, a source snapshot reference.

## 7. Status Accounting and Audits
- `git log` / `git tag` are the authoritative status record.
- Before each release, audit: all planned FRs implemented and tested; docs updated to match code; no secrets (`.env`) committed; `.gitignore` covers build artifacts.
- The `releases/` directory and tags together form the release baseline.

## 8. Tools
| Concern | Tool |
|---|---|
| Version control | Git |
| Remote hosting | GitHub |
| Build/run | Python 3 venv, `pip` |
| Testing | pytest |
| Database | MySQL 8 (schema/seed scripts under version control) |
