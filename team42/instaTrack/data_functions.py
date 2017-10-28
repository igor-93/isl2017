from collections import defaultdict
import operator
import datetime
import time
import pytz
import time
import asyncio
import aiohttp

from django.utils import timezone
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from mongoengine import NotUniqueError
import numpy as np

from .fetch_data import get_complete_posts_of_user_NEW, check_user , get_complete_posts_of_user
from .fetch_data import get_user_data, get_user_data_list, get_comments, get_comments_for_postcodes
from .fetch_data import n_posts_for_list_of_tags

#from nlp.sentiment_anal import SentimentAnalysis
from nlp.sentiment_anal_server import get_sentiments_for_comments 

from .models import UserProfile, WeFollowID, WeTrackID
from .models import WeFollowUser, WeTrackUser, TagPopularity, cache_tag_popularity, NrFollowers


# local_username can be retrieved from request.user


# start tracking a new instagram user
# local_user: UserProfile.user i.e. the currently logged in user
# insta_username: instagram user we want to start tracking
# it also fetches all data
def track_new(local_user, insta_username):
    cur_user = local_user.userprofile

    insta_user_exists = check_user(insta_username)
    if not insta_user_exists:
        print('ERROR in track_new(): %s is not public' % insta_username)
        return False

    try:
        we_follow = cur_user.wetrackid_set.get(instagram_username=insta_username)
        print('%s already tracks %s' % (local_user.username, insta_username))
        return True
    except MultipleObjectsReturned:
        print('Error: %s tracks multiple objects with the insta name %s' % (local_user.username, insta_username))
        return False
    except ObjectDoesNotExist:
        pass

    saved = False
    # check if this user is already tracked by someone )
    try:
        existing_tracked_id = WeTrackID.objects.get(instagram_username=insta_username)

        existing_tracked = WeTrackUser.objects(instagram_username=insta_username)
        if len(existing_tracked) > 1:
            print('ERROR: Multiple WeTrackUser documents for %s found!' % insta_username)
            return False
        if len(existing_tracked) == 0:
            print('ERROR: None WeTrackUser document for %s found!' % insta_username)
            print('But, we are going to save a new document now...')
            new_track = WeTrackUser(instagram_username=insta_username)
            saved = new_track.initial_fetch()
            # return False
        if len(existing_tracked) == 1:
            found_tracked = existing_tracked[0]
            found_tracked.update_data()
            saved = True

        # make local_user also track it in WeTrackID
        existing_tracked_id.tracker_profiles.add(cur_user)
        existing_tracked_id.save()

    except ObjectDoesNotExist:
        # if not, add this user to WeTrackID and also to WeTrackUser
        new_track_id = WeTrackID(instagram_username=insta_username)

        # do initial_fetch()
        new_track = WeTrackUser(instagram_username=insta_username)
        saved = new_track.initial_fetch()

        if saved:
            new_track_id.save()
            new_track_id.tracker_profiles.add(cur_user)
            new_track_id.save()
        else:
            print('ERROR in track_new() while trying to init fetch and save document in mongodb!')
            print('    ... SQL entry will also not be saved...')

    return saved


# stop tracking a given instagram user
# local_user: UserProfile.user i.e. the currently logged in user
# insta_username: instagram user we want to stop tracking
def untrack(local_user, insta_username):
    cur_user = local_user.userprofile

    # check if insta_username is really tracked by local_user
    try:
        we_follow = cur_user.wetrackid_set.get(instagram_username=insta_username)
    except MultipleObjectsReturned:
        print('Error: %s tracks multiple objects with the insta name %s' % (local_user.username, insta_username))
        return False
    except ObjectDoesNotExist:
        # if not, return false
        print('%s hasnt even trakced %s!' % (local_user.username, insta_username))
        return True

    # if yes:
    # 	check if insta_username is tracked by someone else
    #   	if yes, just remove insta_username from up.wefollowid_set (up is UserProfile of local_user)

    # 		if not, this means that nobody tracks that insta_username,
    # 		so we must ALSO delete WeTrackUser entry for this insta_username

    existing_tracked_id = WeTrackID.objects.get(instagram_username=insta_username)
    print('We are gonna untrack: ', existing_tracked_id)
    count = existing_tracked_id.tracker_profiles.all().count()
    if count > 1:
        # somebody else also tracks this insta user
        existing_tracked_id.tracker_profiles.remove(cur_user)
        existing_tracked_id.save()
        return True
    elif count == 1:
        # no one else tracks this insta user except local_user
        # if existing_tracked_id.tracker_profiles[0].user.username != local_user.username:
        #	print('Some strange error ocured!!!!')
        #	return False

        existing_tracked_id.delete()
        existing_tracked = WeTrackUser.objects(instagram_username=insta_username)
        if len(existing_tracked) > 1:
            print('Multiple WeTrackUser documents for %s found!' % insta_username)
            return False
        elif len(existing_tracked) == 0:
            print('None WeTrackUser document for %s found!' % insta_username)
            return False
        elif len(existing_tracked) == 1:
            found_tracked = existing_tracked[0]
            found_tracked.delete()
            return True

    else:
        print('Strange ERROR: %s WeTrackUserID exists without beeing conn. to any local user!' % insta_username)
        return False


