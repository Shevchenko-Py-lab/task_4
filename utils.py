import requests

from decimal import Decimal
from datetime import date


def currency_rates(currency_code):
    # у меня долго не работал запуск из терминала потому что я вбивал 'USD'
    # а не USD, поэтому сделал такой вариант:
    currency_code = ("".join(c for c in currency_code if c.isalpha())).upper()
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp').text
    currency_index = response.find(currency_code)

    if currency_index == -1:
        return

    date_index = response.find("Date")

    currency_date = reversed(response[date_index + 6: date_index + 16].split('.'))
    year, month, day = (int(x) for x in currency_date)
    date_for_print = date(year, month, day)

    # не всегда цена за 1 единицу, поэтому добавлен nominal, оставил свои записи,
    # когда разбирал, как работает функция get_field
    nominal = get_field('Nominal>', response, currency_index)
    # nominal = response[response.find('<Nominal>', currency_index) + 9:
    #                   response.find('</', currency_index)]
    currency_price = get_field('Value>', response, currency_index)
    # currency_price = response[response.find('<Value>', currency_index) + 7 :
    #                          response.find('</', currency_index)]
    currency_name = get_field('Name>', response, currency_index)
    currency_price = currency_price.replace(',', '.')

    return f'На {date_for_print} {nominal} {currency_code} ({currency_name}) == ' \
           f'{Decimal(currency_price)} RUR'


def get_field(field_name, response, currency_index):
    value_start_index = response.find(
        field_name, currency_index
    ) + len(field_name)
    # print(value_start_index)
    value_end_index = response.find('</', value_start_index)
    # print(value_end_index)
    return response[value_start_index: value_end_index]


if __name__ == '__main__':
    from sys import argv
    _module_name, currency_code_arg = argv
    print(currency_rates(currency_code_arg))
