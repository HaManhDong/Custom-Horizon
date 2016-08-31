from __future__ import absolute_import

import logging

from django.conf import settings

from novaclient import client as nova_client

from horizon.utils import functions as utils
from horizon.utils.memoized import memoized  # noqa
from horizon.utils.memoized import memoized_with_request  # noqa

from openstack_dashboard.api import base


LOG = logging.getLogger(__name__)

# Supported compute versions
VERSIONS = base.APIVersionManager("compute", preferred_version=2)
VERSIONS.load_supported_version(1.1, {"client": nova_client, "version": 1.1})
VERSIONS.load_supported_version(2, {"client": nova_client, "version": 2})
VERSIONS.load_supported_version(2.9, {"client": nova_client, "version": 2.9})

# API static values
INSTANCE_ACTIVE_STATE = 'ACTIVE'
VOLUME_STATE_AVAILABLE = "available"
DEFAULT_QUOTA_NAME = 'default'
INSECURE = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
CACERT = getattr(settings, 'OPENSTACK_SSL_CACERT', None)

def get_auth_params_from_request(request):
    """Extracts the properties from the request object needed by the novaclient
    call below. These will be used to memoize the calls to novaclient
    """
    return (
        request.user.username,
        request.user.token.id,
        request.user.tenant_id,
        base.url_for(request, 'compute'),
        base.url_for(request, 'identity')
    )

@memoized_with_request(get_auth_params_from_request)
def novaclient(request_auth_params):
    username, token_id, project_id, nova_url, auth_url = request_auth_params
    c = nova_client.Client(VERSIONS.get_active_version()['version'],
                           username,
                           token_id,
                           project_id=project_id,
                           auth_url=auth_url,
                           insecure=INSECURE,
                           cacert=CACERT,
                           http_log_debug=settings.DEBUG)
    c.client.auth_token = token_id
    c.client.management_url = nova_url
    return c

def update_pagination(entities, page_size, marker, sort_dir, sort_key,
                      reversed_order):
    has_more_data = has_prev_data = False
    if len(entities) > page_size:
        has_more_data = True
        entities.pop()
        if marker is not None:
            has_prev_data = True
    # first page condition when reached via prev back
    elif reversed_order and marker is not None:
        has_more_data = True
    # last page condition
    elif marker is not None:
        has_prev_data = True

    # restore the original ordering here
    if reversed_order:
        entities = sorted(entities, key=lambda entity:
                          (getattr(entity, sort_key) or '').lower(),
                          reverse=(sort_dir == 'asc'))

    return entities, has_more_data, has_prev_data

class FlavorExtraSpec(object):
    def __init__(self, flavor_id, key, val):
        self.flavor_id = flavor_id
        self.id = key
        self.key = key
        self.value = val

def flavor_get_extras(request, flavor_id, raw=False, flavor=None):
    """Get flavor extra specs."""
    if flavor is None:
        flavor = novaclient(request).flavors.get(flavor_id)
    extras = flavor.get_keys()
    if raw:
        return extras
    return [FlavorExtraSpec(flavor_id, key, value) for
            key, value in extras.items()]

@memoized
def flavor_list_paged(request, is_public=True, get_extras=False, marker=None,
                      paginate=False, sort_key="name", sort_dir="desc",
                      reversed_order=False):
    """Get the list of available instance sizes (flavors)."""
    has_more_data = False
    has_prev_data = False

    if paginate:
        if reversed_order:
            sort_dir = 'desc' if sort_dir == 'asc' else 'asc'
        page_size = utils.get_page_size(request)
        flavors = novaclient(request).flavors.list(is_public=is_public,
                                                   marker=marker,
                                                   limit=page_size + 1,
                                                   sort_key=sort_key,
                                                   sort_dir=sort_dir)
        flavors, has_more_data, has_prev_data = update_pagination(
            flavors, page_size, marker, sort_dir, sort_key, reversed_order)
    else:
        flavors = novaclient(request).flavors.list(is_public=is_public)

    if get_extras:
        for flavor in flavors:
            flavor.extras = flavor_get_extras(request, flavor.id, True, flavor)

    return (flavors, has_more_data, has_prev_data)