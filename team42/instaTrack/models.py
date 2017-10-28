import datetime
import dateutil
import pytz
import numpy as np

from django.db import models
#from django.utils import timezone
from django.contrib.auth.models import User

from mongoengine import Document, EmbeddedDocument, fields

from .fetch_data import n_followers_of_user, get_posts_of_user_ts, check_user, \
get_complete_posts_of_user, get_complete_posts_of_user_NEW, get_list_of_followings


DATA_UPDATE_PERIOD_mins = 60 



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile')
    instagram_username = models.CharField(max_length=50, blank=False)
    instagram_id = models.CharField(max_length=50, blank=True)
    nr_followers = models.IntegerField(default=0)
    nr_followers_timestamp = models.DateTimeField('time nr fol checked', default=datetime.datetime.now, blank=True)
    access_token = models.CharField(max_length=60, blank=True)

    # represent object as a string
    def __str__(self):
        return 'Local username: ' + self.user.username + ', insta username: ' + self.instagram_username

    # TO BE CALLED PERIODICALLY
    def update_nr_followers(self):
        print('Yeaaaah I am WORKING!!')
        pass

    def save_nr_foll(self, nr_foll):
        self.nr_followers = nr_foll
        nr_followers_timestamp = datetime.datetime.now
        self.save()

    # if it is already more than 23:55h ago
    def if_save_nr_foll(self):
        now = datetime.datetime.now
        saved = self.nr_followers_timestamp

        if saved >= datetime.datetime.utcnow() - datetime.timedelta(hours=23, minutes=55):
            return False
        else:
            return True

    # list of who we follow
    def list_of_followings(self, with_activity=False):
        followings = self.wefollowid_set.all()
        followings_names = []
        for insta_user in followings:
            followings_names.append(insta_user.instagram_username)

        if not with_activity:
            return followings_names

        result = []

        following_users = WeFollowUser.objects.filter(instagram_username__in=followings_names)

        for insta_user in following_users:
            activity = insta_user.activity()
            result.append((insta_user.instagram_username, activity))

        return result

    # list of who we track
    def list_of_trackings(self):
        trackings = self.wetrackid_set.all()
        result = []
        for insta_user in trackings:
            result.append(insta_user.instagram_username)

        return result

    def set_token(self, token):
        self.access_token = token
        self.save()

    # TO BE CALLED on LOGIN
    # it updates the list of the people we follow
    def update_list_of_followings(self):
        print('UserProfile.update_list_of_followings():')
        user_exists = check_user(self.instagram_username)
        if not user_exists:
            print(
                'ERROR in UserProfile.update_list_of_followings(): %s is not a valid insta username!' % self.instagram_username)
            return False
        new_list = get_list_of_followings(self.instagram_id)
        old_list = self.list_of_followings()
        #print('old_list: ', old_list)
        # if not in new, remove it from DB
        old_set = set(old_list)
        new_set = set(new_list)
        only_new = list(new_set - old_set)
        only_old = list(old_set - new_set)

        # check if old is followed by someone else, if yes, just remove connection from self
        # otherwise remove from DB
        for old_insta_user in only_old:
            print('Only old followed user: ', old_insta_user)
            resID = WeFollowID.objects.get(instagram_username=old_insta_user)
            count = resID.follower_profiles.all().count()
            if count > 1:
                print('There is also someone else following %s' % old_insta_user)
                print('Total count is: ', count)
                resID.follower_profiles.remove(self)
                resID.save()

            elif count == 1:
                resID.delete()
                # update mongoDB document also
                old_following = WeFollowUser.objects(instagram_username=old_insta_user)
                old_following.delete()

        # if not in old, add to DB
        # check first if some other UserProfile is following him, if yes, just add connection,
        # otherwise create new WeFollowID
        for new_insta_user in only_new:
            print('Only new followed user: ', new_insta_user)
            resID, created = WeFollowID.objects.get_or_create(instagram_username=new_insta_user)
            resID.follower_profiles.add(self)
            # resID.save()
            # update mongoDB document also
            #print('created: ', created)
            if created:
                new_following = WeFollowUser(instagram_username=new_insta_user)
                new_following.update_posting_activity()
                resID.save()
            else:
                existing_following = WeFollowUser.objects(instagram_username=new_insta_user)
                if len(existing_following) > 1:
                    print('Multiple WeFollowUser documents for %s found!' % new_insta_user)
                    return False
                if len(existing_following) == 0:
                    print('None WeFollowUser document for %s found!' % new_insta_user)
                    return False
                if len(existing_following) == 1:
                    found_doc = existing_following[0]
                    found_doc.update_posting_activity()
                    resID.save()

        self.save()
        return True

    def update_tracked_data(self, insta_user=None):
        track_ids = self.list_of_trackings()
        if insta_user != None:
            if insta_user in track_ids:
                track_ids = [insta_user]
            else:
                print('ERROR in UserProfile.update_tracked_data(): %s not tracked by %s' % (
                insta_user, self.instagram_username))
                return False
        print('We are gonna update ', len(track_ids), ' tracked people...')
        track_objects = WeTrackUser.objects.filter(instagram_username__in=track_ids)
        succeeded = True
        for track_obj in track_objects:
            res = track_obj.update_data()
            if not res:
                succeeded = False

        return succeeded

    # TO BE CALLED ON LOGIN
    # for the existing list of followings, update their activity
    def update_following_data(self):
        following_list = self.list_of_followings()
        print('UserProfile.update_following_data... ', len(following_list))

        following_users = WeFollowUser.objects.filter(instagram_username__in=following_list)

        for insta_user in following_users:
            insta_user.update_posting_activity()

        return True



