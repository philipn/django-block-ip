from django.http import HttpResponseForbidden
from django.conf import settings

from models import BlockIP


def get_ip(req):
    return req.META['REMOTE_ADDR']


def is_ip_in_nets(ip, nets):
    for net in nets:
        if ip in net:
            return True
    return False


class BlockIPMiddleware(object):
    def process_request(self, request):
        is_banned = False

        ip = get_ip(request)
        # TODO: Look into something more optimized for large numbers
        # of blocks. https://github.com/jimfunk/django-postgresql-netfields
        deny_ips = [i.get_network() for i in BlockIP.objects.all()]

        for net in deny_ips:
            if ip in net:
                is_banned = True
                break

        if is_banned:
            # delete sessions when denied
            for k in request.session.keys():
                del request.session[k]
            return HttpResponseForbidden("")