# get list of posts for the current user
# local_user: UserProfile.user i.e. the currently logged in user
# end_cursor: first one is 1, after that give the new_cursor
# returns:
# 	list of dict defined in fetchdata.prepare_post_data()
#   new_cursor
def get_my_posts(local_user, end_cursor=1):
    # print('get_my_posts....')
    inst_name = local_user.userprofile.instagram_username
    # post_codes, posts, new_cursor = get_complete_posts_of_user(inst_name, with_next=True, next=end_cursor)
    post_codes, posts, new_cursor = get_complete_posts_of_user_NEW(inst_name, with_next=True, next=end_cursor)

    return posts, new_cursor


# get comments for last 'from_last_many_posts' posts
# returns ONLY comments that are since last 24 hours
def get_all_comments(local_user=None, from_last_many_posts=50, sentiment=True, since_hours=24, start_ts = None):
    if start_ts is not None and start_ts < 0:
        return [], {}, -1

    print('get_all_comments()... from_last_many_posts = ', from_last_many_posts)
    inst_name = local_user.userprofile.instagram_username
    # inst_name = 'moira_photography'
    # post_codes, posts = get_complete_posts_of_user(inst_name, nr_posts=from_last_many_posts, with_next=False)
    post_codes, posts = get_complete_posts_of_user_NEW(inst_name, nr_posts=from_last_many_posts, with_next=False)
    codes_to_posts = dict(zip(post_codes, posts))
    all_comments_list = []

    loop = asyncio.new_event_loop()

    cursors = [1]*len(post_codes)
    print('getting first_chunk_comments...')
    session = aiohttp.ClientSession(loop=loop)
    first_chunk_comments = get_comments_for_postcodes(loop, session, post_codes, cursors)
    session.close()
    print('DONE first_chunk_comments!')

    if start_ts is None:
        from_ts = int(time.time())
    else:
        from_ts = start_ts

    timedelta_ts = since_hours * 3600
    target_oldest_ts = from_ts - timedelta_ts

    for postcode, start_cursor, comments in first_chunk_comments:
        next_cursor = start_cursor
        prev_cursor = None
        post_comments = comments
        if len(comments) > 0:
            last_date = comments[-1]['date']
            while next_cursor is not None and last_date > target_oldest_ts:
                prev_cursor = next_cursor
                next_cursor, more_comments = get_comments(postcode, last_comment=next_cursor)
                more_comments = list(reversed(more_comments))
                post_comments.extend(more_comments)
                last_date = more_comments[-1]['date']

        if prev_cursor is not None:
            codes_to_posts[postcode]["_comments_nextCursor"] = prev_cursor
            codes_to_posts[postcode]["_comments_fetchStatus"] = "SUCCESS"

        # post_comments_filtered = [comm for comm in post_comments if (comm['date'] <= from_ts) and (comm['date'] > (from_ts - timedelta_ts))]
        for comment in post_comments:
            comment["post_code"] = postcode

        all_comments_list.extend(post_comments)

    all_comments_list = [comm for comm in all_comments_list if (comm['date'] <= from_ts)]
    all_comments_list = sorted(all_comments_list, key=lambda comm: comm["date"], reverse=True)
    all_comments_list_filtered = [comm for comm in all_comments_list if (comm['date'] > (from_ts - timedelta_ts))]

    if len(all_comments_list_filtered) >= 20:
        all_comments_list = all_comments_list_filtered
    else:
        all_comments_list = all_comments_list[:20]

    for comm in all_comments_list:
        codes_to_posts[comm["post_code"]]["comments"].append(comm["id"])

    if len(all_comments_list) > 0:
        comment_oldest_ts = all_comments_list[-1]["date"]
    else:
        comment_oldest_ts = -1

    if sentiment:
        #sent = SentimentAnalysis()
        #comments_with_sentiment = sent.get_sentiments_for_comments(all_comments_list)
        #sent.close()
        loop = asyncio.new_event_loop()
        session = aiohttp.ClientSession(loop=loop)
        comments_with_sentiment = get_sentiments_for_comments(loop, session, all_comments_list)
        session.close()

        all_comments_list = comments_with_sentiment

    return all_comments_list, codes_to_posts, comment_oldest_ts




