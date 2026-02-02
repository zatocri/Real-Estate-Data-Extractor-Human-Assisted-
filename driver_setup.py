# driver_setup.py
import undetected_chromedriver as uc

def get_stealth_driver(headless=False):
    """
    Initializes Chrome with undetected-chromedriver to bypass 
    standard automation flags.
    """
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")

    # Use version_main to match your local Chrome version (144)
    driver = uc.Chrome(options=options, version_main=144, headless=headless)
    return driver