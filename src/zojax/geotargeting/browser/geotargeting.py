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
from zojax.layoutform import Fields, PageletEditSubForm
from zojax.wizard.interfaces import ISaveable
from zojax.content.type.interfaces import IContentType, IPortalType

from interfaces import _, IGeotargeting


class HTMLTags(object):
    interface.implements(IHTMLTags)

    def isAvailable(self):
        context = self.context

        if IPortalType.providedBy(context) or ISite.providedBy(context):
            annotation = IAnnotations(context, None)
            if annotation is not None:
                return True
        return False


class GeotargetingEditForm(PageletEditSubForm):

    label = _(u'Geotargeting')
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