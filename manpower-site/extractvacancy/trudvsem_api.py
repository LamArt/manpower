import requests

from extractvacancy.models import Vacancy


def send_request(url, params):
    """
    Send get request to url whit params, parse request to json and check, that status in response json equals to 200.
    :param url: Url of api server
    :type url: str
    :param params: Response params
    :type params: dict
    :return: Http response
    :rtype: requests.models.Response
    """
    response = requests.get(url, params)
    response_json = response.json()
    if response_json['status'] != '200':
        raise RuntimeError
    return response


def download_vacancy_one_page(url, params):
    """
    Download one page of vacancies from vsemtrud api and parse it to list of jsons
    :param url: URL of api server
    :type url: str
    :param params: requests parameters
    :type params: dict
    :return: List of vacancies
    :rtype: list of dict
    """
    response = send_request(url, params)
    response_json = response.json()
    vacancies = response_json['results']['vacancies']

    return vacancies


def download_all_available_pages(url, params):
    """
    Download all available page with vacancies from vsemtrud api. If number of vacancies greater then 10000, download
    only first 10000  because of restriction of api.
    :param url: Url of api server
    :type url: str
    :param params: requests parameters
    :type params: dict
    :return: List of vacancies
    :rtype: list of dict
    """
    local_params = params.copy()
    LIMIT = 100
    local_params['limit'] = LIMIT
    local_params['offset'] = 0

    all_vacancies = []
    total_number_of_pages = 100
    first_response = send_request(url, local_params)
    response_json = first_response.json()
    number_of_vacancies = int(response_json['meta']['total'])
    if number_of_vacancies < 10000:
        total_number_of_pages = number_of_vacancies // LIMIT
    all_vacancies += response_json['results']['vacancies']
    for i in range(1, total_number_of_pages):
        print(i)
        local_params['offset'] = i
        all_vacancies += download_vacancy_one_page(url, local_params)
    return all_vacancies


def parse_vacancy(vacancy):
    """

    :param vacancy:
    :type vacancy: dict
    :return: Dict with parsed vacancy
    :rtype: dict
    """
    vacancy_dict = vacancy['vacancy']
    parsed_vacancy = dict()
    parameters = [
        ('site_id', 'id'),
        ('name', 'job-name'),
        ('salary_min', 'salary_min'),
        ('salary_max', 'salary_max'),
        ('employment', 'employment'),
        ('duty', 'duty'),
    ]

    for model_parameter_name, api_parameter_name in parameters:
        parsed_vacancy[model_parameter_name] = vacancy_dict.get(api_parameter_name, None)
    requirement = vacancy_dict.get('requirement', None)
    parsed_vacancy['specialisation'] = None
    parsed_vacancy['qualification'] = None
    if requirement is not None:
        parsed_vacancy['qualification'] = requirement.get('qualification')
    category = vacancy_dict.get('category', None)
    if category is not None:
        parsed_vacancy['specialisation'] = category.get('specialisation')

    return parsed_vacancy


