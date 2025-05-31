# vibe25-2-hackathon

## Overview
This project fetches professional profile data from CrustData API and processes it through Llama AI to generate insights and job fit analysis.

## Workflow
The project consists of three main files:

1. **`crustdata.py`** - Fetches person data from CrustData API and saves to `person_data.json`
2. **`llama_client.py`** - Reads the saved data and analyzes it using Llama AI
3. **`main.py`** - Orchestrates the complete workflow (optional, you can run files individually)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and replace the placeholder values with your actual API keys:
   - `CRUSTDATA_API_TOKEN`: Your Crustdata API token
   - `LLAMA_API_KEY`: Your Llama API key

## Usage

### Option 1: Run the complete workflow
```bash
python main.py
# OR with a specific LinkedIn URL
python main.py "https://www.linkedin.com/in/username/"
```

### Option 2: Run steps individually

**Step 1: Fetch person data**
```bash
python crustdata.py
# OR with a specific LinkedIn URL
python crustdata.py "https://www.linkedin.com/in/username/"
```

**Step 2: Analyze the data**
```bash
python llama_client.py
```

When you run `llama_client.py`, you'll be prompted to choose:
1. **Job Fit Analysis** - Compare the candidate against a specific job description
2. **General Professional Analysis** - Get overall insights about the person's career

## Environment Variables

- `CRUSTDATA_API_TOKEN`: Your Crustdata API token
- `LLAMA_API_KEY`: Your Llama API key

## Files

- `crustdata.py`: Fetches data from CrustData API and saves to JSON file
- `llama_client.py`: Analyzes person data using Llama AI (job fit analysis)
- `main.py`: Complete workflow orchestrator
- `person_data.json`: Generated file containing the fetched person data
- `.env`: Environment variables (not committed to git)
- `.env.example`: Template for environment variables

## Example Output

After running `crustdata.py`, you'll see:
```
✅ Data successfully saved to person_data.json
📊 Found 1 person record(s)
👤 Name: John Doe
💼 Current Role: Software Engineer at Company XYZ
```

After running `llama_client.py` with job fit analysis, you'll get:
- Fit Score (1-10)
- Strengths matching the job
- Potential gaps
- Hiring recommendation
- Interview questions to ask