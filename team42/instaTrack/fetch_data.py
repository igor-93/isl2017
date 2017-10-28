from lxml import html
import requests
import json  
from datetime import datetime
import traceback
import pycurl
import io
import pytz

import re   # for emojis
from collections import Counter

# for async functions
import asyncio
import aiohttp


def comments_headers(postcode):
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
        'referer':'https://www.instagram.com/p/'+postcode+'/',
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        'x-csrftoken':'zMwzbE9UFebKKB9A8lesuvZeY28oaBYv',
        'x-instagram-ajax':'1',
        'x-requested-with':'XMLHttpRequest',
    }

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


def prepare_user_data(user_raw):
    user = {}
    user['full_name'] = user_raw['full_name']
    user['id'] = user_raw['id']
    user['username'] = user_raw['username']
    user['n_follows'] = user_raw['follows']['count']
    user['n_followed_by'] = user_raw['followed_by']['count']
    user['n_posts'] = user_raw['media']['count']
    user['img_src_url'] = user_raw['profile_pic_url']
    user['is_private'] = user_raw['is_private']

    last_post_ts = None
    if user['n_posts'] > 0:
        last_post_ts = user_raw['media']['nodes'][0]['date']

    user['last_post_ts'] = last_post_ts
    return user



def prepare_comment_data(comment_raw, postcode=None):
    comment = {
        'id': comment_raw['id'],
        'post_code': postcode,
        'date': int(comment_raw['created_at']),
        'text': comment_raw['text'],
        'username': comment_raw['owner']['username'],
        'user_img_src_url': comment_raw['owner']['profile_pic_url'],
        'user_id': comment_raw['owner']['id'],
        'sentiment': 0
    }
    return comment



