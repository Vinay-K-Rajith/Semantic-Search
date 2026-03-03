
import pyodbc
import pymssql
import os

SERVER = '13.201.233.99'
DATABASE = 'ENTABI'
USERNAME = 'entab'
PASSWORD = 'Office@786'

def test_pyodbc():
    print("\n--- Testing pyodbc ---")
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )
    print(f"Connection string: {conn_str}")
    try:
        conn = pyodbc.connect(conn_str, timeout=10)
        print("SUCCESS: Connected with pyodbc (Encrypt=yes, Trust=no)!")
        conn.close()
    except Exception as e:
        print(f"FAILED: {e}")

    print("\n--- Testing pyodbc (Trust=yes) ---")
    conn_str_trust = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    try:
        conn = pyodbc.connect(conn_str_trust, timeout=10)
        print("SUCCESS: Connected with pyodbc (Encrypt=yes, Trust=yes)!")
        conn.close()
    except Exception as e:
        print(f"FAILED: {e}")

def test_pymssql():
    print("\n--- Testing pymssql ---")
    try:
        # Default
        conn = pymssql.connect(server=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE)
        print("SUCCESS: Connected with pymssql (default)!")
        conn.close()
    except Exception as e:
        print(f"FAILED (default): {e}")

    try:
        # Encryption workaround? 
        # pymssql doesn't expose TrustServerCertificate easily.
        # But we can try passing tds_version
        conn = pymssql.connect(server=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE, tds_version='7.4')
        print("SUCCESS: Connected with pymssql (tds 7.4)!")
        conn.close()
    except Exception as e:
        print(f"FAILED (tds 7.4): {e}")

if __name__ == "__main__":
    test_pyodbc()
    test_pymssql()
