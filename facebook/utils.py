import json

from facebook.api import FacebookApi


def _update_button_type(buttonJson):
    buttonJson['type'] = 'postback'
    return buttonJson

def _update_button_type_in_element(elementJson):
    if 'buttons' in elementJson:
        buttons = elementJson['buttons']
        postback_buttons = map(_update_button_type, buttons)
        elementJson['buttons'] = postback_buttons
    return elementJson

def response_text(text):
    return json.dumps({'text': text})

def response_buttons(text, buttons):
    postback_buttons = map(_update_button_type, buttons)
    return json.dumps({
        'attachment': {
            'type': 'template',
            'payload': {
                'template_type': 'button',
                'text': text,
                'buttons': postback_buttons
            }
        }
    })

def quick_buttons(text, buttons):
    return json.dumps({
        'text': text,
        'quick_replies': buttons
      })

def response_multiple_bubbles_buttons(texts_list, buttons_set ):
    elements = []
    for i in range(0, len(texts_list)):
        postback_button = map(_update_button_type, buttons_set[i])
        text = texts_list[i]
        if elements:
            elements.append( {
                        'title': text,
                        'buttons': postback_button
                    } )
        else:
            elements = [ {
                        'title': text,
                        'buttons': postback_button
                    } ]

    return response_elements( elements )


def response_elements(elements):
    postback_elements = map(_update_button_type_in_element, elements)
    return json.dumps({
        'attachment': {
            'type': 'template',
            'payload': {
                'template_type': 'generic',
                'elements': postback_elements
            }
        }
    })

def send_greeting_text_config():
    api = FacebookApi()
    response = json.dumps({
        'setting_type': 'greeting',
        'greeting': {
            'text': 'Hi {{user_first_name}}. I am a Prayer helper bot.'
        }
    })
    api.post('/me/thread_settings', response)
