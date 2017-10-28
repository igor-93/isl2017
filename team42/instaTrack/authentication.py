from django.http import HttpResponseRedirect
import requests
import json

CLIENT_ID = "b33eae2ce7fb4a379a3cc190f5d12ab5"
CLIENT_SECRET = "8b3d2cfc324f4529bc6e61062b175ed1"
REDIRECT_URI = "http://127.0.0.1:8000/instaTrack/app/"
INSTA_AUTH_URL = "https://api.instagram.com/oauth/authorize/?client_id=" +\
                 CLIENT_ID +\
                 "&redirect_uri=" + \
                 REDIRECT_URI + \
                 "&response_type=code"
INSTA_REQUEST_TOKEN = "https://api.instagram.com/oauth/access_token/?"

# Not returning true even though there may be some error
def get_token(request):
    """Requests access_token from instagram
    
    The functions tries to fetch the 'code' put by Instagram in the http address, and then using that code a POST request
    is made to receive the token. Then the token is saved in the database. If the code is not in the http adress the user
    is redirected to the Instagram log in page to authorise us to get the token, then in a second call of this function 
    the code is extracted. In case the code is there, but it's already used by Instagram, a new request is performed.
    Please see views.py/app(request) to learn how to use this function properly
    :param request: HttpRequest object of view.py
    :return: Either the HttpResponseRedirect to Instagram or nothing if there is nothing else to do
    """
    response = _get_raw_token_from_code(request)
    if(not response):
        return _direct_to_instagram_log_in()


    if(_request_succeeded(response)):
        request.user.userprofile.set_token(_get_access_token_from_res(response))
        return

    if(_code_is_already_used(response)):
        return _direct_to_instagram_log_in()


def _direct_to_instagram_log_in():
    """Redirects the user to Instagram authentication URL to allow us access their account"""
    return HttpResponseRedirect(INSTA_AUTH_URL)

def _get_raw_token_from_code(request):
    """Make a POST request with the 'code' extracted from http address to get the token
    
    :param request: HttpRequest object of view.py
    :return: The response turned back by Instagram. If the code does not exist, returns empty.
    """
    code = request.GET.get('code')
    if(not code):
        return code

    payload = {'client_id': CLIENT_ID,
               'client_secret':CLIENT_SECRET,
               'grant_type':'authorization_code',
               'redirect_uri': REDIRECT_URI,
               'code': code}
    resp = requests.post(INSTA_REQUEST_TOKEN, data= payload)
    response = json.loads(resp.text)
    return response

def _code_is_already_used(response):
    """If response contains an error indicating the code has been already used"""
    if(not _request_succeeded(response)):
        return response['error_message'] == 'Matching code was not found or was already used.'
    return False

def _access_is_denied_by_user(response):
    if(not _request_succeeded(response)):
        return response['error'] == 'access_denied'
    return False

def _request_succeeded(response):
    """If there is no error message in the response"""
    if 'error_type' in response:
        print(response['error_message'])
        return False
    return True


def _get_access_token_from_res(response):
    """Extract the access_token from the response"""
    if(not _request_succeeded(response)):
        return []
    access_token = response['access_token']
    return access_token

def _get_username_from_res(response):
    """Extract the username from the response"""
    if(not _request_succeeded(response)):
        return []
    username = response['user']['username']
    return username

def _get_user_id_from_res(response):
    """Extract the user_id from the response"""
    if(not _request_succeeded(response)):
        return []
    user_id = response['user']['id']
    return user_id