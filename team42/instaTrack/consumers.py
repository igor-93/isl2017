import time
import os

from channels.generic.websockets import WebsocketDemultiplexer, JsonWebsocketConsumer

from .data_functions import get_my_posts
from .fetch_data import user_search
from .fetch_data import fetch_user_data
from .data_functions import track_new
from .data_functions import untrack
from .data_functions import get_best_tags
from .data_functions import update_followings
from .data_functions import update_tracked_data
from .data_functions import get_full_user_data, get_unfollow_suggestions, get_tracked_users
from .data_functions import get_best_time
from .data_functions import get_classified_comments
from .data_functions import get_comments
from .data_functions import get_all_comments
from .fetch_data import get_post_emojis



def is_windows():
    return os.name == 'nt'

def get_logged_user_profile(consumer):
    return consumer.message.user.userprofile

def get_logged_user(consumer):
    return consumer.message.user

def create_response(request_data, response_data):
    data = response_data
    data["action"] = request_data["action"]
    data["_ts"] = int(time.time())
    return data


def create_connected_response(stream):
    return {"action": "STREAM_CONNECTED", "name": stream}

# NOTE: things we send in messages must be JSON serializable

class PostsConsumer(JsonWebsocketConsumer):
    http_user = True

    def get_user_posts(self, content):
        user_profile = get_logged_user_profile(self)
        if user_profile is None:
            return []

        cursor = content["cursor"]
        posts, new_cursor = get_my_posts(get_logged_user(self), cursor)
        return {"posts": posts, "new_cursor": new_cursor}

    def get_post_comments(self, content):
        user_profile = get_logged_user_profile(self)
        postcode = content["postcode"]
        if user_profile is None:
            return {}

        #can't classify on WIN
        if is_windows():
            new_cursor, comments = get_comments(postcode, content["cursor"])
        else:
            new_cursor, comments = get_classified_comments(postcode, content["cursor"])
        return {"comments": comments, "new_cursor": new_cursor, "postcode": postcode}

    def get_recent_comments(self, content):
        user = get_logged_user(self)
        do_sentiment_analysis = not is_windows()
        from_ts = content['from_ts']
        comments_list, posts, oldest_ts = get_all_comments(user, 20, sentiment=do_sentiment_analysis, start_ts=from_ts)

        return {"comments": comments_list, "postsMap": posts, "oldestComment_ts": oldest_ts}

    def fetch_post_emojis(self, content):
        code = content['postcode']
        n_comments, result = get_post_emojis(code, limit_comments=200, nr_most_common=5)
        return {"n_comments": n_comments, "emojis": result, "postcode": code}

    ACTIONS = {
        "GET_USER_POSTS": get_user_posts,
        "GET_POST_COMMENTS": get_post_comments,
        "GET_RECENT_COMMENTS": get_recent_comments,
        "GET_POST_EMOJIS": fetch_post_emojis
    }

    def connect(self, message, multiplexer, **kwargs):
        multiplexer.send(create_connected_response(multiplexer.stream))

    def disconnect(self, message, multiplexer, **kwargs):
        print("Stream %s is closed" % multiplexer.stream)

    def receive(self, content, multiplexer, **kwargs):
        action = self.ACTIONS.get(content["action"], None)
        if action is not None:
            multiplexer.send(create_response(content, action(self, content)))


