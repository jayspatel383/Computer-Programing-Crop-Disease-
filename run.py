"""
Crop Disease Early Warning System - Launcher
"""

import os
import sys
from datetime import datetime

def check_files():
    required = ['config.py', 'crop_database.py', 'data_fetcher.py', 
                'disease_engine.py', 'main_dashboard.py']
    for f in required:
        if not os.path.exists(f):
            print(f"❌ Missing: {f}")
            return False
    return True

def main():
    print("\n" + "="*60)
    print("🌾 CROP DISEASE EARLY WARNING SYSTEM")
    print("="*60)
    print(f"Date: {datetime.now().strftime('%d %B %Y')}")
    print(f"Python: {sys.version.split()[0]}")
    print("="*60)
    
    if not check_files():
        print("\n❌ Missing files! Make sure all files are in the same directory.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("\n✅ All files found!")
    print("🎯 Starting application...")
    print("📊 Dashboard will open in a new window.\n")
    
    try:
        from main_dashboard import main as dashboard_main
        dashboard_main()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()