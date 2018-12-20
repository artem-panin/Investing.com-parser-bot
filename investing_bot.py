from bs4 import BeautifulSoup
import requests
from time import sleep
from config import TOKEN, urls


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        results = self.get_updates()
        if len(results) > 0:      
            last_update = results[-1]
        else:
            last_update = None
        return last_update


def investing_parser(ticker):
    try:
        response = requests.get(urls[ticker], headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64) \
                                                                     AppleWebKit/537.36 (K HTML, like Gecko) \
                                                                     Chrome/53.0.2785.143 Safari/537.36"})
        soup = BeautifulSoup(response.content, "html.parser")
        value = soup.find('input', {'class': 'newInput inputTextBox alertValue'}).get('value')
        investing_price = round(float(value.replace(",", "")), 4)
        resp = '{} price: {} \n\nDownloaded from {}'.format(ticker, investing_price, urls[ticker])
    except KeyError:
        resp = "Please, append {}'s URL to config file.".format(ticker)
    return resp


def main():  
    investing_bot = BotHandler(TOKEN)
    new_offset = None
    while True:
        investing_bot.get_updates(new_offset)
        last_update = investing_bot.get_last_update()
        if last_update:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']
            response = investing_parser(last_chat_text)
            investing_bot.send_message(last_chat_id, '{}, \n\n{}'.format(last_chat_name, response))
            new_offset = last_update_id + 1
        sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
