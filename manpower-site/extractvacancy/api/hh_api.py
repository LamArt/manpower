import json

import requests


def get_list_id_vacancies(area, text):
    """
    Send get request to url whit params
    Ищет area только по name (надо изменить search_field)
    :param url: Url of api server
    :type url: str
    :param params: Response params
    :type params: dict
    :return: Http response
    :rtype: requests.models.Response
    """
    url_list = 'https://api.hh.ru/vacancies'
    list_id = []
    params = {'text': text, 'area': area}
    r = requests.get(url_list, params=params)
    found = json.loads(r.text)['found'] #кол-во всего найденных вакансий

    if found <= 500: # API не отдает больше 500 вакансий за раз (на странице). Если найденно меньше 500 то получим все  сразу.
        params['per_page'] = found
        r = requests.get(url_list, params=params)
        data = json.loads(r.text)['items']
        for vac in data:
            list_id.append(vac['id'])
    else:
        i = 0
        while i <= 3: # если больше 500 то "перелистываем" страницы с 0 по 3 и получаем все вакансии поочереди. API не отдаст вам больше 2000 вакансий, поэтому тут захардкожено 3.
            params['per_page'] = 500
            params['page'] = i
            r = requests.get(url_list, params=params)
            if 200 != r.status_code:
                break
            data = json.loads(r.text)['items']
            for vac in data:
                list_id.append(vac['id'])
            i += 1

    return list_id


def get_vacancy(id):
    """

    :param id: number of vacancy
    :return: full info about vacancy
    """

    url_vac = 'https://api.hh.ru/vacancies/%s'
    r = requests.get(url_vac % id)

    return json.loads(r.text)


buff = get_list_id_vacancies(1261, 'django')
id_vac = buff[0]
buff_vac = get_vacancy(id_vac)
buff1 = buff_vac
