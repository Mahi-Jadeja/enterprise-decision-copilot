# helpers/db.py
# Database connection manager for Supabase PostgreSQL

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', 'config', '.env'))


def get_connection():
    """Create and return a new database connection."""
    conn = psycopg2.connect(
        host=os.getenv("SUPABASE_DB_HOST"),
        port=os.getenv("SUPABASE_DB_PORT", "5432"),
        dbname=os.getenv("SUPABASE_DB_NAME", "postgres"),
        user=os.getenv("SUPABASE_DB_USER", "postgres"),
        password=os.getenv("SUPABASE_DB_PASSWORD"),
        sslmode="require"
    )
    return conn


def insert_batch(conn, table_name, columns, rows, batch_size=500):
    """
    Insert rows into a table in batches.
    
    Args:
        conn: psycopg2 connection
        table_name: target table
        columns: list of column names
        rows: list of tuples (each tuple = one row)
        batch_size: how many rows per commit
    """
    if not rows:
        print(f"  ⚠ No data to insert into {table_name}")
        return

    cols_str = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    query = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})"

    cursor = conn.cursor()
    total = len(rows)
    inserted = 0

    for i in range(0, total, batch_size):
        batch = rows[i:i + batch_size]
        try:
            cursor.executemany(query, batch)
            conn.commit()
            inserted += len(batch)
            print(f"  ✓ {table_name}: {inserted}/{total} rows inserted")
        except Exception as e:
            conn.rollback()
            print(f"  ✗ Error inserting into {table_name} at batch {i}: {e}")
            # Print the first failing row for debugging
            if batch:
                print(f"    Sample row: {batch[0]}")
            raise

    cursor.close()
    print(f"  ✅ {table_name}: {total} rows total\n")


def test_connection():
    """Quick connection test."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT current_database(), current_user;")
        db, user = cur.fetchone()
        print(f"✅ Connected to database '{db}' as user '{user}'")
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False