class UserConsumer(JsonWebsocketConsumer):
    http_user = True

    def get_profile_data(self, content):
        user_profile = get_logged_user_profile(self)
        if user_profile is None:
            return {}
        user = {}
        result = get_full_user_data([user_profile.instagram_username])
        if result is not None:
            user = result[0]
        return {
            "user": user
        }

    def track_user(self, content):
        user_profile = get_logged_user_profile(self)
        insta_username = content["instagram_username"]
        if user_profile is None:
            return {}

        success_msg = track_new(get_logged_user(self), insta_username)

        tracked_usernames = get_tracked_users(get_logged_user(self))
        tracked_users = get_full_user_data(tracked_usernames)

        return {"users": tracked_users, "success_msg": success_msg}


    def untrack_user(self, content):
        user_profile = get_logged_user_profile(self)
        insta_username = content["instagram_username"]
        if user_profile is None:
            return {}

        success_msg = untrack(get_logged_user(self), insta_username)

        tracked_usernames = get_tracked_users(get_logged_user(self))
        tracked_users = get_full_user_data(tracked_usernames)

        return {"users": tracked_users, "success_msg": success_msg}

    def search_users(self, content):
        if "query" not in content:
            return {"users": []}
        search_users = user_search(content["query"])
        return {"users": search_users}

    def get_tracked_users(self, content):
        tracked_users = []
        tracked_usernames = get_tracked_users(get_logged_user(self))
        tracked_users = get_full_user_data(tracked_usernames)
        #for username in tracked_usernames:
        #    tracked_users.append({"username": username, "full_name": username, "_details_ts": None})
        return {"users": tracked_users}

    def get_tracking_data(self, content):
        print('DEBUG: get_tracking_data()....')
        user = get_logged_user(self)
        insta_username = content["instagram_username"]

        best_tags_raw = get_best_tags(user, count=20, single_user=True, insta_username=insta_username)
        best_time = get_best_time(user, single_user=True, insta_username=insta_username)

        best_tags = []
        for tag in best_tags_raw:
            best_tags.append({"tag": tag[0], "score": tag[1]})

        return {"best_tags": best_tags, "best_time": best_time, "instagram_username": insta_username}

    def get_tracking_data_aggregated(self, content):
        print('DEBUG: get_tracking_data_aggregated()....')
        user = get_logged_user(self)

        best_tags_raw = get_best_tags(user)

        best_tags = []
        for tag in best_tags_raw:
            best_tags.append({"tag": tag[0], "score": tag[1]})

        best_time = get_best_time(user)
        return {"best_tags": best_tags, "best_time": best_time}

    def get_unfollowing_users(self, content):
        user = get_logged_user(self)

        suggestions = get_unfollow_suggestions(user)
        full_users_data = get_full_user_data([usr for usr, act in suggestions])

        if len(full_users_data) != len(suggestions):
            print('ERROR in data_functons.get_unfollowing_users()!')
            print('    ',len(full_users_data),' != ', len(suggestions))

        suggestions = dict(suggestions)

        for user in full_users_data:
            user['activity'] = suggestions[user['username']]
        return {"users": full_users_data}

    def update_tracking_data(self, content):
        update_tracked_data(get_logged_user(self))
        now = int(time.time())

        tracked_usernames = get_tracked_users(get_logged_user(self))
        tracked_users = get_full_user_data(tracked_usernames)

        return {"update_ts": now, "users": tracked_users}

    def update_following_data(self, content):
        user = get_logged_user(self)
        print('Calling update_followings()...')
        update_followings(user)
        now = int(time.time())

        suggestions = get_unfollow_suggestions(user)
        full_users_data = get_full_user_data([usr for usr, act in suggestions])

        if len(full_users_data) != len(suggestions):
            print('ERROR in data_functons.get_unfollowing_users()!')
            print('    ',len(full_users_data),' != ', len(suggestions))

        suggestions = dict(suggestions)

        for user in full_users_data:
            user['activity'] = suggestions[user['username']]

        return {"users": full_users_data, "update_ts": now}


    ACTIONS = {
        "GET_USER_PROFILE": get_profile_data,
        "TRACK_USER": track_user,
        "UNTRACK_USER": untrack_user,
        "GET_TRACKED_USERS": get_tracked_users,
        "SEARCH_USERS": search_users,
        "GET_TRACKING_DATA": get_tracking_data,
        "GET_TRACKING_DATA_AGGREGATED": get_tracking_data_aggregated,
        "GET_UNFOLLOWING_USERS": get_unfollowing_users,
        "UPDATE_TRACKING_DATA": update_tracking_data,
        "UPDATE_FOLLOWING_DATA": update_following_data
    }

    def connect(self, message, multiplexer, **kwargs):
        multiplexer.send(create_connected_response(multiplexer.stream))

    def disconnect(self, message, multiplexer, **kwargs):
        print("Stream %s is closed" % multiplexer.stream)

    def receive(self, content, multiplexer, **kwargs):
        action = self.ACTIONS.get(content["action"], None)
        if action is not None:
            multiplexer.send(create_response(content, action(self, content)))

class Demultiplexer(WebsocketDemultiplexer):
    consumers = {
        "POSTS": PostsConsumer,
        "USER": UserConsumer
    }
