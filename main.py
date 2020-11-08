import requests
import os
import requests
import time
from bs4 import BeautifulSoup

bot_token = str(input("Please enter security token:")) 
bot_chatID = '832555466'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
page = "https://etherscan.io/address/0x66aeeadd49026a7cfbde0240a7b148f18966b7b7#tokentxns"
#change the page variable to a preffered address.

def main():
    print("init")
    recent_tx = ""
    while 1==1 :
        temp = transaction_scraper()
        print(temp)
        if (recent_tx != temp):
            msg = transaction_detail_scraper(temp)
            telegram = telegram_bot_sendtext(msg, temp)
            print(telegram)
        recent_tx = temp
        print(recent_tx)
        time.sleep(15)

def transaction_scraper():
    source = requests.get(page, headers=headers)
    soup = BeautifulSoup(source.content, 'html.parser')
    recent_transaction_url_raw = str(soup.select(".myFnExpandBox_searchVal")[0])
    recent_transaction_url_stripped = recent_transaction_url_raw.split('"')[3]
    return recent_transaction_url_stripped

def transaction_detail_scraper(transaction_url):
    page = "https://etherscan.io{}".format(transaction_url)
    source = requests.get(page, headers=headers)
    soup = BeautifulSoup(source.content, 'html.parser')
    transaction_details = soup.select(".mn-3:nth-child(13) .col-md-9")
    print(transaction_details)
    info = str(transaction_details[0])
    return info
#https://etherscan.io/tx/0xd64f38e6d5b0cc3cbe289761ed0ab0b610205c2a68c35fe800bc1f58451655b2

def telegram_bot_sendtext(bot_message, tx_hash):
    page = "https://etherscan.io{}".format(tx_hash)
    bot_message = 'New transaction: ' + bot_message + '\n Link: ' + page
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


main()
#transaction_detail_scraper("/tx/0xd64f38e6d5b0cc3cbe289761ed0ab0b610205c2a68c35fe800bc1f58451655b2")
