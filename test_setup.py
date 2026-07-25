"""
Test Setup Script
=================
Tests if all required packages are installed and working.
"""

print("=" * 60)
print("TESTING PROJECT SETUP")
print("=" * 60)

# Test core packages
packages = {
    'Flask': 'flask',
    'scikit-learn': 'sklearn',
    'pandas': 'pandas',
    'NumPy': 'numpy',
    'joblib': 'joblib'
}

all_ok = True

for name, module in packages.items():
    try:
        __import__(module)
        print(f"✓ {name:15} - Installed")
    except ImportError:
        print(f"✗ {name:15} - NOT FOUND")
        all_ok = False

print("=" * 60)

if all_ok:
    print("✓ All core packages are installed!")
    print("\nTesting configuration import...")
    
    try:
        from config import Config
        print("✓ Configuration loaded successfully")
        print(f"  - Features defined: {len(Config.FEATURE_COLUMNS)}")
        print(f"  - Model path: {Config.MODEL_PATH}")
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        all_ok = False
    
    print("\nTesting utility modules...")
    
    try:
        from utils import (
            GradingSystem,
            StudyPlanner,
            PredictionEngine,
            InputValidator,
            SuggestionsGenerator
        )
        print("✓ All utility modules imported successfully")
    except Exception as e:
        print(f"✗ Utility import error: {e}")
        all_ok = False

print("=" * 60)

if all_ok:
    print("\n🎉 PROJECT SETUP COMPLETE!")
    print("\nYou can now run:")
    print("  python app_new.py")
else:
    print("\n⚠️  SETUP INCOMPLETE")
    print("\nInstall missing packages:")
    print("  pip install -r requirements.txt")

print("=" * 60)
