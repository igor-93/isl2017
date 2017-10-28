import asyncio
import schedule
import time
import aiohttp

from django.core.management.base import BaseCommand, CommandError

from instaTrack.models import UserProfile, WeFollowUser, NrFollowers
from instaTrack.fetch_data import get_user_data_list

class Command(BaseCommand):
    help = 'Run all the jobs that have to be executed periodically'

    #def add_arguments(self, parser):
    #parser.add_argument('poll_id', nargs='+', type=int)


    def myjob(self):
        # for all UserProfiles update their number of followers
        # user_profiles = UserProfile.objects.all()
        # for up in user_profiles:
        #     up.update_nr_followers()

        # # for all followed users update their number of followers
        # followed_users = WeFollowUser.objects.all()
        # for fu in followed_users:
        #     print('we follow: ',fu.instagram_username)
        #     fu.add_nr_followers_now()

        all_nr_foll_objects = NrFollowers.objects
        print('Saving new nr_followers...')

        insta_usernames = [nr_foll.instagram_username for nr_foll in all_nr_foll_objects]
        loop = asyncio.get_event_loop()
        session = aiohttp.ClientSession(loop=loop)
        users = get_user_data_list(loop, session, insta_usernames)
        session.close()
        usernames_to_nr_foll = {user['username']:user['n_followed_by'] for user in users}

        for nr_foll in all_nr_foll_objects:
            if nr_foll.is_time_to_add():
                try:
                    nr_foll.add(usernames_to_nr_foll[nr_foll.instagram_username])
                except:
                    print('Failed to add ',nr_foll.instagram_username)



    def handle(self, *args, **options):
        # UTC time = zurich time - 2h
        schedule.every().day.at("21:00").do(self.myjob)  
        while True:
            schedule.run_pending()
            time.sleep(1)  

        
