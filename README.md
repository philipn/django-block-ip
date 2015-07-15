django-block-ip
---------------

This is a simple application to restrict access by IP address.  There's a few other apps that do this out there, but they tend to have other features such as rate limiting.  I think it's best to leave rate-limiting to rate-limiting specific apps, so this just blocks IPs.

Usage
=====

1. `pip install django-block-ip`
1. Add `block_ip` to your `INSTALLED_APPS`.
1. Add `block_ip.middleware.BlockIPMiddleware` to your `MIDDLEWARE_CLASSES`.
1. Run `syncdb`.
1. Add one or more entries to the `BlockIP` list in the admin.
  You can just enter a single IP or use a network mask, like this: 213.67.43.0/24

Acknowledgments
===============

This is based on http://github.com/svetlyak40wt/django-ban, which was based on the Justquick's django snippet (http://www.djangosnippets.org/snippets/725/).
