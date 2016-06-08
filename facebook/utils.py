import json
import os
import requests

GRAPH_API_URL = '/v2.6/'

def response_text(text):
    return json.dumps({"text": text})

def response_buttons(text, buttons):
    return json.dumps({
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"button",
                "text": text,
                "buttons": buttons
            }
        }
    })

def response_elements(elements):
    return json.dumps({
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"generic",
                "elements": elements
            }
        }
    })

def get_user_data(user_id):
    access_token = os.environ.get('ACCESS_TOKEN')
    return requests.get('https://graph.facebook.com'+ GRAPH_API_URL + str(user_id), params={'access_token': access_token }).json()

def user_name(user_id):
    data = get_user_data(user_id)
    if ('first_name' in data):
        return data['first_name'].encode("utf-8")
    else:
        if ('name' in data):
            return data['name'].split(' ')[0].encode("utf-8")
        else:
            raise NameError('Name not found in data provided')

def get_img_url(user_id):
    try:
        return get_user_data(user_id)['profile_pic']
    except Exception as e:
        return 'http://s32.postimg.org/hw25wtznp/def_prof_pic.jpg'

def get_user_locale(user_id):
    return get_user_data(user_id)['locale']
