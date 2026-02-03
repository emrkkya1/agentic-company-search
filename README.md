# LLM Internship Finder

A powerful tool driven by Large Language Models (Google Gemini) to discover tech companies attending summits and conferences in specific locations. This tool is designed to help students and job seekers find potential internship opportunities at startups, small, and medium-sized enterprises (SMEs) across Europe and beyond.

## 🚀 Features

- **Intelligent Discovery**: Uses Gemini AI to identify tech summits and the companies attending them.
- **Precise Targeting**: Search by specific city and date range (e.g., "Berlin" in "2025").
- **Batch Processing**: Pre-configured script to scan 15 major European tech hubs automatically.
- **Smart Filtering**: Post-processing tools to:
  - Filter by company scale (Startup, Small, Medium).
  - Exclude companies from specific regions (e.g., US-based companies if looking for EU roles).
  - Deduplicate results.
- **Structured Output**: Saves data in clean, machine-readable JSON format.

## 🛠️ Prerequisites

- Python 3.10 or higher
- A Google Cloud Project with the Gemini API enabled
- A valid `GEMINI_API_KEY`

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd llm-internship-finder
   ```

2. **Set up a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   Create a `.env` file in the root directory and add your API Key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## 💻 Usage

### 1. Single City Search (CLI)
You can search for a specific location using the command-line interface:

```bash
# Syntax
python -m src.main find-companies <City> <Start-Date> <End-Date> [OPTIONS]

# Example: Search for companies in Berlin for the year 2025
python -m src.main find-companies "Berlin" "2025-01-01" "2025-12-31" --save-result
```

**Options:**
- `--save-result / --no-save-result`: Save the output to JSON (Default: True).
- `--output-path`: Specify a custom output file path.

### 2. Batch Processing (New!)
You can scan multiple locations at once, or use the built-in "Europe Tech Hubs" preset. This replaces the old shell script.

**Run for specific locations:**
```bash
python -m src.main run-batch "New York" "San Francisco" "Tokyo"
```

**Run for the top European tech hubs (Berlin, Paris, Amsterdam, etc.):**
```bash
python -m src.main run-batch --europe
```

**Mix both:**
```bash
python -m src.main run-batch "London" --europe
```

**Options:**
- `--europe`: Include 15 major European tech hubs.
- `--time-start`, `--time-end`: Date range (Default: 2025 full year).
- `--output-dir`: JSON output directory (Default: `results/`).

### 3. Process and Aggregate Results
After running searches, you will have multiple JSON files in the `results/` directory. Use the processing script to consolidate them into a single, clean list:

```bash
python process_companies.py
```

This will:
- Combine all JSON files from `results/`.
- Filter for **Startup**, **Small**, and **Medium** sized companies.
- Exclude companies based in the US (configurable).
- Remove duplicates.
- Generate `filtered_companies.json` with the final list.

## 📂 Project Structure

```
├── src/                        # Source code
│   ├── agents/                 # AI Agents for finding summits and companies
│   ├── service/                # Business logic orchestration
│   │   ├── companies_service/  # Company finding logic (batch & single)
│   ├── models/                 # Data models (Pydantic)
│   ├── adapters/               # API adapters (Gemini)
│   ├── config.py               # Configuration settings
│   └── main.py                 # CLI entry point
├── results/                    # Directory where search results are saved
├── process_companies.py        # Script to filter and aggregate results
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 🔧 Customization

- **Adjust Filters**: Edit `process_companies.py` to change allowed scales (e.g., add "Large") or excluded countries.
- **Modify Batch Cities**: Edit `src/service/companies_service/batch_service.py` to change the `EUROPE_TECH_HUBS` list.
- **Model Settings**: Edit `src/config.py` or use environment variables to change the Gemini model version or temperature.
