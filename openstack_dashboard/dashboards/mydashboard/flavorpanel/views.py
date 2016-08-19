# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from horizon import exceptions

from openstack_dashboard import api

from openstack_dashboard.dashboards.mydashboard.flavorpanel import tabs as mydashboard_tabs

class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = mydashboard_tabs.MypanelTabs
    template_name = 'mydashboard/flavorpanel/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context

    # def has_prev_data(self, table):
    #     return self._prev
    #
    # def has_more_data(self, table):
    #     return self._more
    #
    # def get_data(self):
    #     request = self.request
    #     prev_marker = request.GET.get(
    #         mydashboard_tabs.FlavorsTable._meta.prev_pagination_param, None)
    #
    #     if prev_marker is not None:
    #         marker = prev_marker
    #     else:
    #         marker = request.GET.get(
    #             mydashboard_tabs.FlavorsTable._meta.pagination_param, None)
    #     reversed_order = prev_marker is not None
    #     flavors = []
    #     try:
    #         # Removing the pagination params and adding "is_public=None"
    #         # will return all flavors.
    #         flavors, self._more, self._prev = api.nova.flavor_list_paged(
    #             request, None,
    #             marker=marker,
    #             paginate=True,
    #             sort_dir='asc',
    #             sort_key='name',
    #             reversed_order=reversed_order)
    #     except Exception:
    #         self._prev = self._more = False
    #         exceptions.handle(request,
    #                           _('Unable to retrieve flavor list.'))
    #     return flavors
