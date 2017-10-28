import requests
import json
import pprint


SERVER_URL = 'http://localhost:9000'
PROPERTIES = '{"annotators":"sentiment", "ssplit.eolonly":"true", "outputFormat":"json"}'


comment="It sucks. I hate it. Beautiful day today.\n"


r = requests.post(SERVER_URL, params={'properties': PROPERTIES}, data=comment)

#data = json.loads(r.text)


print(json.dumps(r.json(), indent=2))