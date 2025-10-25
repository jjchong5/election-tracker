"""
Web scraping module for election data collection.
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import re
from datetime import datetime
from tqdm import tqdm


class ElectionScraper:
    """Base class for election data scrapers."""

    def __init__(self, delay: float = 1.0):
        """
        Initialize the scraper.

        Args:
            delay: Delay in seconds between requests (be respectful to servers)
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def _sleep(self):
        """Sleep to avoid overwhelming the server."""
        time.sleep(self.delay)

    def scrape(self) -> List[Dict]:
        """
        Scrape election data. To be implemented by subclasses.

        Returns:
            List of election dictionaries
        """
        raise NotImplementedError


class BallotpediaScraper(ElectionScraper):
    """Scraper for Ballotpedia election data."""

    def __init__(self, delay: float = 2.0):
        """Initialize Ballotpedia scraper with longer delay."""
        super().__init__(delay)
        self.base_url = "https://ballotpedia.org"

    def get_state_elections(self, state: str, year: int) -> List[Dict]:
        """
        Scrape elections for a specific state and year.

        Args:
            state: State name (e.g., "California")
            year: Election year

        Returns:
            List of election dictionaries
        """
        elections = []

        # Try state legislative elections
        url = f"{self.base_url}/{state}_State_Senate_elections,_{year}"
        elections.extend(self._scrape_state_leg_page(url, state, "State Senate", year))

        self._sleep()

        url = f"{self.base_url}/{state}_House_of_Representatives_elections,_{year}"
        elections.extend(self._scrape_state_leg_page(url, state, "State House", year))

        return elections

    def _scrape_state_leg_page(self, url: str, state: str, office: str, year: int) -> List[Dict]:
        """Scrape a state legislative elections page."""
        elections = []

        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Warning: Could not access {url} (status {response.status_code})")
                return elections

            soup = BeautifulSoup(response.content, 'lxml')

            # Look for election tables
            tables = soup.find_all('table', {'class': ['wikitable', 'bptable']})

            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header

                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) < 2:
                        continue

                    # Extract district/location
                    location_text = cells[0].get_text(strip=True)
                    if not location_text:
                        continue

                    # Check if uncontested
                    row_text = row.get_text().lower()
                    is_uncontested = 'uncontested' in row_text or 'unopposed' in row_text

                    # Extract incumbent info if available
                    incumbent = None
                    if len(cells) > 1:
                        incumbent_cell = cells[1].get_text(strip=True)
                        if incumbent_cell and incumbent_cell.lower() not in ['vacant', 'none', '']:
                            incumbent = incumbent_cell

                    election = {
                        'location': f"{state} - {office} {location_text}",
                        'state': self._state_to_abbrev(state),
                        'office': office,
                        'district': location_text,
                        'election_date': f"{year}-11-05",  # Approximate general election date
                        'r_plus': None,  # Will need separate source for partisan data
                        'is_uncontested': is_uncontested,
                        'incumbent': incumbent,
                        'source_url': url,
                        'last_updated': datetime.now().isoformat()
                    }
                    elections.append(election)

        except Exception as e:
            print(f"Error scraping {url}: {e}")

        return elections

    def scrape_upcoming_elections(self, years: List[int] = None) -> List[Dict]:
        """
        Scrape upcoming elections for multiple years.

        Args:
            years: List of years to scrape (defaults to next 6 years)

        Returns:
            List of election dictionaries
        """
        if years is None:
            current_year = datetime.now().year
            years = list(range(current_year, current_year + 7))

        all_elections = []

        # Major states to start with (can be expanded)
        states = [
            "California", "Texas", "Florida", "New York", "Pennsylvania",
            "Illinois", "Ohio", "Georgia", "North_Carolina", "Michigan"
        ]

        print(f"Scraping elections for {len(states)} states across {len(years)} years...")

        for year in tqdm(years, desc="Years"):
            for state in tqdm(states, desc="States", leave=False):
                elections = self.get_state_elections(state, year)
                all_elections.extend(elections)
                self._sleep()

        return all_elections

    def _state_to_abbrev(self, state_name: str) -> str:
        """Convert state name to abbreviation."""
        state_abbrevs = {
            'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
            'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
            'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
            'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
            'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
            'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
            'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
            'New_Hampshire': 'NH', 'New_Jersey': 'NJ', 'New_Mexico': 'NM', 'New_York': 'NY',
            'North_Carolina': 'NC', 'North_Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
            'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode_Island': 'RI', 'South_Carolina': 'SC',
            'South_Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
            'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West_Virginia': 'WV',
            'Wisconsin': 'WI', 'Wyoming': 'WY'
        }
        return state_abbrevs.get(state_name, state_name[:2].upper())


class PartisanDataScraper(ElectionScraper):
    """Scraper for partisan lean data (R+ values)."""

    def __init__(self):
        """Initialize partisan data scraper."""
        super().__init__()

    def get_partisan_lean(self, state: str, district: str, office: str) -> Optional[float]:
        """
        Get partisan lean (R+) for a specific district.

        This is a stub that should be implemented with actual data sources like:
        - Cook Political Report
        - FiveThirtyEight
        - Daily Kos Elections
        - State-specific election results

        Args:
            state: State abbreviation
            district: District identifier
            office: Office type

        Returns:
            R+ value (positive for Republican, negative for Democrat) or None
        """
        # TODO: Implement actual partisan data scraping
        # For now, return None
        return None

    def bulk_enrich_with_partisan_data(self, elections: List[Dict]) -> List[Dict]:
        """
        Enrich election data with partisan lean information.

        Args:
            elections: List of election dictionaries

        Returns:
            Elections list with r_plus values added where available
        """
        # TODO: Implement bulk partisan data lookup
        # This could query election results APIs or scrape historical data
        return elections


class LocalElectionsScraper(ElectionScraper):
    """Scraper for county and municipal elections."""

    def __init__(self):
        """Initialize local elections scraper."""
        super().__init__()

    def scrape_county_elections(self, state: str, county: str, year: int) -> List[Dict]:
        """
        Scrape county-level elections.

        This is a stub - implementation would require:
        - County-specific election websites
        - Secretary of State websites
        - Local news sources

        Args:
            state: State abbreviation
            county: County name
            year: Election year

        Returns:
            List of election dictionaries
        """
        # TODO: Implement county elections scraping
        return []

    def scrape_municipal_elections(self, state: str, city: str, year: int) -> List[Dict]:
        """
        Scrape city/municipal elections.

        Args:
            state: State abbreviation
            city: City name
            year: Election year

        Returns:
            List of election dictionaries
        """
        # TODO: Implement municipal elections scraping
        return []
