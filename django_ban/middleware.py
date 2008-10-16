# realization from http://www.djangosnippets.org/snippets/725/
import logging

from django.http import HttpResponseForbidden
from django.conf import settings

from models import DenyIP, AllowIP

logger = logging.getLogger('django_ban')

splits = lambda x: x.replace(' ','').split(',')

# either 'allow,deny' 'deny,allow' or any ONE of the choices
order = getattr(settings, 'BAN_POLICY', 'allow,deny')
opts = filter(None,splits(order)[:2])


# a var you could override
forbid = HttpResponseForbidden("""
    <html>
    <head>
        <title>403 Forbidden</title>
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>This resource is unavailable at this time from this computer.</p>
    </body>
    </html>""")

def get_ip(req):
    ip = req.META['REMOTE_ADDR']
    # forwarded proxy fix for webfaction
    if (not ip or ip == '127.0.0.1') and req.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = req.META['HTTP_X_FORWARDED_FOR']
    return ip

def is_ip_in_nets(ip, nets):
    for net in nets:
        if ip in net:
            return True
    return False

class Ban(object):
    def process_request(self, request):
        # gather some info
        user = None
        if hasattr(request, 'user'):
            user = request.user
        elif request.session.has_key('_auth_user_id'):
            user = request.session['_auth_user_id']
        ip = get_ip(request)

        deny_ips = [i.getNetwork() for i in DenyIP.objects.all()]
        allow_ips = [i.getNetwork() for i in AllowIP.objects.all()]

        logger.debug(deny_ips)
        logger.debug(allow_ips)

        allow = lambda: is_ip_in_nets(ip, allow_ips)
        deny = lambda: is_ip_in_nets(ip, deny_ips)

        is_banned = True
        if opts and opts[-1] == 'allow':
            is_banned = False

        if opts:
            for opt in opts:
                if opt=='allow' and allow():
                    is_banned = False
                    break
                elif opt=='deny' and deny():
                    is_banned = True
                    break
        else:
            if allow(): is_banned = False
            elif deny(): is_banned = True

        if is_banned:
            # delete sessions when denied
            for k in request.session.keys():
                del request.session[k]
            logger.warning('Banned user from IP %s' % ip)
            return forbid

