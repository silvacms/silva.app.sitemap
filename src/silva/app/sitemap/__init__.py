# Copyright (c) 2012 Infrae. All rights reserved.
# See also LICENSE.txt

from silva.core import conf as silvaconf
from silva.core.conf.installer import DefaultInstaller

from .interfaces import ISitemapService

silvaconf.extension_name("silva.app.sitemap")
silvaconf.extension_title("Silva Sitemaps")


class SilvaSitemapInstaller(DefaultInstaller):
	""" Silva sitemap installer
	"""

	def install_custom(self, root):
		if queryUtility(ISitemapService) is None:
			factory = root.manage_addProduct['silva.app.sitemap']
			factory.manage_addSitemapService('service_sitemap')


class IExtension(Interface):
    """silva.app.sitemap extension
    """


install = SilvaSitemapInstaller("silva.app.sitemap", IExtension)
