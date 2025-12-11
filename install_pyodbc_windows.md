# Hướng Dẫn Cài Đặt pyodbc trên Windows

## Lỗi: Failed building wheel for pyodbc

Lỗi này xảy ra khi pip không thể build pyodbc từ source code.

## Giải Pháp

### Cách 1: Cài đặt Pre-built Wheel (KHUYẾN NGHỊ)

1. **Cài đặt ODBC Driver 17 for SQL Server** (nếu chưa có):
   - Tải từ: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
   - Hoặc tìm "ODBC Driver 17 for SQL Server" trên Microsoft Store

2. **Cài đặt pyodbc bằng pre-built wheel**:
   ```powershell
   pip install --only-binary :all: pyodbc
   ```

   Hoặc cài đặt từ wheel file:
   ```powershell
   pip install pyodbc --prefer-binary
   ```

### Cách 2: Cài đặt Visual C++ Build Tools

Nếu muốn build từ source:

1. **Tải Visual C++ Build Tools**:
   - Truy cập: https://visualstudio.microsoft.com/downloads/
   - Tải "Build Tools for Visual Studio"
   - Chọn "C++ build tools" workload

2. **Cài đặt lại pyodbc**:
   ```powershell
   pip install pyodbc
   ```

### Cách 3: Sử dụng Conda (Nếu có)

```powershell
conda install -c conda-forge pyodbc
```

### Cách 4: Cài đặt từ Wheel File Trực Tiếp

1. Tải wheel file phù hợp với Python version của bạn:
   - Python 3.11: https://github.com/mkleehammer/pyodbc/releases
   - Hoặc tìm trên: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyodbc

2. Cài đặt:
   ```powershell
   pip install pyodbc-4.0.39-cp311-cp311-win_amd64.whl
   ```
   (Thay tên file phù hợp với version của bạn)

## Kiểm Tra Sau Khi Cài Đặt

```powershell
python -c "import pyodbc; print('pyodbc version:', pyodbc.version)"
```

## Lưu Ý

- Đảm bảo đã cài **ODBC Driver 17 for SQL Server** trước
- Nếu vẫn lỗi, thử upgrade pip: `python -m pip install --upgrade pip`
- Kiểm tra Python version: `python --version`

