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
from zope import interface, component
from zope.component import getMultiAdapter
from zope.annotation.interfaces import IAnnotations
from zope.app.component.hooks import getSite
from zope.app.component.interfaces import ISite
from zope.dublincore.interfaces import IDCDescriptiveProperties
from z3c.breadcrumb.interfaces import IBreadcrumb
from zojax.layoutform import Fields
from zojax.wizard.step import WizardStepForm
from zojax.wizard.interfaces import ISaveable
from zojax.content.type.interfaces import IContentType, IPortalType

from interfaces import _, IHTMLTags


class HTMLTags(object):
    interface.implements(IHTMLTags)

    def isAvailable(self):
        context = self.context

        if IPortalType.providedBy(context) or ISite.providedBy(context):
            annotation = IAnnotations(context, None)
            if annotation is not None:
                return True
        return False


class HTMLTagsEditForm(WizardStepForm):
    interface.implements(ISaveable)

    label = _(u'SEO html tags')
    fields = Fields(IHTMLTags)

    def update(self):
        self.content = self.context

        tags = IHTMLTags(self.content, None)
        if tags is not None and tags.isAvailable():
            self.context = tags
            super(HTMLTagsEditForm, self).update()
        else:
            self.context = None

    def isAvailable(self):
        if super(HTMLTagsEditForm, self).isAvailable():
            return self.context is not None
        return False


class PageTitle(object):

    notRoot = False

    def update(self):
        super(PageTitle, self).update()
        context = self.context
        request = self.request

        if not ISite.providedBy(context):
            self.notRoot = True

            site = getSite()
            tags = IHTMLTags(site, None)
            if tags is not None and tags.isAvailable() and tags.title:
                self.portal_title = tags.title
            else:
                self.portal_title = getMultiAdapter(
                    (site, request), IBreadcrumb).name

        tags = IHTMLTags(context, None)
        if tags is not None and tags.isAvailable() and tags.title:
            self.title = tags.title
        else:
            self.title = getMultiAdapter(
                (context, request), IBreadcrumb).name


class PageMeta(object):

    keywords = u''
    description = u''

    def update(self):
        super(PageMeta, self).update()
        context = self.context

        tags = IHTMLTags(context, None)
        if tags is not None and tags.isAvailable():
            self.keywords = tags.keywords
            self.description = tags.description

        if not self.description:
            dc = IDCDescriptiveProperties(context, None)
            if dc is not None:
                self.description = dc.description

        if not self.description or not self.keywords:
            tags = IHTMLTags(getSite(), None)
            if tags is not None and tags.isAvailable():
                if not self.description:
                    self.description = tags.description

                if not self.keywords:
                    self.keywords = tags.keywords
