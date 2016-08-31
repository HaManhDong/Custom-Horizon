from django.utils.translation import ugettext_lazy as _

from horizon import tables

class MyFilterAction(tables.FilterAction):
    name = "myfilter"

class LogNovaTable(tables.DataTable):
    id = tables.Column("name", verbose_name=_("Name")),
    # id = tables.Column("id", verbose_name=_("ID")),
    # time = tables.Column("time", verbose_name=_("Time")),
    # pid = tables.Column("pid", verbose_name=_("Pid")),
    # level = tables.Column("level", verbose_name=_("Level")),

    class Meta(object):
        name = "lognovaapi"
        verbose_name = _("Log nova api")
        # table_actions = (MyFilterAction,)
