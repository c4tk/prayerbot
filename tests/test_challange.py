import pytest
import unittest
from flask import url_for

@pytest.mark.usefixtures('client_class')
class ChallengeTestSuite(unittest.TestCase):

    def test_fail_verify(self):
        assert self.client.get(url_for('webhook')).status_code == 400

    def test_verify(self):
        assert self.client.get(url_for('webhook')+'?hub.verify_token=challenge_me&hub.challenge=123').status_code == 200
