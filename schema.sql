CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB,
    request_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS outbox (
    id UUID PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    aggregate_id UUID NOT NULL,
    payload JSONB,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS loan_projection (
    loan_id UUID PRIMARY KEY,
    status VARCHAR(50),
    credit_score INTEGER,
    monthly_income INTEGER,
    risk VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS snapshots (
    aggregate_id UUID PRIMARY KEY,
    state JSONB,
    last_event_time TIMESTAMP,
    event_count INTEGER
);

CREATE TABLE IF NOT EXISTS saga_checkpoints (
    saga_name VARCHAR(100) PRIMARY KEY,
    last_event_id UUID
);

CREATE TABLE IF NOT EXISTS projection_checkpoints (
    projection_name VARCHAR(100) PRIMARY KEY,
    last_event_id UUID
);

CREATE TABLE IF NOT EXISTS risk_dashboard_projection (
    id INTEGER PRIMARY KEY,
    low_risk_count INTEGER DEFAULT 0,
    high_risk_count INTEGER DEFAULT 0,
    approved_count INTEGER DEFAULT 0,
    rejected_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS loan_statistics_projection (
    id INTEGER PRIMARY KEY,
    total_loans INTEGER DEFAULT 0,
    approved_loans INTEGER DEFAULT 0,
    rejected_loans INTEGER DEFAULT 0
);

INSERT INTO saga_checkpoints (saga_name, last_event_id)
VALUES ('loan_saga', NULL)
ON CONFLICT (saga_name) DO NOTHING;

INSERT INTO projection_checkpoints (projection_name, last_event_id)
VALUES ('loan_projection', NULL)
ON CONFLICT (projection_name) DO NOTHING;

INSERT INTO risk_dashboard_projection (
    id,
    low_risk_count,
    high_risk_count,
    approved_count,
    rejected_count
)
VALUES (1,0,0,0,0)
ON CONFLICT (id) DO NOTHING;

INSERT INTO loan_statistics_projection (
    id,
    total_loans,
    approved_loans,
    rejected_loans
)
VALUES (1,0,0,0)
ON CONFLICT (id) DO NOTHING;