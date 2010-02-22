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
""" geotargeting configlet interfaces

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory

from zojax.widget.googlemap.field import MapLocation

_ = MessageFactory('zojax.geotargeting')


class IGeotargetingProduct(interface.Interface):
    """ product interface """
    
    applyOnEachQuery = schema.Bool(
        title = _('Apply geotargeting on each catalog query'),
        required = True,
        default = False)


class IGeotargeting(interface.Interface):
    """ geotargeting """

    location = MapLocation(
        title = _('Location'),
        description = _('Your location.'),
        required = False)
    
    
class IGeotargetingPreference(IGeotargeting):
    """ geotargeting preference """
    
    enabled = schema.Bool(
        title = _('Enable geotargeting'),
        required = True,
        default = True)
    
    location = MapLocation(
        title = _('Location'),
        description = _('Your location.'),
        required = True)