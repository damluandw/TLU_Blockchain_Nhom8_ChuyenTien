import pyodbc

try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-CRFJV4A\\SQL2022;'
        'DATABASE=DB_BLOCKCHAIN;'
        'UID=sa;'
        'PWD=12345;'
        'TrustServerCertificate=yes'
    )
    print("✓ Kết nối thành công!")
    conn.close()
except Exception as e:
    print(f"✗ Lỗi kết nối: {e}")