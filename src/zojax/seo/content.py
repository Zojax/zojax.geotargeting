##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import cgi
from zope import interface, schema, component
from zope.location import Location
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
from zope.session.interfaces import ISession
from zope.app.intid.interfaces import IIntIds
from zope.traversing.browser import absoluteURL
from zope.dublincore.interfaces import IDCTimes

from zojax.layoutform import Fields, PageletEditForm
from zojax.wizard.interfaces import ISaveable
from zojax.wizard.step import WizardStepForm
from zojax.catalog.interfaces import ICatalog
from zojax.batching.session import SessionBatch
from zojax.ownership.interfaces import IOwnership
from zojax.content.type.interfaces import IItem, IContentViewView, IContentType
from zojax.content.table.title import TitleColumn
from zojax.content.table.interfaces import IContentsTable
from zojax.table.table import Table
from zojax.table.column import Column
from zojax.pageelement.interfaces import IPageElement
from zojax.principal.profile.interfaces import IPersonalProfile

from zojax.seo.interfaces import _, ISEO, IHTMLTags

SESSIONKEY = u'zojax.seo'


class ISearchForm(interface.Interface):

    searchableText = schema.TextLine(
        title = u'Searchable text',
        required = False)

    type = schema.List(
        title = u'Content type',
        value_type = schema.Choice(
            vocabulary='zojax.content.portalContent'),
        required = False)


class PortalContent(WizardStepForm):
    interface.implements(ISaveable)

    fields = Fields(ISearchForm)

    def __init__(self, context, *args):
        super(PortalContent, self).__init__(context, *args)

        self.ids = getUtility(IIntIds)

    def applyChanges(self, data):
        session = ISession(self.request)
        session[SESSIONKEY]['params'] = data
        return True

    def getContent(self):
        session = ISession(self.request)
        return session[SESSIONKEY].get('params', {})


class PortalContentsTable(Table):
    interface.implements(IContentsTable)
    component.adapts(ISEO, interface.Interface, interface.Interface)

    pageSize = 30
    sessionBatch = True
    enabledColumns = ('title', 'titletag', 'author',
                      'type', 'location', 'created')
    msgEmptyTable = _('No content.')

    def initDataset(self):
        catalog = getUtility(ICatalog)

        session = ISession(self.request)
        data = session[SESSIONKEY].get('params', {})

        query = {
            'isDraft': {'any_of': (False,)},
            'typeType': {'any_of': ('Portal type',)},
            'sort_on': 'title',
            'noPublishing': True, 'noSecurityChecks': True,
            }

        if 'type' in data and data['type']:
            query['type'] = {'any_of': data['type']}

        if 'searchableText' in data and data['searchableText']:
            query['searchableText'] = data['searchableText']

        try:
            self.dataset = catalog.searchResults(**query)
        except:
            self.dataset = ()


class TitleColumn(TitleColumn):
    component.adapts(ISEO, interface.Interface, PortalContentsTable)

    def update(self):
        self.ids = getUtility(IIntIds)
        self.contexturl = u'%s/index.html/content'%absoluteURL(
            self.context, self.request)

    def contentUrl(self):
        return u'%s/view.html?id=%s'%(
            self.contexturl, self.ids.getId(self.content))


class TitleTagColumn(Column):
    component.adapts(ISEO, interface.Interface, PortalContentsTable)

    title = _('HTML title tag')

    def query(self, default=None):
        pageelement = getMultiAdapter(
            (self.content, self.request, None), IPageElement, u'page.title')
        return pageelement.updateAndRender()

    def render(self):
        return cgi.escape(self.query().strip()[7:-8])


class ContentView(PageletEditForm):

    fields = Fields(IHTMLTags)

    title = u''
    description = u''

    def update(self):
        try:
            content = getUtility(IIntIds).getObject(
                int(self.request.get('id')))
        except:
            self.redirect('./')
            return

        self.content = content

        item = IItem(content, None)
        if item is not None:
            self.title = item.title
            self.description = item.description

        dctimes = IDCTimes(content)
        self.created = dctimes.created
        self.modified = dctimes.modified

        pagetitle = getMultiAdapter(
            (content, self.request, None), IPageElement, u'page.title')
        self.pagetitle = cgi.escape(pagetitle.updateAndRender().strip()[7:-8])

        super(ContentView, self).update()

    def getContent(self):
        return self.content

    def getLocation(self):
        request = self.request
        content = self.content.__parent__

        item = IItem(content, None)

        title = u''
        description = u''
        if item is not None:
            title = item.title
            description = item.description

        view = queryMultiAdapter((content, request), IContentViewView)
        if view is not None:
            url = '%s/%s'%(absoluteURL(content, request), view.name)
        else:
            url = '%s/'%absoluteURL(content, request)

        return {'url': url,
                'title': title or _('[No title]'),
                'content': content,
                'icon': queryMultiAdapter((content, request), name='zmi_icon'),
                'description': description or u''}

    def getAuthor(self):
        ownership = IOwnership(self.content, None)
        if ownership is not None:
            principal = ownership.owner
        else:
            principal = None

        if principal is not None:
            request = self.request
            profile = IPersonalProfile(principal)

            info = {'title': profile.title,
                    'profile': ''}

            space = profile.space
            if space is not None:
                info['profile'] = '%s/'%absoluteURL(space, request)

            return info

    def getContentType(self):
        ct = IContentType(self.content)

        return {'title': ct.title,
                'icon': queryMultiAdapter(
                (self.content, self.request), name='zmi_icon')}
