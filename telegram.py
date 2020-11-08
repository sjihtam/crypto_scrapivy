import os
import requests

def ip_addr():
    ip = os.popen("curl 'https://api.ipify.org?format=json'").read()
    return ip


def telegram_bot_sendtext(bot_message):
    
    bot_token = '1033876640:AAFU2TCvM0Ol5145QdkU-EWXUxclQiQdpfA'
    bot_chatID = '832555466'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    daan = "hey daann"
    return response.json()

test = telegram_bot_sendtext(ip_addr())

print(test)

# token : 1033876640:AAFU2TCvM0Ol5145QdkU-EWXUxclQiQdpfA
# chat_id: 	832555466
