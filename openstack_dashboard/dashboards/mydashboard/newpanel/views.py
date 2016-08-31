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

from horizon import exceptions
from horizon import tables
import json

from openstack_dashboard.dashboards.mydashboard.newpanel import tables as log_nova_api_tables

class Log:
	def __init__(self, log_id, name):
	# def __init__(self, log_id, time, pid, level):
		self.id = log_id
		self.name = name
	# 	self.pid = pid
	# 	self.level = level

class IndexView(tables.DataTableView):
    # A very simple class-based view...
    table_class = log_nova_api_tables.LogNovaTable
    template_name = 'mydashboard/newpanel/index.html'
    page_title = _("Log nova api")

    # def get_context_data(self, **kwargs):
    #     context = super(IndexView, self).get_context_data(**kwargs)
    #     return context

    def get_data(self):
        # obj = '[{"id": 1, "time": "2015-11-14 00:23:46.664", "pid": 4180, "level": "INFO"}, {"id": 2, "time": "2015-11-14 00:23:46.889", "pid": 4191, "level": "ERROR"}, {"id": 3, "time": "2015-11-14 00:23:47.264", "pid": 4200, "level": "INFO"}, {"id": 4, "time": "2015-11-14 00:23:48.664", "pid": 4180, "level": "WARNING"}, {"id": 5, "time": "2015-11-14 00:23:48.964", "pid": 4191, "level": "INFO"}]'
        # logs = json.loads(obj)
        # context = []
        # for log in logs:
        #     context.append(Log(log['id'], log['time'], log['pid'], log['level']))

        l1 = Log( 1,"INFO")
        l2 = Log(2,"ERROR")
        context = [l1,l2]
        return context
