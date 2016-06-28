import os
import requests

GRAPH_API_URL = '/v2.6/'

def _get_user_data(user_id):
    access_token = os.environ.get('ACCESS_TOKEN')
    return requests.get('https://graph.facebook.com'+ GRAPH_API_URL + str(user_id), params={'access_token': access_token }).json()

def user_name(user_id):
    data = _get_user_data(user_id)
    if ('first_name' in data):
        return data['first_name'].encode("utf-8")
    else:
        if ('name' in data):
            return data['name'].split(' ')[0].encode("utf-8")
        else:
            raise NameError('Name not found in data provided')

def img_url(user_id):
    try:
        return _get_user_data(user_id)['profile_pic']
    except Exception as e:
        return 'http://s32.postimg.org/hw25wtznp/def_prof_pic.jpg'

def locale(user_id):
    try:
        return _get_user_data(user_id)['locale']
    except Exception as e:
        return 'pl_PL'

def gender(user_id):
    try:
        return _get_user_data(user_id)['gender']
    except Exception as e:
        return 'male'
