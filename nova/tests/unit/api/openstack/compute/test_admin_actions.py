#   Copyright 2011 OpenStack Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

from nova.api.openstack.compute import admin_actions
from nova.tests.unit.api.openstack.compute import admin_only_action_common


class AdminActionsTest(admin_only_action_common.CommonTests):

    def setUp(self):
        super().setUp()
        self.controller = admin_actions.AdminActionsController()
        self.compute_api = self.controller.compute_api

    def test_actions(self):
        actions = ['_inject_network_info']
        method_translations = {'_inject_network_info': 'inject_network_info'}

        self._test_actions(
            actions, method_translations,
            {'_inject_network_info': {'injectNetworkInfo': None}})

    def test_actions_with_non_existed_instance(self):
        actions = ['_inject_network_info']
        self._test_actions_with_non_existed_instance(
            actions,
            {'_inject_network_info': {'injectNetworkInfo': None}})

    def test_actions_with_locked_instance(self):
        actions = ['_inject_network_info']
        method_translations = {'_inject_network_info': 'inject_network_info'}

        self._test_actions_with_locked_instance(
            actions, method_translations,
            {'_inject_network_info': {'injectNetworkInfo': None}})