# post_raw is the 'node' from the insta json
# data['user']['media']['nodes']
def prepare_post_data(post_raw):
    post = {}
    post = {
        'id': post_raw['id'],
        'code': post_raw['code'],
        'img_src_url': post_raw['display_src'],
        'date': post_raw['date'],
        'n_likes': post_raw['likes']['count'],
        'n_comments': post_raw['comments']['count'],
        'comments': [],
        '_comments_nextCursor':  1,
        '_comments_fetchStatus':  None,
        '_emoji_fetchStatus': None,
        'emojis': None
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
    post['user_tags'] = user_tags

    post['comments'] = []
    post['comments_ids'] = []
    post['_comments_nextCursor'] = None
    post['_comments_fetchStatus'] = None

    return post


# gets page content as string
# Note: used only for pages that display JSON
def get_json_txt(url):
    buffer = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()

    body = buffer.getvalue().decode('UTF-8')

    return body


# check if a given user exists and if its profile is public
def check_user(username):
    user_uri = 'https://www.instagram.com/'+username+'/'
    obj = get_json_txt(user_uri+'?__a=1')
    try:
        data = json.loads(obj)
    except:
        print('ERROR in check_user(): %s DOESNT EXIST '%username)
        return False

    if data['user']['is_private']:
        print('ERROR in check_user(): %s IS PRIVATE' %username)
        return False

    return True


# TODO: remove this function later
def get_user_data(username):
    user_uri = 'https://www.instagram.com/'+username+'/'
    if check_user(username):
        obj = get_json_txt(user_uri+'?__a=1')
        data = json.loads(obj)
        result = prepare_user_data(data['user'])
    else:
        result = None

    return result



async def fetch_user_data(session, username):
    user_uri = 'https://www.instagram.com/'+username+'/?__a=1'

    #async with aiohttp.ClientSession() as session:
    #    async with sem:
    async with session.get(user_uri) as resp:
        data = await resp.json()
        result = prepare_user_data(data['user'])
        
    return result


def get_user_data_list(loop, session, usernames):
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    #sem = asyncio.Semaphore(800)


    final_result = loop.run_until_complete(
        asyncio.gather(
            *(fetch_user_data(session, username) for username in usernames)
        )
    )

    # list of user_obejcts defined above
    return final_result



def get_user_id(username):    
    user_uri = 'https://www.instagram.com/'+username+'/'
    if check_user(username):
        obj = get_json_txt(user_uri+'?__a=1')
    
        data = json.loads(obj)
        user_id = data['user']['id']
    else:
        user_id = None

    return user_id


# TODO: remove this function
#
# returns total number of posts that use this tag
# def n_posts_for_tag(tag):
#     tag_uri = 'https://www.instagram.com/explore/tags/'+tag+'/'
#     try:
#         obj = get_json_txt(tag_uri+'?__a=1')

#         n_posts = json.loads(obj)['tag']['media']['count']
#         return float(n_posts)
#     except UnicodeEncodeError:
#         return 1     


async def fetch_n_posts_for_tag( session, tag):
    tag_uri = 'https://www.instagram.com/explore/tags/'+tag+'/?__a=1'

    #async with session:
    #async with sem:
    async with session.get(tag_uri) as resp:
    #print(resp)
        try:
            data = await resp.json()
            count = float(data['tag']['media']['count'])
        except:
            count = 0.0
          
    return tag, count



# returns list of tuples: [(tag,count)]
def n_posts_for_list_of_tags(loop, session, tags):
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    #sem = asyncio.Semaphore(800)
    

    final_result = loop.run_until_complete(
        asyncio.gather(
            *(fetch_n_posts_for_tag(session, tag) for tag in tags)
        )
    )

    return final_result






def n_followers_of_user(username):
    if not check_user(username):
        return 0, 0
    user_uri = 'https://www.instagram.com/'+username+'/'
    obj = get_json_txt(user_uri+'?__a=1')

    followed_by = json.loads(obj)['user']['followed_by']['count']
    follows = json.loads(obj)['user']['follows']['count']

    return followed_by, follows


# return ALL the information about the user posts
# if with_next = True we return only one page of posts per function call
#   otherwise         we return nr_posts many posts
def get_complete_posts_of_user(username, nr_posts=21, with_next=False, next=1):
    
    user_uri = 'https://www.instagram.com/'+username+'/'
    post_codes = []
    result = []

    if not with_next:
        obj = get_json_txt(user_uri+'?__a=1')
    else: 
        obj = get_json_txt(user_uri+'?__a=1&max_id={}'.format(next))
    data = json.loads(obj)

    nr_media = data['user']['media']['count']
    if not with_next:
        if int(nr_media) < nr_posts:
            nr_posts = nr_media
        print('Fetching '+str(nr_posts)+' posts of user: ', username)    


    # nodes from the first page
    nodes = data['user']['media']['nodes']
    for node in nodes:
        post = prepare_post_data(node)
        result.append(post)
        post_codes.append(node['code'])

    # in this case we return only nodes from the first page 
    if with_next:
        return post_codes, result, data['user']['media']['page_info']['end_cursor']
            

    end_cursors = []
    stop = False

    # nodes from the next pages
    while data['user']['media']['page_info']['has_next_page']:
        end_cursors.append(data['user']['media']['page_info']['end_cursor'])
        data = json.loads(get_json_txt(user_uri+'?__a=1&max_id={}'.format(end_cursors[-1])))
        nodes = data['user']['media']['nodes']
        print(100*(len(post_codes)/nr_posts),'% ...')
        for node in nodes:
            post = prepare_post_data(node)
            post_codes.append(node['code'])
            result.append(post)
            if len(post_codes) >= nr_posts:
                stop = True
                break
            #print 'DEBUG: Nr likes: ',  node['likes']['count']

        if stop:
            break

    return post_codes[:nr_posts], result[:nr_posts]






# returns posts after the given timestamp
# if ts_include is True:
#     we return list of postcodes and a list of coresponding timestamps
# otherwise:
#     we return list of postcodes and a list of all the data related to posts
def get_posts_of_user_ts(username, timestamp, ts_include=False):
    timestamp = timestamp.replace(tzinfo=None)
    user_uri = 'https://www.instagram.com/'+username+'/'

    data = json.loads(get_json_txt(user_uri+'?__a=1'))

    post_codes = []
    post_ts = []
    result = []       # complete result
    stop = False

    # nodes from the first page
    nodes = data['user']['media']['nodes']
    for node in nodes:
        if datetime.fromtimestamp(int(node['date'])) > timestamp:
            post = {}
            post['code'] = node['code']
            post['date'] = float(node['date'])
            post['n_likes'] = node['likes']['count']
            post['n_comments'] = node['comments']['count']
            try:
                caption = node['caption']
            except Exception as err:
                #print('postcode: ',node['code'])
                #traceback.print_tb(err.__traceback__)
                caption = ''
            words = caption.split()
            tags = []
            user_tags = []
            for word in words:
                if word[0] == '#':
                    tags.extend(word[1:].split('#'))
                if word[0] == '@':
                    user_tags.extend(word[1:].split('@'))

            post['tags'] = tags
            post['user_tags'] = user_tags
            result.append(post)
            post_codes.append(node['code'])
            post_ts.append(float(node['date']))
        else:
            stop = True
            if ts_include:
                return post_codes, post_ts
            else:
                return post_codes, result
            break


    end_cursors = []

    # nodes from the next pages
    while data['user']['media']['page_info']['has_next_page']:
        end_cursors.append(data['user']['media']['page_info']['end_cursor'])
        data = json.loads(get_json_txt(user_uri+'?__a=1&max_id={}'.format(end_cursors[-1])))
        nodes = data['user']['media']['nodes']
        for node in nodes:
            if datetime.fromtimestamp(int(node['date'])) > timestamp:
                post = {}
                post['code'] = node['code']
                post['date'] = float(node['date'])
                post['n_likes'] = node['likes']['count']
                post['n_comments'] = node['comments']['count']
                try:
                    caption = node['caption']
                except Exception as err:
                    #print('postcode: ',post_code)
                    #traceback.print_tb(err.__traceback__)
                    caption = ''
                words = caption.split()
                tags = []
                user_tags = []
                for word in words:
                    if word[0] == '#':
                        tags.extend(word[1:].split('#'))
                    if word[0] == '@':
                        user_tags.extend(word[1:].split('@'))


                post['tags'] = tags
                post['user_tags'] = user_tags
                result.append(post)
                post_codes.append(node['code'])
                post_ts.append(float(node['date']))
            else:
                stop = True
                if ts_include:
                    return post_codes, post_ts
                else:
                    return post_codes, result
                break
            #print 'DEBUG: Nr likes: ',  node['likes']['count']

        if stop:
            break

    if ts_include:
        return post_codes, post_ts
    else:
        return post_codes, result



# This is a new function that will replace get_posts_of_user_ts() and get_complete_posts_of_user()
# It has 3 MODES:
#     1. give nr_post:        it returns given number of postcodes and posts of a user
#     2. with_next=True:      it fetches only the data from the 1st page starting with cursor=next
#                              (used for infinte scrolling)
#     3. with_timestamp=True  it returns postcode and posts newer than the given timestamp
#                              if ts_inluce=True it returns timestamps instead of posts
def get_complete_posts_of_user_NEW(username, nr_posts=12, with_next=False, next=1, 
    with_timestamp=False, timestamp=None, ts_include=False):

    if with_timestamp and with_next:
        print('ERROR in get_complete_posts_of_user_NEW(): error 1')
        return None
    elif with_timestamp and timestamp == None:
        print('ERROR in get_complete_posts_of_user_NEW(): no timestamp given!')
        return None
    if with_next and next==None:
        print('ERROR in get_complete_posts_of_user_NEW(): next is None!')
        #print('next = ', next)
        return [], [], None


    foo_number = None

    # simple case where we we fetch just json with GET request
    user_uri = 'https://www.instagram.com/'+username+'/'
    post_codes = []
    result = []
    post_ts = []

    if not with_next:
        obj = get_json_txt(user_uri+'?__a=1')
    else: 
        my_url = user_uri+'?__a=1&max_id={}'.format(next)
        #print('my_url: ', my_url)
        obj = get_json_txt(my_url)
        #print('obj: ', obj)

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
        date = datetime.utcfromtimestamp(post['date'])
        #date = date.replace(tzinfo=pytz.UTC)
        date = date.replace(tzinfo=None)
        if with_timestamp and date <= timestamp:
            found_last_date = True
            break
        result.append(post)
        post_codes.append(node['code'])
        post_ts.append(float(node['date']))

    has_next_page = data['user']['media']['page_info']['has_next_page']
    end_cursor = data['user']['media']['page_info']['end_cursor']
    if not has_next_page:
        end_cursor = None

    # in this case we return only nodes from the first page 
    if with_next:
        #print('DEBUG: 1st case')
        # we need only first page but with cursos
        return post_codes, result, end_cursor
    elif has_next_page == False or found_last_date:
        # no next cursor needed but there is also no more media to load or we have found all up to this timestamp
        #print('DEBUG: 2nd case')
        if ts_include:
            return post_codes, post_ts
        else:
            return post_codes, result
    else:
        # no next cursor needed and there is more media to load
        #print('DEBUG: 3th case')

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
                date = datetime.utcfromtimestamp(post['date'])
                #date = date.replace(tzinfo=pytz.UTC)
                if with_timestamp and date <= timestamp:
                    found_last_date = True
                    break
                result.append(post)
                post_codes.append(node['code'])
                post_ts.append(float(node['date']))

            if not with_timestamp:
                print('Fetched ', 100.0*(len(result)/nr_posts), '% of posts for ', username)

            if data['media']['page_info']['has_next_page'] == False:
                break

        if with_timestamp:
            if ts_include:
                return post_codes, post_ts
            else:
                return post_codes, result
        else:
            return post_codes[:nr_posts], result[:nr_posts]




# input is the instagram user ID, not instagram username
# it returns the list of usernames that we follow
def get_list_of_followings(user_id):
    res = []
    # for igor
    #res = ['sahyadri_clickers', 'world_inside', 'thecaesarshow','sledheadzzz', 'lbsept','rosgm']
    #res += ['srbija_u_slikama', 'ig_belgrade']
    #res += ['tilt.club']
    #res += ['andrew_traveler']

    url = 'https://i.instagram.com'
    headers = {
    'Host':                  'i.instagram.com',                                                                                                                      
    'X-IG-Capabilities':     '36o=',                                                                                                                               
    'Proxy-Connection':      'keep-alive',                                                                                                                           
    'Accept-Encoding':       'gzip, deflate',                                                                                                                      
    'Accept':                '*/* ',                                                                                                                                 
    'Accept-Language':       'en-CH;q=1',                                                                                                                           
    'Cookie': 'csrftoken=g7s7ELbAuhZzNk2f3CclMdrO3x37MmTA; ds_user=team4587team42; ds_user_id=5008162016; igfl=team4587team42; is_starred_enabled=yes; mid=WOUwzQAAAAENYt5vAkwMMbRpq0C-; rur=ATN; s_network=""; sessionid=IGSC8669c43d6626319480b315dd3b26fb20531575c2a1d74a872d13e58c5ce1c060%3AyjGDize5A7PCV0jWQnJGt8R0Gw2gschL%3A%7B%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A0%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_token%22%3A%225008162016%3Ac8EhzjednJIYkt1BLCcc20eNPjbHh6Ca%3A8a0351ce1d0b4e5f63f468b7f253b401e980413b0d7af1b862c6f351920e12d7%22%2C%22asns%22%3A%7B%2262.12.154.122%22%3A15623%2C%22time%22%3A1491415334%7D%2C%22_token_ver%22%3A2%2C%22_auth_user_id%22%3A5008162016%2C%22last_refreshed%22%3A1491415332.264898777%7D',            
    'Connection':            'keep-alive',                                                                                                                          
    'X-IG-Connection-Type':  'WiFi',                                                                                                                                 
    'User-Agent': 'Instagram 10.15.0 (iPhone4,1; iPhone OS 9_3_1; en_CH; en-CH; scale=2.00; gamut=normal; 640x960) AppleWebKit/420+',
    }
    full_url = 'https://i.instagram.com/api/v1/friendships/'+user_id+'/following/?rank_token=5008162016_11FB259F-B376-422C-995D-E27EBE3364D8&rank_mutual=0'
    r = requests.get(full_url, headers=headers)

    json_data = json.loads(r.text)
    users = json_data['users']
    for user in users:
        if user['is_private'] == False:
            res.append(user['username'])

    #print('get_list_of_followings(): ', res)

    return res


# ATTENTION: if we call this function multiple times, then we must display comments in the reversed order!

# this returns from comments of the given postcode 
# in order: oldest to the newest comment
# it returns new last_comment and list of comments as defined in prepare_comment_data()
# if we reached the END, the function returns None as last_comment
def get_comments(postcode, last_comment=1):
    if last_comment == 1:
        post_uri = 'https://www.instagram.com/p/'+postcode+'/'
        obj = get_json_txt(post_uri+'?__a=1')
        data = json.loads(obj)

        data = data['graphql']['shortcode_media']['edge_media_to_comment']
        #print(data)
        #start_cursor = data['media']['comments']['page_info']['start_cursor']
        #nodes = data['media']['comments']['nodes']
        start_cursor = data['page_info']['end_cursor']
        nodes = data['edges']
        res = []
        for node in nodes:
            res.append(prepare_comment_data(node['node'], postcode))

        #return start_cursor, reversed(res)
        return start_cursor, res

    elif last_comment == None:
        print('We reached the END.')
        return None, []
    else:
        headers = comments_headers(postcode)

        # for old API
        #q = 'q=ig_shortcode('+postcode+')+%7B%0A++comments.before(%0A++++++++++++'+last_comment+'%2C%0A++++++++++++20%0A++++++++++)+%7B%0A++++count%2C%0A++++nodes+%7B%0A++++++id%2C%0A++++++created_at%2C%0A++++++text%2C%0A++++++user+%7B%0A++++++++id%2C%0A++++++++profile_pic_url%2C%0A++++++++username%0A++++++%7D%0A++++%7D%2C%0A++++page_info%0A++%7D%0A%7D%0A&ref=media%3A%3Ashow&query_id=17867562154006893'

        q = 'query_id=17852405266163336&shortcode='+postcode+'&first=20&after='+last_comment

        full_url = 'https://www.instagram.com/graphql/query/'
        r = requests.post(full_url, headers=headers, data=q)

        data = json.loads(r.text)
        #print(data)
        data = data['data']['shortcode_media']['edge_media_to_comment']
        
        #nodes = data['comments']['nodes']
        nodes = data['edges']
        start_cursor = data['page_info']['end_cursor']
        res = []
        for node in nodes:
            res.append(prepare_comment_data(node['node'], postcode))

        #return start_cursor, reversed(res)
        return start_cursor, res




async def fetch_comments_for_postcode(session, postcode, last_comment=1):
    if last_comment == 1:
        post_uri = 'https://www.instagram.com/p/'+postcode+'/?__a=1'
        #async with aiohttp.ClientSession() as session:
        #    async with sem:
        async with session.get(post_uri) as resp:
            data = await resp.json()
            data = data['graphql']['shortcode_media']['edge_media_to_comment']
            start_cursor = data['page_info']['end_cursor']
            nodes = data['edges']
            comments = []
            for node in nodes:
                ready_comment = prepare_comment_data(node['node'], postcode)
                comments.append(ready_comment)

                    
        return postcode, start_cursor, list(reversed(comments))

    elif last_comment == None:
        print('fetch_comments_for_postcode(): we reached the END.')
        return postcode, None, []

    else:
        #print('DEBUG: fetch_comments_for_postcode(): last_comment = ',last_comment)
        headers = comments_headers(postcode)

        q = 'query_id=17852405266163336&shortcode='+postcode+'&first=20&after='+last_comment

        full_url = 'https://www.instagram.com/graphql/query/'

        #async with aiohttp.ClientSession() as session:
        #    async with sem:
        async with session.post(full_url, headers=headers, data=q) as resp:
            data = await resp.json()
            #print(data)
            data = data['data']['shortcode_media']['edge_media_to_comment']

            nodes = data['edges']
            start_cursor = data['page_info']['end_cursor']
            comments = []
            for node in nodes:
                ready_comment = prepare_comment_data(node['node'], postcode)
                comments.append(ready_comment)

                   
        return postcode, start_cursor, list(reversed(comments))



# returns list of triples: [(postcode, cursor, comments)] where comments is a list of objects descirbed above
def get_comments_for_postcodes(loop, session, postcodes, cursors):

    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    #sem = asyncio.Semaphore(1000)

    final_result = loop.run_until_complete(
        asyncio.gather(
            *(fetch_comments_for_postcode(session, postcode, cursor) for postcode, cursor in zip(postcodes, cursors))
        )
    )

    # final_result is a list of triples (postcode, cursor, comments)
    return final_result



# input a search query
# returns the list of usernames and their full names
def user_search(query):
    post_uri = 'https://www.instagram.com/web/search/topsearch/?query='+query
    obj = get_json_txt(post_uri)
    data = json.loads(obj)
    nodes = data['users']
    result = []
    for node in nodes:
        n = node['user']
        if n['is_private']:
            continue
        user = {}
        user['username'] = n['username']
        user['full_name'] = n['full_name']
        result.append(user)

    return result



# PART for the emoji count

JUNK_RE = (
u'[' +
    # Supplemental Multilingual Plane
    u'\U00010000-\U0001ffff' +

    # The weird extra planes
    u'\U00030000-\U0010ffff' +

    # E000-EFFF private use area,since I noticed \ue056 (doesnt display for me)
    u'\U0000e000-\U0000efff' +


    u'\U00002500-\U00002bff' +

    # zero-width space, joiner, nonjoiner .. ZW Joiner is mentioned on Emoji wikipedia page
    # omg the ZWJ examples are downright non-heteronormative http://www.unicode.org/emoji/charts/emoji-zwj-sequences.html
    u'\U0000200B-\U0000200D' +

    # http://unicode.org/reports/tr51/
    # Certain emoji have defined variation sequences, where an emoji character can be followed by one of two invisible emoji variation selectors:
    # U+FE0E for a text presentation
    # U+FE0F for an emoji presentation
    u'\U0000fe0e-\U0000fe0f' +

u']+')

# Add optional whitespace. Because we want
# 1. A symbol surrounded by nonwhitespace => change to whitespace
# 2. A symbol surrounded by whitespace => no extra whitespace
# the current rule is too aggressive: also collapses pre-existing whitespace.
# this is ok for certain applications including ours.
SUB_RE = re.compile( r'\s*' + JUNK_RE + r'\s*', re.UNICODE)

# get the most common emojis from comments of the given post
def get_post_emojis(post_code, limit_comments=50, nr_most_common=3):
    cursor = 1   
    all_comments = []
    while cursor != None:
        cursor, comments = get_comments(post_code, cursor)
        all_comments.extend(comments)
        if len(all_comments) > limit_comments:
            break


    n_comments = min(limit_comments, len(all_comments))

    emojis_all = []
    deli = b'\\'

    for i in range(n_comments):
        text = all_comments[i]['text']
        emojis = SUB_RE.findall(text)
        comment_emojis = set([])
        for em in emojis:
            em = em.strip()
            for sym in em:
                sym_s = sym.strip()
                if sym_s:
                    comment_emojis.add(sym_s)
        emojis_all.extend(comment_emojis)

    #print('DEBUG: we read ', n_comments, ' comments')
    res = Counter(emojis_all).most_common(nr_most_common)
    return n_comments, res
