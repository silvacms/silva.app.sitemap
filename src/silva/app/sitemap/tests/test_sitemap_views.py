# -*- coding: utf-8 -*-

import unittest

from zope.component import queryUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from silva.core.interfaces import IPublicationWorkflow
from ..interfaces import ISitemapService
from ..testing import FunctionalLayer


class SitemapViewTestCase(unittest.TestCase):
    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()
        self.layer.login('manager')
        factory = self.root.manage_addProduct['Silva']
        factory.manage_addFolder('folder', 'Folder')
        factory = self.root.folder.manage_addProduct['Silva']
        factory.manage_addMockupVersionedContent('index', 'Index')
        notify(ObjectModifiedEvent(self.root.folder))
        IPublicationWorkflow(self.root.folder.index).publish()
        self.assertTrue(self.root.folder.is_published())

    def test_simple_view(self):
        service = queryUtility(ISitemapService)
        service.set_trim_index(False)
        service.set_allowed_meta_types([
            'Mockup VersionedContent'])

        with self.layer.get_browser() as browser:
            self.assertEquals(browser.open('/root/sitemap.xml'), 200)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SitemapViewTestCase))
    return suite
