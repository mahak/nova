# Copyright (c) 2012 OpenStack Foundation
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

import ddt
from nova import exception
from nova.pci import whitelist
from nova import test


dev_dict = {
    'compute_node_id': 1,
    'address': '0000:00:0a.1',
    'product_id': '0001',
    'vendor_id': '8086',
    'status': 'available',
    'phys_function': '0000:00:0a.0',
    }


@ddt.ddt
class WhitelistTestCase(test.NoDBTestCase):
    def test_whitelist(self):
        white_list = '{"product_id":"0001", "vendor_id":"8086"}'
        parsed = whitelist.Whitelist([white_list])
        self.assertEqual(1, len(parsed.specs))

    def test_whitelist_list_format(self):
        white_list = '[{"product_id":"0001", "vendor_id":"8086"},'\
                       '{"product_id":"0002", "vendor_id":"8086"}]'
        parsed = whitelist.Whitelist([white_list])
        self.assertEqual(2, len(parsed.specs))

    def test_whitelist_empty(self):
        parsed = whitelist.Whitelist()
        self.assertFalse(parsed.device_assignable(dev_dict))

    def test_whitelist_multiple(self):
        wl1 = '{"product_id":"0001", "vendor_id":"8086"}'
        wl2 = '{"product_id":"0002", "vendor_id":"8087"}'
        parsed = whitelist.Whitelist([wl1, wl2])
        self.assertEqual(2, len(parsed.specs))

    def test_device_assignable_glob(self):
        white_list = '{"address":"*:00:0a.*", "physical_network":"hr_net"}'
        parsed = whitelist.Whitelist(
            [white_list])
        self.assertTrue(parsed.device_assignable(dev_dict))

    def test_device_not_assignable_glob(self):
        white_list = '{"address":"*:00:0b.*", "physical_network":"hr_net"}'
        parsed = whitelist.Whitelist(
            [white_list])
        self.assertFalse(parsed.device_assignable(dev_dict))

    def test_device_assignable_regex(self):
        white_list = ('{"address":{"domain": ".*", "bus": ".*", '
                      '"slot": "0a", "function": "[0-1]"}, '
                      '"physical_network":"hr_net"}')
        parsed = whitelist.Whitelist(
            [white_list])
        self.assertTrue(parsed.device_assignable(dev_dict))

    def test_device_not_assignable_regex(self):
        white_list = ('{"address":{"domain": ".*", "bus": ".*", '
                      '"slot": "0a", "function": "[2-3]"}, '
                      '"physical_network":"hr_net"}')
        parsed = whitelist.Whitelist(
            [white_list])
        self.assertFalse(parsed.device_assignable(dev_dict))

    def test_device_assignable(self):
        white_list = '{"product_id":"0001", "vendor_id":"8086"}'
        parsed = whitelist.Whitelist([white_list])
        self.assertTrue(parsed.device_assignable(dev_dict))

    @ddt.data(
        {"tag": "managed", "value": "yes", "expected": "true"},
        {"tag": "managed", "value": "true", "expected": "true"},
        {"tag": "managed", "value": "1", "expected": "true"},
        {"tag": "managed", "value": "no", "expected": "false"},
        {"tag": "managed", "value": "false", "expected": "false"},
        {"tag": "managed", "value": "0", "expected": "false"},
        {"tag": "live_migratable", "value": "yes", "expected": "true"},
        {"tag": "live_migratable", "value": "true", "expected": "true"},
        {"tag": "live_migratable", "value": "1", "expected": "true"},
        {"tag": "live_migratable", "value": "no", "expected": "false"},
        {"tag": "live_migratable", "value": "false", "expected": "false"},
        {"tag": "live_migratable", "value": "0", "expected": "false"},
    )
    def test_device_tags(self, data):
        wl = (
            '{"product_id":"0001", "vendor_id":"8086", "' +
            data["tag"] +
            '":"' +
            data["value"] +
            '"}'
        )
        white_list = wl
        parsed = whitelist.Whitelist([white_list])
        self.assertEqual(1, len(parsed.specs))
        self.assertEqual(parsed.specs[0].tags[data["tag"]], data["expected"])

    @ddt.data({"tag": "managed"},
              {"tag": "live_migratable"})
    def test_device_managed_not_set(self, data):
        white_list = (
            '{"product_id":"0001", "vendor_id":"8086"}'
        )
        parsed = whitelist.Whitelist([white_list])
        self.assertEqual(1, len(parsed.specs))
        self.assertNotIn(data["tag"], parsed.specs[0].tags)

    @ddt.data({"tag": "managed"},
              {"tag": "live_migratable"})
    def test_device_managed_invalid_value(self, data):
        wl = '{"product_id":"0001", "vendor_id":"8086", "' + \
            data["tag"] + '":"' + 'invalid"}'
        white_list = (wl)

        exc = self.assertRaises(
            exception.PciConfigInvalidSpec, whitelist.Whitelist, [white_list]
        )

        self.assertEqual(
            "Invalid [pci]device_spec config: Cannot parse tag "
            f"'{data['tag']}': Unrecognized value 'invalid', "
            "acceptable values are: '0', '1', 'f', 'false', 'n', 'no', 'off', "
            "'on', 't', 'true', 'y', 'yes'",
            str(exc)
        )
