from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime
import re
from selenium.common.exceptions import NoSuchElementException

# Function to check if CAPTCHA is present
def is_captcha_present(driver):
    try:
        # Adjust this selector based on the CAPTCHA implementation on Amazon
        driver.find_element(By.XPATH, "//*[contains(text(), 'captcha')]")  # Modify the XPath to match the CAPTCHA message
        return True
    except NoSuchElementException:
        return False

# Function to login to Amazon
def login_to_amazon(driver):
    driver.get("https://www.amazon.in/")
    # time.sleep(10)
    if is_captcha_present(driver):
        print("CAPTCHA detected! Please solve the CAPTCHA.")
        input("Press Enter after solving the CAPTCHA to continue...")
        # time.sleep(5)  # Optional: Wait a bit before checking again
    
    # Click on the sign-in button
    sign_in_button = driver.find_element(By.ID, 'nav-link-accountList')
    sign_in_button.click()

    time.sleep(30)

# Function to change the delivery pincode
def change_pincode(driver,pincode):
    try:
        # Click on the pincode input
        pincode_input = driver.find_element(By.ID, 'glow-ingress-line2')
        pincode_input.click()
        time.sleep(1)
        
        # Enter new pincode
        pincode_input_box = driver.find_element(By.ID, 'GLUXZipUpdateInput')
        pincode_input_box.clear()
        pincode_input_box.send_keys(pincode)
        pincode_input_box.send_keys(Keys.RETURN)
        time.sleep(3)
    except Exception as e:
        print(f"Error changing pincode: {e}")
    
# Function to scrape product title and delivery date using Selenium
def get_product_info(driver, asin_list, results, pin):
    for asin in asin_list:
        url = f"https://www.amazon.in/dp/{asin}"
        driver.get(url)

        # Check for CAPTCHA
        if is_captcha_present(driver):
            print("CAPTCHA detected! Please solve the CAPTCHA.")
            input("Press Enter after solving the CAPTCHA to continue...")
            # time.sleep(5)  # Optional: Wait a bit before checking again

        # Initialize placeholders
        product_title = "Title not found"
        price = "price not found"
        delivery_date = "Delivery date not found"
        
        try:
            # Attempt to locate the product title
            product_title = driver.find_element(By.ID, 'productTitle').text
        except:
            pass

        try:
            price_element = driver.find_element(By.ID, 'corePriceDisplay_desktop_feature_div')
            price = price_element.text
        except:
            pass

        try:
            # Attempt to locate the delivery date
            delivery_date_element = driver.find_element(By.ID, 'mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE')
            delivery_date = delivery_date_element.text
        except:
            pass

        results.append({
            'ASIN': asin,
            'Pincode': pin,
            'Product Title': product_title,
            'Price': price,
            'Delivery Date': delivery_date,
        })
    return results

# Main script to login and scrape data for multiple ASINs and pincodes
def main():
    file_path = 'avf.xlsx'
    data = pd.read_excel(file_path)
    asin_list = data['ASIN']
    # pincodes = data['pincodes']
    pincodes = ['500001', '560001','700001','110001']

    print()
    # Set up Selenium with Chrome
    driver = webdriver.Chrome()
    results = []

    login_to_amazon(driver)
    
    for pin in pincodes:
        change_pincode(driver, pin)
        get_product_info(driver, asin_list, results, pin)
    
    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    
    # Save results to a new Excel file
    output_file_path = 'amazon_delivery_dates.xlsx'
    results_df.to_excel(output_file_path, index=False)
    
    print(f"Results saved to {output_file_path}")
    driver.quit()

if __name__ == "__main__":
    main()