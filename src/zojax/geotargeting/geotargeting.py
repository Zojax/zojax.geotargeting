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
from zope.app.component.interfaces import ISite
from zope.annotation.interfaces import IAnnotations
from zojax.content.type.interfaces import IContentType, IPortalType

from interfaces import _, IGeotargeting


class Geotargeting(object):
    interface.implements(IGeotargeting)

    def isAvailable(self):
        context = self.context

        if IPortalType.providedBy(context) or ISite.providedBy(context):
            annotation = IAnnotations(context, None)
            if annotation is not None:
                return True
        return False