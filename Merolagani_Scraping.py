import csv

import requests
from bs4 import BeautifulSoup

try:
    response = requests.get('https://merolagani.com/StockQuote.aspx').text
    stock_content = BeautifulSoup(response, 'lxml')

    # table containing all stock price details
    table = stock_content.find('table', class_='table table-bordered table-striped table-hover sortable')

    # table contains thead and tbody
    # getting all table head rows to obtain title of table
    table_head = table.find('thead').find_all('tr')
    for head in table_head:
        # titles of table content
        titles = head.text.split('\n')
        # removing empty strings
        updated_title_list = [i for i in titles if i != ""]
        # adding link to title_list to store link of companies
        updated_title_list.append('link')

        # writing headings to csv file
        with open('merolagani_scrape.csv', 'w') as f:
            # creating csv writer object
            csv_writer = csv.writer(f)
            # adding header which is titles for scraped data
            csv_writer.writerow(updated_title_list)

    # remaining rows which contains data
    table_rows = table.find('tbody').find_all('tr')
    for row in table_rows:
        # getting each row data
        each_row = row.text.split()

        # getting link of each row
        a_tag = row.find('a')
        # changing to string to apply split method
        a_tag = str(a_tag)

        # splitting a_tag content to get link
        split_tag = a_tag.split()[1].split('"')
        # just getting the link for viewing company details
        company_link = split_tag[1]
        # adding website name for the complete link
        full_link = f"merolagani.com{company_link}"

        # appending row data we get with link for company details
        each_row.append(full_link)

        # finally appending the scraped data to csv file
        with open('merolagani_scrape.csv', 'a') as f:
            # creating csv writer object
            csv_writer = csv.writer(f)
            # writing the row data along with the link to each row of csv file
            csv_writer.writerow(each_row)
except Exception as e:
    print(e)

my_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS \
                            X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) \
                            Chrome/71.0.3578.98 Safari/537.36",
              "Accept": "text/html,application/xhtml+xml,application/xml; \
                        q=0.9,image/webp,image/apng,*/*;q=0.8"}
