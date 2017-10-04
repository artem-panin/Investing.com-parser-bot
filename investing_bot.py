from bs4 import BeautifulSoup
import requests
import time

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

    url_dict = {'GAZP' : 'https://www.investing.com/equities/gazprom?cid=32732',
            'LKOD' : 'https://www.investing.com/equities/nk-lukoil-oao?cid=48436', 
            'ROSN' : 'https://www.investing.com/equities/rosneft?cid=48483',
            'NVTK' : 'https://www.investing.com/equities/novatek-gdr?cid=48475',
            'SGGD' : 'https://www.investing.com/equities/surgutneftegaz?cid=48477',
            'USDRUB' : 'https://www.investing.com/currencies/usd-rub',
            'LCO' : 'https://www.investing.com/commodities/brent-oil',
            'EU50' : 'https://www.investing.com/indices/eu-stoxx50',
            'USDNOK' : 'https://www.investing.com/currencies/usd-nok',
            'EURUSD' : 'https://www.investing.com/currencies/eur-usd',
            'OBX' : 'https://www.investing.com/indices/oslo-obx',
            'BHP' : 'https://www.investing.com/equities/bhp-billiton-ltd-nyse-exch',
            'MNOD' : 'https://www.investing.com/equities/jsc-mmc-norilsk-nickel?cid=48470',
            'PL1' : 'https://www.investing.com/commodities/platinum',
            'RSX' : 'https://www.investing.com/etfs/marketvectors-tr-russia',
            'RTS' : 'https://www.investing.com/indices/rtsi',
            'CLR' : 'https://www.investing.com/equities/continental-resources-inc',
            'DVN' : 'https://www.investing.com/equities/devon-energy', 
            'MRO' : 'https://www.investing.com/equities/marathon-oil',
            'EOG' : 'https://www.investing.com/equities/eog-resources',
            'WLL' : 'https://www.investing.com/equities/whiting-petroleum-corp', 
            'SM1' : 'https://www.investing.com/indices/switzerland-20',
            'USDCHF' : 'https://www.investing.com/currencies/usd-chf',
            'CHL' : 'https://www.investing.com/equities/china-mobile-limited-exch',
            'T' : 'https://www.investing.com/equities/at-t', 
            'VOD' : 'https://www.investing.com/equities/vodafone-group-plc-exch',
            'AMX' : 'https://www.investing.com/equities/america-movil',
            'SP1' : 'https://www.investing.com/indices/us-spx-500', 
            'IYZ' : 'https://www.investing.com/etfs/ishares-djsu-telecommunications',
            'DM1' : 'https://www.investing.com/indices/us-30-futures',
            'DX1' : 'https://www.investing.com/quotes/us-dollar-index', 
            'UX1' : 'https://www.investing.com/indices/us-spx-vix-futures',
            'EWA' : 'https://www.investing.com/etfs/ishares-msci-australia-index',
            'EWC' : 'https://www.investing.com/etfs/ishares-msci-canada', 
            'AUDCAD' : 'https://www.investing.com/currencies/aud-cad',
            'USDCAD' : 'https://www.investing.com/currencies/usd-cad',
            'AUDUSD' : 'https://www.investing.com/currencies/aud-usd',
            'EZU' : 'https://www.investing.com/etfs/ishares-msci-emu', 
            'EURCAD' : 'https://www.investing.com/currencies/eur-cad',
            'EURUSD' : 'https://www.investing.com/currencies/eur-usd',
            'EWU' : 'https://www.investing.com/etfs/ishares-msci-uk',
            'EURGBP' : 'https://www.investing.com/currencies/eur-gbp',
            'GBPUSD' : 'https://www.investing.com/currencies/gbp-usd',
            'XME' : 'https://www.investing.com/etfs/spdr-s-p-metals---mining',
            'PL1' :  'https://www.investing.com/commodities/platinum',
            'HG1' : 'https://www.investing.com/commodities/copper'}

    try:
        response = requests.get(url_dict[ticker], headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (K HTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"})
        soup = BeautifulSoup(response.content, "html.parser")
        value = soup.find('input', {'class':'newInput inputTextBox alertValue'}).get('value')
        investing_price = round(float(value.replace(",", "")), 4)
        resp =  '{} price: {} \n\nDownloaded from {}'.format(ticker, investing_price, url_dict[ticker])
    except KeyError:
        resp =  'Investing.com doesnt contain current prices of {} asset. Please, use other source.'.format(ticker)
    return resp

def main():  
    investing_bot = BotHandler('394461543:AAFG-QxI56h5guRboUMyrSeHXPRt551R2FA')  
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
        time.sleep(1)

if __name__ == '__main__':  

    try:
        main()
    except KeyboardInterrupt:
        exit()
