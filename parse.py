import grequests
import requests
from pprint import pp
import json
from time import perf_counter
from exel import create_xlsx
#import logging


DOMAIN = "https://api.hh.ru/"
HH_DOMAIN = "https://api.hh.ru/"
ACCESS_TOKEN = "R8CL8BSMREO9LF305P1A3L9NV8RI0LHVO2JQ4E7UA3IC8IFT27V0CP39N7LK1DOC"
REFRESH_TOKEN = "H88P8UDFR176597KK6PRU26S72SUJFL3IQHJIECSCC6758CEKP7MR7CB4TAAE9IJ"
#logging.basicConfig(filename="test.log", level=logging.DEBUG, format="%(message)s")
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}


class ParserStats:
    """
    При создании класса укажите домен, метод и параметры.
    params attrs: "text" , "area" , "professional_role"
    """
    ext = ".json"
    def __init__(self, domain: str="https://api.hh.ru/", url: str="vacancies", params: dict=None, data = None):
        self.domain = domain
        self.url = url
        self.params = params
        self.data = data

    
    def get_num_pages(self):
        result = requests.get(url=f"{self.domain}{self.url}?{'&'.join([key +'='+ val for key, val in self.params.items()])}")
        return int(result.json()['pages'])

    def parse_pages(self):
        page_list = [f"{self.domain}{self.url}?{'&'.join([key+'='+val+'&page='+str(i) for key, val in self.params.items()])}" for i in range(1, self.get_num_pages() + 1)]
        url_list = []
        resp = (grequests.get(page, headers=HEADERS) for page in page_list)
        result = grequests.map(resp)
        for res in result:
            url_list += [vac['url'] for vac in res.json()['items']]
        try:
            resp = (grequests.get(url, headers=HEADERS) for url in url_list)
        except Exception as ex:
            print(ex)
        else:
            result = grequests.map(resp)
            parsed_data = [res.json()['key_skills'] for res in result]
            data = {}
            for lst in parsed_data:
                for dct in lst:
                    if dct['name'].lower() in data.keys():
                        data[dct['name'].lower()] += 1
                    else:
                        data[dct['name'].lower()] = 1
            new_data = {}
            for key in data:
                if data[key] > 4:
                    new_data[key] = data[key]
            self.data = new_data
            return new_data

    def save_data_to_file(self, file_name: str):
        """
        Введите имя файла c расширением .json
        """
        try:
            with open(f"static/results/{file_name}", 'w', encoding="utf-8") as file:
                file.write(json.dumps(self.data))
        except Exception as ex:
            return ex
        else:
            return "Файл успешно добавлен!"
    
    def execute(self, file_name):
        self.parse_pages()
        self.save_data_to_file(file_name=file_name)
        return "Готово!"

class ParserTable:
    """
    При создании класса укажите домен, метод и параметры.
    params attrs: "text" , "area" 
    """
    ext = ".xlsx"
    def __init__(self, domain: str="https://api.hh.ru/", url: str="vacancies", params: dict=None, pages=None, data = None):
        self.domain = domain
        self.url = url
        self.params = params
        self.data = data
        if pages == None:
            self.pages = self.get_num_pages()
        else:
            self.pages = pages

    
    def get_num_pages(self):
        result = requests.get(url=f"{self.domain}{self.url}?{'&'.join([key +'='+ val for key, val in self.params.items()])}")
        return int(result.json()['pages'])

    def parse_pages(self):
        page_list = [f"{self.domain}{self.url}?{'&'.join([key+'='+val for key, val in self.params.items()])}&page={str(i)}" for i in range(1, self.pages + 1)]
        print(self.pages)
        print(page_list)
        resp = (grequests.get(page, headers=HEADERS) for page in page_list)
        result = grequests.map(resp)
        print(result)
        parsed_data =[]
        [parsed_data.extend(res.json()['items']) if 'items' in res.json() else print(res.json()) for res in result]
        
        self.data = parsed_data
        return parsed_data

    def filter_data(self, params: list):
        
        for param in params:
            if param in ['area', 'salary', 'address', 'employer', 'snippet', 'contacts', 'schedule', 'professional_roles']:
                if param == 'area':
                    lst = [vac[param]['name'] for vac in self.data]
                elif param == 'salary':
                    lst = [f"От - {vac[param]['from']} до - {vac[param]['to']}. {vac[param]['currency']}" if vac[param] is not None else "Не указанно!" for vac in self.data]
                elif param == 'address':
                    lst = [vac[param]['raw'] if vac[param] is not None else "Не указанно!" for vac in self.data]
                elif param == 'employer':
                    lst = [f"{vac[param]['name']}\n{vac[param]['alternate_url']}" if 'alternate_url' in vac[param] else str(vac[param]) for vac in self.data]
                elif param == 'snippet':
                    lst = [f"Требования: {vac[param]['requirement']}\nОбязанности: {vac[param]['responsibility']}" for vac in self.data]
                elif param == 'contacts':
                    lst = [str(vac[param]) if vac[param] is not None else "Не указанно!" for vac in self.data]
                elif param == 'contacts':
                    lst = [f"{vac[param]['name']}\n{vac[param]['email']}\n{vac[param]['phones'][0]['formatted']}" for vac in self.data]
                elif param == 'schedule':
                    lst = [vac[param]['name'] for vac in self.data]
                elif param == 'professional_roles':
                    lst = [vac[param][0]['name'] for vac in self.data]
            else:
                lst = [vac[param] for vac in self.data]
            yield param, lst
    
    

    def save_data_to_file(self, data: dict, file_name: str):
        """
        file_name: str 
        Введите имя файла .xlsx
        """
        
        try:
            create_xlsx(data=data, file_name=file_name)
        except Exception as ex:
            print(ex)
        else:
            return "Файл успешно добавлен!"
    
    def execute(self, params: list, file_name: str):
        """
        params: list
        file_name: str

        Парсит, фильтрует а затем сохраняет данные в файл
        """

        self.parse_pages()
        data = dict(self.filter_data(params=params))
        self.save_data_to_file(data=data, file_name=file_name)
        return "Готово!"
    

hh = ParserStats(HH_DOMAIN, url="vacancies", params={
    "text": "python",
    "area": "2", #Санкт-Петербург
    "professional_role": "96" #Программист-разработчик
    })

hh_u = ParserTable(HH_DOMAIN, url="vacancies", pages=1, params={
    "text": "Юрист",
    "area": "2", #Санкт-Петербург
    "industry": "44"
    })



if __name__ == "__main__":
    start = perf_counter()
    #print(hh_u.execute(file_name="Bitrix"))
    # pp(a:=requests.get(f"{DOMAIN}vacancies", params={
    # "text": "python",
    # "area": "2", #Санкт-Петербург
    # "professional_role": "96" #Программист-разработчик
    # }, headers=HEADERS).json()['items'][0])
    # print(a.keys())
    # hh.execute("pizda.json")
    print(list(hh_u.parse_pages()))
    print(dict(hh_u.filter_data(params=['employer'])))
    print(f"Время выполнения: {(perf_counter() - start):.03f}")
