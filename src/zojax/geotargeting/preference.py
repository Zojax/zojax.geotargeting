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
"""Job Profile implementation

$Id$
"""
from datetime import datetime

from pytz import utc
from zope.app.intid.interfaces import IIntIds
from zope.component import adapter, getUtility
from zope.event import notify
from zope.interface import implements
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zojax.principal.users.interfaces import IPrincipal

from interfaces import IGeotargetingPreference


class GeotargetingPreference(object):
    implements(IGeotargetingPreference)

    def isAvailable(self):
        # we don't to show it in menus
        return False

    @property
    def modified(self):
        return getattr(self.data, 'modified', None)

    def touch(self):
        self.data.modified = datetime.now(utc)


@adapter(IGeotargetingPreference, IObjectModifiedEvent)
def preferenceModified(preference, event):
    # 1. Update modification time
    preference.touch()

    # 2. Stored principals are indexed, so to update profile indexes
    # we need to notify about principal modification.
    #stored_principal = IPrincipal(preference.__principal__)
    #notify(ObjectModifiedEvent(stored_principal))