### EXAMPLES: ########################################
# get list of followings of our user up1 (up1 is instance of UserProfile):
# up1.wefollowid_set.all() 

# get list of our users (i.e. UserProfiles) that follow p on instagram (p is instance of WeFollow)
# p.follower_profiles.all()

# analog for WeTrack
######################################################

# used for unfollow suggestions
class WeFollowID(models.Model):
    follower_profiles = models.ManyToManyField(UserProfile)
    instagram_username = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.instagram_username


class WeTrackID(models.Model):
    tracker_profiles = models.ManyToManyField(UserProfile)
    instagram_username = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.instagram_username




####################### MongoDB Part #######################

class WeFollowNrFollowers(EmbeddedDocument):
    nr_followers = fields.IntField(min_value=0)
    timestamp = fields.DateTimeField()


class NrFollowers(Document):
    instagram_username = fields.StringField(required=True, unique=True)
    data = fields.EmbeddedDocumentListField(WeFollowNrFollowers)

    def __str__(self):
        return 'instagram_username: '+self.instagram_username

    def add(self, nr_foll):
        ts = datetime.datetime.utcnow()
        nr_foll_obj = WeFollowNrFollowers(nr_followers=nr_foll, timestamp=ts)
        self.update(add_to_set__data=[nr_foll_obj])

    # if it is already more than 23:45h ago
    def is_time_to_add(self):
        now = datetime.datetime.utcnow()
        if len(self.data) == 0:
            return True
            
        latest = max([obj.timestamp for obj in self.data])

        if latest >= datetime.datetime.utcnow() - datetime.timedelta(hours=23, minutes=45):
            return False
        else:
            return True    

    # returns the list of tuples (date, nr_followers)
    # list is sorted from the oldest to the newest
    def get_data(self):
        res = [(obj.timestamp, obj.nr_followers) for obj in self.data]
        return sorted(res, key=lambda tup: tup[0])



####################### Our Followers #######################

# time pariods used to calculate the activity
FOLL_RECENT_PERIOD_days = 14
FOLL_TOTAL_PERIOD_days = 42





