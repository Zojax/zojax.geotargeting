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
from zope.app.intid.interfaces import IIntIds
from zope.security import checkPermission

from zojax.principal.profile.interfaces import IPersonalProfileCompleteChecker, IPersonalProfile, \
                       IProfileFields

from interfaces import IGeotargetingPreference

class GeotargetingChecker(object):
    
    component.adapts(IPersonalProfile)
    interface.implements(IPersonalProfileCompleteChecker)

    def __init__(self, context):
        self.context = context

    def check(self):
        preference = IGeotargetingPreference(self.context.__principal__, None)
        if preference is not None and preference.enabled:
            return bool(preference.location)
        return True