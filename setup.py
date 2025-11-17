"""
Setup script to help configure the application
"""
import os

def create_env_file():
    """Create .env file with database credentials"""
    env_content = """# Database Configuration
DB_HOST=212.2.245.85
DB_PORT=6432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=Tea_IWMZ5wuUta97gupb

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
"""
    
    if os.path.exists('.env'):
        print("WARNING: .env file already exists. Skipping...")
        return
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("SUCCESS: Created .env file with database credentials")

def main():
    print("Setting up OneTrueAddress Application\n")
    
    # Create .env file
    create_env_file()
    
    print("\nNext steps:")
    print("1. Activate your virtual environment:")
    print("   Windows: venv\\Scripts\\activate")
    print("   Mac/Linux: source venv/bin/activate")
    print("\n2. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n3. Run the application:")
    print("   python app.py")
    print("\n4. Open your browser:")
    print("   http://localhost:5000")
    print("\nHappy searching!")

if __name__ == '__main__':
    main()

