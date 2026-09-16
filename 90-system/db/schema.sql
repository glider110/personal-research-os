-- Personal Research OS / SQLite schema v0.1
-- This file defines the data contract. It does not insert real market data.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS topic (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    kind TEXT NOT NULL,
    scope TEXT,
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source (
    id TEXT PRIMARY KEY,
    topic_id TEXT,
    title TEXT NOT NULL,
    source_type TEXT NOT NULL,
    publisher TEXT,
    canonical_uri TEXT,
    published_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topic(id)
);

CREATE TABLE IF NOT EXISTS source_snapshot (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    storage_uri TEXT NOT NULL,
    drive_file_id TEXT,
    content_hash TEXT NOT NULL,
    captured_at TEXT NOT NULL,
    revision_label TEXT,
    is_official_input INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (source_id) REFERENCES source(id)
);

CREATE TABLE IF NOT EXISTS metric_definition (
    id TEXT PRIMARY KEY,
    topic_id TEXT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    unit TEXT,
    frequency TEXT,
    geography TEXT,
    methodology TEXT,
    version TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    FOREIGN KEY (topic_id) REFERENCES topic(id)
);

CREATE TABLE IF NOT EXISTS metric_observation (
    id TEXT PRIMARY KEY,
    metric_id TEXT NOT NULL,
    period_start TEXT NOT NULL,
    period_end TEXT,
    value_numeric REAL,
    value_text TEXT,
    dimension_json TEXT,
    source_snapshot_id TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    revision INTEGER NOT NULL DEFAULT 0,
    quality_status TEXT NOT NULL DEFAULT 'unreviewed',
    FOREIGN KEY (metric_id) REFERENCES metric_definition(id),
    FOREIGN KEY (source_snapshot_id) REFERENCES source_snapshot(id)
);

CREATE TABLE IF NOT EXISTS evidence (
    id TEXT PRIMARY KEY,
    topic_id TEXT,
    source_snapshot_id TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    claim TEXT NOT NULL,
    excerpt TEXT,
    locator TEXT,
    scope TEXT,
    supports_json TEXT,
    contradicts_json TEXT,
    review_status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topic(id),
    FOREIGN KEY (source_snapshot_id) REFERENCES source_snapshot(id)
);

CREATE TABLE IF NOT EXISTS factor_definition (
    id TEXT PRIMARY KEY,
    topic_id TEXT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    mechanism TEXT NOT NULL,
    scope TEXT,
    assessment_method TEXT NOT NULL,
    version TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    FOREIGN KEY (topic_id) REFERENCES topic(id)
);

CREATE TABLE IF NOT EXISTS factor_state (
    id TEXT PRIMARY KEY,
    factor_id TEXT NOT NULL,
    as_of_date TEXT NOT NULL,
    direction TEXT NOT NULL,
    strength TEXT,
    confidence TEXT NOT NULL,
    evidence_ids_json TEXT NOT NULL,
    reversal_conditions TEXT,
    assessment_method TEXT NOT NULL,
    assessment_version TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (factor_id) REFERENCES factor_definition(id)
);

CREATE TABLE IF NOT EXISTS causal_edge (
    id TEXT PRIMARY KEY,
    topic_id TEXT,
    from_factor_id TEXT,
    to_factor_id TEXT,
    outcome_name TEXT,
    sign TEXT NOT NULL,
    mechanism TEXT NOT NULL,
    lag_description TEXT,
    scope TEXT,
    evidence_ids_json TEXT,
    status TEXT NOT NULL DEFAULT 'hypothesis',
    version TEXT NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topic(id),
    FOREIGN KEY (from_factor_id) REFERENCES factor_definition(id),
    FOREIGN KEY (to_factor_id) REFERENCES factor_definition(id)
);

CREATE TABLE IF NOT EXISTS scenario (
    id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    name TEXT NOT NULL,
    scenario_type TEXT NOT NULL,
    assumptions_json TEXT NOT NULL,
    path_json TEXT NOT NULL,
    observable_signals_json TEXT NOT NULL,
    falsifiers_json TEXT NOT NULL,
    version TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    FOREIGN KEY (topic_id) REFERENCES topic(id)
);

CREATE TABLE IF NOT EXISTS behavior_rule (
    id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    parent_id TEXT,
    node_type TEXT NOT NULL,
    name TEXT NOT NULL,
    condition_json TEXT,
    action_json TEXT,
    order_index INTEGER NOT NULL DEFAULT 0,
    version TEXT NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topic(id),
    FOREIGN KEY (parent_id) REFERENCES behavior_rule(id)
);

CREATE TABLE IF NOT EXISTS run_snapshot (
    id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    run_at TEXT NOT NULL,
    as_of_date TEXT NOT NULL,
    horizon_end TEXT,
    data_version TEXT NOT NULL,
    model_version TEXT NOT NULL,
    rule_version TEXT NOT NULL,
    factor_states_json TEXT NOT NULL,
    scenarios_json TEXT NOT NULL,
    judgment_json TEXT NOT NULL,
    action_json TEXT,
    status TEXT NOT NULL DEFAULT 'published',
    FOREIGN KEY (topic_id) REFERENCES topic(id)
);

CREATE TABLE IF NOT EXISTS review (
    id TEXT PRIMARY KEY,
    run_snapshot_id TEXT NOT NULL,
    reviewed_at TEXT NOT NULL,
    outcome_json TEXT NOT NULL,
    error_class TEXT,
    findings TEXT,
    revision_actions_json TEXT,
    FOREIGN KEY (run_snapshot_id) REFERENCES run_snapshot(id)
);

CREATE INDEX IF NOT EXISTS idx_metric_observation_metric_period
    ON metric_observation(metric_id, period_start);
CREATE INDEX IF NOT EXISTS idx_factor_state_factor_date
    ON factor_state(factor_id, as_of_date);
CREATE INDEX IF NOT EXISTS idx_run_snapshot_topic_date
    ON run_snapshot(topic_id, run_at);

-- v0.2 additive ingestion metadata; no implicit promotion of AI output.
CREATE TABLE IF NOT EXISTS processing_package (
    id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL REFERENCES topic(id),
    content_hash TEXT NOT NULL,
    storage_uri TEXT NOT NULL,
    producer_json TEXT NOT NULL,
    imported_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source_provenance (
    source_snapshot_id TEXT PRIMARY KEY REFERENCES source_snapshot(id),
    source_class TEXT NOT NULL,
    original_type TEXT NOT NULL,
    capture_method TEXT NOT NULL,
    coverage TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evidence_review (
    evidence_id TEXT PRIMARY KEY REFERENCES evidence(id),
    reviewer TEXT NOT NULL,
    reviewed_at TEXT NOT NULL,
    method TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS metric_evidence (
    observation_id TEXT NOT NULL REFERENCES metric_observation(id),
    evidence_id TEXT NOT NULL REFERENCES evidence(id),
    PRIMARY KEY (observation_id, evidence_id)
);

CREATE TRIGGER IF NOT EXISTS immutable_source_snapshot_update
BEFORE UPDATE ON source_snapshot BEGIN SELECT RAISE(ABORT, 'source snapshots are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_source_snapshot_delete
BEFORE DELETE ON source_snapshot BEGIN SELECT RAISE(ABORT, 'source snapshots are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_run_snapshot_update
BEFORE UPDATE ON run_snapshot BEGIN SELECT RAISE(ABORT, 'run snapshots are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_run_snapshot_delete
BEFORE DELETE ON run_snapshot BEGIN SELECT RAISE(ABORT, 'run snapshots are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_processing_package_update
BEFORE UPDATE ON processing_package BEGIN SELECT RAISE(ABORT, 'processing packages are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_review_update
BEFORE UPDATE ON review BEGIN SELECT RAISE(ABORT, 'reviews are append-only'); END;
CREATE TRIGGER IF NOT EXISTS immutable_review_delete
BEFORE DELETE ON review BEGIN SELECT RAISE(ABORT, 'reviews are append-only'); END;

-- Shared identities are independent of topics and ingestion batches.
CREATE TABLE IF NOT EXISTS shared_object (
    id TEXT PRIMARY KEY,
    kind TEXT NOT NULL CHECK(kind IN ('source','evidence','metric','factor','hypothesis'))
);
CREATE TABLE IF NOT EXISTS shared_revision (
    id TEXT PRIMARY KEY,
    object_id TEXT NOT NULL REFERENCES shared_object(id),
    definition_json TEXT NOT NULL,
    UNIQUE(object_id, definition_json)
);
CREATE TABLE IF NOT EXISTS shared_usage (
    package_id TEXT NOT NULL REFERENCES processing_package(id),
    kind TEXT NOT NULL,
    local_id TEXT NOT NULL,
    revision_id TEXT NOT NULL REFERENCES shared_revision(id),
    topic_id TEXT NOT NULL REFERENCES topic(id),
    payload_json TEXT NOT NULL,
    PRIMARY KEY(package_id, kind, local_id)
);
CREATE TABLE IF NOT EXISTS shared_relation (
    id TEXT PRIMARY KEY,
    from_revision TEXT NOT NULL REFERENCES shared_revision(id),
    relation TEXT NOT NULL CHECK(relation IN
      ('extracted_from','measured_by','uses_evidence','uses_metric','supports','refutes')),
    to_revision TEXT NOT NULL REFERENCES shared_revision(id),
    package_id TEXT REFERENCES processing_package(id),
    status TEXT NOT NULL CHECK(status IN ('reference','pending','reviewed')),
    rationale TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_shared_usage_revision ON shared_usage(revision_id);
CREATE INDEX IF NOT EXISTS idx_shared_relation_target ON shared_relation(to_revision);
