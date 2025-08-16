"""
Import script for TRIZ parameters (1..39), principles (1..40), and the 39x39 matrix mapping
into Postgres using psycopg. This script expects CSV/JSON inputs and will upsert records.

Environment:
  POSTGRES_URL=postgresql://user:pass@host:5432/db
Usage:
  python import_triz_matrix.py --principles principles.json --parameters parameters.json --matrix matrix.csv
"""
from __future__ import annotations
import argparse
import csv
import json
import os
from typing import List, Dict, Any

import psycopg

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def ensure_schema(conn: psycopg.Connection) -> None:
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        ddl = f.read()
    with conn.cursor() as cur:
        cur.execute(ddl)
    conn.commit()


def upsert_principles(conn: psycopg.Connection, items: List[Dict[str, Any]]):
    with conn.cursor() as cur:
        for it in items:
            cur.execute(
                """
                INSERT INTO triz_principle (id, name, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name, description=EXCLUDED.description
                """,
                (it["id"], it.get("name"), it.get("description")),
            )
    conn.commit()


def upsert_parameters(conn: psycopg.Connection, items: List[Dict[str, Any]]):
    with conn.cursor() as cur:
        for it in items:
            cur.execute(
                """
                INSERT INTO triz_parameter (id, name, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name, description=EXCLUDED.description
                """,
                (it["id"], it.get("name"), it.get("description")),
            )
    conn.commit()


def import_matrix(conn: psycopg.Connection, matrix_csv: str):
    """
    CSV format: improving_param,worsening_param,principles
      principles as a semicolon-separated list of integers, e.g., "1;10;35"
    """
    with open(matrix_csv, newline="", encoding="utf-8") as f, conn.cursor() as cur:
        reader = csv.DictReader(f)
        for row in reader:
            improving = int(row["improving_param"])
            worsening = int(row["worsening_param"])
            principles = [int(x) for x in row["principles"].split(";") if x.strip()]
            for pid in principles:
                cur.execute(
                    """
                    INSERT INTO triz_matrix_link (improving_param, worsening_param, principle_id)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (improving_param, worsening_param, principle_id) DO NOTHING
                    """,
                    (improving, worsening, pid),
                )
    conn.commit()


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--principles", required=True, help="Path to principles.json")
    ap.add_argument("--parameters", required=True, help="Path to parameters.json")
    ap.add_argument("--matrix", required=True, help="Path to matrix.csv")
    ap.add_argument("--postgres", default=os.getenv("POSTGRES_URL"), help="Postgres URL")
    return ap.parse_args()


def load_json(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    args = parse_args()
    if not args.postgres:
        raise SystemExit("POSTGRES_URL not provided (env or --postgres)")

    # Connect
    with psycopg.connect(args.postgres) as conn:
        ensure_schema(conn)
        upsert_principles(conn, load_json(args.principles))
        upsert_parameters(conn, load_json(args.parameters))
        import_matrix(conn, args.matrix)
    print("TRIZ data import completed.")


if __name__ == "__main__":
    main()

