import pycurl, json, requests
import io



def get_json_txt(url):
    buffer = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()

    body = buffer.getvalue().decode('UTF-8')

    return body



def get_comments(postcode, last_comment=1):
	if last_comment == 1:
		post_uri = 'https://www.instagram.com/p/'+postcode+'/'
		obj = get_json_txt(post_uri+'?__a=1')
		data = json.loads(obj)

		start_cursor = data['media']['comments']['page_info']['start_cursor']
		nodes = data['media']['comments']['nodes']
		res = []
		for node in nodes:
			res.append(node['text'])

		return start_cursor, reversed(res)

	elif last_comment == None:
		print('We reached the END.')
		return None, []
	else:
		headers = {
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

		q = 'q=ig_shortcode('+postcode+')+%7B%0A++comments.before(%0A++++++++++++'+last_comment+'%2C%0A++++++++++++20%0A++++++++++)+%7B%0A++++count%2C%0A++++nodes+%7B%0A++++++id%2C%0A++++++created_at%2C%0A++++++text%2C%0A++++++user+%7B%0A++++++++id%2C%0A++++++++profile_pic_url%2C%0A++++++++username%0A++++++%7D%0A++++%7D%2C%0A++++page_info%0A++%7D%0A%7D%0A&ref=media%3A%3Ashow&query_id=17867562154006893'

		full_url = 'https://www.instagram.com/query/'
		r = requests.post(full_url, headers=headers, data=q)

		json_data = json.loads(r.text)
		#print(json_data)
		nodes = json_data['comments']['nodes']
		start_cursor = json_data['comments']['page_info']['start_cursor']
		res = []
		for node in nodes:
			res.append(node['text'])

		return start_cursor, reversed(res)


#last_comment = 'AQC1dR4j-vwtDrgtxOL45p8IZeohHNcwPvNqWSQIVTbpy2Qw3sw7GUp9t9XGEvOSwYSX4NYwhDcWQUueKn7v5HJQHnV1Sx5MH2UkVbQ9aMDuuw'	

postcode = 'BSK8UqPDc1j'
# this print from newest to the oldest comment
start, res = get_comments(postcode, 1)
for r in res:
	print(r)
start, res = get_comments(postcode, start)
for r in res:
	print(r)
start, res = get_comments(postcode, start)
for r in res:
	print(r)