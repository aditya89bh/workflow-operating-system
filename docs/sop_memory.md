# SOP Memory

The SOP memory layer captures institutional knowledge as **standard operating
procedures (SOPs)**: versioned, searchable, authored documents linked to the
kinds of workflows they describe. It answers:

- How do we normally perform this workflow?
- What are our best practices?
- What lessons have we learned?
- What exceptions changed our process?
- Which SOP version should we follow?

It lives in the `workflow_os.sop` subpackage and is fully additive: it builds on
the workflow, memory, and decision layers without modifying them. Everything is
**deterministic and rule-based** — no LLMs, no autonomous generation. The flow
is **Capture -> Version -> Search -> Retrieve -> Link -> Analyze**.

## Concepts

### SOPRecord

A `SOPRecord` documents how a workflow type is performed:

| Field | Meaning |
|-------|---------|
| `sop_id` | Unique id for the SOP |
| `title` | Human-readable title |
| `workflow_type` | The kind of workflow this SOP documents |
| `description` | Longer description of the procedure |
| `version` | Monotonic version number (starts at 1) |
| `status` | Lifecycle status (see `SOPStatus`) |
| `author` | Primary author |
| `created_at` / `updated_at` | Timezone-aware UTC timestamps |
| `tags` | Free-form labels for search and grouping |
| `metadata` | Free-form key/value data (reviewers, owners, contributors) |

`SOPStatus` is one of `draft`, `active`, `deprecated`, or `archived`.

### Stores

`SOPStore` is a protocol with `add`, `get`, `update`, `delete`, `list`, and
`query`. `SQLiteSOPStore` is the standard implementation, backed by the standard
library `sqlite3` module (file-based or in-memory). `SOPQuery` filters by
workflow type, status, author, tags, and version.

## Versioning and change history

- `SOPVersionHistory` records immutable version snapshots and answers
  `current_version`, `previous_version`, and full `history`.
- `SOPChangeLog` records why a SOP changed, when, which fields changed, and who
  changed it. `diff_fields` computes the changed fields between two records.

## Authorship

`get_authorship` returns the author plus reviewers, owners, and contributors
(stored in metadata). `set_*` and `add_*` helpers manage those lists without
disturbing other metadata.

## Search

`search_by_title`, `search_by_workflow_type`, `search_by_tags`, `text_search`,
and the combined `search_sops` find SOPs by content and attributes.

## Workflow linking

Each SOP names a `workflow_type`, giving an implicit link. `WorkflowSOPLinks`
adds explicit many-to-many associations. `get_sops_for_workflow`,
`get_sops_for_workflow_type`, and `get_workflow_types_for_sop` retrieve across
both.

## Recommendation

The recommendation engine is deterministic and rule-based. `recommend_sop` /
`recommend_sops` rank SOPs by a fixed priority: explicit link, workflow-type
match, tag overlap, active status, then latest version, with `sop_id` as the
tie-breaker. `score_sops` provides numeric scores in `[0, 1]` from a fixed
weighted sum of workflow match, version recency, tag match, and usage frequency.

## Knowledge capture

- `LessonStore` / `capture_lesson` capture lessons, observations, postmortems,
  and operational notes.
- `BestPracticeStore` / `capture_best_practice` capture practices, guidelines,
  conventions, and standards.
- `SOPExceptionStore` / `capture_exception` and
  `capture_exception_from_decision` capture workflow exceptions, optionally
  derived from a Phase 3 exception decision.

## Analysis

- `detect_conflicts` (and the per-rule detectors) surface duplicate SOPs,
  version conflicts, ownership conflicts, and ambiguous workflow mappings.
- `generate_lifecycle_report` produces totals, active/inactive counts, version
  statistics, workflow coverage, and per-author counts.

## Demo

Run the end-to-end demonstration:

```bash
workflow-os sop-demo
# or
python -m workflow_os sop-demo
# or
python examples/sop_demo.py
```
