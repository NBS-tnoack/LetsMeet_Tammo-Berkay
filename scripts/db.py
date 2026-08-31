"""Gemeinsame PostgreSQL-Verbindung fuer alle Importskripte."""

from __future__ import annotations

import os

import psycopg2


def connect():
    # Die Standardwerte passen zu compose.yml, damit das Skript ohne .env laeuft.
    return psycopg2.connect(
        host=os.getenv("PGHOST", "127.0.0.1"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "lf8_lets_meet_db"),
        user=os.getenv("PGUSER", "user"),
        password=os.getenv("PGPASSWORD", "secret"),
    )
