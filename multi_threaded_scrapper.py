import threading
import urllib.request
from bs4 import BeautifulSoup
import time
import csv
import queue

# Read portfolio file and build initial value of portfolio

holding = []
with open('portfolio.csv', 'r') as f:
    rows = csv.reader(f)
    headers = next(rows)
    for row in rows:
        row[1] = int(row[1])
        row[2] = float(row[2])
        record = dict(zip(headers, row))
        holding.append(record)

portfolio_value_2017 = 0.0

for record in holding:
    portfolio_value_2017 += record["shares"] * record["price"]

print('Portfolio value at the end of year 2017 was USD {:.0f}'.format(portfolio_value_2017), '\n')

# Setup web crawler to read latest stock price from yahoo finance
que = queue.Queue()

def get_latest_price(stock, *args):
    url = 'https://ca.finance.yahoo.com/quote/{}'.format(stock)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')
    current_price = float(soup.find("div", {"class": "My(6px) smartphone_Mt(15px)"}).text.split("-")[0].replace(",", ""))
    que.put(current_price)
    return current_price

# Find out current portfolio value WITHOUT threading:
without_threading_portfolio_value_today = 0.0
without_threading_start_time = time.time()
for symbol in holding:
    without_threading_portfolio_value_today += symbol["shares"]*get_latest_price(symbol["name"])
print('WITHOUT THREADING:')
print('Current value of portfolio is USD {:.0f}'.format(without_threading_portfolio_value_today))
print('Time took WITHOUT threading: {:.2F}'.format(time.time()-without_threading_start_time), '\n')

# Find out current portfolio value WITH threading:
with_threading_portfolio_value_today = 0.0
with_threading_start_time = time.time()
list_of_threads = {}

for symbol in holding:
    each_thread = threading.Thread(target=get_latest_price, args=(symbol["name"], que))
    each_thread.start()
    list_of_threads[symbol["shares"]] = each_thread

for shares, process in list_of_threads.items():
    process.join()
    current_price = que.get()
    with_threading_portfolio_value_today += shares * current_price

print('WITH THREADING:')
print('Current value of portfolio is USD {:.0f}'.format(with_threading_portfolio_value_today))   
print('Time took WITH threading: {:.2F}'.format(time.time()-with_threading_start_time))
