# Copyright 2011 OpenStack Foundation
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

from nova.api.openstack import api_version_request
from nova.api.openstack.compute.schemas import versions as schema
from nova.api.openstack.compute.views import versions as views_versions
from nova.api.openstack import wsgi
from nova.api import validation


LINKS = {
   'v2.0': {
       'html': 'http://docs.openstack.org/'
    },
   'v2.1': {
       'html': 'http://docs.openstack.org/'
    },
}


VERSIONS = {
    "v2.0": {
        "id": "v2.0",
        "status": "SUPPORTED",
        "version": "",
        "min_version": "",
        "updated": "2011-01-21T11:33:21Z",
        "links": [
            {
                "rel": "describedby",
                "type": "text/html",
                "href": LINKS['v2.0']['html'],
            },
        ],
        "media-types": [
            {
                "base": "application/json",
                "type": "application/vnd.openstack.compute+json;version=2",
            }
        ],
    },
    "v2.1": {
        "id": "v2.1",
        "status": "CURRENT",
        "version": api_version_request._MAX_API_VERSION,
        "min_version": api_version_request._MIN_API_VERSION,
        "updated": "2013-07-23T11:33:21Z",
        "links": [
            {
                "rel": "describedby",
                "type": "text/html",
                "href": LINKS['v2.1']['html'],
            },
        ],
        "media-types": [
            {
                "base": "application/json",
                "type": "application/vnd.openstack.compute+json;version=2.1",
            }
        ],
    }
}


@validation.validated
class Versions(wsgi.Resource):

    # The root version API isn't under the microversion control.
    support_api_request_version = False

    def __init__(self):
        super(Versions, self).__init__(None)

    @validation.query_schema(schema.show_query)
    @validation.response_body_schema(schema.index_response)
    def index(self, req, body=None):
        """Return all versions."""
        builder = views_versions.get_view_builder(req)
        return builder.build_versions(VERSIONS)

    @wsgi.response(300)
    @validation.query_schema(schema.multi_query)
    @validation.response_body_schema(schema.multi_response)
    def multi(self, req, body=None):
        """Return multiple choices."""
        builder = views_versions.get_view_builder(req)
        return builder.build_choices(VERSIONS, req)

    def get_action_args(self, request_environment):
        """Parse dictionary created by routes library."""
        args = {}
        if request_environment['PATH_INFO'] == '/':
            args['action'] = 'index'
        else:
            args['action'] = 'multi'

        return args


@validation.validated
class VersionsV2(wsgi.Resource):

    def __init__(self):
        super(VersionsV2, self).__init__(None)

    # NOTE(stephenfin): Despite being called index, this is actually called as
    # a show action
    @validation.query_schema(schema.show_query)
    @validation.response_body_schema(schema.show_response)
    def index(self, req, body=None):
        builder = views_versions.get_view_builder(req)
        ver = 'v2.0' if req.is_legacy_v2() else 'v2.1'
        return builder.build_version(VERSIONS[ver])

    def get_action_args(self, request_environment):
        """Parse dictionary created by routes library."""
        return {'action': 'index'}
