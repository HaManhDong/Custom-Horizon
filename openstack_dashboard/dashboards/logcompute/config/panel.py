from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.logcompute import dashboard

class Config(horizon.Panel):
    name = _("Config")
    slug = "config"



dashboard.LogManagement.register(Config)
