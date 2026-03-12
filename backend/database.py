"""
Database layer for storing network scan history and switch events.
Uses SQLite for zero-configuration persistence.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Optional

DB_PATH = "network_history.db"


def init_db():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            profile_used TEXT NOT NULL,
            total_networks INTEGER,
            best_network_name TEXT,
            best_network_score REAL,
            weights_json TEXT,
            all_scores_json TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS switch_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            from_network TEXT,
            to_network TEXT NOT NULL,
            to_network_score REAL,
            reason TEXT,
            profile_used TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS network_metrics_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            network_name TEXT NOT NULL,
            network_type TEXT,
            signal_strength REAL,
            bandwidth REAL,
            latency REAL,
            reliability REAL,
            composite_score REAL
        )
    """)
    
    conn.commit()
    conn.close()


def save_scan(profile: str, total: int, best_name: str, best_score: float,
              weights: dict, all_scores: list):
    """Save a scan result to history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO scan_history 
           (timestamp, profile_used, total_networks, best_network_name, 
            best_network_score, weights_json, all_scores_json)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            datetime.now().isoformat(),
            profile,
            total,
            best_name,
            best_score,
            json.dumps(weights),
            json.dumps(all_scores),
        )
    )
    
    conn.commit()
    conn.close()


def save_switch_event(from_net: Optional[str], to_net: str, score: float,
                      reason: str, profile: str):
    """Log a network switch event."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO switch_events 
           (timestamp, from_network, to_network, to_network_score, reason, profile_used)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (datetime.now().isoformat(), from_net, to_net, score, reason, profile)
    )
    
    conn.commit()
    conn.close()


def save_metrics_log(scores_data: list):
    """Save individual network metrics for time-series tracking."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    
    for entry in scores_data:
        cursor.execute(
            """INSERT INTO network_metrics_log 
               (timestamp, network_name, network_type, signal_strength, 
                bandwidth, latency, reliability, composite_score)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                timestamp,
                entry.get("name", ""),
                entry.get("type", ""),
                entry.get("signal", 0),
                entry.get("bandwidth", 0),
                entry.get("latency", 0),
                entry.get("reliability", 0),
                entry.get("score", 0),
            )
        )
    
    conn.commit()
    conn.close()


def get_scan_history(limit: int = 50) -> List[dict]:
    """Retrieve recent scan history."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM scan_history ORDER BY id DESC LIMIT ?", (limit,)
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_switch_events(limit: int = 50) -> List[dict]:
    """Retrieve recent switch events."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM switch_events ORDER BY id DESC LIMIT ?", (limit,)
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_metrics_timeseries(network_name: str = None, limit: int = 100) -> List[dict]:
    """Retrieve metrics time-series data for charting."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if network_name:
        cursor.execute(
            "SELECT * FROM network_metrics_log WHERE network_name = ? ORDER BY id DESC LIMIT ?",
            (network_name, limit)
        )
    else:
        cursor.execute(
            "SELECT * FROM network_metrics_log ORDER BY id DESC LIMIT ?", (limit,)
        )
    
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


# Initialize on import
init_db()
