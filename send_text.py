import os, time, pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import atexit

COOKIES_FILE = "whatsapp_cookies.pkl"



class WhatsApp:
    def __init__(self, phone_number: str, headless=True):
        self.phone_number = phone_number
        self.headless = headless
        self.driver = self.make_driver(headless)
        atexit.register(self.cleanup)

    def make_driver(self, headless=True, profile_dir="whatsapp-profile"):
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--user-data-dir={profile_dir}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("window-size=1920,1080")

        try:
            driver = webdriver.Chrome(options=options)
            stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    run_on_insecure_origins=True)
        
            return driver
        
        except Exception as e:
            raise RuntimeError(f"Error initializing WebDriver: {e}")


    def set_react_value(self, driver, element, value):
        js = """
        const el = arguments[0];
        const value = arguments[1];
        const nativeSetter = Object.getOwnPropertyDescriptor(
        HTMLInputElement.prototype, 'value'
        ).set;
        nativeSetter.call(el, value);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        """
        driver.execute_script(js, element, value)

    def login(self):
        """
        1) Opens WhatsApp Web
        2) Clicks “Log in with phone number”
        3) Waits until chats UI loads (user enters code on phone)
        4) Saves cookies to COOKIES_FILE
        """
        self.driver.get("https://web.whatsapp.com")

        # click “Log in with phone number”
        btn = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Log in with phone number')]"))
        )
        btn.click()

        # fill phone input
        phone_in = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Type your phone number.']"))
        )
        self.set_react_value(self.driver, phone_in, self.phone_number)

        next_btn = self.driver.find_element(By.XPATH, "//button[.//div[text()='Next']]")
        next_btn.click()

        code_div = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-link-code]"))
        )

        link_code = code_div.get_attribute("data-link-code")
        print("🔑 data-link-code =", link_code)

        # WAIT for main chat UI: e.g. the “Chats” tab button
        WebDriverWait(self.driver, 300).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Chats']"))
        )
        print("✅ Logged in — saving cookies.")

        # save cookies
        # with open(COOKIES_FILE, "wb") as f:
        #     pickle.dump(driver.get_cookies(), f)


    def send_whatsapp_message(self, phone_numbers: list, message: str, headless=True):
        """
        1) Loads cookies from COOKIES_FILE into a headless driver
        2) Opens WhatsApp Web (already logged in)
        3) Opens chat for phone_number and sends `message`
        """

        self.driver.get("https://web.whatsapp.com")

        try:
            continue_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()='Continue']]"))
            )
            continue_btn.click()
        except Exception as e:
            pass


        # open chat and send
        for phone_number in phone_numbers:
            chat_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
            self.driver.get(chat_url)
            # wait for send button
            send_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send']"))
            )
            send_btn.click()
            WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Voice message']"))
            )
            print(f"📨 Sent to {phone_number}: {message}")


    def send_text(self, toNumbers: list, message: str):
        self.send_whatsapp_message(toNumbers, message, self.headless)


    def cleanup(self):
        print("Cleaning up...")
        if hasattr(self, "driver") and self.driver:
            self.driver.quit()

    