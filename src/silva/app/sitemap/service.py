# Copyright (c) 2012 Infrae. All rights reserved.
# See also LICENSE.txt

from five import grok

from silva.core.services.base import SilvaService
from .interfaces import ISitemapService


class SitemapService(SilvaService):
	grok.name('service_sitemap')
	grok.implements(ISitemapService)
	meta_type = "Silva Sitemap Service"
	silvaconf.icon('static/sitemap.png')

    manage_options = (
        {'label': 'Edit', 'action': 'manage_main'},
        ) + SilvaService.manage_options