def get_classified_comments(postcode, last_comment=1):
    print('get_classified_comments()...')
    cursor, res = get_comments(postcode, last_comment)

    #sent = SentimentAnalysis()
    #res = sent.get_sentiments_for_comments(res)
    #sent.close()
    loop = asyncio.new_event_loop()
    session = aiohttp.ClientSession(loop=loop)
    res = get_sentiments_for_comments(loop, session, res)
    session.close()

    return cursor, res


# updates the data needed for the unfollow suggestions section
#     To be called ONLY once
def update_followings(local_user):
    
    local_userprofile = local_user.userprofile
    print('data_functions.update_followings(): local_userprofile: ', local_userprofile)
    
    res1 = local_userprofile.update_list_of_followings()
    res2 = local_userprofile.update_following_data()

    return (res1 and res2)


# updates the data needed for the tracking section
#     To be called ONLY once
def update_tracked_data(local_user, single_user=False, insta_username=None):
    local_userprofile = local_user.userprofile
    if not single_user:
        res = local_userprofile.update_tracked_data()
    else:
        res = local_userprofile.update_tracked_data(insta_user=insta_username)

    return res


# returns the list of usernames we track 
def get_tracked_users(local_user):
    local_userprofile = local_user.userprofile
    tracked_usernames = local_userprofile.list_of_trackings()

    return tracked_usernames


# input the list of instagram usernames
# returns list of users in the form defined in GIT Wiki page
def get_full_user_data(insta_usernames):
    loop = asyncio.new_event_loop()
    session = aiohttp.ClientSession(loop=loop)
    result = get_user_data_list(loop, session, insta_usernames)
    session.close()
    
    return result


# TODO: adjust this so it also takes into account the number of followers from the past

# returns the list of least active users that we follow on instagram
# still it doesn't mean that the user is inactive. 
# The metric is nr of posts last week as the percentage of average in 6 weeks before
# local_user: UserProfile.user i.e. the currently logged in user
# count: how many suggestions to return
def get_unfollow_suggestions(local_user, count=20):
    local_userprofile = local_user.userprofile

    result = local_userprofile.list_of_followings(with_activity=True)
    # print('result: ', result)
    result = sorted(result, key=lambda x: x[1])
    # print('result: ', result)
    count = min(count, len(result))
    # return "count" many users with the least activity
    return result[:count]


# TODO: maybe cache the tagscore for each user

# returns suggestions for the hash tags based on the users we track
# local_user: UserProfile.user i.e. the currently logged in user
# if single_user == True, we only return data based on the given insta_username
# count: how many suggestions to return

