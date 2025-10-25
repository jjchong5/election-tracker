# Election Tracker

A Python-based tool for scraping and tracking upcoming local elections across the United States, including location, partisan lean (R+), and contested status.

## Features

- Scrapes upcoming election data for the next 0-6 years
- Tracks state legislative elections (State Senate, State House)
- Stores data in both CSV and JSON formats
- Tracks key metrics:
  - Location (state, district, office)
  - Election date
  - R+ value (Republican advantage from last election)
  - Contested/uncontested status
  - Incumbent information
- Query and filter election data
- View statistics about tracked elections

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Navigate to the project directory:
```bash
cd election-tracker
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Scrape Election Data

Scrape elections for priority states (default: 25 major states):
```bash
python main.py scrape
```

Scrape specific states:
```bash
python main.py scrape --states California Texas Florida
```

Scrape specific years:
```bash
python main.py scrape --years 2025 2026 2027
```

Scrape all 50 states (warning: this will take a while):
```bash
python main.py scrape --all-states
```

### View Statistics

Show summary statistics about your database:
```bash
python main.py stats
```

### Query Elections

Query all elections:
```bash
python main.py query
```

Filter by state:
```bash
python main.py query --state CA
```

Find uncontested races only:
```bash
python main.py query --uncontested
```

Filter by partisan lean:
```bash
python main.py query --min-r-plus 5 --max-r-plus 15
```

Combine filters:
```bash
python main.py query --state TX --office "State Senate" --uncontested
```

### Access Data Files

After scraping, data is stored in:
- `data/elections.csv` - CSV format (easy to open in Excel/Google Sheets)
- `data/elections.json` - JSON format (structured data)

## Data Schema

Each election record contains:

| Field | Type | Description |
|-------|------|-------------|
| location | string | Full location description (e.g., "California - State Senate District 1") |
| state | string | Two-letter state abbreviation (e.g., "CA") |
| office | string | Office type (e.g., "State Senate", "State House") |
| district | string | District identifier |
| election_date | string | Election date in YYYY-MM-DD format |
| r_plus | float/null | Republican advantage (positive = R+, negative = D+) |
| is_uncontested | boolean | Whether the race is uncontested |
| incumbent | string/null | Name of incumbent if available |
| source_url | string | URL where data was scraped from |
| last_updated | string | ISO timestamp of when data was collected |

## Configuration

Edit `config.py` to customize:

- `PRIORITY_STATES`: List of states to scrape by default
- `YEARS_TO_TRACK`: Years to track (default: current year + 6)
- `REQUEST_DELAY`: Delay between requests (default: 2 seconds)
- `OFFICE_TYPES`: Types of offices to track

## Current Limitations

### 1. R+ Data Not Yet Implemented
The R+ (partisan lean) field is currently set to `null` for all races. To implement:
- Add scrapers for Cook Political Report, FiveThirtyEight, or Daily Kos Elections
- Parse historical election results from Secretary of State websites
- Calculate partisan lean from previous election results

### 2. Limited to State Legislative Races
Currently only scrapes:
- State Senate elections
- State House/Assembly elections

Not yet implemented:
- County Commissioner races
- Mayoral elections
- City Council elections
- School Board elections
- Special districts

### 3. Data Source Limitations
- Relies primarily on Ballotpedia
- May miss elections not well-documented on Ballotpedia
- Some states have better coverage than others
- Uncontested race detection is basic keyword matching

### 4. No Real-Time Updates
- Data is static once scraped
- Need to re-run scraper to get updates
- No automatic scheduling

## Future Improvements

### High Priority
1. **Add R+ Calculation**: Implement partisan lean calculation from historical results
2. **Expand to County/Municipal Elections**: Add scrapers for local races
3. **Multiple Data Sources**: Add scrapers for:
   - State Secretary of State websites
   - Local election boards
   - News sources
4. **Better Uncontested Detection**: Improve accuracy of contested status
5. **Automatic Updates**: Add scheduling to refresh data periodically

### Medium Priority
6. **Web Interface**: Build a simple web UI to browse elections
7. **Export Options**: Add more export formats (Excel, PDF reports)
8. **Historical Data**: Track changes over time
9. **Candidate Information**: Add candidate names, party affiliations
10. **Filing Deadline Tracking**: Track when candidates can file

### Low Priority
11. **Email Alerts**: Notify about new uncontested races or competitive districts
12. **Data Visualization**: Charts and maps of election data
13. **API**: RESTful API for programmatic access

## Contributing

To add new data sources:

1. Create a new scraper class in `scraper.py` inheriting from `ElectionScraper`
2. Implement the `scrape()` method to return election dictionaries
3. Add the scraper to `main.py`
4. Update documentation

Example:
```python
class NewSourceScraper(ElectionScraper):
    def scrape(self) -> List[Dict]:
        # Your scraping logic here
        return elections
```

## Legal and Ethical Considerations

- Respects robots.txt and rate limiting
- Uses 2-second delays between requests by default
- Only scrapes publicly available information
- For research and informational purposes

## Troubleshooting

**Error: "Connection refused" or "Timeout"**
- Check your internet connection
- Increase `REQUEST_DELAY` in config.py
- Some sites may block automated requests

**Error: "No module named 'requests'"**
- Run `pip install -r requirements.txt`

**No data scraped**
- Check if Ballotpedia URLs have changed
- Verify the year and state are valid
- Some states may have limited data for future years

## License

This project is for educational and research purposes. Please respect the terms of service of websites being scraped.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the limitations section
3. Examine the source code comments
4. Modify scrapers to match current website structures

---

**Note**: This tool is a starting point. Election data is complex and decentralized in the US. Expect to customize and extend the scrapers for your specific needs.