class WeFollowUser(Document):
    instagram_username = fields.StringField(required=True, unique=True)
    #posts = EmbeddedDocumentListField(WeFollowPost)
    posting_timestamps = fields.ListField(fields.DateTimeField(unique=True))
    nr_followers = fields.EmbeddedDocumentListField(WeFollowNrFollowers)
    last_updated = fields.DateTimeField()

    def __str__(self):
    	return self.instagram_username


    # TO BE CALLED PERIODICALLY!!
    # updates the number of followers of the user
    def add_nr_followers_now(self):
        # find nr_followers.timestamp < today -50 days and delete them
        nr_folls = self.nr_followers
        remaining = []
        for n_f in nr_folls:
            #n_f.timestamp = n_f.timestamp.replace(tzinfo=pytz.UTC)
            n_f.timestamp = n_f.timestamp.replace(tzinfo=None)
            if n_f.timestamp > datetime.datetime.utcnow() - datetime.timedelta(days=49):
                remaining.append(n_f)

        # create new  WeFollowNrFollowers new.nr_followers = nr_foll and new.timestamp = now
        followed_by, follows = n_followers_of_user(self.instagram_username)
        current = WeFollowNrFollowers(timestamp=datetime.datetime.now, nr_followers=followed_by)
        remaining.append(current)
        self.nr_followers = remaining

        self.save()


	# updates posting activity. 
	# called by UserProfile.update_list_of_followings()
	# and UserProfile.update_following_data()
    def update_posting_activity(self):

        if self.last_updated == None:
            self.last_updated = datetime.datetime.utcnow() - datetime.timedelta(days=365)
        if self.last_updated > datetime.datetime.utcnow() - datetime.timedelta(minutes=DATA_UPDATE_PERIOD_mins):
            print('WeFollowUser.update_posting_activity(): updated recently, skipping... ', self. instagram_username)
            return True


        # delete posting_timestamps < today -50 days
        postings = self.posting_timestamps
        remaining = []

        to_keep_ts = datetime.datetime.utcnow() - datetime.timedelta(days=FOLL_TOTAL_PERIOD_days)

        for posting in postings:
            # if posting newer that FOLL_TOTAL_PERIOD_days, keep it
            if posting > to_keep_ts:
                remaining.append(posting)


        # fetch since the latest post stored
        if len(remaining) == 0:
            #print('This document is new, so no existing remainings ')
            latest = to_keep_ts
        else:
            latest = np.max(remaining)

        # save timestamps of the posts later than max (to be fetched from instagram)
        codes, tss = get_complete_posts_of_user_NEW(self.instagram_username, 
            with_timestamp=True, timestamp=latest, ts_include=True)

        #print('Last 35 days posts of ', self.instagram_username, ', len of tss: ',len(tss))
        tss_new = []
        for ts in tss:
            ts = datetime.datetime.utcfromtimestamp(ts)
            tss_new.append(ts)

        remaining.extend(tss_new)
        self.posting_timestamps = remaining

        self.last_updated = datetime.datetime.utcnow()
        self.save()



    # TODO: should also take nr. followers into cosideration
    # higher value means more active
    def activity(self):
        my_now = datetime.datetime.utcnow()    

        recent = len([i for i in self.posting_timestamps if i > my_now - datetime.timedelta(days=FOLL_RECENT_PERIOD_days)])
        rest = len([i for i in self.posting_timestamps if i < my_now - datetime.timedelta(days=FOLL_RECENT_PERIOD_days)])

        n_weeks_recent = FOLL_RECENT_PERIOD_days / 7.0
        n_weeks_before = (FOLL_TOTAL_PERIOD_days - FOLL_RECENT_PERIOD_days) / 7.0   # 7 days in the week
        try:
            if recent == 0:
                result = 0.0
            else:
                result = (recent/n_weeks_recent) / (rest/n_weeks_before)

        except ZeroDivisionError:
            result = 1.0

        #print('WeFollowUser.activity(): instagram_username: ', self.instagram_username)
        #print('    posts in recent: ', recent)
        #print('    posts in weeks before that: ', rest)
        
        return result






####################### Users we track #######################

TR_RECENT_PERIOD_days = 14
TR_TOTAL_POSTS_nr = 2000




class WeTrackPost(EmbeddedDocument):
    postcode = fields.StringField(max_length=50)
    postscore = fields.DecimalField(min_value=0, precision=10)
    timestamp = fields.DateTimeField()
    nr_likes = fields.FloatField(min_value=0, precision=10)
    nr_comments = fields.FloatField(min_value=0, precision=10)
    tags = fields.ListField(fields.StringField(max_length=100))

# def __str__(self):
#	return 'postcode: ',self.postcode,' tags: ', ', '.join(self.tags)