def get_best_tags(local_user, count=20, single_user=False, insta_username=None):
    cur_user = local_user.userprofile

    # something like:
    # 	for each tag sum up postscores of all the posts it appears in
    #   and then divide by total number of posts (in istagram) that use that hashtag

    MIN_TAG_SIZE = np.exp(3)    # 10 being the minimum Font
    MAX_TAG_SIZE = np.exp(14)   # 30 being the maximum size
    TAG_PERCENTILE = 50         # Take tags which have scores more than this percentile
    alpha = 1e-11

    tag_to_postscore = defaultdict(int)
    if not single_user:
        tracked_user_ids = cur_user.list_of_trackings()
    else:
        tracked_user_ids = [insta_username]
        # print('tracked_user_ids: ', tracked_user_ids)
    tracked_users = WeTrackUser.objects.filter(instagram_username__in=tracked_user_ids)

    all_tags = []
    for tr in tracked_users:
        # print('tr ', tr)
        for post in tr.posts:
            for tag in post.tags:
                tag_to_postscore[tag] += post.postscore
                all_tags.append(tag)

    all_tags = set(all_tags)
    print('We have in total ', len(all_tags), ' tags')
    existing_tags = TagPopularity.objects.filter(tag__in=all_tags)
    existing_tags_only = [obj['tag'] for obj in existing_tags]

    existing_tags = {obj['tag']: obj['n_posts'] for obj in existing_tags}

    existing_tags_only = set(existing_tags_only)
    print('We have found ', len(existing_tags_only), ' cached tags')
    new_tags = list(all_tags - existing_tags_only)
    print('So, we have ', len(new_tags), ' new tags.')

    new_dict = {}
    # fetching number of posts for the new hastags ASYNCH
    if len(new_tags) > 0:
        print('Fetching counts from instagram...')
        loop = asyncio.new_event_loop()
        session = aiohttp.ClientSession(loop=loop)
        new_tags_count = []

        new_tags_count = n_posts_for_list_of_tags(loop, session, new_tags)
        session.close()
        new_dict = dict(new_tags_count)

    cache_tag_popularity(new_dict)

    count = min(count, len(tag_to_postscore))

    for i, tag in enumerate(tag_to_postscore.keys()):
        n_posts_for_t = 1.0
        try:
            n_posts_for_t = new_dict[tag]
        except:
            try:
                n_posts_for_t = existing_tags[tag]
            except:
                print('ERROR: we counld find tag %s in any dictionary!' % tag)
                n_posts_for_t = 0.0

        if float(n_posts_for_t) == 0.0:
            tag_to_postscore[tag] = 0.0
        else:
            tag_to_postscore[tag] = float(tag_to_postscore[tag]) + alpha * float(n_posts_for_t)

    if len(list(tag_to_postscore.values())) == 0:
        max_value = 0
    else:    
        max_value = np.max(list(tag_to_postscore.values()))
        min_value = np.percentile(list(tag_to_postscore.values()), TAG_PERCENTILE)

    tag_to_postscore = { k:v for k, v in tag_to_postscore.items() if v > min_value }
    for tag in tag_to_postscore.keys():
        tag_to_postscore[tag] = (float(tag_to_postscore[tag]) - min_value)/ (max_value - min_value)
        tag_to_postscore[tag] = np.log(MIN_TAG_SIZE + (MAX_TAG_SIZE - MIN_TAG_SIZE) * tag_to_postscore[tag])

    tag_to_postscore = sorted(tag_to_postscore.items(), key=operator.itemgetter(1), reverse=True)[:count]

    # convert to dict
    # tag_to_postscore = dict(tag_to_postscore)
    # print('tag_to_postscore')
    # print(tag_to_postscore)
    return tag_to_postscore


# days_in_week = ['mon','tue','wed','thu','fr','sat','sun']
days_in_week = range(0, 7)
time_intervals = range(0, 24, 2)


def init_dict(val_type='float'):
    res = {}
    if val_type == 'float':
        for day in days_in_week:
            res[day] = {ti: 0.0 for ti in time_intervals}
    elif val_type == 'list':
        for day in days_in_week:
            res[day] = {ti: [] for ti in time_intervals}
    else:
        print('ERROR in init_dict(): val_type is not supported! ', val_type)
    return res


