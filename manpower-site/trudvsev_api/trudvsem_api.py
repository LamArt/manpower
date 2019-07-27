import requests


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
        total_number_of_pages = number_of_vacancies//LIMIT
    all_vacancies += response_json['results']['vacancies']
    for i in range(1, total_number_of_pages):
        print(i)
        local_params['offset'] = i
        all_vacancies += download_vacancy_one_page(url, local_params)
    return all_vacancies
