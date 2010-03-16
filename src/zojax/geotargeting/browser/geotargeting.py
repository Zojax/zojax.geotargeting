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
from zope import interface, event, component
from zope.component import queryMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.lifecycleevent import Attributes, ObjectModifiedEvent
from z3c.form import subform, button

from zojax.layoutform import Fields, PageletEditSubForm, PageletAddSubForm
from zojax.layoutform.utils import applyChanges
from zojax.layoutform.interfaces import ISaveAction

from zojax.geotargeting.interfaces import _, IGeotargeting


class GeotargetingBaseForm(object):

    label = _(u'Geotargeting')
    fields = Fields(IGeotargeting)
    prefix="geotargeting."


class GeotargetingEditForm(GeotargetingBaseForm, PageletEditSubForm):
    
    def update(self):
        self.content = self.context

        extension = IGeotargeting(self.content, None)
        if extension is not None and extension.isAvailable():
            self.context = extension
            super(GeotargetingBaseForm, self).update()
        else:
            self.context = None

    def isAvailable(self):
        if super(GeotargetingBaseForm, self).isAvailable():
            return self.context is not None
        return False
    
    @button.handler(ISaveAction)
    def handleApply(self, action):
        data, errors = self.extractData()

        if not errors:
            changes = self.applyChanges(data)
            if changes:
                descriptions = []
                for interface, names in changes.items():
                    descriptions.append(Attributes(interface, *names))

                self.changesApplied = True
                event.notify(
                    ObjectModifiedEvent(self.content, *descriptions))
    
    
class GeotargetingAddForm(GeotargetingBaseForm, PageletAddSubForm):
    
    extension = None
    
    def getContent(self):
        return {}

    def update(self):
        extension = IGeotargeting(self.context, None)

        if extension is not None:
            self.extension = extension
            super(GeotargetingAddForm, self).update()

    def isAvailable(self):
        return self.extension is not None

    def applyChanges(self, data):
        extension = IGeotargeting(self.parentForm._addedObject, None)
        if extension is not None and extension.isAvailable():
            return applyChanges(self, extension, data)
        else:
            return {}
