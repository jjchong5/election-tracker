"""
Main script to run the election tracker.
"""
import argparse
from database import ElectionDatabase
from scraper import BallotpediaScraper, PartisanDataScraper
import config
from datetime import datetime


def scrape_elections(states=None, years=None, save=True):
    """
    Scrape election data from various sources.

    Args:
        states: List of state names to scrape (None = use priority states)
        years: List of years to scrape (None = use config years)
        save: Whether to save to database

    Returns:
        List of election dictionaries
    """
    if states is None:
        states = config.PRIORITY_STATES

    if years is None:
        years = config.YEARS_TO_TRACK

    print(f"Starting election scraper...")
    print(f"Target: {len(states)} states, {len(years)} years")
    print(f"Years: {min(years)}-{max(years)}")
    print("-" * 60)

    # Initialize scraper
    scraper = BallotpediaScraper(delay=config.REQUEST_DELAY)

    all_elections = []

    # Scrape state legislative elections
    print("\n[1/2] Scraping state legislative elections...")
    for year in years:
        for state in states:
            print(f"  Processing {state} {year}...")
            try:
                elections = scraper.get_state_elections(state, year)
                all_elections.extend(elections)
                print(f"    Found {len(elections)} elections")
            except Exception as e:
                print(f"    Error: {e}")

    print(f"\nTotal elections scraped: {len(all_elections)}")

    # Save to database
    if save and all_elections:
        print("\n[2/2] Saving to database...")
        db = ElectionDatabase(config.DATA_DIR)
        db.add_elections_batch(all_elections)
        db.remove_duplicates()
        print(f"Saved to {db.csv_file} and {db.json_file}")

    return all_elections


def view_statistics():
    """Display database statistics."""
    db = ElectionDatabase(config.DATA_DIR)
    stats = db.get_statistics()

    print("\n" + "=" * 60)
    print("ELECTION TRACKER STATISTICS")
    print("=" * 60)
    print(f"Total elections tracked: {stats['total_elections']}")
    print(f"Uncontested races: {stats['uncontested_count']}")
    print(f"States covered: {stats['states_covered']}")
    if stats.get('offices_tracked'):
        print(f"Office types tracked: {stats['offices_tracked']}")
    if stats.get('avg_r_plus') is not None:
        print(f"Average R+ value: {stats['avg_r_plus']:.2f}")
    print("=" * 60 + "\n")


def query_elections(args):
    """Query elections with filters."""
    db = ElectionDatabase(config.DATA_DIR)

    results = db.query_elections(
        state=args.state,
        office_type=args.office,
        uncontested_only=args.uncontested,
        min_r_plus=args.min_r_plus,
        max_r_plus=args.max_r_plus
    )

    print(f"\nFound {len(results)} matching elections:\n")

    for i, election in enumerate(results[:20], 1):  # Show first 20
        print(f"{i}. {election['location']}")
        print(f"   Date: {election['election_date']}")
        print(f"   R+: {election['r_plus'] if election['r_plus'] is not None else 'N/A'}")
        print(f"   Uncontested: {'Yes' if election['is_uncontested'] else 'No'}")
        if election.get('incumbent'):
            print(f"   Incumbent: {election['incumbent']}")
        print()

    if len(results) > 20:
        print(f"... and {len(results) - 20} more results")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Election Tracker - Track upcoming local elections across the US"
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Scrape command
    scrape_parser = subparsers.add_parser('scrape', help='Scrape election data')
    scrape_parser.add_argument(
        '--states',
        nargs='+',
        help='List of states to scrape (e.g., California Texas)'
    )
    scrape_parser.add_argument(
        '--years',
        nargs='+',
        type=int,
        help='List of years to scrape (e.g., 2025 2026)'
    )
    scrape_parser.add_argument(
        '--all-states',
        action='store_true',
        help='Scrape all 50 states'
    )

    # Stats command
    subparsers.add_parser('stats', help='Show database statistics')

    # Query command
    query_parser = subparsers.add_parser('query', help='Query election database')
    query_parser.add_argument('--state', help='Filter by state abbreviation (e.g., CA)')
    query_parser.add_argument('--office', help='Filter by office type')
    query_parser.add_argument('--uncontested', action='store_true', help='Only uncontested races')
    query_parser.add_argument('--min-r-plus', type=float, help='Minimum R+ value')
    query_parser.add_argument('--max-r-plus', type=float, help='Maximum R+ value')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export data')
    export_parser.add_argument('--format', choices=['csv', 'json'], default='csv')
    export_parser.add_argument('--output', help='Output file path')

    args = parser.parse_args()

    if args.command == 'scrape':
        states = config.ALL_STATES if args.all_states else (args.states or config.PRIORITY_STATES)
        years = args.years or config.YEARS_TO_TRACK
        scrape_elections(states=states, years=years)
        view_statistics()

    elif args.command == 'stats':
        view_statistics()

    elif args.command == 'query':
        query_elections(args)

    elif args.command == 'export':
        db = ElectionDatabase(config.DATA_DIR)
        output = args.output or f"elections_export_{datetime.now().strftime('%Y%m%d')}.{args.format}"
        print(f"Data already available at:")
        print(f"  CSV: {db.csv_file}")
        print(f"  JSON: {db.json_file}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
