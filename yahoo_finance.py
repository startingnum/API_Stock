import csv
import time
from datetime import datetime
import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError


def get_data():
    global old_time, now_time, old_price, now_price, change_rate, data_volume, corona_date , corona_price, corona_time ,corona_rate
    my_share = share.Share(row_str + '.T')
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_YEAR, 20, share.FREQUENCY_TYPE_MONTH, 1)
        #time.sleep(1)
        date = symbol_data["timestamp"]
        old_date = date[0]
        now_date = date[-1]
        corona_date = date[-6]
        old_time = datetime.utcfromtimestamp(old_date / 1000)
        now_time = datetime.utcfromtimestamp(now_date / 1000)
        corona_time = datetime.utcfromtimestamp(corona_date / 1000)
        price = symbol_data["close"]
        old_price = price[0]
        now_price = price[-1]
        corona_price = price[-6]
        change_rate = '{:.2f}'.format(now_price / old_price)
        corona_rate = '{:.2f}'.format(corona_price / old_price)
        data_volume = len(date)
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)

def write_csv():
    with open("225PriceData.csv", "a", newline="") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([row_str, data_volume, old_time, old_price, now_time, now_price, change_rate,corona_time,corona_price,corona_rate])

count = 1
csvfile = "225.csv"
with open(csvfile, "r") as f:
    rows = csv.reader(f)
    for row in rows:
        print("ループ回数：" + str(count))
        row_str = str("".join(row))

        get_data()
        write_csv()
        count = count + 1
