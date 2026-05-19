import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "runs.db")

def init_db():
    """Crée la table si elle n'existe pas encore."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            api TEXT,
            passed INTEGER,
            failed INTEGER,
            total INTEGER,
            error_rate REAL,
            latency_avg INTEGER,
            latency_p95 INTEGER,
            disponibilite TEXT,
            tests_json TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_run(run):
    """Sauvegarde un run dans la base."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    summary = run["summary"]
    cursor.execute("""
        INSERT INTO runs 
        (timestamp, api, passed, failed, total, error_rate, latency_avg, latency_p95, disponibilite, tests_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        run["timestamp"],
        run["api"],
        summary["passed"],
        summary["failed"],
        summary["total"],
        summary["error_rate"],
        summary["latency_ms_avg"],
        summary["latency_ms_p95"],
        summary["disponibilite"],
        json.dumps(run["tests"])
    ))
    conn.commit()
    conn.close()

def list_runs(limit=20):
    """Retourne les derniers runs."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, api, passed, failed, total, error_rate, 
               latency_avg, latency_p95, disponibilite, tests_json
        FROM runs 
        ORDER BY id DESC 
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    runs = []
    for row in rows:
        runs.append({
            "id": row[0],
            "timestamp": row[1],
            "api": row[2],
            "summary": {
                "passed": row[3],
                "failed": row[4],
                "total": row[5],
                "error_rate": row[6],
                "latency_ms_avg": row[7],
                "latency_ms_p95": row[8],
                "disponibilite": row[9]
            },
            "tests": json.loads(row[10])
        })
    return runs
