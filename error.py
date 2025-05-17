import undetected_chromedriver as uc  # <--- using undetected-chromedriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Chrome Options
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Full screen
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Extra stealth

# Setup Driver
driver = uc.Chrome(options=chrome_options)

# Open Website
driver.get('https://www.crexi.com/properties?pageSize=60')

wait = WebDriverWait(driver, 20)

# Scroll slowly
for i in range(5):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)

# Wait until properties appear
wait.until(EC.presence_of_all_elements_located((By.XPATH, '//crx-property-tile-aggregate')))

# Find all properties
properties = driver.find_elements(By.XPATH, '//crx-property-tile-aggregate')

print(f"Total Properties Found: {len(properties)}")

data = []

# Loop over each property
for prop in properties:
    try:
        title = prop.find_element(By.XPATH, './/h5[@data-cy="propertyName"]').text
    except:
        title = ''
    try:
        location = prop.find_element(By.XPATH, './/h4[@data-cy="propertyAddress"]').text
    except:
        location = ''
    try:
        link = prop.find_element(By.XPATH, './/a').get_attribute('href')
    except:
        link = ''
    try:
        price = prop.find_element(By.XPATH, './/span[@data-cy="propertyPrice"]').text
    except:
        price = ''

    data.append({
        'Title': title,
        'Location': location,
        'Link': link,
        'Price': price
    })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv(' News.csv', index=False)

print('✅ Data saved into crexi_properties.csv')

driver.quit()
