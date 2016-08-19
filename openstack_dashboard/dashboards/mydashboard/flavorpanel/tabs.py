from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.mydashboard.flavorpanel import tables


class FlavorTab(tabs.TableTab):
    name = _("Flavors Tab")
    slug = "flavors_tab"
    table_classes = (tables.FlavorsTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_flavors_data(self):
        try:
            marker = self.request.GET.get(
                        tables.FlavorsTable._meta.pagination_param, None)

            flavors, self._has_more = api.nova.server_list(
                self.request,
                search_opts={'marker': marker, 'paginate': True})

            return flavors
        except Exception:
            self._has_more = False
            error_message = _('Unable to get flavors')
            exceptions.handle(self.request, error_message)

            return []

class MypanelTabs(tabs.TabGroup):
    slug = "mypanel_tabs"
    tabs = (FlavorTab,)
    sticky = True