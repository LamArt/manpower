from django.core.management import BaseCommand

from extractvacancy.models import Vacancy
from extractvacancy.trudvsem_api import download_all_available_pages, parse_vacancy


class Command(BaseCommand):
    help = "Download IT vacancies from trudvsem"

    def handle(self, *args, **kwargs):
        url = 'http://opendata.trudvsem.ru/api/v1/vacancies'
        vacancies = download_all_available_pages(url, {})
        for vacancy in vacancies:
            parsed_vacancy = parse_vacancy(vacancy)
            if parsed_vacancy['specialisation'] == 'Информационные технологии, телекоммуникации, связь':
                vacancy_model, created = Vacancy.objects.get_or_create(site_id=parsed_vacancy['site_id'],
                                                                       defaults=parsed_vacancy)
                if not created:
                    for attr, value in parsed_vacancy.items():
                        setattr(vacancy_model, attr, value)
                    vacancy_model.save()
