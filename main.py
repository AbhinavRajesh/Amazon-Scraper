# For accessing the command line arguments
import sys

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# For stopping the execution of program while page loads
from time import sleep

# For saving the file in CSV Format
import csv
# For saving the file in JSON Format
import json

# Time to sleep so that the content on the page loads
# Keep it low(1-3) for fast internet
# Keep it high(4-8) for slow internet
SLEEP_TIME=3

# To get the product to be searched for
def get_product_name() -> str:
    return input("Enter the product to be searched on amazon: ")

# For scraping the products
def get_products(product_name: str) -> list:
    print(f"Searching for '{product_name}' on Amazon...")
    # Location to chrome driver
    options = Options()
    chrome_driver_dir = "/usr/bin/chromedriver"

    options.headless = any("--headless" in arg for arg in sys.argv)
    service = Service(chrome_driver_dir)
    global driver 
    driver = webdriver.Chrome(options=options, service=service)
    driver.get("https://amazon.in")

    # Waiting for browser to load amazon
    sleep(SLEEP_TIME)

    print(f"Scraping the results for {product_name}...")
    # Selecting search bar
    search_bar = driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')

    # Entering the search query to search bar
    search_bar.send_keys(product_name)

    # Searching the product by pressing "ENTER"
    search_bar.send_keys(Keys.ENTER)

    # Waiting for products to be loaded
    sleep(SLEEP_TIME)

    # Assigning the search results
    search_results = driver.find_elements(By.XPATH, "//*[@data-component-type='s-search-result']")

    # List to store dictionary of product details
    products = []
    for result in search_results:
        try:
            # Get the actual price of the product
            actual_price = result.find_element(By.CSS_SELECTOR, "span.a-price.a-text-price > span.a-offscreen").get_attribute("textContent")
        except Exception as e:
            # Product is not available as price is not present
            continue
        link = result.find_element(By.CLASS_NAME, "a-link-normal").get_attribute("href")
        title = result.find_element(By.CLASS_NAME, "a-text-normal").get_attribute("textContent")
        image = result.find_element(By.CLASS_NAME, "s-image").get_attribute("src");
        try:
            # Get discounted price for the product
            discounted_price = result.find_element(By.CLASS_NAME, "a-offscreen").get_attribute("textContent")
        except Exception as e:
            # Product has no discount so discount is set as 0
            discounted_price = "0"
        # Dictionary to store the details of a single product
        product = {
            "link": link,
            "title": title,
            "actual_price": actual_price,
            "discounted_price": discounted_price,
            "image": image
        }
        products.append(product)
    print(f"{len(products)} results found")
    return products

# To save the file in CSV and JSON Format
def save_file(product_name: str, products: list):
    # Save in CSV Format
    if not any("--no-csv" in arg for arg in sys.argv):
        print(f"Saving the CSV File as {product_name}.csv...", end="")
        csv_file = open(f"./{product_name}.csv", "w")
        writer = csv.writer(csv_file)
        writer.writerow(["URL", "Name", "Actual Price", "Discounted Price", "Image URL"])
        for product in products:
            writer.writerow(product.values())
        print("Done!")
    if not any("--no-json" in arg for arg in sys.argv):
        print(f"Saving the JSON File as {product_name}.json...", end="")
        # Save in JSON Format
        json_file = open(f"./{product_name}.json", "w")
        json_file.write(json.dumps(products, indent=2))
        print("Done!")


# Get product name from the CLI else ask for product name
def get_product_name_from_cli(substrings: list) -> str:
    try:
        for s in sys.argv:
            for substring in substrings:
                if substring in s:
                    return s.split("=")[1]
        # Fallback
    except Exception:
        print("Format for entering the product is wrong.")
        return get_product_name()

# To display all the available flags in command line
def show_commands():
    print("-----------------------------------------------------------------------------------------")
    print("Available script arguments")
    print('1. --product="PRODUCT_NAME" or -p="PRODUCT_NAME": Enter product name directly as argument')
    print("2. --headless: To run the script in headless mode")
    print("3. --no-csv: To not save as CSV by default would save as CSV")
    print("4. --no-json: To not save as JSON by default would save as JSON")
    print("-----------------------------------------------------------------------------------------")

def main():
    try:
        product = ""
        # Checking if the product name is given in argument
        if any("--product" in arg for arg in sys.argv) or any("-p" in arg for arg in sys.argv):
            product = get_product_name_from_cli(["--product", "-p"])
        else:
            show_commands()
            # Loop just to handle invalid condition
            while True:
                product = get_product_name()
                if len(product) == 0:
                    print("Product name should be atleast 1 character long!")
                else:
                    # Break when the product name length is greater than 0
                    break
        # Fetching products
        products = get_products(product)
        # Saving products
        save_file(product, products)
        if not any("--no-csv" in arg for arg in sys.argv) or not any("--no-json" in arg for arg in sys.argv):
            print(f"Access the scraped files from the directory {sys.path[0]}")
    except Exception as e:
        print(e)
if __name__ == "__main__":
    main()