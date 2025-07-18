# Copyright 2014 NEC Corporation.  All rights reserved.
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

from nova.api.validation import parameter_types

update = {
    'type': 'object',
    'properties': {
        'status': {
             'type': 'string',
             'enum': ['enable', 'disable',
                      'Enable', 'Disable',
                      'ENABLE', 'DISABLE'],
        },
        'maintenance_mode': {
             'type': 'string',
             'enum': ['enable', 'disable',
                      'Enable', 'Disable',
                      'ENABLE', 'DISABLE'],
        },
    },
    'anyOf': [
        {'required': ['status']},
        {'required': ['maintenance_mode']}
    ],
    'additionalProperties': False,
}

index_query = {
    'type': 'object',
    'properties': {
        'zone': parameter_types.multi_params({'type': 'string'})
    },
    # NOTE(gmann): This is kept True to keep backward compatibility.
    # As of now Schema validation stripped out the additional parameters and
    # does not raise 400. This API is deprecated in microversion 2.43 so we
    # do not to update the additionalProperties to False.
    'additionalProperties': True
}

# NOTE(stephenfin): These schemas are intentionally empty since these APIs are
# deprecated proxy APIs
startup_query = {}
shutdown_query = {}
reboot_query = {}
show_query = {}

index_response = {
    'type': 'object',
    'properties': {
        'hosts': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'host_name': {'type': 'string'},
                    # TODO(stephenfin): This should be an enum
                    'service': {'type': 'string'},
                    'zone': {'type': 'string'},
                },
                'required': ['host_name', 'service', 'zone'],
                'additionalProperties': False,
            },
        },
    },
    'required': ['hosts'],
    'additionalProperties': False,
}

show_response = {
    'type': 'object',
    'properties': {
        'host': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'resource': {
                        'type': 'object',
                        'properties': {
                            'cpu': {'type': 'integer'},
                            'disk_gb': {'type': 'integer'},
                            'host': {'type': 'string'},
                            'memory_mb': {'type': 'integer'},
                            'project': {'type': 'string'},
                        },
                        'required': [
                            'cpu', 'disk_gb', 'host', 'memory_mb', 'project'
                        ],
                        'additionalProperties': False,
                    },
                },
                'required': ['resource'],
                'additionalProperties': False,
            },
        },
    },
    'required': ['host'],
    'additionalProperties': False,
}

update_response = {
    'type': 'object',
    'properties': {
        'host': {'type': 'string'},
        'maintenance_mode': {'enum': ['on_maintenance', 'off_maintenance']},
        'status': {'enum': ['enabled', 'disabled']},
    },
    'required': ['host'],
    'additionalProperties': False,
}

_power_action_response = {
    'type': 'object',
    'properties': {
        'host': {'type': 'string'},
        # NOTE(stephenfin): This is virt driver specific and the API is
        # deprecated, so this is left empty
        'power_action': {},
    },
    'required': ['host', 'power_action'],
    'additionalProperties': False,
}

startup_response = copy.deepcopy(_power_action_response)
shutdown_response = copy.deepcopy(_power_action_response)
reboot_response = copy.deepcopy(_power_action_response)
