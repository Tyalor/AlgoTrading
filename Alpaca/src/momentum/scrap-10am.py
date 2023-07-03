import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

url = 'https://www.barchart.com/options/most-active/stocks?orderBy=optionsTotalVolume&orderDir=desc&viewName=main'

while True:
    # Get current time
    now = datetime.now()

    # Check if it's 10 AM EST
    if now.hour == 10 and now.minute == 0 and now.second == 0:
        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML response
        soup = BeautifulSoup(response.content, 'html.parser')

        stock_universe = []

        # Find the table with the most active stock options
        table = soup.find('table', {'class': 'dataTable'})

        # Loop through the rows of the table
        for row in table.find_all('tr')[1:]:
            # Get the ticker symbol from the first column
            ticker = row.find_all('td')[0].text.strip()

            # Add the ticker symbol to the stock universe
            stock_universe.append(ticker)

        # Print the stock universe
        print(stock_universe)

    # Wait for 1 second before checking the time again
    time.sleep(1)
