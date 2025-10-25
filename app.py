"""
Flask web application for Election Tracker.
Run with: python app.py
Access at: http://localhost:4000
"""
from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
from database import ElectionDatabase
import config

app = Flask(__name__)

# Initialize database
db = ElectionDatabase(config.DATA_DIR)

@app.route('/')
def index():
    """Home page with overview statistics."""
    stats = db.get_statistics()
    return render_template('index.html', stats=stats)

@app.route('/elections')
def elections():
    """Elections listing page with filtering."""
    # Get filter parameters
    state = request.args.get('state', '')
    office = request.args.get('office', '')
    uncontested = request.args.get('uncontested', '')
    min_r_plus = request.args.get('min_r_plus', '')
    max_r_plus = request.args.get('max_r_plus', '')
    
    # Convert parameters
    uncontested_only = uncontested == 'true'
    min_r = float(min_r_plus) if min_r_plus else None
    max_r = float(max_r_plus) if max_r_plus else None
    
    # Query elections
    elections = db.query_elections(
        state=state if state else None,
        office_type=office if office else None,
        uncontested_only=uncontested_only,
        min_r_plus=min_r,
        max_r_plus=max_r
    )
    
    # Get unique states and offices for filter dropdowns
    all_elections = db.load_elections()
    states = sorted(list(set(e.get('state') for e in all_elections if e.get('state'))))
    offices = sorted(list(set(e.get('office') for e in all_elections if e.get('office'))))
    
    return render_template('elections.html', 
                          elections=elections,
                          states=states,
                          offices=offices,
                          current_filters={
                              'state': state,
                              'office': office,
                              'uncontested': uncontested,
                              'min_r_plus': min_r_plus,
                              'max_r_plus': max_r_plus
                          })

@app.route('/api/elections')
def api_elections():
    """API endpoint for elections data."""
    # Get filter parameters
    state = request.args.get('state', '')
    office = request.args.get('office', '')
    uncontested = request.args.get('uncontested', '')
    min_r_plus = request.args.get('min_r_plus', '')
    max_r_plus = request.args.get('max_r_plus', '')
    
    # Convert parameters
    uncontested_only = uncontested == 'true'
    min_r = float(min_r_plus) if min_r_plus else None
    max_r = float(max_r_plus) if max_r_plus else None
    
    # Query elections
    elections = db.query_elections(
        state=state if state else None,
        office_type=office if office else None,
        uncontested_only=uncontested_only,
        min_r_plus=min_r,
        max_r_plus=max_r
    )
    
    return jsonify(elections)

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics."""
    stats = db.get_statistics()
    return jsonify(stats)

@app.route('/states')
def states():
    """States overview page."""
    all_elections = db.load_elections()
    df = pd.DataFrame(all_elections)
    
    # Group by state
    state_stats = df.groupby('state').agg({
        'location': 'count',
        'is_uncontested': 'sum',
        'office': lambda x: list(x.unique())
    }).rename(columns={'location': 'total_elections'})
    
    state_stats = state_stats.reset_index()
    state_stats = state_stats.sort_values('total_elections', ascending=False)
    
    return render_template('states.html', state_stats=state_stats.to_dict('records'))

if __name__ == '__main__':
    print("Starting Election Tracker Web Server...")
    print("Access at: http://localhost:4000")
    app.run(host='0.0.0.0', port=4000, debug=True)
