#!/usr/bin/env python3
"""
Main workflow for person analysis using CrustData and Llama AI

This script orchestrates the two-step process:
1. Fetch person data from CrustData API
2. Analyze the data using Llama AI

Usage:
    python main.py [linkedin_url]
"""

import subprocess
import sys
import os

def run_crustdata(linkedin_url=None):
    """Run crustdata.py to fetch person data"""
    print("🔍 Step 1: Fetching person data from CrustData...")
    
    if linkedin_url:
        result = subprocess.run([sys.executable, "crustdata.py", linkedin_url], 
                              capture_output=True, text=True)
    else:
        result = subprocess.run([sys.executable, "crustdata.py"], 
                              capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    return result.returncode == 0

def run_llama_analysis():
    """Run llama_client.py to analyze the data"""
    print("\n🤖 Step 2: Analyzing data with Llama AI...")
    
    # Check if data file exists
    if not os.path.exists("person_data.json"):
        print("❌ No person data found. Step 1 (CrustData fetch) must have failed.")
        return False
    
    result = subprocess.run([sys.executable, "llama_client.py"], 
                          capture_output=False, text=True)
    
    return result.returncode == 0

def main():
    """Main function to run the complete workflow"""
    print("=== PERSON ANALYSIS WORKFLOW ===\n")
    
    # Get LinkedIn URL from command line argument if provided
    linkedin_url = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Step 1: Fetch data
    if run_crustdata(linkedin_url):
        print("✅ Data fetch completed successfully!")
        
        # Step 2: Analyze data
        run_llama_analysis()
    else:
        print("❌ Data fetch failed. Please check your API credentials and try again.")

if __name__ == "__main__":
    main()
