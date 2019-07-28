import datetime
import json

import requests


def get_list_id_vacancies(date_from, date_to, **kwargs):
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
    params = {}
    date_from_datetime_real = datetime.datetime.fromisoformat(date_from)
    day_15 = datetime.timedelta(days=15)
    now = datetime.datetime.now()
    cursor_date = now-day_15
    cursor_date_iso = cursor_date.isoformat().split("T")[0]
    while cursor_date > date_from_datetime_real:
        for key, val in kwargs.items():
            params[key] = val
        params['date_from'] = cursor_date_iso
        r = requests.get(url_list, params=params)
        found = json.loads(r.text)['found'] #кол-во всего найденных вакансий

        if found <= 100: # API не отдает больше 100 вакансий за раз (на странице). Если найденно меньше 100 то получим все  сразу.
            params['per_page'] = found
            r = requests.get(url_list, params=params)
            data = json.loads(r.text)['items']
            for vac in data:
                list_id.append(vac['id'])
        else:
            all_pages = found//100 + 1
            i = 0
            while i <= all_pages: # если больше 100 то "перелистываем" страницы с 0 по all_pages и получаем все вакансии
                # поочереди. API не отдаст вам больше 2000 вакансий, поэтому ищем по месяцам.
                params['per_page'] = 100
                params['page'] = i
                r = requests.get(url_list, params=params)
                if 200 != r.status_code:
                    break
                data = json.loads(r.text)['items']
                for vac in data:
                    list_id.append(vac['id'])
                i += 1
        params.pop('per_page', None)
        params.pop('page', None)
        params['date_to'] = cursor_date_iso
        cursor_date = cursor_date - day_15
        cursor_date_iso = cursor_date.isoformat().split("T")[0]

    return list_id


def get_vacancy(id):
    """

    :param id: number of vacancy
    :return: full info about vacancy
    """

    url_vac = 'https://api.hh.ru/vacancies/%s'
    r = requests.get(url_vac % id)

    return json.loads(r.text)


def parse_vacancy(vacancy):
    """
    :param vacancy:
    :type vacancy: dict
    :return: Dict with parsed vacancy
    :rtype: dict
    """
    # vacancy_dict = vacancy['vacancy']
    parsed_vacancy = dict()
    # В тупле далее первое - бд, второе - как на сайте
    # !!! в duty лежит описание
    parameters = [
        ('site_id', 'id'),
        ('name', 'name'),
        ('salary_min', 'salary[from]'),
        ('salary_max', 'salary[to]'),
        ('employment', 'employment'),
        ('duty', 'description'),
        ('created_at', 'created_at')
    ]
    for model_parameter_name, api_parameter_name in parameters:
        if model_parameter_name == 'salary_min':
            salary_min = vacancy.get('salary', None)
            if salary_min is not None:
                salary_min = salary_min['from']
            else:
                salary_min = 0
            parsed_vacancy[model_parameter_name] = salary_min
        elif model_parameter_name == 'salary_max':
            salary_max = vacancy.get('salary', None)
            if salary_max is not None:
                salary_max = salary_max['to']
            else:
                salary_max = 0
            parsed_vacancy[model_parameter_name] = salary_max
        else:
            parsed_vacancy[model_parameter_name] = vacancy.get(api_parameter_name, None)
    requirement = vacancy.get('requirement', None)
    parsed_vacancy['qualification'] = None
    # if requirement is not None:
    #     parsed_vacancy['qualification'] = requirement.get('qualification')
    specializations = vacancy.get('specializations')
    if specializations is not None:
        spec_string = ''
        for spec in specializations:
            spec_string+=spec['name']+','
            last_spec = spec
        spec_string+=last_spec['profarea_name']
        parsed_vacancy['specialisation'] = spec_string
    return parsed_vacancy

