"""
Script để tạo SECRET_KEY ngẫu nhiên cho Flask
"""
import secrets

# Tạo SECRET_KEY ngẫu nhiên mạnh (32 bytes = 64 ký tự hex)
secret_key = secrets.token_hex(32)

print("=" * 60)
print("SECRET_KEY mới đã được tạo:")
print("=" * 60)
print(secret_key)
print("=" * 60)
print("\nCopy dòng trên và dán vào file backend/.env:")
print(f"SECRET_KEY={secret_key}")
print("=" * 60)

