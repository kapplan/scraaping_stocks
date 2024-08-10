import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

start_time = time.time()
pages = []
for page_number in range(1, 95):  # Assuming there are 200 pages
    base_url = 'https://www.capitoltrades.com/trades?pageSize=96&page='
    date_filter = '&txDate=365d'
    url = base_url + str(page_number) + date_filter
    pages.append(url)

values_list = []
for page_number, page in enumerate(pages, 1):
    webpage = requests.get(page)
    soup = bs(webpage.text, 'html.parser')

    # Debug: Check if the page was loaded correctly
    if webpage.status_code != 200:
        print(f"Failed to retrieve page {page_number}: Status code {webpage.status_code}")
        continue

    stock_table = soup.find('table', class_='q-table trades-table')
    if stock_table:
        tr_tag_list = stock_table.find_all('tr')
        for each_tr_tag in tr_tag_list:
            th_tag_list = each_tr_tag.find_all('th')  # Get all th tags within the tr
            td_tag_list = each_tr_tag.find_all('td')  # Get all td tags within the tr

            row_values = []

            if th_tag_list:  # If th tags are found, process them
                for each_th_tag in th_tag_list[:9]:  # Scrape only the first 9 columns
                    new_value = each_th_tag.text.strip()
                    row_values.append(new_value)
            elif td_tag_list:  # If td tags are found, process them
                for each_td_tag in td_tag_list[:9]:  # Scrape only the first 9 columns
                    new_value = each_td_tag.text.strip()
                    row_values.append(new_value)

            # Append row_values to values_list only if it's not empty
            if row_values:
                values_list.append(row_values)
    else:
        print(f"Table not found on page {page_number}")

# Print the results or save them to a file
for row in values_list:
    print(row)

# Define the columns for the DataFrame
columns = ['Politician', 'Traded Issuer', 'Published', 'Traded', 'Filed After', 'Owner', 'Type', 'Size', 'Price']

# Convert the list of values into a DataFrame
df = pd.DataFrame(values_list, columns=columns)

# Save the DataFrame to an Excel file
df.to_excel('capitol_trades_data.xlsx', index=False, header=False)

print("Data has been saved to capitol_trades_data.xlsx")

