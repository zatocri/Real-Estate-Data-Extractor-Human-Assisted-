# ui_components.py
import time
import random
import os
import pandas as pd
from datetime import datetime
from PySide6.QtCore import QThread, Signal
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from driver_setup import get_stealth_driver
from config import TARGET_URL


class ScraperWorker(QThread):
    log_message = Signal(str)
    progress_update = Signal(int)
    finished_scraping = Signal()

    def __init__(self, zip_code, limit):
        super().__init__()
        self.zip_code = zip_code
        self.limit = limit
        self.is_running = True
        self.driver = None

    def run(self):
        self.log_message.emit("Initializing browser...")

        try:
            self.driver = get_stealth_driver(headless=False)
        except Exception as e:
            self.log_message.emit(f"Browser initialization failed: {str(e)}")
            self.finished_scraping.emit()
            return

        # Navigation
        search_url = f"{TARGET_URL}/homes/{self.zip_code}_rb/"
        self.log_message.emit(f"Navigating to: {search_url}")

        try:
            self.driver.get(search_url)
            time.sleep(random.uniform(4, 7))
        except Exception:
            self.log_message.emit("Connection error. Stopping.")
            self.shutdown()
            return

        # Main Scraping Loop
        total_scraped = 0
        scraped_data = []

        self.log_message.emit("Starting data extraction...")

        while total_scraped < self.limit and self.is_running:

            # Security Check Handler
            # If a captcha is detected, loop here until the user solves it manually.
            while self.check_for_captcha():
                if not self.is_running: break
                self.log_message.emit("Security check detected. Please solve manually to continue...")
                time.sleep(3)

                # Scroll down to load lazy-loaded elements
            try:
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(3)
            except Exception:
                pass

            cards = self.driver.find_elements(By.TAG_NAME, "article")

            for card in cards:
                if total_scraped >= self.limit or not self.is_running:
                    break

                try:
                    # Extract Price
                    price_el = card.find_element(By.CSS_SELECTOR, "[data-test='property-card-price']")
                    price = price_el.text
                    if not price:
                        price = price_el.find_element(By.XPATH, ".//span[contains(text(), '$')]").text

                    # Extract Address
                    address = card.find_element(By.TAG_NAME, "address").text

                    # Extract Link
                    link_el = card.find_element(By.CSS_SELECTOR, "[data-test='property-card-link']")
                    link = link_el.get_attribute("href")

                    # Save and Log
                    record = {"Price": price, "Address": address, "Link": link}
                    scraped_data.append(record)

                    total_scraped += 1
                    self.progress_update.emit(total_scraped)
                    self.log_message.emit(f"Extracted {total_scraped}: {price}")

                except Exception:
                    # Skip incomplete cards
                    continue

            # Pagination Logic
            if total_scraped < self.limit:
                try:
                    next_btn = self.driver.find_element(By.CSS_SELECTOR, "[title='Next page']")
                    if next_btn.is_enabled():
                        self.log_message.emit("Navigating to next page...")
                        next_btn.click()
                        time.sleep(random.uniform(5, 8))
                    else:
                        self.log_message.emit("No more pages available.")
                        break
                except Exception:
                    self.log_message.emit("Pagination ended.")
                    break

        self.log_message.emit(f"Scraping complete. Saving {len(scraped_data)} records...")
        self.save_data_to_excel(scraped_data)
        self.shutdown()

    def save_data_to_excel(self, data):
        """Saves the scraped list of dictionaries to an Excel file on the Desktop."""
        if not data:
            return
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Leads_{self.zip_code}_{timestamp}.xlsx"

            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            if not os.path.exists(desktop):
                desktop = os.getcwd()

            full_path = os.path.join(desktop, filename)

            df = pd.DataFrame(data)
            df.to_excel(full_path, index=False)
            self.log_message.emit(f"File saved: {full_path}")

        except Exception as e:
            self.log_message.emit(f"Error saving file: {e}")

    def check_for_captcha(self):
        """Checks if the site is currently blocking access."""
        try:
            if "security check" in self.driver.title.lower():
                return True

            body_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            if "press and hold" in body_text or "verify you are human" in body_text:
                return True

            return False
        except Exception:
            return False

    def shutdown(self):
        if self.driver:
            self.driver.quit()
        self.finished_scraping.emit()

    def stop(self):
        self.is_running = False