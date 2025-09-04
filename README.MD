# 🏗️ Melbourne Planning Permit Scraper

This project is a **Python 3.10 web scraping skeleton** using **Playwright** with the **Page Object Model (POM)**, designed to scrape planning permit data from the [City of Melbourne Planning Permit Register](https://www.melbourne.vic.gov.au/planning-permit-register).

---

## 📦 Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/tobiasprima/python-exam-web-scraping.git
cd python-exam-web-scraping
```

### 2. Create and Activate a Virtual Environment

#### Using `venv`

```bash
python3.10 -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

#### Using Conda

```bash
conda create -n scraper python=3.10 -y
conda activate scraper
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install
```

This will download Chromium (and optionally other browsers).

---

## ⚙️ Configuration

The scraper uses a `config.json` file for its settings.

* A template is provided as `config.json.example`.
* Copy it and adjust values:

```bash
cp config.json.example config.json
```

### Example `config.json`

```json
{
  "output_dir": "output",
  "csv_path": "input.csv",
  "csv_delimiter": ",",
  "threads": 2,
  "contexts_per_browser": 3,
  "details_concurrency": 5,
  "headless": true
}
```

#### Key Settings

* **output\_dir** → where scraped data will be saved.
* **csv\_path** → path to your input file (must contain `date_from`, `date_to`, etc.).
* **threads** → number of worker processes.
* **contexts\_per\_browser** → Playwright contexts limit per browser.
* **details\_concurrency** → how many detail pages can be scraped concurrently.
* **headless** → set to `false` while debugging to see the browser.

---

## ▶️ Running the Scraper

```bash
python index.py
```

* The program will read your **CSV input file**.
* Results and details will be saved under the **output/** folder.
* Logs will be created automatically in a `logs/` directory at runtime.

---

## 📁 Output Structure

Each scraping run generates a unique case folder inside your `output/` directory:

```
output/
  2025-01-01_to_2025-01-15_case123/
    results_20250904_1530.csv
    results_20250904_1530.json
    results_20250904_1530.xlsx
    details_20250904_1530.csv
    details_20250904_1530.json
    details_20250904_1530.xlsx
```

---

## 📝 Logs

* Logs are stored in the `logs/` directory automatically.
* Each run will create a log file per case (based on date ranges and unique IDs).

---

## 🔧 Development Notes

* Python version: **3.10**
* Project uses **Page Object Model (POM)** with factories for easy extension (e.g., adding `SydneyScraper`).
* To debug and see realtime, set `"headless": false` in `config.json`.

---
