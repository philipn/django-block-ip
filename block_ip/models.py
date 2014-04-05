import ipcalc

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BlockIP(models.Model):
    network = models.CharField(_('IP address or mask'), max_length=18)
    reason_for_block = models.TextField(blank=True, null=True, help_text=_("Optional reason for block"))

    def __unicode__(self):
        return 'BlockIP: %s' % self.network

    def get_network(self):
        return ipcalc.Network(self.network)

    class Meta:
        verbose_name = _('IPs & masks to ban')
        verbose_name_plural = _('IPs & masks to ban')
