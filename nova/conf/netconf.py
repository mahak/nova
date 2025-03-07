# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# Copyright 2012 Red Hat, Inc.
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

import socket

from oslo_config import cfg
from oslo_utils import netutils


netconf_opts = [
    cfg.StrOpt("my_ip",
        default=netutils.get_my_ipv4(),
        sample_default='<host_ipv4>',
        help="""
The IP address which the host is using to connect to the management network.

Possible values:

* String with valid IP address. Default is IPv4 address of this host.

Related options:

* my_block_storage_ip
* my_shared_fs_storage_ip
"""),
    cfg.StrOpt("my_block_storage_ip",
        default="$my_ip",
        help="""
The IP address which is used to connect to the block storage network.

Possible values:

* String with valid IP address. Default is IP address of this host.

Related options:

* my_ip - if my_block_storage_ip is not set, then my_ip value is used.
"""),
    cfg.StrOpt("my_shared_fs_storage_ip",
        default="$my_ip",
        help="""
The IP address which is used to connect to the shared_fs storage (manila)
network.

Possible values:

* String with valid IP address. Default is IP address of this host.

Related options:

* my_ip - if my_shared_fs_storage_ip is not set, then my_ip value is used.
"""),
    cfg.HostDomainOpt("host",
        default=socket.gethostname(),
        sample_default='<current_hostname>',
        help="""
Hostname, FQDN or IP address of this host.

Used as:

* the oslo.messaging queue name for nova-compute worker
* we use this value for the binding_host sent to neutron. This means if you use
  a neutron agent, it should have the same value for host.
* cinder host attachment information

Must be valid within AMQP key.

Possible values:

* String with hostname, FQDN or IP address. Default is hostname of this host.
"""),
    # TODO(sfinucan): This option is tied into the VMWare and Libvirt drivers.
    # We should remove this dependency by either adding a new opt for each
    # driver or simply removing the offending code. Until then we cannot
    # deprecate this option.
    cfg.BoolOpt("flat_injected",
        default=False,
        help="""
This option determines whether the network setup information is injected into
the VM before it is booted. While it was originally designed to be used only
by nova-network, it is also used by the vmware virt driver to control whether
network information is injected into a VM. The libvirt virt driver also uses it
when we use config_drive to configure network to control whether network
information is injected into a VM.
"""),
]


def register_opts(conf):
    conf.register_opts(netconf_opts)


def list_opts():
    return {'DEFAULT': netconf_opts}
