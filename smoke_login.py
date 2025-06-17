from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service("/usr/bin/chromedriver")           # system driver
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")               # comment out to watch

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://the-internet.herokuapp.com/login")

# wait up to 5 s for the username field – proves page really loaded
WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.ID, "username"))
)
print("✅ Page loaded (username field visible)")

driver.find_element(By.ID, "username").send_keys("tomsmith")
driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

assert "/secure" in driver.current_url, "Login failed"
print("✅ Login succeeded")
driver.quit()

