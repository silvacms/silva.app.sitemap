# Copyright (c) 2012 Infrae. All rights reserved.
# See also LICENSE.txt

from five import grok

from zope.interface import Interface
from zope.lifecycleevent import IObjectAddedEvent
from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from silva.core.interfaces.content import IPublishable
from silva.core.interfaces.adapters import IAddableContents
from silva.core import conf as silvaconf
from silva.core.services.base import SilvaService

from .interfaces import ISitemapService
from zeam.form import silva as silvaforms
from zeam.form.ztk.actions import EditAction

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Acquisition import aq_parent


class SitemapService(SilvaService):
    grok.name('service_sitemap')
    grok.implements(ISitemapService)
    meta_type = "Silva Sitemap Service"
    silvaconf.icon('static/sitemap.png')

    security = ClassSecurityInfo()

    manage_options = (
        {'label': 'Edit', 'action': 'manage_settings'},
        ) + SilvaService.manage_options

    _allowed_meta_types = None
    _excluded_paths = None
    _paths = None
    _trim_index = True

    def __init__(self, id):
        super(SitemapService, self).__init__(id)
        self._allowed_meta_types = set()
        self._excluded_paths = set()
        self._paths = set()

    def get_trim_index(self):
        return self._trim_index

    security.declareProtected(
        'View Management Screens', 'set_trim_index')
    def set_trim_index(self, value):
        self._trim_index = value

    def get_allowed_meta_types(self):
        return self._allowed_meta_types

    security.declareProtected(
        'View Management Screens', 'set_allowed_meta_types')
    def set_allowed_meta_types(self, meta_types):
        self._allowed_meta_types = set(meta_types)
        # get addables IAllowedAddables

    def get_excluded_paths(self):
        return self._excluded_paths

    security.declareProtected(
        'View Management Screens', 'set_excluded_paths')
    def set_excluded_paths(self, excluded_paths):
        self._excluded_paths = set(excluded_paths)

    def get_paths(self):
        return self._paths

    security.declareProtected(
        'View Management Screens', 'set_paths')
    def set_paths(self, paths):
        self._paths = set(paths)


InitializeClass(SitemapService)


@grok.subscribe(ISitemapService, IObjectAddedEvent)
def set_defaults(service, event):
    service.set_paths(['/'.join(aq_parent(service).getPhysicalPath())])
    addables = IAddableContents(
        aq_parent(service)).get_all_addables(IPublishable)
    service.set_allowed_meta_types(addables)


@grok.provider(IContextSourceBinder)
def addables_content_types(context):
    addables = IAddableContents(aq_parent(context)).get_all_addables()
    entries = []
    for addable in addables:
        entries.append(SimpleTerm(value=addable,
                                  token=addable,
                                  title=addable))
    return SimpleVocabulary(entries)


class ISitemapFields(Interface):
    _allowed_meta_types = schema.Set(
        title=u'Allowed Meta types',
        value_type=schema.Choice(source=addables_content_types),
        required=True)
    _excluded_paths = schema.Set(
        title=u'Excluded paths',
        value_type=schema.TextLine(),
        required=False)
    _paths = schema.Set(
        title=u'Allowed paths',
        value_type=schema.TextLine(),
        required=True)
    _trim_index = schema.Bool(
        title=u'Remove index from path',
        description=u'When a content is index of a folder remove the '
        u'/index part of the url.')


class SitemapConfigurationForm(silvaforms.ZMIForm):
    grok.name('manage_settings')
    grok.context(ISitemapService)
    label = 'Manage sitemap settings'
    ignoreContent = False
    fields = silvaforms.Fields(ISitemapFields)
    actions = silvaforms.Actions(EditAction('Save changes'))
