from copyreg import dispatch_table

import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime, time
import json
import time

def get_source_page(url: str | None = None) :
    if url is None :
        raise ValueError("enter url adress")

    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}
    request = requests.get(url=url,headers=headers)

    soup = BeautifulSoup(request.text,'lxml')
    return soup

def parse_page(soup: BeautifulSoup) -> str | dict:
    all_trains_blocks = soup.find_all('div', class_='sch-table__row')[1:]
    result_dict = {}

    for block in all_trains_blocks:
        train_id = block.get("data-train-number")

        dispatch_time = block.find('div', class_='sch-table__time train-from-time').text.strip()
        dispatch_time = datetime.strptime(dispatch_time,'%H:%M')

        arrive_time = block.find('div', class_='sch-table__time train-to-time').text.strip()
        arrive_time = datetime.strptime(arrive_time, '%H:%M')

        seats_identify = float(block.find('div',class_='sch-table__tickets').get('data-value'))  #if number > 0 that mean tickets appear
        seats_info = []
        if seats_identify > 0:
            seats = block.find('div', class_='sch-table__cell cell-4').find_all('div', class_='sch-table__t-item has-quant')
            for seat in seats:
                amount = int(seat.find('a',class_='sch-table__t-quant js-train-modal dash').find('span').text)
                price = float(seat.find('div',class_='sch-table__t-cost').find('div',class_='ticket-wrap').find('span',class_='ticket-cost').text.replace(',','.'))
                seats_info.append([amount, price])

        result = {
            'dispatch_time': dispatch_time,
            'arrive_time': arrive_time,
            'seats_info': seats_info
        }
        result_dict[train_id] = result

    return result_dict






    # print(all_trains_blocks)
    # print(len(all_trains_blocks))
    # print(all_trains_blocks[0])
    # print(all_trains_blocks[-1])

def store_to_file(data):
    print('запись в json')
    def datetime_processing(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

    with open(f'result_in_json.json', 'w',encoding='utf-8') as file:
        json.dump(data, file,default=datetime_processing,ensure_ascii=False,indent=4)



def read_from_json():
    with open('result_in_json.json', 'r', encoding='utf-8') as file:
        data_from_json = json.load(file)
        for key in data_from_json.keys():
            data_from_json[key]['arrive_time'] = datetime.strptime(data_from_json[key]['arrive_time'],
                                                                   '%Y-%m-%d %H:%M:%S')
            data_from_json[key]['dispatch_time'] = datetime.strptime(data_from_json[key]['dispatch_time'],
                                                                     '%Y-%m-%d %H:%M:%S')
    return data_from_json


def main():
    data = get_source_page(url='https://pass.rw.by/ru/route/?from=%D0%91%D0%B5%D1%80%D1%91%D0%B7%D0%B0&from_exp=2100003&from_esr=134116&to=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA&to_exp=2100000&to_esr=140210&front_date=10+%D0%BD%D0%BE%D1%8F.+2024&date=2024-11-10')
    data_from_json = read_from_json()

    changes = []
    while True:
        train_info = parse_page(data)
        if train_info != data_from_json:
            for key in data_from_json.keys():
                if data_from_json[key]['seats_info'] != train_info[key]['seats_info']:
                    print(f'Были найдены изменения в местах: Было -----> {data_from_json[key]["seats_info"]} \n Стало ------> {train_info[key]["seats_info"]}')
                    if len(data_from_json[key]["seats_info"]) < len(train_info[key]["seats_info"]):
                        print("Были добавлены билеты")
                    changes.append(f'{key}:::{data_from_json[key]["seats_info"]} ------> {train_info[key]["seats_info"]} {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                    store_to_file(train_info)


        for key in data_from_json.keys():
            if train_info[key]['seats_info']:
                print(f"Доступны места на поезд в {train_info[key]['dispatch_time']} \n https://pass.rw.by/ru/route/?from=%D0%91%D0%B5%D1%80%D1%91%D0%B7%D0%B0&from_exp=2100003&from_esr=134116&to=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA&to_exp=2100000&to_esr=140210&front_date=10+%D0%BD%D0%BE%D1%8F.+2024&date=2024-11-10",end='\n\n\n')


        time.sleep(10)


if __name__ == '__main__':
    main()