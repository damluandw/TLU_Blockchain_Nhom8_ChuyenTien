"""
Script kiểm tra file .env
"""
import os
import sys
from pathlib import Path

# Đường dẫn đến file .env
env_path = Path('backend/.env')

print("=" * 60)
print("KIỂM TRA FILE .env")
print("=" * 60)

# Kiểm tra file tồn tại
if not env_path.exists():
    print("❌ File backend/.env không tồn tại!")
    print("\nTạo file backend/.env với nội dung:")
    print("-" * 60)
    print("SQL_SERVER=localhost")
    print("SQL_DATABASE=BankingBlockchain")
    print("SQL_USERNAME=sa")
    print("SQL_PASSWORD=your_password")
    print("BLOCKCHAIN_NETWORK=http://127.0.0.1:8545")
    print("CONTRACT_ADDRESS=")
    print("PRIVATE_KEY=")
    print("SECRET_KEY=your-secret-key")
    print("DEBUG=True")
    print("-" * 60)
    sys.exit(1)

print(f"✓ File tồn tại: {env_path}")
print()

# Đọc file .env
env_vars = {}
required_vars = [
    'SQL_SERVER',
    'SQL_DATABASE', 
    'SQL_USERNAME',
    'SQL_PASSWORD',
    'BLOCKCHAIN_NETWORK',
    'CONTRACT_ADDRESS',
    'PRIVATE_KEY',
    'SECRET_KEY',
    'DEBUG'
]

try:
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    print("Nội dung file .env (dòng 1-13):")
    print("-" * 60)
    for i, line in enumerate(lines[:13], 1):
        # Ẩn giá trị nhạy cảm
        display_line = line.rstrip()
        if 'PASSWORD' in line or 'PRIVATE_KEY' in line or 'SECRET_KEY' in line:
            if '=' in line:
                key, value = line.split('=', 1)
                if value.strip():
                    display_line = f"{key}=***HIDDEN***"
                else:
                    display_line = f"{key}="
        print(f"{i:2d}: {display_line}")
    print("-" * 60)
    print()
    
    # Parse các biến môi trường
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            env_vars[key] = value
    
    print("Kiểm tra các biến môi trường:")
    print("-" * 60)
    
    errors = []
    warnings = []
    
    # Kiểm tra từng biến
    for var in required_vars:
        if var not in env_vars:
            errors.append(f"❌ {var}: Thiếu")
        else:
            value = env_vars[var]
            if not value:
                if var in ['CONTRACT_ADDRESS', 'PRIVATE_KEY']:
                    warnings.append(f"⚠️  {var}: Chưa điền (có thể điền sau khi deploy contract)")
                elif var == 'SQL_PASSWORD':
                    errors.append(f"❌ {var}: Chưa điền (bắt buộc)")
                else:
                    warnings.append(f"⚠️  {var}: Chưa điền")
            else:
                # Validate format
                if var == 'BLOCKCHAIN_NETWORK':
                    if not value.startswith('http'):
                        errors.append(f"❌ {var}: Format sai (phải bắt đầu với http://)")
                    else:
                        print(f"✓ {var}: {value}")
                elif var == 'CONTRACT_ADDRESS':
                    if value and not value.startswith('0x'):
                        errors.append(f"❌ {var}: Format sai (phải bắt đầu với 0x)")
                    elif value:
                        print(f"✓ {var}: {value[:10]}...{value[-8:]}")
                    else:
                        warnings.append(f"⚠️  {var}: Chưa điền")
                elif var == 'PRIVATE_KEY':
                    if value and not value.startswith('0x'):
                        errors.append(f"❌ {var}: Format sai (phải bắt đầu với 0x)")
                    elif value:
                        print(f"✓ {var}: ***HIDDEN***")
                    else:
                        warnings.append(f"⚠️  {var}: Chưa điền")
                elif var == 'SQL_PASSWORD':
                    print(f"✓ {var}: ***HIDDEN***")
                elif var == 'SECRET_KEY':
                    if len(value) < 32:
                        warnings.append(f"⚠️  {var}: Quá ngắn (nên >= 32 ký tự)")
                    print(f"✓ {var}: ***HIDDEN***")
                elif var == 'DEBUG':
                    if value.upper() not in ['TRUE', 'FALSE', 'True', 'False']:
                        errors.append(f"❌ {var}: Giá trị sai (phải là True hoặc False)")
                    else:
                        print(f"✓ {var}: {value}")
                else:
                    print(f"✓ {var}: {value}")
    
    print("-" * 60)
    print()
    
    # Hiển thị warnings
    if warnings:
        print("⚠️  CẢNH BÁO:")
        for warning in warnings:
            print(f"  {warning}")
        print()
    
    # Hiển thị errors
    if errors:
        print("❌ LỖI:")
        for error in errors:
            print(f"  {error}")
        print()
        print("Vui lòng sửa các lỗi trên trước khi chạy backend!")
        sys.exit(1)
    
    # Kiểm tra format tổng thể
    print("=" * 60)
    print("✅ KIỂM TRA HOÀN TẤT")
    print("=" * 60)
    print("✓ Tất cả các biến môi trường đã được khai báo")
    if warnings:
        print(f"⚠️  Có {len(warnings)} cảnh báo (không ảnh hưởng đến việc chạy)")
    print()
    print("Lưu ý:")
    print("- CONTRACT_ADDRESS và PRIVATE_KEY có thể điền sau khi deploy contract")
    print("- Đảm bảo SQL Server đang chạy và database đã được tạo")
    print("- Kiểm tra kết nối: python backend/app.py")
    
except Exception as e:
    print(f"❌ Lỗi khi đọc file .env: {e}")
    sys.exit(1)

