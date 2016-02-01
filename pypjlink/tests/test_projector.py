# -*- coding: utf-8 -*-

import hashlib
import unittest

from pypjlink.projector import Projector
from .utils import MockProjSocket


class AuthenticationTC(unittest.TestCase):

    def test_no_auth(self):
        """test detection of no auth projector"""
        no_auth_response = u'PJLINK 0\r'
        power_response = u'%1POWR=1\r'
        with MockProjSocket(no_auth_response + power_response) as mock_stream:
            proj = Projector.from_address('projhost')
            self.assertFalse(proj.authenticate(lambda: u''))
            # since projector said no auth required, I shouldn't have written
            # anything to it
            self.assertFalse(mock_stream.write.called)

    def test_auth(self):
        """test authentication"""
        auth_response = u'PJLINK 1 00112233\r'
        power_response = u'%1POWR=1\r'

        with MockProjSocket(auth_response + power_response) as mock_stream:
            proj = Projector.from_address('projhost')
            self.assertTrue(proj.authenticate(lambda: u'p'))
            # test write of authentication
            self.assertEqual(
                mock_stream.written,
                self._md5_auth_code('00112233', 'p') + '%1POWR ?\r')

    def test_wrong_auth(self):
        """test failed authentication"""
        response = (
            u'PJLINK 1 00112233\r'
            u'PJLINK ERRA\r'
        )

        with MockProjSocket(response) as mock_stream:
            proj = Projector.from_address('projhost')
            self.assertFalse(proj.authenticate(lambda: u'p'))
            self.assertEqual(
                mock_stream.written,
                self._md5_auth_code('00112233', 'p') + '%1POWR ?\r')

    def _md5_auth_code(self, salt, password):
        return hashlib.md5((salt + password).encode('utf-8')).hexdigest()
