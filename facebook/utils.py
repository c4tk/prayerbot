import json

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