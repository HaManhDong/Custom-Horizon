from django.utils.translation import ugettext_lazy as _

from horizon import tables

class MyFilterAction(tables.FilterAction):
    name = "myfilter"

class FlavorsTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Flavor name"))
    vcpus = tables.Column("vcpus", verbose_name=_("VCPUs"))
    size = tables.Column("ram", verbose_name=_("Size"))
    disk = tables.Column("disk", verbose_name=_("Root disk"))
    public = tables.Column("is_public",verbose_name=_("Public"))

    class Meta(object):
        name = "flavors"
        verbose_name = _("Flavors")
        table_actions = (MyFilterAction,)