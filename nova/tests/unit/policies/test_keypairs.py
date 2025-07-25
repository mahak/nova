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

import datetime
from unittest import mock

from oslo_utils.fixture import uuidsentinel as uuids

from nova.api.openstack.compute import keypairs
from nova import objects
from nova.policies import keypairs as policies
from nova.tests.unit.api.openstack import fakes
from nova.tests.unit.objects import test_keypair
from nova.tests.unit.policies import base


FAKE_KEYPAIR = objects.KeyPair(
    created_at=datetime.datetime(2024, 10, 29, 13, 42, 2),
    deleted=False,
    deleted_at=None,
    fingerprint='foo',
    id=123,
    name='foo',
    private_key='ssh-rsa foo',
    public_key='ssh-rsa foo',
    type='ssh',
    updated_at=None,
    user_id=uuids.user_alt_id,
)


class KeypairsPolicyTest(base.BasePolicyTest):
    """Test Keypairs APIs policies with all possible context.
    This class defines the set of context with different roles
    which are allowed and not allowed to pass the policy checks.
    With those set of context, it will call the API operation and
    verify the expected behaviour.
    """

    def setUp(self):
        super(KeypairsPolicyTest, self).setUp()
        self.controller = keypairs.KeypairController()
        self.req = fakes.HTTPRequest.blank('')

        # Check that everyone is able to create, delete and get
        # their keypairs.
        self.everyone_authorized_contexts = set([
            self.legacy_admin_context, self.system_admin_context,
            self.project_admin_context,
            self.system_member_context, self.system_reader_context,
            self.system_foo_context, self.project_manager_context,
            self.project_member_context, self.project_reader_context,
            self.project_foo_context,
            self.other_project_manager_context,
            self.other_project_member_context,
            self.other_project_reader_context,
        ])

        # Check that admin is able to create, delete and get
        # other users keypairs.
        self.admin_authorized_contexts = set([
            self.legacy_admin_context, self.system_admin_context,
            self.project_admin_context])

    @mock.patch('nova.compute.api.KeypairAPI.get_key_pairs')
    def test_index_keypairs_policy(self, mock_get):
        mock_get.return_value = objects.KeyPairList(objects=[])
        rule_name = policies.POLICY_ROOT % 'index'
        self.common_policy_auth(self.everyone_authorized_contexts,
                                rule_name,
                                self.controller.index,
                                self.req)

    @mock.patch('nova.compute.api.KeypairAPI.get_key_pairs')
    def test_index_others_keypairs_policy(self, mock_get):
        mock_get.return_value = objects.KeyPairList(objects=[])
        req = fakes.HTTPRequest.blank('?user_id=user2', version='2.10')
        rule_name = policies.POLICY_ROOT % 'index'
        self.common_policy_auth(self.admin_authorized_contexts,
                                rule_name,
                                self.controller.index,
                                req)

    @mock.patch('nova.compute.api.KeypairAPI.get_key_pair')
    def test_show_keypairs_policy(self, mock_get):
        mock_get.return_value = FAKE_KEYPAIR
        rule_name = policies.POLICY_ROOT % 'show'
        self.common_policy_auth(self.everyone_authorized_contexts,
                                rule_name,
                                self.controller.show,
                                self.req, fakes.FAKE_UUID)

    @mock.patch('nova.compute.api.KeypairAPI.get_key_pair')
    def test_show_others_keypairs_policy(self, mock_get):
        mock_get.return_value = FAKE_KEYPAIR
        # Change the user_id in request context.
        req = fakes.HTTPRequest.blank('?user_id=user2', version='2.10')
        rule_name = policies.POLICY_ROOT % 'show'
        self.common_policy_auth(self.admin_authorized_contexts,
                                rule_name,
                                self.controller.show,
                                req, fakes.FAKE_UUID)

    @mock.patch('nova.compute.api.KeypairAPI.create_key_pair')
    def test_create_keypairs_policy(self, mock_create):
        mock_create.return_value = (test_keypair.fake_keypair, 'FAKE_KEY')
        rule_name = policies.POLICY_ROOT % 'create'
        self.common_policy_auth(self.everyone_authorized_contexts,
                                rule_name,
                                self.controller.create,
                                self.req,
                                body={'keypair': {'name': 'create_test'}})

    @mock.patch('nova.compute.api.KeypairAPI.create_key_pair')
    def test_create_others_keypairs_policy(self, mock_create):
        # Change the user_id in request context.
        req = fakes.HTTPRequest.blank('', version='2.10')
        rule_name = policies.POLICY_ROOT % 'create'
        mock_create.return_value = (test_keypair.fake_keypair, 'FAKE_KEY')
        body = {'keypair': {'name': 'test2', 'user_id': 'user2'}}
        self.common_policy_auth(self.admin_authorized_contexts,
                                rule_name,
                                self.controller.create,
                                req, body=body)

    @mock.patch('nova.compute.api.KeypairAPI.delete_key_pair')
    def test_delete_keypairs_policy(self, mock_delete):
        rule_name = policies.POLICY_ROOT % 'delete'
        self.common_policy_auth(self.everyone_authorized_contexts,
                                rule_name,
                                self.controller.delete,
                                self.req, fakes.FAKE_UUID)

    @mock.patch('nova.compute.api.KeypairAPI.delete_key_pair')
    def test_delete_others_keypairs_policy(self, mock_delete):
        # Change the user_id in request context.
        req = fakes.HTTPRequest.blank('?user_id=user2', version='2.10')
        rule_name = policies.POLICY_ROOT % 'delete'
        self.common_policy_auth(self.admin_authorized_contexts,
                                rule_name,
                                self.controller.delete,
                                req, fakes.FAKE_UUID)


class KeypairsNoLegacyNoScopeTest(KeypairsPolicyTest):
    """Test Keypairs API policies with deprecated rules
    disabled, but scope checking still disabled.
    """

    without_deprecated_rules = True

    def setUp(self):
        super(KeypairsNoLegacyNoScopeTest, self).setUp()


class KeypairsScopeTypePolicyTest(KeypairsPolicyTest):
    """Test Keypairs APIs policies with system scope enabled.
    This class set the nova.conf [oslo_policy] enforce_scope to True
    so that we can switch on the scope checking on oslo policy side.
    It defines the set of context with scoped token
    which are allowed and not allowed to pass the policy checks.
    With those set of context, it will run the API operation and
    verify the expected behaviour.
    """

    def setUp(self):
        super(KeypairsScopeTypePolicyTest, self).setUp()
        self.flags(enforce_scope=True, group="oslo_policy")

        # With scope checking, only project-scoped users are allowed
        self.reduce_set('everyone_authorized', self.all_project_contexts)
        self.admin_authorized_contexts = [
            self.legacy_admin_context,
            self.project_admin_context]


class KeypairsNoLegacyPolicyTest(KeypairsScopeTypePolicyTest):
    """Test Keypairs APIs policies with system scope enabled,
    and no more deprecated rules that allow the legacy admin API to
    access system APIs.
    """
    without_deprecated_rules = True
