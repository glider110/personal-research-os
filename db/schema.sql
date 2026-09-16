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
