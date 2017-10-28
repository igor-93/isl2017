from django.core.management.base import BaseCommand, CommandError
from mongoengine import NotUniqueError

from instaTrack.models import NrFollowers


class Command(BaseCommand):
    help = 'Add new users whose number of followers we want to save peridically'


    def handle(self, *args, **options):

        list_of_users = [
        'philibertbarelli_photographie',
        ]
        for item in list_of_users:
            try:
                new_nr_foll_doc = NrFollowers(instagram_username=item)
                new_nr_foll_doc.save()
                print(new_nr_foll_doc, ' SAVED!')
            except NotUniqueError:
                    print(new_nr_foll_doc, ' already exists')

        
