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
    :rtype: requests.models.Response
    """
    response = send_request(url, params)
    response_json = response.json()
    vacancies = response_json['results']['vacancies']

    return vacancies

