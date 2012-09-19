# -*- coding: utf-8 -*-

import unittest

from zope.component import queryUtility

from ..interfaces import ISitemapService
from ..testing import FunctionalLayer


class SitemapViewTestCase(unittest.TestCase):
    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()
        factory = self.root.manage_addProduct['Silva']
        factory.manage_addFolder('folder', 'Folder')
        factory = self.root.folder.manage_addProduct['Silva']
        with self.layer.open_fixture('photo.tif') as image:
            factory.manage_addImage('test_image', u'Image élaboré', image)

    def test_simple_view(self):
        service = queryUtility(ISitemapService)
        service.set_allowed_meta_types(['Silva Root', 'Silva Folder', 'Silva Image'])

        with self.layer.get_browser() as browser:
            self.assertEquals(browser.open('/root/sitemap.xml'), 200)
            self.assertEquals("", browser.contents)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SitemapViewTestCase))
    return suite
