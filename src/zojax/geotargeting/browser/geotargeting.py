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
from zojax.layoutform import Fields, PageletEditSubForm

from zojax.geotargeting.interfaces import _, IGeotargeting


class GeotargetingEditForm(PageletEditSubForm):

    label = _(u'Geotargeting')
    fields = Fields(IGeotargeting)
    prefix="geotargeting."

    def update(self):
        self.content = self.context

        extension = IGeotargeting(self.content, None)
        if extension is not None and extension.isAvailable():
            self.context = extension
            super(GeotargetingEditForm, self).update()
        else:
            self.context = None

    def isAvailable(self):
        if super(GeotargetingEditForm, self).isAvailable():
            return self.context is not None
        return False