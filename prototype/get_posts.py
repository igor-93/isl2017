from lxml import html
import requests
import json  
import datetime
import pytz
import traceback
import pycurl
import io
from django.utils import timezone
from django.conf import settings

import re   # for emojis
from collections import Counter

# for async functions
import asyncio
import aiohttp


def get_json_txt(url):
    buffer = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()

    body = buffer.getvalue().decode('UTF-8')

    return body




def user_headers(username):
    return {
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-US,en;q=0.8',
        'cache-control':'no-cache',
        'content-length':'484',
        'content-type':'application/x-www-form-urlencoded',
        'cookie':'mid=WJSRFgAEAAHxRpTTXPOhV7JcTqmS; fbm_124024574287414=base_domain=.instagram.com; s_network=""; ig_pr=1; ig_vw=1920; csrftoken=zMwzbE9UFebKKB9A8lesuvZeY28oaBYv; rur=FRC; fbsr_124024574287414=2rHtUEIqldvUnd692TMQxb0a9ahyduKC-l1D8Q2pXDw.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUR4a1ltWkxITHdpTDk2SnQ4ZzJHNWcyb1BXS2ktbmlnRnUxVmV1YUpOUnZUUzFoOGY0NkJSRWNjRThlYS1KYzZHVHVmX1VMLVFMd1dBWEFacXZpUVlkakZrTjNmNGVsMS0ydGRxQUFIaE1DRVhybEZuT1hnZ3RSazZGNl80RkdSYjBSX2drMzBFUERIeHpxNUJlNHl2THphaldRRnk0b2NJWnFhMHNQYUQ0XzhhdzM2MXBrMVNjQTJ2SnNnQmpQMmFzOXZvbTl4UDB3djhpZHQySmR3RHExeGtSYXBwN3Y0cDg1NWE2VDVsQ1F0SU5uNjNzV0tiOUJ0MUd1MlBxU3lKSG9DNXhLWnpENXhNVzdSU1Q1UmhqSzhBNGozWk5jeVhRak1GQTBncTJCeFpDS2l0MEVsdmdUdlV2YXMxTEFvWTdRcS1qc1BzclFZa1VMczRxcmtOMSIsImlzc3VlZF9hdCI6MTQ5MTQyNTU2NSwidXNlcl9pZCI6IjEwMDAwMjc5MzMzNDM1NyJ9',
        'origin':'https://www.instagram.com',
        'pragma':'no-cache',
        'referer':'https://www.instagram.com/'+username+'/',
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        'x-csrftoken':'zMwzbE9UFebKKB9A8lesuvZeY28oaBYv',
        'x-instagram-ajax':'1',
        'x-requested-with':'XMLHttpRequest',
    }    


# post_raw is the 'node' from the insta json
# data['user']['media']['nodes']
def prepare_post_data(post_raw):
    post = {}
    post = {
        'id': post_raw['id'],
        'code': post_raw['code'],
        #'img_src_url': post_raw['display_src'],
        'date': post_raw['date'],
        'n_likes': post_raw['likes']['count'],
        #'n_comments': post_raw['comments']['count'],
    }

    try:
        caption = post_raw['caption']
    except Exception as err:
        caption = ''

    post['caption'] = caption
    words = caption.split()
    tags = []
    user_tags = []
    for word in words:
        if word[0] == '#':
            tags.extend(word[1:].split('#'))
        if word[0] == '@':
            user_tags.extend(word[1:].split('@'))

    post['tags'] = tags
    #post['user_tags'] = user_tags

    #post['comments'] = []
    #post['_comments_nextCursor'] = None
    #post['_comments_fetchStatus'] = None

    return post


