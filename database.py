"""
Database manager for election tracking using CSV and JSON files.
"""
import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd


class ElectionDatabase:
    """Manages election data storage in CSV and JSON formats."""

    def __init__(self, data_dir: str = "data"):
        """
        Initialize the database manager.

        Args:
            data_dir: Directory to store data files
        """
        self.data_dir = data_dir
        self.csv_file = os.path.join(data_dir, "elections.csv")
        self.json_file = os.path.join(data_dir, "elections.json")
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist."""
        os.makedirs(self.data_dir, exist_ok=True)

    def add_election(self, election: Dict) -> None:
        """
        Add a single election record.

        Args:
            election: Dictionary containing election data with keys:
                - location: str (e.g., "New York, NY - City Council District 1")
                - state: str
                - office: str
                - election_date: str (YYYY-MM-DD format)
                - r_plus: float or None (Republican advantage from last election)
                - is_uncontested: bool
                - incumbent: str or None
                - source_url: str
                - last_updated: str (ISO format timestamp)
        """
        elections = self.load_elections()

        # Add timestamp if not present
        if 'last_updated' not in election:
            election['last_updated'] = datetime.now().isoformat()

        elections.append(election)
        self.save_elections(elections)

    def add_elections_batch(self, elections: List[Dict]) -> None:
        """
        Add multiple election records at once.

        Args:
            elections: List of election dictionaries
        """
        existing = self.load_elections()

        # Add timestamps
        for election in elections:
            if 'last_updated' not in election:
                election['last_updated'] = datetime.now().isoformat()

        existing.extend(elections)
        self.save_elections(existing)

    def load_elections(self) -> List[Dict]:
        """
        Load all elections from JSON file.

        Returns:
            List of election dictionaries
        """
        if not os.path.exists(self.json_file):
            return []

        with open(self.json_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_elections(self, elections: List[Dict]) -> None:
        """
        Save elections to both JSON and CSV files.

        Args:
            elections: List of election dictionaries
        """
        # Save to JSON
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(elections, f, indent=2, ensure_ascii=False)

        # Save to CSV
        if elections:
            df = pd.DataFrame(elections)
            df.to_csv(self.csv_file, index=False, encoding='utf-8')

    def query_elections(
        self,
        state: Optional[str] = None,
        office_type: Optional[str] = None,
        uncontested_only: bool = False,
        min_r_plus: Optional[float] = None,
        max_r_plus: Optional[float] = None
    ) -> List[Dict]:
        """
        Query elections with filters.

        Args:
            state: Filter by state abbreviation (e.g., "NY")
            office_type: Filter by office type (e.g., "State Senate")
            uncontested_only: Only return uncontested races
            min_r_plus: Minimum R+ value
            max_r_plus: Maximum R+ value

        Returns:
            Filtered list of elections
        """
        elections = self.load_elections()

        if state:
            elections = [e for e in elections if e.get('state') == state]

        if office_type:
            elections = [e for e in elections if e.get('office') == office_type]

        if uncontested_only:
            elections = [e for e in elections if e.get('is_uncontested') == True]

        if min_r_plus is not None:
            elections = [
                e for e in elections
                if e.get('r_plus') is not None and e.get('r_plus') >= min_r_plus
            ]

        if max_r_plus is not None:
            elections = [
                e for e in elections
                if e.get('r_plus') is not None and e.get('r_plus') <= max_r_plus
            ]

        return elections

    def get_statistics(self) -> Dict:
        """
        Get summary statistics about the election database.

        Returns:
            Dictionary with statistics
        """
        elections = self.load_elections()

        if not elections:
            return {
                'total_elections': 0,
                'uncontested_count': 0,
                'states_covered': 0,
                'avg_r_plus': None
            }

        r_plus_values = [
            e['r_plus'] for e in elections
            if e.get('r_plus') is not None
        ]

        return {
            'total_elections': len(elections),
            'uncontested_count': sum(1 for e in elections if e.get('is_uncontested')),
            'states_covered': len(set(e.get('state') for e in elections if e.get('state'))),
            'avg_r_plus': sum(r_plus_values) / len(r_plus_values) if r_plus_values else None,
            'offices_tracked': len(set(e.get('office') for e in elections if e.get('office')))
        }

    def remove_duplicates(self) -> int:
        """
        Remove duplicate election entries based on location and election_date.

        Returns:
            Number of duplicates removed
        """
        elections = self.load_elections()
        original_count = len(elections)

        seen = set()
        unique_elections = []

        for election in elections:
            key = (election.get('location'), election.get('election_date'))
            if key not in seen:
                seen.add(key)
                unique_elections.append(election)

        self.save_elections(unique_elections)
        return original_count - len(unique_elections)