class WeTrackUser(Document):
    instagram_username = fields.StringField(required=True, unique=True)
    #saves list of postocdes of ALL posts of that user
    posts = fields.EmbeddedDocumentListField(WeTrackPost) 

    last_updated = fields.DateTimeField()


    def __str__(self):
    	return self.instagram_username


	# TESTED
	# get ALL the posts of the user
    def initial_fetch(self):
        # check if user exists
        if not check_user(self.instagram_username):
        	print('User ', self.instagram_username,' doesnt exist or is private.')
        	return False
        if len(self.posts) > 0:
        	print('User ', self.instagram_username,' is already initialised.')
        	return False

        new_posts = []
        # get the data from ALL his posts
        n_followers = n_followers_of_user(self.instagram_username)[0]
        #postcodes, posts = get_complete_posts_of_user(self.instagram_username, 1000)
        postcodes, posts = get_complete_posts_of_user_NEW(self.instagram_username, nr_posts=1000)


        print('We have fetched ',str(len(postcodes)),' postcodes of ', self.instagram_username)
        for i, post in enumerate(posts):

        	if n_followers == 0:
        		postscore = 0
        	else:
        		postscore = post['n_likes'] / n_followers
        	date = datetime.datetime.utcfromtimestamp(post['date'])
        	#date.replace(tzinfo=pytz.UTC)

        	post_obj = WeTrackPost(postcode=post['code'], nr_likes=post['n_likes'], 
        		nr_comments=post['n_comments'], timestamp=date, tags=post['tags'], postscore=postscore)

        	new_posts.append(post_obj)


        self.posts = new_posts
        self.last_updated = datetime.datetime.utcnow()

        try:
        	self.save()
        except:
        	print('initial_fetch for %s FAILED!!!'%self.instagram_username)
        	return False

        print('Saved the object to mongodb!')

        return True




    # TESTED	
    # update the data of the last 14 days of posts
    def update_data(self):
        if len(self.posts) == 0:
        	self.initial_fetch()

        if self.last_updated == None:
            self.last_updated = datetime.datetime.utcnow() - datetime.timedelta(days=365)
        if self.last_updated > datetime.datetime.utcnow() - datetime.timedelta(minutes=DATA_UPDATE_PERIOD_mins):
            print('WeTrackUser.update_data(): updated recently, skipping...')
            return True


        # get all the posts (from DB) whose timestamp is < today-14 days
        
        recently = datetime.datetime.utcnow() - datetime.timedelta(days=TR_RECENT_PERIOD_days)
        recent_postcodes, recent_posts = get_complete_posts_of_user_NEW(self.instagram_username, 
        		with_timestamp=True, timestamp=recently, ts_include=False)

        print('WeTrackUser.update_data():')
        print('User ', self.instagram_username,' has ', str(len(recent_postcodes)),' recent posts.')
        n_followers = n_followers_of_user(self.instagram_username)[0]


        # delete recent
        to_remove_count = 0
        for i, existing_post in enumerate(self.posts):
        	if existing_post.postcode in recent_postcodes:
        		to_remove_count += 1
        	if i > len(recent_postcodes) +5:
        		# we can break here because the posts are sorted,
        		# but give some buffer if users are deleting recent posts
        		break   


        clean_old_posts = self.posts[to_remove_count:]
        self.posts = clean_old_posts
        self.save()

        #print('len of updated self.posts after removing new ones: ', len(self.posts))


        recent_posts_obj = []
        for post in recent_posts:
        	#to_remove = WeTrackPost(postcode=postcode)
        	#self.update(pull__posts__postcode=postcode)
        	postscore = post['n_likes'] / n_followers
        	date = datetime.datetime.utcfromtimestamp(post['date'])
        	#date.replace(tzinfo=pytz.UTC)

        	post_obj = WeTrackPost(postcode=post['code'], nr_likes=post['n_likes'], 
        		nr_comments=post['n_comments'], timestamp=date, tags=post['tags'], postscore=postscore)

        	recent_posts_obj.append(post_obj)


        #print('len of recent_posts_obj: ', len(recent_posts_obj))

        for recent_post_obj in reversed(recent_posts_obj):
        	self.posts.insert(0,recent_post_obj)


        # save it
        self.last_updated = datetime.datetime.utcnow()
        self.save()
        return True



		


# caches the tags and their number of posts
class TagPopularity(Document):
    tag = fields.StringField(required=True)
    n_posts = fields.DecimalField(precision=15)

    def __str__(self):
        # return '('+self.tag+','+str(float(self.n_posts),'utf-8')+')'
        return '( %s, %f)' % (self.tag, float(self.n_posts))


def cache_tag_popularity(tag_to_nr_posts):
    for key, value in tag_to_nr_posts.items():
        obj = TagPopularity(tag=key, n_posts=value)
        obj.save()
