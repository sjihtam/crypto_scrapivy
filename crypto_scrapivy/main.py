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
        try:
            temp = transaction_scraper()
            print("Old hash: " + recent_tx + "\n" + "New hash: " + temp)
        except:
            print("Could not fetch data\n")
        if (recent_tx != temp):
            print("Found new transaction!\n")
            try:
                msg = transaction_detail_scraper(temp)
                telegram = telegram_bot_sendtext(msg, temp)
                print("Following data was send: \n")
                print(telegram)
            except:
                print("Could not send data over telegram api\n")
        recent_tx = temp
        time.sleep(60)

def transaction_scraper():
    source = requests.get(page, headers=headers)
    soup = BeautifulSoup(source.content, 'html.parser')
    recent_transaction_url_raw = str(soup.select(".myFnExpandBox_searchVal")[0])
    recent_transaction_url_stripped = recent_transaction_url_raw.split('"')[3]
    return recent_transaction_url_stripped

def transaction_detail_scraper(transaction_url):
    #transaction_url = "/tx/0xd85247233f3b91faafe2e9cc320ba84f1671571c47132893205645b9466cfcbb" # niet succesvol
    #transaction_url = "/tx/0xc105f1f938fc3e89b0ec549b0005714e8fc95fc276eaa3af0f73e6bddb559349" # wel succesvol
    page = "https://etherscan.io{}".format(transaction_url)
    source = requests.get(page, headers=headers)
    soup = BeautifulSoup(source.content, 'html.parser')
    try:
        Token_from = str(soup.select("a.d-inline-block , .d-inline-block:nth-child(7)")[0]).split(">")[1].split("<")[0]
        Token_from_amount = str(soup.select(".d-inline-block:nth-child(2)")[1]).split(">")[1].split("<")[0]
        Token_to = str(soup.select(".d-inline-block:nth-child(7)")[0]).split(">")[1].split("<")[0]
        Token_to_amount = str(soup.select(".d-inline-block~ .text-secondary+ .d-inline-block")[0]).split(">")[1].split("<")[0]
        info = Token_from_amount + "  " + Token_from + " > " + Token_to_amount + "  " + Token_to
        print(info)
        return info
    except:
        info = "Failed transaction"
        print(info)
        return info

#https://etherscan.io/tx/0xd64f38e6d5b0cc3cbe289761ed0ab0b610205c2a68c35fe800bc1f58451655b2

def telegram_bot_sendtext(bot_message, tx_hash):
    page = "https://etherscan.io{}".format(tx_hash)
    bot_message = 'New transaction: ' + bot_message + ' Link: ' + page
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    print(send_text)
    response = requests.get(send_text)
    return response.json()


main()
#transaction_detail_scraper("/tx/0xd64f38e6d5b0cc3cbe289761ed0ab0b610205c2a68c35fe800bc1f58451655b2")