def get_complete_posts_of_user_NEW(username, nr_posts=12, with_next=False, next=1, 
    with_timestamp=False, timestamp=None, ts_include=False):

    if with_timestamp and with_next:
        print('ERROR in get_complete_posts_of_user_NEW(): error 1')
        return None
    elif with_timestamp and timestamp == None:
        print('ERROR in get_complete_posts_of_user_NEW(): no timestamp given!')
        return None


    foo_number = None

    # simple case where we we fetch just json with GET request
    user_uri = 'https://www.instagram.com/'+username+'/'
    post_codes = []
    result = []
    post_ts = []

    if not with_next:
        obj = get_json_txt(user_uri+'?__a=1')
    else: 
        obj = get_json_txt(user_uri+'?__a=1&max_id={}'.format(next))

    data = json.loads(obj)

    nr_media = int(data['user']['media']['count'])
    if not with_next:
        if nr_media < nr_posts:
            nr_posts = nr_media
        if not with_timestamp:
            print('Fetching '+str(nr_posts)+' posts of user: ', username)    
        else:
            print('Fetching posts until timestamp for user: ', username) 

    found_last_date = False

    # nodes from the first page
    nodes = data['user']['media']['nodes']
    for node in nodes:
        post = prepare_post_data(node)
        date = datetime.datetime.utcfromtimestamp(post['date'])
        date = date.replace(tzinfo=pytz.UTC)
        if date < timestamp:
            found_last_date = True
            break
        result.append(post)
        post_codes.append(node['code'])
        post_ts.append(float(node['date']))

    # in this case we return only nodes from the first page 
    if with_next:
        print('DEBUG: 1st case')
        # we need only first page but with cursos
        return post_codes, result, data['user']['media']['page_info']['end_cursor']
    elif data['user']['media']['page_info']['has_next_page'] == False or found_last_date:
        # no next cursor needed but there is also no more media to load or we have found all up to this timestamp
        print('DEBUG: 2nd case')
        if ts_include:
            return post_codes, post_ts
        else:
            return post_codes, result
    else:
        # no next cursor needed and there is more media to load
        print('DEBUG: 3th case')

        url = 'https://www.instagram.com/query/'
        userid = data['user']['id']
        headers = user_headers(userid)
        chunk_size = '200'
        #foo_number = '1351725610321594806'

        while len(result) < nr_posts or (not found_last_date and with_timestamp):
            foo_number = str(nodes[-1]['id'])

            q = 'q=ig_user('+userid+')+%7B+media.after('+foo_number+'%2C+'+chunk_size+')+%7B%0A++count%2C%0A++nodes+%7B%0A++++__typename%2C%0A++++caption%2C%0A++++code%2C%0A++++comments+%7B%0A++++++count%0A++++%7D%2C%0A++++comments_disabled%2C%0A++++date%2C%0A++++dimensions+%7B%0A++++++height%2C%0A++++++width%0A++++%7D%2C%0A++++display_src%2C%0A++++id%2C%0A++++is_video%2C%0A++++likes+%7B%0A++++++count%0A++++%7D%2C%0A++++owner+%7B%0A++++++id%0A++++%7D%2C%0A++++thumbnail_src%2C%0A++++video_views%0A++%7D%2C%0A++page_info%0A%7D%0A+%7D&ref=users%3A%3Ashow&query_id=17849115430193904'

            r = requests.post(url, headers=headers, data=q)

            data = json.loads(r.text)
            nodes = data['media']['nodes']
            for node in nodes:
                post = prepare_post_data(node)
                date = datetime.datetime.utcfromtimestamp(post['date'])
                date = date.replace(tzinfo=pytz.UTC)
                if date < timestamp:
                    found_last_date = True
                    break
                result.append(post)
                post_codes.append(node['code'])
                post_ts.append(float(node['date']))

            if not with_timestamp:
                print('Fetched ', 100.0*(len(result)/nr_posts), '% of posts')

            if data['media']['page_info']['has_next_page'] == False:
                break

        if with_timestamp:
            if ts_include:
                return post_codes, post_ts
            else:
                return post_codes, result
        else:
            return post_codes[:nr_posts], result[:nr_posts]


                    





settings.configure(USE_TZ = True)
USE_TZ = True

ts = timezone.now() - datetime.timedelta(days=14)#, minutes=55)
postcodes, posts = get_complete_posts_of_user_graphql('natgeo', with_timestamp=True, timestamp=ts)   

print('In Total Fetched ', len(posts), ' posts')

#for post in posts:
#    print()
#    print(post) 