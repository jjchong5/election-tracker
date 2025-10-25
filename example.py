"""
Example usage of the Election Tracker library.
"""
from database import ElectionDatabase
from scraper import BallotpediaScraper
import config


def example_basic_scraping():
    """Example: Basic scraping for one state and year."""
    print("Example 1: Basic Scraping")
    print("-" * 60)

    scraper = BallotpediaScraper(delay=1.0)
    elections = scraper.get_state_elections("Virginia", 2025)

    print(f"Found {len(elections)} elections in Virginia 2025")
    for election in elections[:5]:  # Show first 5
        print(f"  - {election['location']}")
        print(f"    Uncontested: {election['is_uncontested']}")
        print()


def example_database_operations():
    """Example: Working with the database."""
    print("\nExample 2: Database Operations")
    print("-" * 60)

    db = ElectionDatabase("example_data")

    # Add some sample data
    sample_elections = [
        {
            'location': 'Texas - State Senate District 1',
            'state': 'TX',
            'office': 'State Senate',
            'district': 'District 1',
            'election_date': '2025-11-05',
            'r_plus': 15.5,
            'is_uncontested': True,
            'incumbent': 'John Doe',
            'source_url': 'https://example.com',
        },
        {
            'location': 'Texas - State Senate District 2',
            'state': 'TX',
            'office': 'State Senate',
            'district': 'District 2',
            'election_date': '2025-11-05',
            'r_plus': -8.2,
            'is_uncontested': False,
            'incumbent': 'Jane Smith',
            'source_url': 'https://example.com',
        }
    ]

    db.add_elections_batch(sample_elections)
    print(f"Added {len(sample_elections)} sample elections")

    # Query the database
    uncontested = db.query_elections(uncontested_only=True)
    print(f"Found {len(uncontested)} uncontested races")

    # Get statistics
    stats = db.get_statistics()
    print(f"\nDatabase statistics:")
    print(f"  Total elections: {stats['total_elections']}")
    print(f"  States covered: {stats['states_covered']}")


def example_queries():
    """Example: Querying the database."""
    print("\nExample 3: Advanced Queries")
    print("-" * 60)

    db = ElectionDatabase()

    # Find competitive Republican districts (R+ between 0 and 10)
    competitive_r = db.query_elections(min_r_plus=0, max_r_plus=10)
    print(f"Competitive Republican districts: {len(competitive_r)}")

    # Find uncontested races in Texas
    tx_uncontested = db.query_elections(state='TX', uncontested_only=True)
    print(f"Uncontested races in Texas: {len(tx_uncontested)}")

    # Find all State Senate races
    senate_races = db.query_elections(office_type='State Senate')
    print(f"State Senate races: {len(senate_races)}")


if __name__ == "__main__":
    print("Election Tracker - Usage Examples")
    print("=" * 60)
    print()

    # Uncomment the examples you want to run:

    # example_basic_scraping()  # Warning: Makes web requests
    example_database_operations()
    # example_queries()  # Requires data to be scraped first

    print("\n" + "=" * 60)
    print("Examples complete!")
