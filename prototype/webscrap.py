from lxml import html
import requests
import json  
import pycurl
#from StringIO import StringIO
import datetime
from django.utils import timezone
from django.conf import settings
import io
import re   # for emojis
from collections import Counter


# gets page content as string
# Note: used only for pages that display JSON
def get_json_txt(url):
	page = requests.get(url)
	return str(page.content, 'utf-8')


def get_json_pycurl(url):
	buffer = io.BytesIO()
	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(c.WRITEFUNCTION, buffer.write)
	c.perform()
	c.close()

	body = buffer.getvalue().decode('UTF-8')
	return body


def n_posts_for_tag(tag):
	tag_uri = 'https://www.instagram.com/explore/tags/'+tag+'/'
	obj = get_json_txt(tag_uri+'?__a=1')

	n_posts = json.loads(obj)['tag']['media']['count']
	return  n_posts




import asyncio
#import aiofiles
import aiohttp


async def fetch_n_tags(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()



async def main_n_tags(tag):
	tag_uri = 'https://www.instagram.com/explore/tags/'+tag+'/?__a=1'

	async with aiohttp.ClientSession() as session:
		async with session.get(tag_uri) as resp:
		#print(resp)
			try:
				data = await resp.json()
				count = float(data['tag']['media']['count'])
			except:
				count = 0.0
	return tag, count


tags = ['zurich', 'tag', 'belgrade', 'animal', 'paris','swiss', 'germany', 'aachen','zurich', 'mountain', 'belgrade', 'animal', 'paris','swiss', 'germany', 'aachen','zurich', 'mountain', 'belgrade', 'animal', 'paris','swiss', 'germany', 'aachen','zurich', 'mountain', 'belgrade', 'animal', 'paris','swiss', 'germany', 'aachen','zurich', 'mountain', 'belgrade', 'animal', 'paris','swiss', 'germany', 'aachen','zurich', 'mountain', 'belgrade', 'animal', 'paris','swiss', 'germany', 'aachen','zurich', 'mountain', 'belgrade', 'animal', 'paris','swiss', 'germany', 'aachen','zurich', 'mountain', 'belgrade', 'animal', 'paris','swiss', 'germany', 'aachen','zurich', 'mountain', 'belgrade', 'animal', 'paris','swiss', 'germany', 'aachen','zurich', 'mountain', 'belgrade', 'animal', 'paris','swiss', 'germany', 'aachen','zurich', 'mountain', 'belgrade', 'animal', 'paris','swiss', 'germany', 'aachen','zurich', 'mountain', 'belgrade', 'animal', 'paris','swiss', 'germany', 'aachen','zurich', 'mountain', 'belgrade', 'animal', 'paris','swiss', 'germany', 'aachen']

final_result = []

loop = asyncio.get_event_loop()
final_result = loop.run_until_complete(
    asyncio.gather(
        *(main_n_tags(tag) for tag in tags)
    )
)

d = dict(final_result)
print(d)

print(len(tags))






def n_followers_of_user(username):
	user_uri = 'https://www.instagram.com/'+username+'/'
	obj = get_json_txt(user_uri+'?__a=1')

	followed_by = json.loads(obj)['user']['followed_by']['count']
	follows = json.loads(obj)['user']['follows']['count']

	return followed_by, follows


def get_post_data(post_code):
	post_uri = 'https://www.instagram.com/p/'+post_code+'/'
	obj = get_json_txt(post_uri+'?__a=1')

	post_id = json.loads(obj)['media']['id']
	date = json.loads(obj)['media']['date']
	n_likes = json.loads(obj)['media']['likes']['count']
	n_comments = json.loads(obj)['media']['comments']['count']
	caption = json.loads(obj)['media']['caption']

	words = caption.split()
	tags = []
	user_tags = []
	for word in words:
		if word[0] == '#':
			tags.append(word[1:])
		if word[0] == '@':
			user_tags.append(word[1:])	

	return post_id, date, n_likes, n_comments, tags, user_tags


# returns post codes
def get_posts_of_user(username, nr_posts=21):
	print('Fetching '+str(nr_posts)+' posts of user: ', username)
	user_uri = 'https://www.instagram.com/'+username+'/'

	#data = json.loads(get_json_txt(user_uri+'?__a=1'))
	obj = get_json_pycurl(user_uri+'?__a=1')
	data = json.loads(obj)

	nr_media = data['user']['media']['count']
	if int(nr_media) < nr_posts:
		nr_posts = nr_media

	post_codes = []

	# nodes from the first page
	nodes = data['user']['media']['nodes']
	for node in nodes:
		post_codes.append(node['code'])


	end_cursors = []
	stop = False

	# nodes from the next pages
	while data['user']['media']['page_info']['has_next_page']:
		end_cursors.append(data['user']['media']['page_info']['end_cursor'])
		data = json.loads(get_json_txt(user_uri+'?__a=1&max_id={}'.format(end_cursors[-1])))
		nodes = data['user']['media']['nodes']
		print(100*(len(post_codes)/nr_posts),'% ...')
		for node in nodes:
			post_codes.append(node['code'])
			if len(post_codes) >= nr_posts:
				stop = True
				break
			#print 'DEBUG: Nr likes: ',  node['likes']['count']

		if stop:
			break

	return post_codes[:nr_posts]



# returns post codes
def get_complete_posts_of_user(username, nr_posts=21):
	print('Fetching '+str(nr_posts)+' posts of user: ', username)
	user_uri = 'https://www.instagram.com/'+username+'/'

	#data = json.loads(get_json_txt(user_uri+'?__a=1'))
	obj = get_json_pycurl(user_uri+'?__a=1')
	data = json.loads(obj)

	nr_media = data['user']['media']['count']
	if int(nr_media) < nr_posts:
		nr_posts = nr_media

	post_codes = []
	result = []

	# nodes from the first page
	nodes = data['user']['media']['nodes']
	for node in nodes:
		post = {}
		post['date'] = node['date']
		post['n_likes'] = node['likes']['count']
		post['n_comments'] = node['comments']['count']
		caption = node['caption']
		words = caption.split()
		tags = []
		user_tags = []
		for word in words:
			if word[0] == '#':
				tags.append(word[1:])
			if word[0] == '@':
				user_tags.append(word[1:])	


		post['tags'] = tags
		post['user_tags'] = user_tags
		post_codes.append(node['code'])
		result.append(post)


	end_cursors = []
	stop = False

	# nodes from the next pages
	while data['user']['media']['page_info']['has_next_page']:
		end_cursors.append(data['user']['media']['page_info']['end_cursor'])
		data = json.loads(get_json_txt(user_uri+'?__a=1&max_id={}'.format(end_cursors[-1])))
		nodes = data['user']['media']['nodes']
		print(100*(len(post_codes)/nr_posts),'% ...')
		for node in nodes:
			post = {}
			post['date'] = node['date']
			post['n_likes'] = node['likes']['count']
			post['n_comments'] = node['comments']['count']
			caption = node['caption']
			words = caption.split()
			tags = []
			user_tags = []
			for word in words:
				if word[0] == '#':
					tags.append(word[1:])
				if word[0] == '@':
					user_tags.append(word[1:])	


			post['tags'] = tags
			post['user_tags'] = user_tags
			post_codes.append(node['code'])
			result.append(post)
			if len(post_codes) >= nr_posts:
				stop = True
				break
			#print 'DEBUG: Nr likes: ',  node['likes']['count']

		if stop:
			break

	return post_codes[:nr_posts], result[:nr_posts]



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



# TODO: get the most common emojis from comments of the given post
def get_post_emojis(post_code, limit_posts=50):
	post_uri = 'https://www.instagram.com/p/'+post_code+'/'
	obj = get_json_txt(post_uri+'?__a=1')

	data = json.loads(obj)
	n_comments = data['media']['comments']['count']

	n_comments = limit_posts

	# counts how many comments we read, so we dont go into inf. loop
	comment_counter = 0

	emojis_all = []
	deli = b'\\'
	# nodes from the first page
	nodes = data['media']['comments']['nodes']
	for node in nodes:
		text = node['text']		

		emojis = SUB_RE.findall(text)
		for em in emojis:
			em = em.encode('unicode-escape')
			print(em)
			em = [deli+e for e in em.split(deli) if e]
			em = [str(e, 'utf-8') for e in em if len(e)>2]
			print(em)
			#print em
			emojis_all += em

		#text = SUB_RE.sub(u" ",text)

		comment_counter += 1


	end_cursors = []
	stop = comment_counter >= n_comments

	# nodes from the next pages
	while data['media']['comments']['page_info']['has_next_page']:
		if stop == True:
			break
		end_cursors.append(data['media']['comments']['page_info']['end_cursor'])
		data = json.loads(get_json_txt(post_uri+'?__a=1&max_id={}'.format(end_cursors[-1])))
		nodes = data['media']['comments']['nodes']
		for node in nodes:
			text = node['text']

			emojis = SUB_RE.findall(text)
			for em in emojis:
				em = em.encode('unicode-escape')
				#print em
				em = [deli+e for e in em.split(deli) if e]
				em = [str(e, 'utf-8') for e in em if len(e)>2]
				#print em
				emojis_all += em

			comment_counter += 1
			if comment_counter >= n_comments:
				stop = True
				break
		


	print('DEBUG: we read ', comment_counter, ' comments')
	nr_most_common = 3
	res = Counter(emojis_all).most_common(nr_most_common)
	
	return n_comments, res    




# TODO: get posts from user, but only those after certain time
# similar as get_posts_of_user but instead of number of posts, fetch until
# timestamp is higher/lower (?) then the given one
# this means store the timestamp of the last sotred post for each user that we track to the DB

# get posts from user, but only those after certain time
def get_posts_of_user_ts(username, timestamp, ts_include=False):
	timestamp = timestamp.replace(tzinfo=None)
	user_uri = 'https://www.instagram.com/'+username+'/'

	data = json.loads(get_json_txt(user_uri+'?__a=1'))

	post_codes = []
	post_ts = []
	stop = False

	# nodes from the first page
	nodes = data['user']['media']['nodes']
	for node in nodes:
		if datetime.datetime.fromtimestamp(int(node['date'])) > timestamp:
			post_codes.append(node['code'])
			post_ts.append(datetime.datetime.fromtimestamp(int(node['date'])))
		else:
			stop = True
			if ts_include:
				return post_codes, post_ts
			else:
				return post_codes
			break


	end_cursors = []

	# nodes from the next pages
	while data['user']['media']['page_info']['has_next_page']:
		end_cursors.append(data['user']['media']['page_info']['end_cursor'])
		data = json.loads(get_json_txt(user_uri+'?__a=1&max_id={}'.format(end_cursors[-1])))
		nodes = data['user']['media']['nodes']
		for node in nodes:
			if datetime.datetime.fromtimestamp(int(node['date'])) > timestamp:
				post_codes.append(node['code'])
				post_ts.append(datetime.datetime.fromtimestamp(int(node['date'])))
			else:
				stop = True
				if ts_include:
					return post_codes, post_ts
				else:
					return post_codes
				break
			#print 'DEBUG: Nr likes: ',  node['likes']['count']

		if stop:
			break

	return post_codes



# check if a given user exists and if its profile is public
def check_user(username):
	user_uri = 'https://www.instagram.com/'+username+'/'
	data = json.loads(get_json_txt(user_uri+'?__a=1'))
	if not data['user']['is_verified']:
		return False
	if data['user']['is_private']:
		return False
	
	return True





#settings.configure(USE_TZ = True)
#USE_TZ = True
#last5days = timezone.now() - datetime.timedelta(days=2)

#results, tss= get_posts_of_user_ts('natgeo', last5days, ts_include=True)

#for ts in tss:
#	print( ts)

#print(check_user('natgeo'))

# username = 'igor93bgd'
# user_uri = 'https://www.instagram.com/'+username+'/?__a=1'
# #get_json_pycurl(user_uri)
# postcodes, results = get_complete_posts_of_user('natgeo', 100)

# for res in results[:20]:
# 	print(res)




