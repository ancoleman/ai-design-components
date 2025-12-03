"""
FastAPI backend for metrics dashboard.

Features:
- Query TimescaleDB for metrics
- Automatic downsampling with LTTB
- Adaptive data source selection (raw vs. rollups)
- WebSocket streaming for real-time updates
"""

from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import asyncio
import json

app = FastAPI(title="Metrics Dashboard API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="password",
        cursor_factory=RealDictCursor
    )

# LTTB downsampling algorithm
def lttb(data: List[Tuple], threshold: int) -> List[Dict]:
    """
    Largest-Triangle-Three-Buckets downsampling algorithm.

    Args:
        data: List of (timestamp, value) tuples
        threshold: Target number of points

    Returns:
        Downsampled list of dicts
    """
    if len(data) <= threshold:
        return [{"time": row[0].isoformat(), "value": row[1]} for row in data]

    sampled = [data[0]]
    every = (len(data) - 2) / (threshold - 2)
    a = 0

    for i in range(threshold - 2):
        avg_range_start = int((i + 1) * every) + 1
        avg_range_end = min(int((i + 2) * every) + 1, len(data))
        avg_x = sum(data[j][0].timestamp() for j in range(avg_range_start, avg_range_end)) / (avg_range_end - avg_range_start)
        avg_y = sum(data[j][1] for j in range(avg_range_start, avg_range_end)) / (avg_range_end - avg_range_start)

        range_offs = int(i * every) + 1
        range_to = int((i + 1) * every) + 1

        point_a_x = data[a][0].timestamp()
        point_a_y = data[a][1]

        max_area = -1
        next_a = 0

        for j in range(range_offs, range_to):
            area = abs(
                (point_a_x - avg_x) * (data[j][1] - point_a_y) -
                (point_a_x - data[j][0].timestamp()) * (avg_y - point_a_y)
            ) * 0.5

            if area > max_area:
                max_area = area
                next_a = j

        sampled.append(data[next_a])
        a = next_a

    sampled.append(data[-1])

    return [{"time": row[0].isoformat(), "value": row[1]} for row in sampled]

# Parse duration string (e.g., "1h", "7d", "30d")
def parse_duration(duration_str: str) -> timedelta:
    """Convert duration string to timedelta."""
    units = {
        'm': 'minutes',
        'h': 'hours',
        'd': 'days',
    }
    value = int(duration_str[:-1])
    unit = duration_str[-1]
    return timedelta(**{units[unit]: value})

# API Endpoints

@app.get("/api/metrics/{metric_name}")
async def get_metric(
    metric_name: str,
    start: str = Query("1h", description="Time range: 1h, 6h, 1d, 7d, 30d"),
    host: Optional[str] = Query(None, description="Filter by host"),
    points: int = Query(800, ge=100, le=2000, description="Target number of points")
):
    """
    Get metric data with automatic downsampling.

    Strategy:
    - < 1 hour: Raw data
    - 1-24 hours: 1-minute rollups
    - 1-7 days: 1-hour rollups
    - > 7 days: Daily rollups
    """
    duration = parse_duration(start)

    # Select data source based on time range
    if duration <= timedelta(hours=1):
        table = "metrics"
        time_col = "time"
    elif duration <= timedelta(days=1):
        table = "metrics_1min"
        time_col = "bucket"
    elif duration <= timedelta(days=7):
        table = "metrics_1hour"
        time_col = "bucket"
    else:
        table = "metrics_daily"
        time_col = "bucket"

    # Build query
    conn = get_db()
    cur = conn.cursor()

    query = f"""
        SELECT {time_col}, {'value' if table == 'metrics' else 'avg_value'}
        FROM {table}
        WHERE {time_col} > NOW() - INTERVAL %s
          AND metric_name = %s
    """

    params = [start, metric_name]

    if host:
        query += " AND host = %s"
        params.append(host)

    query += f" ORDER BY {time_col} ASC"

    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()
    conn.close()

    # Convert to list of tuples for LTTB
    data_tuples = [(row[time_col], row['value'] if table == 'metrics' else row['avg_value']) for row in data]

    # Downsample if needed
    if len(data_tuples) > points:
        result = lttb(data_tuples, points)
    else:
        result = [{"time": row[0].isoformat(), "value": row[1]} for row in data_tuples]

    return {
        "metric_name": metric_name,
        "start": start,
        "host": host,
        "points_requested": points,
        "points_returned": len(result),
        "data_source": table,
        "data": result
    }

@app.get("/api/metrics/{metric_name}/latest")
async def get_latest_metric(
    metric_name: str,
    host: Optional[str] = Query(None)
):
    """Get the latest value for a metric (for KPI cards)."""
    conn = get_db()
    cur = conn.cursor()

    query = """
        SELECT time, host, value
        FROM metrics
        WHERE metric_name = %s
    """
    params = [metric_name]

    if host:
        query += " AND host = %s"
        params.append(host)

    query += " ORDER BY time DESC LIMIT 1"

    cur.execute(query, params)
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return {"error": "No data found"}

    return {
        "metric_name": metric_name,
        "host": row["host"],
        "time": row["time"].isoformat(),
        "value": row["value"]
    }

@app.get("/api/hosts")
async def get_hosts():
    """Get list of all hosts."""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT host FROM metrics ORDER BY host")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {"hosts": [row["host"] for row in rows]}

@app.get("/api/metrics")
async def get_metric_names():
    """Get list of all metric names."""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT metric_name FROM metrics ORDER BY metric_name")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {"metrics": [row["metric_name"] for row in rows]}

# WebSocket endpoint for real-time streaming
@app.websocket("/ws/metrics/{metric_name}")
async def websocket_metrics(websocket: WebSocket, metric_name: str, host: Optional[str] = None):
    """
    Stream real-time metric updates via WebSocket.

    Usage:
      const ws = new WebSocket('ws://localhost:8000/ws/metrics/cpu_usage?host=server-01');
      ws.onmessage = (event) => console.log(JSON.parse(event.data));
    """
    await websocket.accept()

    try:
        while True:
            # Query latest value
            conn = get_db()
            cur = conn.cursor()

            query = """
                SELECT time, host, value
                FROM metrics
                WHERE metric_name = %s
            """
            params = [metric_name]

            if host:
                query += " AND host = %s"
                params.append(host)

            query += " ORDER BY time DESC LIMIT 1"

            cur.execute(query, params)
            row = cur.fetchone()
            cur.close()
            conn.close()

            if row:
                await websocket.send_text(json.dumps({
                    "metric_name": metric_name,
                    "host": row["host"],
                    "time": row["time"].isoformat(),
                    "value": row["value"]
                }))

            # Wait 5 seconds before next update
            await asyncio.sleep(5)

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for {metric_name}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
