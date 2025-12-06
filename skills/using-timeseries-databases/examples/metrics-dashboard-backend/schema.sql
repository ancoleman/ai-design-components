-- TimescaleDB schema for metrics dashboard backend
-- Use case: System monitoring dashboard with CPU, memory, disk metrics

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create metrics table
CREATE TABLE metrics (
  time        TIMESTAMPTZ NOT NULL,
  host        TEXT NOT NULL,
  metric_name TEXT NOT NULL,
  value       DOUBLE PRECISION NOT NULL,
  tags        JSONB
);

-- Convert to hypertable
SELECT create_hypertable('metrics', 'time');

-- Create indexes for fast filtering
CREATE INDEX idx_metrics_host_time ON metrics (host, time DESC);
CREATE INDEX idx_metrics_name_time ON metrics (metric_name, time DESC);
CREATE INDEX idx_metrics_tags ON metrics USING GIN (tags jsonb_path_ops);

-- Enable compression on chunks older than 7 days
ALTER TABLE metrics SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'host, metric_name',
  timescaledb.compress_orderby = 'time DESC'
);

SELECT add_compression_policy('metrics', INTERVAL '7 days');

-- Continuous aggregate: 1-minute rollups
CREATE MATERIALIZED VIEW metrics_1min
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 minute', time) AS bucket,
       host,
       metric_name,
       AVG(value) AS avg_value,
       MAX(value) AS max_value,
       MIN(value) AS min_value,
       COUNT(*) AS sample_count
FROM metrics
GROUP BY bucket, host, metric_name;

-- Refresh policy: update every minute for last 3 hours
SELECT add_continuous_aggregate_policy('metrics_1min',
  start_offset => INTERVAL '3 hours',
  end_offset => INTERVAL '1 minute',
  schedule_interval => INTERVAL '1 minute');

-- Continuous aggregate: 1-hour rollups
CREATE MATERIALIZED VIEW metrics_1hour
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', time) AS bucket,
       host,
       metric_name,
       AVG(value) AS avg_value,
       MAX(value) AS max_value,
       MIN(value) AS min_value,
       STDDEV(value) AS stddev_value
FROM metrics
GROUP BY bucket, host, metric_name;

-- Refresh policy: update every hour for last 7 days
SELECT add_continuous_aggregate_policy('metrics_1hour',
  start_offset => INTERVAL '7 days',
  end_offset => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour');

-- Continuous aggregate: daily rollups
CREATE MATERIALIZED VIEW metrics_daily
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 day', time) AS bucket,
       host,
       metric_name,
       AVG(value) AS avg_value,
       MAX(value) AS max_value,
       MIN(value) AS min_value,
       STDDEV(value) AS stddev_value
FROM metrics
GROUP BY bucket, host, metric_name;

-- Refresh policy: update daily for last 90 days
SELECT add_continuous_aggregate_policy('metrics_daily',
  start_offset => INTERVAL '90 days',
  end_offset => INTERVAL '1 day',
  schedule_interval => INTERVAL '1 day');

-- Retention policy: delete raw data older than 30 days
SELECT add_retention_policy('metrics', INTERVAL '30 days');

-- Retention policy: delete 1-minute rollups older than 90 days
SELECT add_retention_policy('metrics_1min', INTERVAL '90 days');

-- Keep hourly and daily rollups forever (no retention policy)

-- Sample data for testing
INSERT INTO metrics (time, host, metric_name, value, tags) VALUES
  (NOW(), 'server-01', 'cpu_usage', 45.2, '{"region": "us-west", "env": "production"}'),
  (NOW(), 'server-01', 'memory_usage', 62.8, '{"region": "us-west", "env": "production"}'),
  (NOW(), 'server-01', 'disk_usage', 78.5, '{"region": "us-west", "env": "production"}'),
  (NOW(), 'server-02', 'cpu_usage', 32.1, '{"region": "us-east", "env": "production"}'),
  (NOW(), 'server-02', 'memory_usage', 55.3, '{"region": "us-east", "env": "production"}'),
  (NOW(), 'server-02', 'disk_usage', 65.2, '{"region": "us-east", "env": "production"}');

-- Verify setup
SELECT * FROM metrics ORDER BY time DESC LIMIT 10;
SELECT * FROM metrics_1min ORDER BY bucket DESC LIMIT 10;
