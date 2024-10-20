from recaptchaSolver import solve_recaptcha
from recaptchaSolver import find_between
from datetime import datetime
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Initialize Selenium WebDriver with options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--remote-debugging-port=9222")
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=chrome_options)



def solve_captcha_if_present():
    """Check and solve CAPTCHA if necessary"""
    try:
        captcha_warning_text = "reCAPTCHA"
        if captcha_warning_text in driver.page_source:
            print("Starting to solve he captcha at, " , datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            verbose=False
            solve_recaptcha(driver, verbose)    
            for request in driver.requests:
                if 'recaptcha/api2/userverify' in request.url: 
                    token = find_between(request.response.body.decode('utf-8'), 'uvresp","', '"')
            driver.get_cookies()
            
            print(f"CAPTCHA solved at {datetime.now().strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"Error while solving CAPTCHA: {e}")


"""Go to google.com/recaptcha/api2/demo to solve the v2 captcha for testing"""
driver.get("https://www.google.com/recaptcha/api2/demo")
solve_captcha_if_present()
    
driver.quit()
