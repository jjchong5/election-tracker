# Election Tracker - Deployment Guide

## 🚀 Replicate Deployment

### Prerequisites
1. **Install Replicate package:**
   ```bash
   pip install replicate
   ```

2. **Set up Replicate API token:**
   ```bash
   export REPLICATE_API_TOKEN=your_token_here
   ```

### Deploy to Replicate

1. **Run the deployment script:**
   ```bash
   python deploy.py
   ```

2. **Or use the direct Replicate code:**
   ```python
   import replicate

   deployment = replicate.deployments.get("jjchong5/election-tracker")
   prediction = deployment.predictions.create(
     input={"message": "Election Tracker deployed successfully"}
   )
   prediction.wait()
   print(prediction.output)
   ```

### Manual Deployment Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export REPLICATE_API_TOKEN=your_token_here
   ```

3. **Run deployment:**
   ```bash
   python deploy.py
   ```

## 🌐 Local Web Server

### Start the web interface:
```bash
python app.py
```

Access at: http://localhost:4000

### Alternative startup:
```bash
python start_election_tracker.bat
```

## 📊 Current Database Status
- **Total Elections**: 7,835
- **States Covered**: 50/50 (100%)
- **Office Types**: State Senate & State House
- **Data Sources**: Ballotpedia

## 🔧 Configuration

### Environment Variables
- `REPLICATE_API_TOKEN`: Your Replicate API token
- `FLASK_ENV`: Set to 'production' for production deployment

### Database Files
- `data/elections.csv`: Main election data (7,835 records)
- `data/elections.json`: Structured JSON format

## 📁 Project Structure
```
election-tracker/
├── app.py                 # Flask web application
├── deploy.py             # Replicate deployment script
├── main.py               # CLI interface
├── database.py           # Database management
├── scraper.py            # Web scraping
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── templates/            # Web templates
│   ├── base.html
│   ├── index.html
│   ├── elections.html
│   └── states.html
└── data/                 # Election data
    ├── elections.csv
    └── elections.json
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start web server:**
   ```bash
   python app.py
   ```

3. **Deploy to Replicate:**
   ```bash
   python deploy.py
   ```

## 📈 Features

### Web Interface
- **Home Dashboard**: Statistics overview
- **Elections Browser**: Filter and search elections
- **State Overview**: Coverage by state
- **Export Functionality**: Download filtered data

### CLI Interface
- **Scrape Elections**: `python main.py scrape`
- **View Statistics**: `python main.py stats`
- **Query Data**: `python main.py query`

### Data Coverage
- **50 States**: Complete coverage
- **7,835 Elections**: Comprehensive database
- **Real-time Filtering**: Advanced search capabilities
- **Export Options**: CSV and JSON formats
