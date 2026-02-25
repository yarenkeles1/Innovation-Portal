<!--
Sync Impact Report
Version change: unspecified → 1.0.0
Modified principles: (added) Security & Auth → Test-First → Local-First Deployment → Attachment & Data Integrity → Idea Lifecycle & Governance
Added sections: Additional Constraints, Development Workflow
Removed sections: placeholder tokens replaced with concrete sections
Templates requiring updates: .specify/templates/plan-template.md ✅ updated
												 .specify/templates/spec-template.md ✅ reviewed
												 .specify/templates/tasks-template.md ✅ reviewed
												 .specify/templates/commands/*.md ⚠ pending (none found)
Follow-up TODOs: RATIFICATION_DATE unresolved (TODO)
-->

# Innovation-Portal Constitution

## Core Principles

### I. Security-First Authentication & Authorization (NON-NEGOTIABLE)
The system MUST use JWT-based authentication for API access and enforce role-based
authorization (roles: `submitter`, `evaluator`, `admin`). Access controls are enforced
server-side for every endpoint and data mutation. Rationale: Protect user data,
support auditability, and prevent privilege escalation.

### II. Test-First Development (MANDATORY)
All new features and bug fixes MUST include automated tests before implementation:
- Backend: `pytest` unit and integration tests covering auth, status transitions, and file handling.
- Frontend: React Testing Library tests for core user flows (register, login, submit idea, admin review).
Rationale: Ensure regressions are caught early and maintainable quality.

### III. Local-First Deployment & Simplicity
Target environment is local development only. The default deployment MUST be
simple to run with documented local steps. Production-grade operational concerns
(scaling, HA) are out of scope unless explicitly added by an amendment.

### IV. Attachment & Data Integrity
Idea submission MUST support a single file attachment; server MUST validate file
type and size, store attachments alongside idea records in SQLite, and record a
checksum for integrity. Attachments MUST be scanned or validated for common
malformed content patterns. Rationale: Maintain data correctness and reduce risk.

### V. Idea Lifecycle & Administrative Governance
Idea records MUST include a `status` field with these states: `submitted`,
`under_review`, `accepted`, `rejected`. Administrative actions (approve/reject)
MUST be recordable with an admin comment and auditor-visible timestamp. Rationale:
Provide clear, auditable decision trails for idea evaluations.

## Additional Constraints
- Architecture: Frontend: React 18 + Vite + TypeScript. Backend: FastAPI with
	SQLite. Authentication: JWT. Authorization: Role-based (submitter/evaluator/admin).
- Testing: Pytest for backend, React Testing Library for frontend. Tests are
	required for all foundation work and high-priority user stories.
- Storage: Use SQLite for persistence; keep migrations or schema versioning in
	repository where appropriate.
- Security: Passwords MUST be hashed with a modern algorithm (e.g., bcrypt);
	JWT secrets managed via environment variables for local dev.

## Development Workflow
- Code reviews REQUIRED for PRs touching security, auth, or idea lifecycle logic.
- Foundational work (DB schema, auth) MUST be completed before feature
	development begins (see tasks template Phase 2 requirements).
- Tests MUST be written to fail before implementation (red → green workflow).
- Feature specs MUST include independent, testable user stories (see spec-template).

## Governance
Amendments to this constitution require a documented proposal and a two-step
approval: (1) technical review by at least one maintainer, (2) ratification by
project owners (or a TODO if ownership not defined). Versioning follows semantic
versioning:
- MAJOR: Backwards-incompatible governance or principle removals/renames.
- MINOR: New principle or material expansion.
- PATCH: Clarifications, wording, typos.

Compliance reviews: Every PR that implements policy-critical changes (auth,
role checks, status transitions, attachment handling) MUST include a checklist
linking relevant constitution sections and tests validating behavior.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): confirm adoption date | **Last Amended**: 2026-02-25
