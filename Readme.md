## Installation Steps:

1. Download and install [Python](https://python.org/downloads) from here based on your operating system. I have used **Python v3.8.10** for this.

2. Clone the repository

   ```sh
   git clone https://github.com/AbhinavRajesh/Amazon-Scraper.git amazon-scraper

   cd amazon-scraper
   ```

3. Creating Virtual Environment: It’s always a best practice to create a virtual environment for each project. Run the following command to create and activate the virtual environment

   ```sh
   # Linux
   python3 -m venv env
   source env/bin/activate

   # Windows
   py -3 -m venv env
   env\Scripts\activate
   ```

4. Install Selenium using the following command

   ```sh
   # Linux
   pip3 install selenium

   #Windows
   pip install selenium
   ```

5. Download Chrome Driver: Download Chrome Driver using this [link](https://chromedriver.chromium.org/downloads) based on your chrome version.

## Usage

The flags supported by the script

| Flags           | Description                                                | Usage                             |
| --------------- | ---------------------------------------------------------- | --------------------------------- |
| -p or --product | To get the product name from CLI                           | --product=”iphone” Or -p=”iphone” |
| --headless      | To run the script in headless mode so no browser is opened | --headless                        |
| --no-csv        | To not save the scraped data as CSV file                   | --no-csv                          |
| --no-json       | To save the scraped data as JSON file                      | --no-json                         |

To run the script, run the following command

```sh
# Linux
python3 main.py --product="apple macbook"

# Windows
py main.py --product="apple macbook"
```

This opens the browser, goes to https://amazon.in, inserts the text “apple macbook” inside the search bar and searches for the product. The product results are then scraped and saved in CSV and JSON files inside the directory with the name “apple macbook.csv” and “apple macbook.json” files respectively.
