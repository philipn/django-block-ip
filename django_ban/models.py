import ipcalc

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class DenyIP(models.Model):
    network = models.CharField(_('IP network'), max_length=18)

    def __unicode__(self):
        return 'DenyIP: %s' % self.network

    def getNetwork(self):
        return ipcalc.Network(self.network)

    class Admin:
        pass

    class Meta:
        verbose_name = _('IP mask to ban')
        verbose_name_plural = _('IP masks to ban')

class AllowIP(models.Model):
    network = models.CharField(_('IP network'), max_length=18)

    def __unicode__(self):
        return 'DenyIP: %s' % self.network

    def getNetwork(self):
        return ipcalc.Network(self.network)

    class Admin:
        pass

    class Meta:
        verbose_name = _('IP mask to alow')
        verbose_name_plural = _('IP masks to allow')
