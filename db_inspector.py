import sqlite3
import os
import sys
from pprint import pprint
from typing import List, Dict, Any, Tuple


def get_database_path() -> str:
    """
    Get the database path from environment or use default
    """
    # You can modify this to match your actual database path
    return os.environ.get('NUTRITION_DB_PATH', 'instance/nutrition_tracker.db')


def connect_to_database(db_path: str) -> sqlite3.Connection:
    """
    Connect to the SQLite database
    """
    try:
        conn = sqlite3.connect(db_path)
        # Enable foreign keys for better constraint checking
        conn.execute("PRAGMA foreign_keys = ON")
        # Set row_factory to get dictionary-like results
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)


def get_all_tables(conn: sqlite3.Connection) -> List[str]:
    """
    Get a list of all tables in the database
    """
    cursor = conn.cursor()
    # Query to get all tables excluding SQLite internal tables
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
    """)
    tables = [row['name'] for row in cursor.fetchall()]
    return tables


def get_table_schema(conn: sqlite3.Connection, table_name: str) -> List[Dict[str, Any]]:
    """
    Get detailed schema information for a specific table
    """
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = []
    for row in cursor.fetchall():
        columns.append({
            'cid': row['cid'],
            'name': row['name'],
            'type': row['type'],
            'notnull': bool(row['notnull']),
            'default_value': row['dflt_value'],
            'primary_key': bool(row['pk']),
        })
    return columns


def get_foreign_keys(conn: sqlite3.Connection, table_name: str) -> List[Dict[str, Any]]:
    """
    Get foreign key information for a specific table
    """
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    foreign_keys = []
    for row in cursor.fetchall():
        foreign_keys.append({
            'id': row['id'],
            'seq': row['seq'],
            'table': row['table'],
            'from': row['from'],
            'to': row['to'],
            'on_update': row['on_update'],
            'on_delete': row['on_delete'],
            'match': row['match'],
        })
    return foreign_keys


def get_sample_data(conn: sqlite3.Connection, table_name: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get sample data from a specific table
    """
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        rows = []
        for row in cursor.fetchall():
            rows.append(dict(row))
        return rows
    except sqlite3.Error as e:
        print(f"Error getting data from {table_name}: {e}")
        return []


def get_row_count(conn: sqlite3.Connection, table_name: str) -> int:
    """
    Get the total number of rows in a table
    """
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
        result = cursor.fetchone()
        return result['count']
    except sqlite3.Error as e:
        print(f"Error counting rows in {table_name}: {e}")
        return 0


def main():
    """
    Main function to inspect database structure
    """
    db_path = get_database_path()
    print(f"\n--- Database Inspection for NutritionTracker ---")
    print(f"Database: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"ERROR: Database file not found at {db_path}")
        print("Please check the path or run database migrations first.")
        sys.exit(1)
    
    conn = connect_to_database(db_path)
    tables = get_all_tables(conn)
    
    print(f"\nFound {len(tables)} tables:")
    for table in tables:
        print(f"  - {table}")
    
    print("\n--- Detailed Table Information ---")
    
    for table in tables:
        row_count = get_row_count(conn, table)
        print(f"\n=== Table: {table} ({row_count} rows) ===")
        
        # Get and print schema information
        schema = get_table_schema(conn, table)
        print("\nColumns:")
        for column in schema:
            pk_indicator = "PK" if column['primary_key'] else ""
            null_indicator = "NOT NULL" if column['notnull'] else "NULL"
            default = f"DEFAULT {column['default_value']}" if column['default_value'] else ""
            print(f"  - {column['name']} ({column['type']}) {pk_indicator} {null_indicator} {default}")
        
        # Get and print foreign key information
        foreign_keys = get_foreign_keys(conn, table)
        if foreign_keys:
            print("\nForeign Keys:")
            for fk in foreign_keys:
                print(f"  - {fk['from']} → {fk['table']}.{fk['to']} (on_delete: {fk['on_delete']})")
        
        # Get and print sample data
        if row_count > 0:
            print("\nSample Data (up to 5 rows):")
            sample_data = get_sample_data(conn, table)
            for i, row in enumerate(sample_data, 1):
                print(f"\n  Row {i}:")
                for key, value in row.items():
                    # Truncate long values for display
                    str_value = str(value)
                    if len(str_value) > 50:
                        str_value = str_value[:47] + "..."
                    print(f"    {key}: {str_value}")
    
    # Provide summary information
    print("\n--- Database Summary ---")
    print(f"Total Tables: {len(tables)}")
    
    # Find tables with most rows
    tables_with_counts = [(table, get_row_count(conn, table)) for table in tables]
    tables_with_counts.sort(key=lambda x: x[1], reverse=True)
    
    print("\nTables by Row Count:")
    for table, count in tables_with_counts:
        print(f"  - {table}: {count} rows")
    
    print("\nDatabase inspection complete!")
    conn.close()


if __name__ == "__main__":
    main()