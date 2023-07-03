import requests
from bs4 import BeautifulSoup

url = 'https://www.barchart.com/options/most-active/stocks?orderBy=optionsTotalVolume&orderDir=desc&viewName=main'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

stock_universe = []

# Find the table with the most active stock options
table = soup.find('table', {'class': 'dataTable'})

# Check if table was found
if table is not None:
    # Loop through the rows of the table
    for row in table.find_all('tr')[1:]:
        # Get the ticker symbol from the first column
        ticker = row.find_all('td')[0].text.strip()

        # Add the ticker symbol to the stock universe
        stock_universe.append(ticker)

print(stock_universe)
