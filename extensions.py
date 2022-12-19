import requests
from lxml import etree
from config import currencies, api_path


class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = currencies[base]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена! Справка: /help')

        try:
            quote_key = currencies[quote]
        except KeyError:
            raise APIException(f'Валюта {quote} не найдена!')

        if base_key == quote_key:
            raise APIException(f'Вы переводите {base} в {quote}!')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        
        xml = requests.get(api_path).content
        root = etree.fromstring(xml)
        data = {
            el.attrib.values()[0]: (
                int(el[2].text),
                float(el[4].text.replace(',', '.')),
                el[1].text
                )
            for el in root
        }
        data['000000'] = (1, 1, 'RUB')
        
        base_data = data[currencies[base]]
        quote_data = data[currencies[quote]]
        quote_amount = round((base_data[1] / base_data[0]) * (quote_data[0] / quote_data[1]) * float(amount), 2)
        message = f'{amount} {base_data[2]} = {quote_amount} {quote_data[2]}'
        return message
        
        