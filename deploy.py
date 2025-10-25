"""
Replicate deployment script for Election Tracker.
This script provides deployment instructions and can be run after installing replicate.
"""
import os
import json
from database import ElectionDatabase
import config

def deploy_to_replicate():
    """
    Deploy the Election Tracker to Replicate.
    Note: Requires 'pip install replicate' to be run first.
    """
    try:
        # Import replicate only when needed
        import replicate
        
        # Get the deployment
        deployment = replicate.deployments.get("jjchong5/election-tracker")
        
        # Prepare input data (you can customize this based on your needs)
        input_data = {
            "message": "Election Tracker deployed successfully",
            "total_elections": get_election_count(),
            "states_covered": get_states_count()
        }
        
        # Create prediction
        prediction = deployment.predictions.create(input=input_data)
        
        # Wait for completion
        prediction.wait()
        
        print("Deployment successful!")
        print(f"Prediction ID: {prediction.id}")
        print(f"Status: {prediction.status}")
        print(f"Output: {prediction.output}")
        
        return prediction
        
    except ImportError:
        print("Replicate package not installed. Please run:")
        print("pip install replicate")
        return None
    except Exception as e:
        print(f"Deployment failed: {e}")
        return None

def get_election_count():
    """Get total number of elections from database."""
    try:
        db = ElectionDatabase(config.DATA_DIR)
        stats = db.get_statistics()
        return stats.get('total_elections', 0)
    except:
        return 0

def get_states_count():
    """Get number of states covered."""
    try:
        db = ElectionDatabase(config.DATA_DIR)
        stats = db.get_statistics()
        return stats.get('states_covered', 0)
    except:
        return 0

def main():
    """Main deployment function."""
    print("=" * 60)
    print("Election Tracker - Replicate Deployment")
    print("=" * 60)
    print()
    
    # Check if Replicate API key is set
    if not os.getenv('REPLICATE_API_TOKEN'):
        print("Error: REPLICATE_API_TOKEN environment variable not set")
        print("Please set your Replicate API token:")
        print("export REPLICATE_API_TOKEN=your_token_here")
        return
    
    print("Starting deployment to Replicate...")
    print(f"Elections in database: {get_election_count()}")
    print(f"States covered: {get_states_count()}")
    print()
    
    # Deploy
    prediction = deploy_to_replicate()
    
    if prediction:
        print("\n✅ Deployment completed successfully!")
        print(f"🔗 Check your deployment at: https://replicate.com/jjchong5/election-tracker")
    else:
        print("\n❌ Deployment failed. Please check your configuration.")

if __name__ == "__main__":
    main()
