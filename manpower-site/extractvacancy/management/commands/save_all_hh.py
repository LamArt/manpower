import datetime

from django.core.management import BaseCommand

from extractvacancy.api.hh_api import get_list_id_vacancies, get_vacancy, parse_vacancy
from extractvacancy.models import Vacancy


class Command(BaseCommand):
    help = "Download IT vacancies from hh"

    def handle(self, *args, **kwargs):
        list_id = get_list_id_vacancies(specialization=1, date_from='2019-01-01', date_to='2019-07-31')
        lenght_list = len(list_id)
        i=0
        for id_vac in list_id:
            buff_vac = get_vacancy(id_vac)
            parsed_vacancy = parse_vacancy(buff_vac)
            vacancy_model, created = Vacancy.objects.get_or_create(site_id=parsed_vacancy['site_id'],
                                                                   created_at=parsed_vacancy['created_at'],
                                                                   defaults=parsed_vacancy)
            print(lenght_list-i)
            if not created:
                for attr, value in parsed_vacancy.items():
                    setattr(vacancy_model, attr, value)
            vacancy_model.save()
            i+=1
