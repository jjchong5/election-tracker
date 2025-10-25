# Election Tracker - Project Summary

## What Was Built

A complete Python application for tracking upcoming local elections across the United States with the following features:

### Core Components

1. **Database Manager** (`database.py`)
   - Stores election data in CSV and JSON formats
   - Supports querying and filtering
   - Tracks statistics
   - Handles duplicates

2. **Web Scraper** (`scraper.py`)
   - Ballotpedia scraper for state legislative elections
   - Extensible architecture for adding more data sources
   - Respects rate limiting and robots.txt
   - Tracks: location, election date, contested status, incumbents

3. **Main Application** (`main.py`)
   - Command-line interface
   - Scrape, query, and export commands
   - Configurable states and years

4. **Configuration** (`config.py`)
   - Easy customization of states, years, and scraping parameters

### Data Tracked

For each election:
- **Location**: State, office type, and district
- **Election Date**: When the election occurs
- **R+ Value**: Republican advantage (placeholder - not yet calculated)
- **Contested Status**: Whether the race is contested
- **Incumbent**: Current officeholder
- **Source URL**: Where the data came from
- **Last Updated**: When data was collected

## Project Structure

```
election-tracker/
├── main.py              # Main application entry point
├── database.py          # Data storage and querying
├── scraper.py           # Web scraping logic
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── example.py           # Usage examples
├── README.md            # Full documentation
├── QUICKSTART.md        # Quick start guide
├── PROJECT_SUMMARY.md   # This file
└── data/                # Generated data files (created on first run)
    ├── elections.csv
    └── elections.json
```

## Getting Started

### 1. Install Dependencies
```bash
cd election-tracker
pip install -r requirements.txt
```

### 2. Run a Test Scrape
```bash
python main.py scrape --states Virginia --years 2025
```

### 3. View Results
```bash
python main.py stats
python main.py query
```

Or open `data/elections.csv` in Excel/Google Sheets.

## What Works Now

- Scrapes state legislative elections (State Senate and House)
- Stores data in CSV/JSON
- Detects uncontested races
- Tracks incumbents
- Query and filter functionality
- Statistics and reporting

## Known Limitations

### 1. R+ Values Not Calculated
- Currently set to `null` for all races
- Requires adding partisan data sources or calculating from historical results
- See README.md for implementation suggestions

### 2. Limited Scope
- Only state legislative races currently
- Does not yet include:
  - County elections
  - Municipal elections
  - School board races
  - Judicial elections

### 3. Data Source
- Relies primarily on Ballotpedia
- Coverage varies by state
- May miss less documented races

### 4. No Automation
- Manual execution required
- No scheduled updates
- No change tracking

## Future Enhancements

High priority improvements are documented in README.md, including:

1. **Add R+ Calculation**: Most important missing feature
2. **Expand Coverage**: Add county, municipal, and school board elections
3. **Multiple Sources**: Add more data sources for better coverage
4. **Web Interface**: Build a UI for easier browsing
5. **Automated Updates**: Schedule regular data refreshes

## How to Extend

### Adding New Data Sources

1. Create a new scraper class in `scraper.py`:
```python
class NewSourceScraper(ElectionScraper):
    def scrape(self) -> List[Dict]:
        # Your scraping logic
        return elections
```

2. Use the same data structure:
```python
{
    'location': 'State - Office District',
    'state': 'XX',
    'office': 'Office Type',
    'election_date': 'YYYY-MM-DD',
    'r_plus': None,  # or float
    'is_uncontested': False,
    'incumbent': 'Name',
    'source_url': 'https://...',
}
```

3. Add to `main.py` scraping logic

### Adding R+ Calculation

Options:
1. Scrape historical election results from Secretary of State websites
2. Use partisan data from Cook Political Report or FiveThirtyEight
3. Calculate from presidential election results by district
4. Use Daily Kos Elections district-level data

## Usage Examples

### Basic Scraping
```bash
# Single state
python main.py scrape --states California --years 2025

# Multiple states and years
python main.py scrape --states Texas Florida Georgia --years 2025 2026

# Priority states (default 25 major states)
python main.py scrape

# All 50 states (takes 1-2 hours)
python main.py scrape --all-states
```

### Querying Data
```bash
# Show all data
python main.py query

# Filter by state
python main.py query --state TX

# Find uncontested races
python main.py query --uncontested

# Find competitive districts (when R+ data available)
python main.py query --min-r-plus -5 --max-r-plus 5

# Combine filters
python main.py query --state CA --office "State Senate" --uncontested
```

### Viewing Statistics
```bash
python main.py stats
```

## Technical Details

- **Language**: Python 3.8+
- **Web Scraping**: Beautiful Soup 4, Requests
- **Data Storage**: Pandas for CSV, JSON for structured data
- **Rate Limiting**: 2-second delay between requests (configurable)
- **Error Handling**: Graceful failure with logging

## Files Generated

After running, you'll have:
- `data/elections.csv` - Spreadsheet format
- `data/elections.json` - Structured data format

Both contain the same data in different formats for different use cases.

## Success Criteria

This application successfully:
- Scrapes publicly available election data
- Stores it in easy-to-use formats (CSV/JSON)
- Provides command-line tools for querying
- Can be extended with additional sources
- Respects web scraping best practices

## Next Steps for Users

1. **Install and test** with a single state
2. **Review the data** to understand what's captured
3. **Customize** config.py for your needs
4. **Extend** with additional scrapers if needed
5. **Analyze** the CSV data in your preferred tools

## Support

- See README.md for detailed documentation
- Check QUICKSTART.md for quick start guide
- Review example.py for programmatic usage
- Read inline code comments for implementation details

---

**Status**: Fully functional core application with room for expansion

**Best for**: Tracking state legislative elections, research, political analysis

**Requires user extension for**: R+ data, local elections, automated updates
