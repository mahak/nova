# Copyright 2013 Cloudbase Solutions Srl
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import copy
from unittest import mock

import webob

from nova.api.openstack import api_version_request
from nova.api.openstack.compute import console_auth_tokens \
    as console_auth_tokens_v21
from nova import exception
from nova import objects
from nova import test
from nova.tests.unit.api.openstack import fakes


class ConsoleAuthTokensExtensionTestV21(test.NoDBTestCase):
    controller_class = console_auth_tokens_v21

    _EXPECTED_OUTPUT = {
        'console': {
            'instance_uuid': fakes.FAKE_UUID,
            'host': 'fake_host',
            'port': '1234',
            'internal_access_path': fakes.FAKE_UUID,
        }
    }
    _EXPECTED_OUTPUT_SPICE = {
        'console': {
            'instance_uuid': fakes.FAKE_UUID,
            'host': 'fake_host',
            'port': '5900',
            'tls_port': '5901',
            'internal_access_path': None
        }
    }

    # The database backend returns a ConsoleAuthToken.to_dict() and o.vo
    # StringField are unicode. And the port is an IntegerField.
    _EXPECTED_OUTPUT_DB = copy.deepcopy(_EXPECTED_OUTPUT)
    _EXPECTED_OUTPUT_DB['console'].update(
        {'host': 'fake_host', 'port': 1234,
         'internal_access_path': fakes.FAKE_UUID})

    _EXPECTED_OUTPUT_DB_SPICE = copy.deepcopy(_EXPECTED_OUTPUT_SPICE)
    _EXPECTED_OUTPUT_DB_SPICE['console'].update(
        {'host': 'fake_host', 'port': 5900, 'tls_port': 5901})

    def setUp(self):
        super(ConsoleAuthTokensExtensionTestV21, self).setUp()
        self.controller = self.controller_class.ConsoleAuthTokensController()
        self.req = fakes.HTTPRequest.blank('', use_admin_context=True)
        self.context = self.req.environ['nova.context']

    @mock.patch.object(objects.ConsoleAuthToken, 'validate')
    def test_get_console_connect_info(self, mock_validate):
        self.assertRaises(webob.exc.HTTPBadRequest,
                          self.controller.show, self.req, fakes.FAKE_UUID)
        mock_validate.assert_not_called()


class ConsoleAuthTokensExtensionTestV231(ConsoleAuthTokensExtensionTestV21):

    def setUp(self):
        super(ConsoleAuthTokensExtensionTestV231, self).setUp()
        self.req.api_version_request = api_version_request.APIVersionRequest(
            '2.31')

    @mock.patch('nova.objects.ConsoleAuthToken.validate',
                return_value=objects.ConsoleAuthToken(
                    instance_uuid=fakes.FAKE_UUID, host='fake_host',
                    port='1234', internal_access_path=fakes.FAKE_UUID,
                    console_type='webmks',
                    token=fakes.FAKE_UUID))
    def test_get_console_connect_info(self, mock_validate):
        output = self.controller.show(self.req, fakes.FAKE_UUID)
        self.assertEqual(self._EXPECTED_OUTPUT_DB, output)
        mock_validate.assert_called_once_with(self.context, fakes.FAKE_UUID)

    @mock.patch('nova.objects.ConsoleAuthToken.validate',
                side_effect=exception.InvalidToken(token='***'))
    def test_get_console_connect_info_token_not_found(self, mock_validate):
        self.assertRaises(webob.exc.HTTPNotFound,
                          self.controller.show, self.req, fakes.FAKE_UUID)
        mock_validate.assert_called_once_with(self.context, fakes.FAKE_UUID)


class ConsoleAuthTokensExtensionTestV299(ConsoleAuthTokensExtensionTestV21):

    def setUp(self):
        super(ConsoleAuthTokensExtensionTestV299, self).setUp()
        self.req.api_version_request = api_version_request.APIVersionRequest(
            '2.99')

    @mock.patch('nova.objects.ConsoleAuthToken.validate',
                return_value=objects.ConsoleAuthToken(
                    instance_uuid=fakes.FAKE_UUID, host='fake_host',
                    port='1234', internal_access_path=fakes.FAKE_UUID,
                    console_type='webmks', token=fakes.FAKE_UUID))
    def test_get_console_connect_info(self, mock_validate):
        output = self.controller.show(self.req, fakes.FAKE_UUID)
        self.assertEqual(self._EXPECTED_OUTPUT_DB, output)
        mock_validate.assert_called_once_with(self.context, fakes.FAKE_UUID)

    @mock.patch('nova.objects.ConsoleAuthToken.validate',
                return_value=objects.ConsoleAuthToken(
                    instance_uuid=fakes.FAKE_UUID, host='fake_host',
                    port='5900', tls_port='5901', internal_access_path=None,
                    console_type='spice-direct', token=fakes.FAKE_UUID))
    def test_get_console_connect_info_spice(self, mock_validate):
        output = self.controller.show(self.req, fakes.FAKE_UUID)
        self.assertEqual(self._EXPECTED_OUTPUT_DB_SPICE, output)
        mock_validate.assert_called_once_with(self.context, fakes.FAKE_UUID)

    @mock.patch('nova.objects.ConsoleAuthToken.validate',
                side_effect=exception.InvalidToken(token='***'))
    def test_get_console_connect_info_token_not_found(self, mock_validate):
        self.assertRaises(webob.exc.HTTPNotFound,
                          self.controller.show, self.req, fakes.FAKE_UUID)
        mock_validate.assert_called_once_with(self.context, fakes.FAKE_UUID)
