"""SQLite persistence layer for MediGuard AI."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).resolve().parents[1] / "database" / "database.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS health_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                recorded_at TEXT NOT NULL,
                height REAL,
                weight REAL,
                bmi REAL,
                systolic_bp REAL,
                diastolic_bp REAL,
                blood_sugar REAL,
                heart_rate REAL,
                sleep_hours REAL,
                exercise_frequency INTEGER,
                smoking TEXT,
                alcohol TEXT,
                stress_level INTEGER,
                water_intake REAL,
                health_score INTEGER,
                risk_category TEXT,
                health_age INTEGER,
                triage_color TEXT,
                triage_level TEXT,
                triage_action TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(id)
            );

            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER NOT NULL,
                disease TEXT NOT NULL,
                risk_probability REAL NOT NULL,
                confidence REAL NOT NULL,
                label TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(record_id) REFERENCES health_records(id)
            );
            """
        )


def save_assessment(profile, health_score: int, category: str, health_age: int, triage: dict, risks: dict) -> int:
    init_db()
    now = datetime.now().isoformat(timespec="seconds")
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO patients (name, age, gender, created_at) VALUES (?, ?, ?, ?)",
            (profile.name, profile.age, profile.gender, now),
        )
        patient_id = cursor.lastrowid
        cursor = conn.execute(
            """
            INSERT INTO health_records (
                patient_id, recorded_at, height, weight, bmi, systolic_bp, diastolic_bp,
                blood_sugar, heart_rate, sleep_hours, exercise_frequency, smoking,
                alcohol, stress_level, water_intake, health_score, risk_category,
                health_age, triage_color, triage_level, triage_action
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                patient_id,
                now,
                profile.height,
                profile.weight,
                profile.bmi,
                profile.systolic_bp,
                profile.diastolic_bp,
                profile.blood_sugar,
                profile.heart_rate,
                profile.sleep_hours,
                profile.exercise_frequency,
                profile.smoking,
                profile.alcohol,
                profile.stress_level,
                profile.water_intake,
                health_score,
                category,
                health_age,
                triage["color"],
                triage["level"],
                triage["action"],
            ),
        )
        record_id = cursor.lastrowid
        for disease, result in risks.items():
            conn.execute(
                """
                INSERT INTO predictions (record_id, disease, risk_probability, confidence, label, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    record_id,
                    disease,
                    float(result["probability"]),
                    float(result.get("confidence", result.get("auc_roc", 0.0))),
                    result["label"],
                    now,
                ),
            )
    return int(record_id)


def load_history(search: str = "") -> pd.DataFrame:
    init_db()
    query = """
        SELECT
            hr.id AS record_id,
            p.name,
            p.age,
            p.gender,
            hr.recorded_at,
            hr.bmi,
            hr.systolic_bp,
            hr.diastolic_bp,
            hr.blood_sugar,
            hr.health_score,
            hr.risk_category,
            hr.health_age,
            hr.triage_color,
            hr.triage_level
        FROM health_records hr
        JOIN patients p ON p.id = hr.patient_id
    """
    params: tuple = ()
    if search:
        query += " WHERE LOWER(p.name) LIKE ?"
        params = (f"%{search.lower()}%",)
    query += " ORDER BY hr.recorded_at DESC"
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)


def load_prediction_history() -> pd.DataFrame:
    init_db()
    query = """
        SELECT
            hr.recorded_at,
            p.name,
            pred.disease,
            pred.risk_probability,
            pred.label
        FROM predictions pred
        JOIN health_records hr ON hr.id = pred.record_id
        JOIN patients p ON p.id = hr.patient_id
        ORDER BY hr.recorded_at ASC
    """
    with get_connection() as conn:
        return pd.read_sql_query(query, conn)


def delete_record(record_id: int) -> bool:
    """Deletes a health record and its associated predictions and patient data."""
    init_db()
    with get_connection() as conn:
        cursor = conn.execute("SELECT patient_id FROM health_records WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        if not row:
            return False
        patient_id = row["patient_id"]
        conn.execute("DELETE FROM predictions WHERE record_id = ?", (record_id,))
        conn.execute("DELETE FROM health_records WHERE id = ?", (record_id,))
        # Check if patient has any remaining records; if not, delete patient entry
        remaining = conn.execute("SELECT COUNT(*) as count FROM health_records WHERE patient_id = ?", (patient_id,)).fetchone()
        if remaining["count"] == 0:
            conn.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
        conn.commit()
    return True


def delete_all_records() -> bool:
    """Deletes all patient, health record, and prediction entries from the database."""
    init_db()
    with get_connection() as conn:
        conn.execute("DELETE FROM predictions")
        conn.execute("DELETE FROM health_records")
        conn.execute("DELETE FROM patients")
        conn.commit()
    return True


def export_record_json(record_id: int) -> str:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM predictions WHERE record_id = ?", (record_id,)).fetchall()
    return json.dumps([dict(row) for row in rows], indent=2)

