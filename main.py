from copyreg import dispatch_table

import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime, time


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

    for block in all_trains_blocks[0:1]:
        train_id = block.get("data-train-number")
        print(train_id)

        dispatch_time = block.find('div', class_='sch-table__time train-from-time').text.strip()
        dispatch_time = datetime.strptime(dispatch_time,'%H:%M')
        print(dispatch_time)

        arrive_time = block.find('div', class_='sch-table__time train-to-time').text.strip()
        arrive_time = datetime.strptime(dispatch_time, '%H:%M')
        print(arrive_time)

    # print(all_trains_blocks)
    # print(len(all_trains_blocks))
    # print(all_trains_blocks[0])
    # print(all_trains_blocks[-1])


def main():
    data = get_source_page(url='https://pass.rw.by/ru/route/?from=%D0%91%D0%B5%D1%80%D1%91%D0%B7%D0%B0+&from_exp=0&from_esr=0&to=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA&to_exp=2100000&to_esr=140210&date=2024-11-10&type=1')
    parse_page(data)


if __name__ == '__main__':
    main()