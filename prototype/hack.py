import pycurl, json, requests



user_id = '2291965097'
user_id = '43668070'
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
	print(user['username'])