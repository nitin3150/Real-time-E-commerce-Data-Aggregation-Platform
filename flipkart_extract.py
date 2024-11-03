import threading
import signal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import time
import sys

# Global variable to store results and track interruptions
results = []
interrupted = False

# Function to save results to Excel
def save_results():
    results_df = pd.DataFrame(results)
    output_file_path = 'f_dates_new_new.xlsx'
    results_df.to_excel(output_file_path, index=False)
    print(f"Results saved to {output_file_path}")

# Signal handler to catch keyboard interrupt (Ctrl+C)
def signal_handler(sig, frame):
    global interrupted
    print("Process interrupted. Saving partial results...")
    interrupted = True
    save_results()
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

# Function to change the delivery pincode
def change_pincode(driver, new_pincode):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        pincode_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'pincodeInputId')))
        current_pincode = pincode_input.get_attribute('value')

        if current_pincode == new_pincode:
            print(f"Pincode already set to {new_pincode}")
            return

        pincode_input.clear()
        pincode_input.send_keys(new_pincode)
        pincode_input.send_keys(Keys.ENTER)

        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.ID, 'pincodeInputId'), new_pincode))
        print(f"Successfully changed pincode to: {new_pincode}")

    except Exception as e:
        print(f"Error changing pincode: {str(e)}")

# Function to scrape product title, price, and delivery date
def get_product_info(driver, url, pincode, results):
    driver.get(url)
    change_pincode(driver, pincode)
    time.sleep(3)
    product_title = "Title not found"
    price = "Price not found"
    delivery_date = "Delivery date not found"

    try:
        product_title = driver.find_element(By.CLASS_NAME, 'VU-ZEz').text
    except:
        pass

    try:
        delivery_date = driver.find_element(By.CLASS_NAME, 'Y8v7Fl').text
    except:
        pass

    try:
        price = driver.find_element(By.CLASS_NAME, 'Nx9bqj').text
    except:
        pass

    results.append({
        'Link': url,
        'Pincode': pincode,
        'Product Title': product_title,
        'Price': price,
        'Delivery Date': delivery_date,
    })

    # Save partial results after each product
    save_results()

    return results

# Function to process each pincode
def process_pincode(urls, pincode):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome()
    try:
        for url in urls:
            if interrupted:
                break
            get_product_info(driver, url, pincode, results)
    finally:
        driver.quit()

# Main script to login and scrape data for multiple URLs and pincodes
def main():
    # Load the Excel file containing URLs
    file_path = 'flink.xlsx'
    link_df = pd.read_excel(file_path)
    urls = link_df['FK link']

    pincodes = ['380001','380002','560001','560002','600001','600002','110001','110002','500001','500002','700001','700002','226001','226002','400001','400002']
    
    with ThreadPoolExecutor(max_workers=len(pincodes)) as executor:
        future_to_pincode = {executor.submit(process_pincode, urls, pincode): pincode for pincode in pincodes}
        for future in future_to_pincode:
            if interrupted:
                break
            try:
                future.result()
            except Exception as e:
                print(f"Error processing pincode: {future_to_pincode[future]}. Details: {str(e)}")

    save_results()

if __name__ == "__main__":
    main()
