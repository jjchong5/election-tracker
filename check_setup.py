"""
Setup verification script for Election Tracker.
Run this after installing dependencies to verify everything works.
"""
import sys


def check_dependencies():
    """Check if all required packages are installed."""
    print("Checking dependencies...")
    required_packages = {
        'requests': 'requests',
        'bs4': 'beautifulsoup4',
        'lxml': 'lxml',
        'pandas': 'pandas',
        'selenium': 'selenium',
        'dotenv': 'python-dotenv',
        'tqdm': 'tqdm'
    }

    missing = []
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"  [OK] {package}")
        except ImportError:
            print(f"  [MISSING] {package} (missing)")
            missing.append(package)

    if missing:
        print("\nMissing packages. Install with:")
        print(f"  pip install {' '.join(missing)}")
        return False

    print("\n[OK] All dependencies installed!")
    return True


def check_modules():
    """Check if project modules can be imported."""
    print("\nChecking project modules...")
    modules = ['database', 'scraper', 'config']

    for module in modules:
        try:
            __import__(module)
            print(f"  [OK] {module}.py")
        except Exception as e:
            print(f"  [ERROR] {module}.py - Error: {e}")
            return False

    print("\n[OK] All project modules OK!")
    return True


def test_database():
    """Test database functionality."""
    print("\nTesting database...")
    try:
        from database import ElectionDatabase

        db = ElectionDatabase("test_data")

        # Test adding data
        test_election = {
            'location': 'Test State - Test Office District 1',
            'state': 'TS',
            'office': 'Test Office',
            'district': 'District 1',
            'election_date': '2025-11-05',
            'r_plus': None,
            'is_uncontested': False,
            'incumbent': None,
            'source_url': 'https://test.com',
        }

        db.add_election(test_election)
        elections = db.load_elections()

        if len(elections) > 0:
            print("  [OK] Database write/read works")
            print(f"  [OK] Created test_data/elections.csv and elections.json")

            # Clean up
            import shutil
            shutil.rmtree("test_data", ignore_errors=True)
            print("  [OK] Cleaned up test files")

            return True
        else:
            print("  [ERROR] Database test failed")
            return False

    except Exception as e:
        print(f"  [ERROR] Database test failed: {e}")
        return False


def main():
    """Run all checks."""
    print("=" * 60)
    print("Election Tracker - Setup Verification")
    print("=" * 60)
    print()

    checks = [
        check_dependencies(),
        check_modules(),
        test_database()
    ]

    print("\n" + "=" * 60)
    if all(checks):
        print("[SUCCESS] ALL CHECKS PASSED!")
        print("\nYou're ready to use Election Tracker!")
        print("\nNext steps:")
        print("  1. Read QUICKSTART.md for usage instructions")
        print("  2. Run: python main.py scrape --states Virginia --years 2025")
        print("  3. Run: python main.py stats")
    else:
        print("[ERROR] SOME CHECKS FAILED")
        print("\nPlease fix the issues above before continuing.")
        print("If you need to install dependencies:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

    print("=" * 60)


if __name__ == "__main__":
    main()
