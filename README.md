# Automated Scraping and Report Processing

This project automates the scraping of market share reports and processes the downloaded data.

## Project Structure

```
├── main.py                # Main script to run the scraping process
├── utils.py               # Utility functions for scraping and processing reports
├── inputs.csv             # CSV file containing input parameters
├── all_reports/           # Folder where raw downloaded reports are stored
├── final_reports/         # Folder where processed and renamed reports are stored
```

## Prerequisites

- Python 3.x
- Required Python packages: `selenium`, `pandas`, `concurrent.futures`, `os`, `shutil`, `csv`, `ast`
- Google Chrome and ChromeDriver installed

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/bryanbisetti/floir_scraping.git
    cd floir_scraping
    ```
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### 1. Prepare Input File
Ensure that `inputs.csv` is present in the root directory. This file contains the input parameters for the scraping process.

### 2. Create Required Folders
Before running the script, ensure that the following folders exist:

- `all_reports/` - This folder will store the raw downloaded reports.
- `final_reports/` - This folder will store processed reports after renaming and organizing.

If these folders do not exist, create them manually:

```sh
mkdir all_reports final_reports
```

### 3. Run the Script
Execute the `main.py` script:

```sh
python main.py
```

### 4. Processed Reports
- **Raw reports** are saved in `all_reports/` during the scraping process.
- After processing, **final reports** are structured and renamed in `final_reports/`.

## Error Handling
- Errors encountered during scraping are stored in a queue.
- The script attempts to reprocess failed reports with increased wait time.
- The input CSV is updated with failed entries for retrying.

## Notes
- Scraping is performed using Selenium WebDriver in headless mode.
- The process is parallelized for efficiency using `ThreadPoolExecutor`.

## License
This project is licensed under the MIT License.

