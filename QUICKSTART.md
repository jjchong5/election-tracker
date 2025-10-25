# Quick Start Guide

Get started with Election Tracker in 5 minutes.

## Step 1: Install Dependencies

```bash
cd election-tracker
pip install -r requirements.txt
```

## Step 2: Run Your First Scrape

Start with a small test - scrape one state for 2025:

```bash
python main.py scrape --states Virginia --years 2025
```

This will:
- Scrape Virginia state legislative elections for 2025
- Save data to `data/elections.csv` and `data/elections.json`
- Show statistics when complete

## Step 3: View Your Data

### Option A: View Statistics
```bash
python main.py stats
```

### Option B: Query the Database
```bash
python main.py query
```

### Option C: Open CSV in Excel
Open `data/elections.csv` in Excel, Google Sheets, or any spreadsheet program.

## Step 4: Expand Your Search

### Scrape Multiple States
```bash
python main.py scrape --states California Texas Florida --years 2025 2026
```

### Scrape Default Priority States (25 states)
```bash
python main.py scrape
```

### Scrape All 50 States (Warning: Takes 1-2 hours)
```bash
python main.py scrape --all-states
```

## Step 5: Query Your Data

Find uncontested races:
```bash
python main.py query --uncontested
```

Filter by state:
```bash
python main.py query --state TX
```

Combine filters:
```bash
python main.py query --state CA --office "State Senate"
```

## Common Use Cases

### Find All Uncontested Republican-Leaning Races
```bash
python main.py query --uncontested --min-r-plus 0
```

### Track Competitive Districts (R+ between -5 and +5)
```bash
python main.py query --min-r-plus -5 --max-r-plus 5
```

### Monitor a Specific State
```bash
python main.py scrape --states Ohio --years 2025 2026 2027
python main.py query --state OH
```

## Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'requests'`
- **Solution**: Run `pip install -r requirements.txt`

**Problem**: Scraping is slow
- **Solution**: This is normal. The scraper uses delays to be respectful to servers. Scraping all states takes time.

**Problem**: No elections found for a state/year
- **Solution**: Not all states have elections every year. Try different years or check if data exists on Ballotpedia.

**Problem**: R+ values are all null
- **Solution**: R+ calculation is not yet implemented. This is a known limitation (see README.md).

## Next Steps

1. **Review the Data**: Open `data/elections.csv` and explore what was collected
2. **Customize**: Edit `config.py` to change which states/years to track
3. **Extend**: Add new scrapers in `scraper.py` for additional data sources
4. **Automate**: Set up a cron job or scheduled task to run scraping weekly

## Example Workflow

```bash
# Initial setup
pip install -r requirements.txt

# Scrape data for your target states
python main.py scrape --states Georgia Pennsylvania Arizona

# View what you got
python main.py stats

# Find interesting races
python main.py query --uncontested
python main.py query --min-r-plus 5 --max-r-plus 15

# Export and analyze
# Open data/elections.csv in Excel for pivot tables and analysis
```

## Getting Help

- Read the full [README.md](README.md) for detailed documentation
- Check the [example.py](example.py) file for programmatic usage
- Review the limitations section in README.md
- Examine the source code - it's well-commented!

---

Happy tracking!