# returns the postscores for each day in the week and for each time interval of 2 hours
# local_user: UserProfile.user i.e. the currently logged in user
# if single_user == True, we only return data based on the given insta_username
# out_type: 
#    if 'sum' we return the sum of the postscores
#    if 'average' we return the average postscore
#
# return format:
# {0: {0: 0.032138442500000003, 2: 0, 4: 0.069805703499999996, 6: 0.057413899598400001, 
#      8: 0.047938842720000006, 10: 0.056396463360000003, 12: 0.067779151233333321, 14: 0.04727018278000001, 
#      16: 0.033016989163636365, 18: 0.027208319395652179, 20: 0.053075036171428565, 22: 0.05407911}, 
#  1: {0: 0, 2: 0, 4: 0.058053901599999999, 6: 0.058858072481249996, 8: 0.051807942345000003, 
#      10: 0.043552191790909092, 12: 0.031930328627272735, 14: 0.038318912233333335, 16: 0.029843843880000005, 
#      18: 0.033533116426315797, 20: 0.042556948628571435, 22: 0.034198599083333329}, 
#  2: {0: 0, 2: 0, 4: 0.061804697200000001, 6: 0.06053864794418605, 8: 0.045256165829411769, 
#      10: 0.079522043666666667, 12: 0.035895352583333338, 14: 0.045184178300000002, 16: 0.052224969100000004, 
#      18: 0.039807013384210534, 20: 0.031707580783333335, 22: 0.034099959916666665}, 
#  3: {0: 0, 2: 0, 4: 0.060534837599999995, 6: 0.060462242873387105, 8: 0.060410559035714288, 
#     10: 0.048429206466666673, 12: 0.04050584768461539, 14: 0.03811289654999999, 16: 0.024627487507692305, 
#     18: 0.028797991608333334, 20: 0.060723114962499991, 22: 0.053696996480000002}, 
# ..... }
def get_best_time(local_user, single_user=False, insta_username=None, out_type='average'):
    cur_user = local_user.userprofile
    if out_type != 'average' or out_type != 'sum':
        out_type = 'average'

    # to be defined
    # return pairs (time_int, score) with time_int are buckets
    # [0-2h, 2-4h, 4-6h, 6-8h....] for each time of the day
    # in total 7 * 12 = 84 buckets

    if not single_user:
        tracked_user_ids = cur_user.list_of_trackings()
    else:
        tracked_user_ids = [insta_username]
    print('tracked_user_ids: ', tracked_user_ids)
    tracked_users = WeTrackUser.objects.filter(instagram_username__in=tracked_user_ids)

    if out_type == 'average':
        result = init_dict('list')
    else:
        result = init_dict('float')

    for tr in tracked_users:
        # print('tr ', tr)
        for post in tr.posts:
            day = post.timestamp.weekday()
            hour = post.timestamp.hour
            if hour % 2 == 1:
                hour -= 1
            if out_type == 'average':
                result[day][hour].append(float(post.postscore))
            else:
                result[day][hour] += float(post.postscore)

    if out_type == 'average':
        for day in days_in_week:
            for h in time_intervals:
                if result[day][h] == []:
                    result[day][h] = 0
                else:
                    result[day][h] = np.mean(result[day][h])

                    # print(result)


    # Normalisation
    max_value = 0
    for day in days_in_week:
        for h in time_intervals:
            max_value = max(max_value, result[day][h])

    if (not (max_value == 0)):
        for day in days_in_week:
            for h in time_intervals:
                result[day][h] = result[day][h] / max_value

    #print('DEBUG: get_best_time(): ', result)
    return result



# here we return the list of followers for the last "days" days
# list contains the tuples of (timestamp, nr_followers)
def get_daily_followers_change(local_user, days=7):
    cur_user = local_user.userprofile

    nr_foll_obj_list = NrFollowers.objects(instagram_username=cur_user.instagram_username)
    if len(nr_foll_obj_list) > 1:
        # this case should never happen
        print('ERROR: Multiple NrFollowers documents for %s found!' % instagram_username)
        return [(0,0)]*days
    if len(nr_foll_obj_list) == 0:
        # we still dont track nr of followers for this user, start tracking now
        new_obj = NrFollowers(instagram_username=instagram_username)
        new_obj.save()
        try:
            new_obj = NrFollowers(instagram_username=instagram_username)
            new_obj.save()
        except NotUniqueError:
            print(new_obj, ' already exists')

        return [(0,0)]*days
    if len(nr_foll_obj_list) == 1:
        found_obj = nr_foll_obj_list[0]

    data = found_obj.get_data()  
    to_pad = days - len(data)
    if to_pad > 0:
        padding = [(0,0)]*to_pad
        data = padding.extend(data)
    else:
        data = data[-days:]

    return data  


