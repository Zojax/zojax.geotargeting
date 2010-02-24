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
from zojax.layoutform import button, Fields
from zojax.layoutform import PageletEditForm, PageletEditSubForm

from zojax.geotargeting.interfaces import _, IGeotargetingPreference


class Geotargeting(PageletEditSubForm):

    fields = Fields(IGeotargetingPreference)
    
    label = _(u'Geotargeting')
    
    prefix="geotargeting."
    
    def getContent(self):
        return IGeotargetingPreference(self.context.__principal__)
