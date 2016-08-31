from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.logcompute import dashboard

class Overview(horizon.Panel):
    name = _("Overview")
    slug = 'overview'
    permissions = ('openstack.roles.admin',)


dashboard.LogManagement.register(Overview)
