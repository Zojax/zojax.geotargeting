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
from zope.lifecycleevent import Attributes, ObjectModifiedEvent
from zope import event

from zojax.layoutform import button, Fields
from zojax.layoutform import PageletEditForm, PageletEditSubForm

from zojax.principal.registration.interfaces import IMemberRegisterAction

from zojax.geotargeting.interfaces import _, IGeotargetingPreference


class Geotargeting(PageletEditSubForm):

    fields = Fields(IGeotargetingPreference).omit('enabled')
    
    label = _(u'Geotargeting')
    
    prefix="geotargeting."
    
    def getContent(self):
        preference = IGeotargetingPreference(self.parentForm.registeredPrincipal, None)
        if preference is not None:
            return preference
        return {} 
    
    @button.handler(IMemberRegisterAction)
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
                    ObjectModifiedEvent(self.getContent(), *descriptions))
