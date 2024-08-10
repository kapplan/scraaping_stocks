import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

start_time = time.time()
pages = []

for page_number in range(1, 126):
    url_start = 'https://www.centralcharts.com/en/price-list-ranking/'
    url_end = 'ALL/asc/ts_19-us-nasdaq-stocks--qc_1-alphabetical-order?p='
    url = url_start + url_end + str(page_number)
    pages.append(url)

values_list = []
for page in pages:
    webpage = requests.get(page)
    soup = bs(webpage.text, 'html.parser')

    # Debug: Check if the page was loaded correctly
    if webpage.status_code != 200:
        print(f"Failed to retrieve page {page_number}: Status code {webpage.status_code}")
        continue

    stock_table = soup.find('table', class_='tabMini tabQuotes')
    if stock_table:
        tr_tag_list = stock_table.find_all('tr')
        for each_tr_tag in tr_tag_list[1:]:
            td_tag_list = each_tr_tag.find_all('td')
            row_values = []
            for each_td_tag in td_tag_list[0:7]:
                new_value = each_td_tag.text.strip()
                row_values.append(new_value)
            values_list.append(row_values)
    else:
        print(f"Table not found on page {page_number}")

# Define the columns for the DataFrame
columns = ['Company Name', 'Last Price', 'Change', 'Open', 'High', 'Low', 'Volume']

# Create a DataFrame from the list
df = pd.DataFrame(values_list, columns=columns)

# Export the DataFrame to an Excel file
df.to_excel('scraped_financial_data.xlsx', index=False)

print("Data has been exported to scraped_financial_data.xlsx")
print('--%s seconds ---' % (time.time() - start_time))

