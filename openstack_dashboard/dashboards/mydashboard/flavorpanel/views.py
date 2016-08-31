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
from django import http
from django.http import JsonResponse

from horizon import exceptions
from horizon import tables

from openstack_dashboard import api
import json

from openstack_dashboard.dashboards.mydashboard.flavorpanel import tables as flavor_tables


class IndexView(tables.DataTableView):
    # A very simple class-based view...
    # tab_group_class = mydashboard_tabs.MypanelTabs
    table_class = flavor_tables.FlavorsTable
    template_name = 'mydashboard/flavorpanel/index.html'
    page_title = _("Flavor")

    def get_context_data(self, **kwargs):
        # Add data to the context here...
        context = super(IndexView, self).get_context_data(**kwargs)
        context['demo'] = "Controller=1|Compute=2|Object Storage=3|Block Storage=4"
        # abc = {}
        # abc["series"] = [
        #       {
        #         "name": "instance-00000005",
        #         "data": [
        #           {"y": 171, "x": "2013-08-21T11:22:25"},
        #           {"y": 172, "x": "2013-08-21T11:22:26"}
        #         ]
        #       }, {
        #         "name": "instance-00000006",
        #         "data": [
        #           {"y": 161, "x": "2013-08-21T11:22:25"},
        #           {"y": 162, "x": "2013-08-21T11:22:26"}
        #         ]
        #       }
        #     ]
        # abc["settings"] = {}
        dataTest = {
            "series": [
              {
                "name": "instance-00000005",
                "data": [
                  {"y": 171, "x": "2013-08-21T11:22:25"},
                  {"y": 172, "x": "2013-08-21T11:22:26"}
                ]
              }, {
                "name": "instance-00000006",
                "data": [
                  {"y": 161, "x": "2013-08-21T11:22:25"},
                  {"y": 162, "x": "2013-08-21T11:22:26"}
                ]
              }
            ],
            "settings": {}
        }
        context['dataLineChar'] = json.dumps(dataTest,ensure_ascii=False)
        return context

    # def has_prev_data(self, table):
    #     return self._prev
    #
    # def has_more_data(self, table):
    #     return self._more

    def get_data(self):
        request = self.request
        prev_marker = request.GET.get(
            flavor_tables.FlavorsTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = request.GET.get(
                flavor_tables.FlavorsTable._meta.pagination_param, None)
        reversed_order = prev_marker is not None
        flavors = []
        try:
            # Removing the pagination params and adding "is_public=None"
            # will return all flavors.
            flavors, self._more, self._prev = api.myapi.flavor_list_paged(
                request, None,
                marker=marker,
                paginate=True,
                sort_dir='asc',
                sort_key='name',
                reversed_order=reversed_order)
        except Exception:
            self._prev = self._more = False
            exceptions.handle(request,
                              _('Unable to retrieve flavor list.'))

        return flavors
