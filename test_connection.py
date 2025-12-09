"""
Script kiểm tra kết nối database và blockchain
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_database():
    """Test database connection"""
    print("Testing database connection...")
    try:
        from backend.config import Config
        from backend.database import db
        from backend.app import app
        
        with app.app_context():
            # Try to query
            from backend.database import User
            count = User.query.count()
            print(f"✅ Database connection successful! (Found {count} users)")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_blockchain():
    """Test blockchain connection"""
    print("\nTesting blockchain connection...")
    try:
        from backend.blockchain import blockchain_service
        
        if blockchain_service.is_connected():
            latest_block = blockchain_service.get_latest_block()
            print(f"✅ Blockchain connection successful! (Latest block: {latest_block})")
            
            if blockchain_service.contract:
                print(f"✅ Contract loaded at: {blockchain_service.contract_address}")
            else:
                print("⚠️  Contract not loaded. Check CONTRACT_ADDRESS in .env")
            return True
        else:
            print("❌ Cannot connect to blockchain node")
            print("   Make sure Ganache/Anvil is running on http://127.0.0.1:8545")
            return False
    except Exception as e:
        print(f"❌ Blockchain connection failed: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("Banking Blockchain System - Connection Test")
    print("=" * 50)
    
    db_ok = test_database()
    blockchain_ok = test_blockchain()
    
    print("\n" + "=" * 50)
    if db_ok and blockchain_ok:
        print("✅ All systems ready!")
    else:
        print("⚠️  Some systems need attention")
    print("=" * 50)

