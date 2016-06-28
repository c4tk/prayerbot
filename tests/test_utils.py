#-*- encoding: utf-8 -*-
import json
import unittest

from facebook import utils

class FacebookUtilsTestSuite(unittest.TestCase):

    def test_response_text(self):
        text = "unit tests are so cool"
        res = utils.response_text(text)
        assert res == json.dumps({"text": text})


    def test_response_buttons(self):
        text = "push the button"
        buttons = [
            {
                "title": "Yes",
                "payload": "press_yes"
            },
            {
                "title": "No",
                "payload": "press_no"
            },
        ]
        res = utils.response_buttons(text, buttons)
        assert res == json.dumps({"attachment": {"type": "template", "payload": {"template_type": "button", "text": text,
            "buttons": [
                {
                    "type":"postback",
                    "title": "Yes",
                    "payload": "press_yes"
                },
                {
                    "type":"postback",
                    "title": "No",
                    "payload": "press_no"
                },
            ]
        }}})

    def test_response_elements(self):
        elements = [
            {
                "title": "elem_title",
                "subtitle": "elem_subtitle",
                "buttons": [
                    {
                        "title": "button_title",
                        "payload": "button_paylod"
                    }
                ]
            },
            {
                "title": "simple_elem_title"
            }
        ]
        res = utils.response_elements(elements)
        assert res == json.dumps({"attachment": {"type": "template", "payload": {"template_type": "generic", "elements": [
            {
                "title": "elem_title",
                "subtitle": "elem_subtitle",
                "buttons": [
                    {
                        "type": "postback",
                        "title": "button_title",
                        "payload": "button_paylod"
                    }
                ]
            },
            {
                "title": "simple_elem_title"
            }
        ]}}})
