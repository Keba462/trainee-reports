from django.core.management.base import BaseCommand
from ...classes import QueryGeneration


class Command(BaseCommand):

    help ='Generate queries'

    def handle(self,*args, **kwargs):
        general_queries =QueryGeneration()
        print('Generating queries for missing screenings')
        general_queries.check_missing_screening()
        print('Generating queries for incomplete Visits')
        general_queries.check_incomplete_visits()
        #print('Generating queries for checking eligibile participants')
        #general_queries.check_eligible_participants()

        print('Done')
