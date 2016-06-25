#-*- encoding: utf-8 -*-
import json
import mock
import unittest

from facebook import user_utils

user_id = "1282323984273"

class JSONData():
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data

class FacebookUserUtilsTestSuite(unittest.TestCase):

    @mock.patch('requests.get')
    def test_user_name(self, mock_get):
        mock_get.return_value = JSONData({"id": user_id, "name": "john"})
        assert "john" == user_utils.user_name(user_id)

    @mock.patch('requests.get')
    def test_user_name_with_first_name(self, mock_get):
        mock_get.return_value = JSONData({"id": user_id, "name": "john", "first_name": "John"})
        assert "John" == user_utils.user_name(user_id)

    @mock.patch('requests.get')
    def test_user_name_with_complex_name(self, mock_get):
        mock_get.return_value = JSONData({"id": user_id, "name": "Mark William"})
        assert "Mark" == user_utils.user_name(user_id)

    @mock.patch('requests.get')
    def test_user_locale(self, mock_get):
        mock_get.return_value = JSONData({"id": user_id, "name": "john", "locale": "de_DE"})
        assert "de_DE" == user_utils.locale(user_id)

    @mock.patch('requests.get')
    def test_user_default_locale(self, mock_get):
        mock_get.return_value = JSONData({"id": user_id, "name": "john"})
        assert "pl_PL" == user_utils.locale(user_id)

    @mock.patch('requests.get')
    def test_user_img_url(self, mock_get):
        profile_pic = "http://fb.postimg.org/h12f124nkas59fk6.jpg"
        mock_get.return_value = JSONData({"id": user_id, "name": "john", "profile_pic": profile_pic})
        assert profile_pic == user_utils.img_url(user_id)

    @mock.patch('requests.get')
    def test_user_default_img_url(self, mock_get):
        mock_get.return_value = JSONData({"id": user_id, "name": "john"})
        assert "http://s32.postimg.org/hw25wtznp/def_prof_pic.jpg" == user_utils.img_url(user_id)

    @mock.patch('requests.get')
    def test_user_gender(self, mock_get):
        mock_get.return_value = JSONData({"id": user_id, "name": "jane", "gender": "female"})
        assert "female" == user_utils.gender(user_id)

    @mock.patch('requests.get')
    def test_user_default_gender(self, mock_get):
        mock_get.return_value = JSONData({"id": user_id, "name": "john"})
        assert "male" == user_utils.gender(user_id)