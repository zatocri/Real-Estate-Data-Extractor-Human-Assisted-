# Real Estate Data Extractor (Human-Assisted)

A robust desktop application designed to scrape real estate listing data from high-security platforms. Unlike standard bots that fail when encountering behavioral challenges (such as "Press & Hold"), this tool utilizes a hybrid automation architecture. It handles data parsing and navigation automatically but pauses for user intervention during security checks, ensuring stability and continuous operation.

## Key Features

* **Hybrid Automation Workflow:** Automatically detects behavioral security blocks (CAPTCHAs). The system pauses execution, alerts the user to solve the challenge manually, and resumes extraction immediately after the block is cleared.
* **Stealth Browser Integration:** Utilizes `undetected_chromedriver` to patch standard Selenium automation flags, minimizing detection rates during navigation.
* **Threaded GUI:** Built with **PySide6 (Qt)**, ensuring the interface remains responsive while the heavy scraping logic runs on a background thread.
* **Automated Data Export:** Parses complex HTML structures to extract Price, Address, and Property Links, saving the output automatically to an Excel file (`.xlsx`).
* **Smart Pagination:** Handles multi-page navigation and infinite scrolling logic to maximize data yield per session.

## Technical Stack

* **Python 3.x**
* **PySide6** (User Interface)
* **Selenium & Undetected-Chromedriver** (Browser Automation)
* **Pandas** (Data Formatting and Export)

## Project Structure

* `main_window.py`: The entry point of the application. Handles the GUI setup and user inputs.
* `ui_components.py`: Contains the `ScraperWorker` thread. Manages the logic for navigation, parsing, CAPTCHA detection, and data export.
* `driver_setup.py`: Configures the Chrome driver with specific arguments to mimic human browser fingerprints.
* `config.py`: Stores global constants and target configurations.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/zatocri/Real-Estate-Data-Extractor-Human-Assisted-.git
    cd real-estate-extractor
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Ensure `undetected-chromedriver`, `PySide6`, `pandas`, `selenium`, and `openpyxl` are installed)*

3.  **Browser Requirement:**
    This tool requires **Google Chrome** to be installed on the host machine.

## Usage

1.  Run the application:
    ```bash
    python main_window.py
    ```
2.  **Configuration:**
    * **Target Area:** Enter the Zip Code (e.g., `90210`).
    * **Max Leads:** Set the maximum number of listings to retrieve.
3.  **Execution:**
    * Click **Start Extraction**. The browser will launch.
    * **Important:** Do not minimize the browser window completely; keep it visible or in the background.
4.  **Handling Security Checks:**
    * If the site presents a "Press & Hold" or "Security Check" screen, the application status log will read:
        `>> Security check detected. Please solve manually to continue...`
    * Manually click the button or solve the puzzle in the browser window.
    * Once the page loads the results, the script will automatically detect the success and resume scraping.

## Disclaimer

This tool is developed for educational purposes and portfolio demonstration. Automated access to websites may conflict with their Terms of Service. Users are responsible for ensuring their scraping activities comply with local laws and the target website's `robots.txt` policy.