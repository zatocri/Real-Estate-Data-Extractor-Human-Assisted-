# main_window.py
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QLineEdit, QSpinBox,
                               QPushButton, QTextEdit, QProgressBar)
from ui_components import ScraperWorker

class RealEstateApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Real Estate Data Extractor")
        self.setGeometry(100, 100, 600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Input Section
        input_layout = QHBoxLayout()

        self.zip_input = QLineEdit()
        self.zip_input.setPlaceholderText("Enter Zip Code")
        input_layout.addWidget(QLabel("Target Area:"))
        input_layout.addWidget(self.zip_input)

        self.limit_input = QSpinBox()
        self.limit_input.setRange(1, 4000)
        self.limit_input.setValue(50)
        input_layout.addWidget(QLabel("Max Leads:"))
        input_layout.addWidget(self.limit_input)

        layout.addLayout(input_layout)

        # Controls
        self.start_btn = QPushButton("Start Extraction")
        self.start_btn.clicked.connect(self.start_scraping)
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        layout.addWidget(self.start_btn)

        # Progress Indicator
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Logs
        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)
        self.log_window.setStyleSheet("background-color: #222; color: #0f0; font-family: Consolas;")
        layout.addWidget(self.log_window)

        self.worker = None

    def log(self, message):
        self.log_window.append(f">> {message}")

    def start_scraping(self):
        zip_code = self.zip_input.text()
        limit = self.limit_input.value()

        if not zip_code:
            self.log("Error: Please enter a Zip Code.")
            return

        self.start_btn.setEnabled(False)
        self.progress_bar.setMaximum(limit)
        self.progress_bar.setValue(0)
        self.log_window.clear()

        self.worker = ScraperWorker(zip_code, limit)
        self.worker.log_message.connect(self.log)
        self.worker.progress_update.connect(self.progress_bar.setValue)
        self.worker.finished_scraping.connect(self.on_finished)
        self.worker.start()

    def on_finished(self):
        self.start_btn.setEnabled(True)
        self.log("Process finished.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealEstateApp()
    window.show()
    sys.exit(app.exec())