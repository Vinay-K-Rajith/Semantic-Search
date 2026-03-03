import pyodbc
try:
    available_drivers = [d for d in pyodbc.drivers() if 'SQL Server' in d]
    print(f'Found drivers: {available_drivers}\n')
except Exception as e:
    print(f'Error listing drivers: {e}')
    available_drivers = []

print('Starting connection tests...\n')

for driver in available_drivers:
    for encrypt in ['yes', 'no']:
        print(f'Testing Driver: {{{driver}}} with Encrypt={encrypt}...')
        
        conn_str = (
            f'DRIVER={{{driver}}};'
            f'SERVER=13.201.233.99;'
            f'DATABASE=ENTABI;'
            f'UID=entab;'
            f'PWD=Office@786;'
            f'Encrypt={encrypt};'
            'TrustServerCertificate=yes;'
            'Connection Timeout=5;'
        )
        
        try:
            conn = pyodbc.connect(conn_str)
            print('✅ SUCCESS! Use this combination.\n')
            conn.close()
        except Exception as e:
            error_msg = str(e)
            if ']' in error_msg:
                parts = error_msg.split(']')
                if len(parts) > 2:
                    error_msg = parts[2].strip()
            print(f'❌ Failed: {error_msg[:80]}...\n')

print('Finished testing all combinations.')